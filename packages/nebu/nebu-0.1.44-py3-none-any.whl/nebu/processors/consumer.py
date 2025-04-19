#!/usr/bin/env python3
import json
import os
import socket
import sys
import time
import traceback
from datetime import datetime
from typing import Dict, TypeVar

import redis
import socks
from redis import ConnectionError, ResponseError

# Define TypeVar for generic models
T = TypeVar("T")

# Environment variable name used as a guard in the decorator
_NEBU_INSIDE_CONSUMER_ENV_VAR = "_NEBU_INSIDE_CONSUMER_EXEC"

# Get function and model source code and create them dynamically
try:
    function_source = os.environ.get("FUNCTION_SOURCE")
    function_name = os.environ.get("FUNCTION_NAME")
    stream_message_source = os.environ.get("STREAM_MESSAGE_SOURCE")
    input_model_source = os.environ.get("INPUT_MODEL_SOURCE")
    output_model_source = os.environ.get("OUTPUT_MODEL_SOURCE")
    content_type_source = os.environ.get("CONTENT_TYPE_SOURCE")
    is_stream_message = os.environ.get("IS_STREAM_MESSAGE") == "True"
    param_type_name = os.environ.get("PARAM_TYPE_NAME")
    return_type_name = os.environ.get("RETURN_TYPE_NAME")
    param_type_str = os.environ.get("PARAM_TYPE_STR")
    return_type_str = os.environ.get("RETURN_TYPE_STR")
    content_type_name = os.environ.get("CONTENT_TYPE_NAME")

    # Get source for the file containing the decorated function
    decorated_func_file_source = os.environ.get("DECORATED_FUNC_FILE_SOURCE")
    # Get sources for the directory containing the decorated function
    # decorated_dir_sources_json = os.environ.get("DECORATED_DIR_SOURCES") # Removed

    # Get init_func source if provided
    init_func_source = os.environ.get("INIT_FUNC_SOURCE")
    init_func_name = os.environ.get("INIT_FUNC_NAME")

    # Check for generic type arguments
    input_model_args = []
    output_model_args = []
    content_type_args = []

    # Get input model arg sources
    i = 0
    while True:
        arg_source = os.environ.get(f"INPUT_MODEL_ARG_{i}_SOURCE")
        if arg_source:
            input_model_args.append(arg_source)
            i += 1
        else:
            break

    # Get output model arg sources
    i = 0
    while True:
        arg_source = os.environ.get(f"OUTPUT_MODEL_ARG_{i}_SOURCE")
        if arg_source:
            output_model_args.append(arg_source)
            i += 1
        else:
            break

    # Get content type arg sources
    i = 0
    while True:
        arg_source = os.environ.get(f"CONTENT_TYPE_ARG_{i}_SOURCE")
        if arg_source:
            content_type_args.append(arg_source)
            i += 1
        else:
            break

    # Get included object sources
    included_object_sources = []
    i = 0
    while True:
        obj_source = os.environ.get(f"INCLUDED_OBJECT_{i}_SOURCE")
        if obj_source:
            args = []
            j = 0
            while True:
                arg_source = os.environ.get(f"INCLUDED_OBJECT_{i}_ARG_{j}_SOURCE")
                if arg_source:
                    args.append(arg_source)
                    j += 1
                else:
                    break
            included_object_sources.append((obj_source, args))
            i += 1
        else:
            break

    if not function_source or not function_name:
        print("FUNCTION_SOURCE or FUNCTION_NAME environment variables not set")
        sys.exit(1)

    # Create a local namespace for executing the function
    local_namespace = {}

    # Include pydantic BaseModel and typing tools for type annotations
    exec("from pydantic import BaseModel, Field", local_namespace)
    exec(
        "from typing import Optional, List, Dict, Any, Generic, TypeVar",
        local_namespace,
    )
    exec("T = TypeVar('T')", local_namespace)
    exec("from nebu.processors.models import *", local_namespace)
    exec("from nebu.processors.processor import *", local_namespace)
    # Add import for the processor decorator itself
    exec("from nebu.processors.decorate import processor", local_namespace)
    # Add import for chatx openai types
    exec("from nebu.chatx.openai import *", local_namespace)

    # Set the guard environment variable before executing any source code
    os.environ[_NEBU_INSIDE_CONSUMER_ENV_VAR] = "1"
    print(f"[Consumer] Set environment variable {_NEBU_INSIDE_CONSUMER_ENV_VAR}=1")

    try:
        # Execute the source file of the decorated function FIRST
        if decorated_func_file_source:
            print("[Consumer] Executing decorated function's file source...")
            try:
                exec(decorated_func_file_source, local_namespace)
                print(
                    "[Consumer] Successfully executed decorated function's file source."
                )
            except Exception as e:
                print(f"Error executing decorated function's file source: {e}")
                traceback.print_exc()  # Warn and continue
        else:
            print(
                "[Consumer] No decorated function's file source found in environment."
            )

        # Execute the sources from the decorated function's directory
        # if decorated_dir_sources_json:
        #     print("[Consumer] Executing decorated function's directory sources...")
        #     try:
        #         dir_sources = json.loads(decorated_dir_sources_json)
        #         # Sort by relative path for some predictability (e.g., __init__.py first)
        #         for rel_path, source_code in sorted(dir_sources.items()):
        #             print(f"[Consumer] Executing source from: {rel_path}...")
        #             try:
        #                 exec(source_code, local_namespace)
        #                 print(f"[Consumer] Successfully executed source from: {rel_path}")
        #             except Exception as e:
        #                 print(f"Error executing source from {rel_path}: {e}")
        #                 traceback.print_exc() # Warn and continue
        #     except json.JSONDecodeError as e:
        #         print(f"Error decoding DECORATED_DIR_SOURCES JSON: {e}")
        #         traceback.print_exc()
        #     except Exception as e:
        #         print(f"Unexpected error processing directory sources: {e}")
        #         traceback.print_exc()
        # else:
        #     print("[Consumer] No decorated function's directory sources found in environment.")

        # Execute included object sources NEXT, as they might define types needed by others
        print("[Consumer] Executing included object sources...")
        for i, (obj_source, args_sources) in enumerate(included_object_sources):
            try:
                exec(obj_source, local_namespace)
                print(
                    f"[Consumer] Successfully executed included object {i} base source"
                )
                for j, arg_source in enumerate(args_sources):
                    try:
                        exec(arg_source, local_namespace)
                        print(
                            f"[Consumer] Successfully executed included object {i} arg {j} source"
                        )
                    except Exception as e:
                        print(
                            f"Error executing included object {i} arg {j} source: {e}"
                        )
                        traceback.print_exc()
            except Exception as e:
                print(f"Error executing included object {i} base source: {e}")
                traceback.print_exc()
        print("[Consumer] Finished executing included object sources.")

        # First try to import the module to get any needed dependencies
        # This is a fallback in case the module is available
        module_name = os.environ.get("MODULE_NAME")
        try:
            if module_name:
                exec(f"import {module_name}", local_namespace)
                print(f"Successfully imported module {module_name}")
        except Exception as e:
            print(f"Warning: Could not import module {module_name}: {e}")
            print(
                "This is expected if running in a Jupyter notebook. Will use dynamic execution."
            )

        # Define the models
        # First define stream message class if needed
        if stream_message_source:
            try:
                exec(stream_message_source, local_namespace)
                print("Successfully defined Message class")
            except Exception as e:
                print(f"Error defining Message: {e}")
                traceback.print_exc()

        # Define content type if available
        if content_type_source:
            try:
                exec(content_type_source, local_namespace)
                print(f"Successfully defined content type {content_type_name}")

                # Define any content type args
                for arg_source in content_type_args:
                    try:
                        exec(arg_source, local_namespace)
                        print("Successfully defined content type argument")
                    except Exception as e:
                        print(f"Error defining content type argument: {e}")
                        traceback.print_exc()
            except Exception as e:
                print(f"Error defining content type: {e}")
                traceback.print_exc()

        # Define input model if different from stream message
        if input_model_source and (
            not is_stream_message or input_model_source != stream_message_source
        ):
            try:
                exec(input_model_source, local_namespace)
                print(f"Successfully defined input model {param_type_str}")

                # Define any input model args
                for arg_source in input_model_args:
                    try:
                        exec(arg_source, local_namespace)
                        print("Successfully defined input model argument")
                    except Exception as e:
                        print(f"Error defining input model argument: {e}")
                        traceback.print_exc()
            except Exception as e:
                print(f"Error defining input model: {e}")
                traceback.print_exc()

        # Define output model
        if output_model_source:
            try:
                exec(output_model_source, local_namespace)
                print(f"Successfully defined output model {return_type_str}")

                # Define any output model args
                for arg_source in output_model_args:
                    try:
                        exec(arg_source, local_namespace)
                        print("Successfully defined output model argument")
                    except Exception as e:
                        print(f"Error defining output model argument: {e}")
                        traceback.print_exc()
            except Exception as e:
                print(f"Error defining output model: {e}")
                traceback.print_exc()

        # Finally, execute the function code
        try:
            exec(function_source, local_namespace)
            target_function = local_namespace[function_name]
            print(f"Successfully loaded function {function_name}")
        except Exception as e:
            print(f"Error creating function from source: {e}")
            traceback.print_exc()
            sys.exit(1)

        # Execute init_func if provided
        if init_func_source and init_func_name:
            print(f"Executing init_func: {init_func_name}...")
            try:
                exec(init_func_source, local_namespace)
                init_function = local_namespace[init_func_name]
                print(
                    f"[Consumer] Environment before calling init_func {init_func_name}: {os.environ}"
                )
                init_function()  # Call the function
                print(f"Successfully executed init_func: {init_func_name}")
            except Exception as e:
                print(f"Error executing init_func '{init_func_name}': {e}")
                traceback.print_exc()
                # Decide if failure is critical. For now, let's exit.
                print("Exiting due to init_func failure.")
                sys.exit(1)
    finally:
        # Unset the guard environment variable after all execs are done
        os.environ.pop(_NEBU_INSIDE_CONSUMER_ENV_VAR, None)
        print(f"[Consumer] Unset environment variable {_NEBU_INSIDE_CONSUMER_ENV_VAR}")

except Exception as e:
    print(f"Error setting up function: {e}")
    traceback.print_exc()
    sys.exit(1)

# Get Redis connection parameters from environment
REDIS_URL = os.environ.get("REDIS_URL", "")
REDIS_CONSUMER_GROUP = os.environ.get("REDIS_CONSUMER_GROUP")
REDIS_STREAM = os.environ.get("REDIS_STREAM")

if not all([REDIS_URL, REDIS_CONSUMER_GROUP, REDIS_STREAM]):
    print("Missing required Redis environment variables")
    sys.exit(1)

# Configure SOCKS proxy before connecting to Redis
# Use the proxy settings provided by tailscaled
socks.set_default_proxy(socks.SOCKS5, "localhost", 1055)
socket.socket = socks.socksocket
print("Configured SOCKS5 proxy for socket connections via localhost:1055")

# Connect to Redis
try:
    # Parse the Redis URL to handle potential credentials or specific DBs if needed
    # Although from_url should work now with the patched socket
    r = redis.from_url(
        REDIS_URL, decode_responses=True
    )  # Added decode_responses for convenience
    r.ping()  # Test connection
    redis_info = REDIS_URL.split("@")[-1] if "@" in REDIS_URL else REDIS_URL
    print(f"Connected to Redis via SOCKS proxy at {redis_info}")
except Exception as e:
    print(f"Failed to connect to Redis via SOCKS proxy: {e}")
    traceback.print_exc()
    sys.exit(1)

# Create consumer group if it doesn't exist
try:
    # Assert types before use
    assert isinstance(REDIS_STREAM, str)
    assert isinstance(REDIS_CONSUMER_GROUP, str)
    r.xgroup_create(REDIS_STREAM, REDIS_CONSUMER_GROUP, id="0", mkstream=True)
    print(f"Created consumer group {REDIS_CONSUMER_GROUP} for stream {REDIS_STREAM}")
except ResponseError as e:
    if "BUSYGROUP" in str(e):
        print(f"Consumer group {REDIS_CONSUMER_GROUP} already exists")
    else:
        print(f"Error creating consumer group: {e}")
        traceback.print_exc()


# Function to process messages
def process_message(message_id: str, message_data: Dict[str, str]) -> None:
    # Initialize variables that need to be accessible in the except block
    return_stream = None
    user_id = None
    try:
        # Extract the JSON string payload from the 'data' field
        payload_str = message_data.get("data")

        # decode_responses=True should mean payload_str is a string if found.
        if not payload_str:
            raise ValueError(
                f"Missing or invalid 'data' field (expected string): {message_data}"
            )

        # Parse the JSON string into a dictionary
        try:
            raw_payload = json.loads(payload_str)
        except json.JSONDecodeError as json_err:
            raise ValueError(f"Failed to parse JSON payload: {json_err}") from json_err

        # Validate that raw_payload is a dictionary as expected
        if not isinstance(raw_payload, dict):
            raise TypeError(
                f"Expected parsed payload to be a dictionary, but got {type(raw_payload)}"
            )

        print(f"Raw payload: {raw_payload}")

        # Extract fields from the parsed payload
        # These fields are extracted for completeness and potential future use
        kind = raw_payload.get("kind", "")  # kind
        msg_id = raw_payload.get("id", "")  # msg_id
        content_raw = raw_payload.get("content", {})
        created_at = raw_payload.get("created_at", 0)  # created_at
        return_stream = raw_payload.get("return_stream")
        user_id = raw_payload.get("user_id")
        orgs = raw_payload.get("organizations")  # organizations
        handle = raw_payload.get("handle")  # handle
        adapter = raw_payload.get("adapter")  # adapter

        # --- Health Check Logic based on kind ---
        if kind == "HealthCheck":
            print(f"Received HealthCheck message {message_id}")
            health_response = {
                "kind": "StreamResponseMessage",  # Respond with a standard message kind
                "id": message_id,
                "content": {"status": "healthy", "checked_message_id": msg_id},
                "status": "success",
                "created_at": datetime.now().isoformat(),
                "user_id": user_id,  # Include user_id if available
            }
            if return_stream:
                # Assert type again closer to usage for type checker clarity
                assert isinstance(return_stream, str)
                r.xadd(return_stream, {"data": json.dumps(health_response)})
                print(f"Sent health check response to {return_stream}")

            # Assert types again closer to usage for type checker clarity
            assert isinstance(REDIS_STREAM, str)
            assert isinstance(REDIS_CONSUMER_GROUP, str)
            r.xack(REDIS_STREAM, REDIS_CONSUMER_GROUP, message_id)
            print(f"Acknowledged HealthCheck message {message_id}")
            return  # Exit early for health checks
        # --- End Health Check Logic ---

        # Parse the content field if it's a string
        if isinstance(content_raw, str):
            try:
                content = json.loads(content_raw)
            except json.JSONDecodeError:
                content = content_raw
        else:
            content = content_raw

        print(f"Content: {content}")

        # For StreamMessage, construct the proper input object
        if is_stream_message and "Message" in local_namespace:
            # If we have a content type, try to construct it
            if content_type_name and content_type_name in local_namespace:
                # Try to create the content type model first
                try:
                    content_model = local_namespace[content_type_name].model_validate(
                        content
                    )
                    print(f"Content model: {content_model}")
                    input_obj = local_namespace["Message"](
                        kind=kind,
                        id=msg_id,
                        content=content_model,
                        created_at=created_at,
                        return_stream=return_stream,
                        user_id=user_id,
                        orgs=orgs,
                        handle=handle,
                        adapter=adapter,
                    )
                except Exception as e:
                    print(f"Error creating content type model: {e}")
                    # Fallback to using raw content
                    input_obj = local_namespace["Message"](
                        kind=kind,
                        id=msg_id,
                        content=content,
                        created_at=created_at,
                        return_stream=return_stream,
                        user_id=user_id,
                        orgs=orgs,
                        handle=handle,
                        adapter=adapter,
                    )
            else:
                # Just use the raw content
                print("Using raw content")
                input_obj = local_namespace["Message"](
                    kind=kind,
                    id=msg_id,
                    content=content,
                    created_at=created_at,
                    return_stream=return_stream,
                    user_id=user_id,
                    orgs=orgs,
                    handle=handle,
                    adapter=adapter,
                )
        else:
            # Otherwise use the param type directly
            try:
                if param_type_str in local_namespace:
                    print(f"Validating content against {param_type_str}")
                    input_obj = local_namespace[param_type_str].model_validate(content)
                else:
                    # If we can't find the exact type, just pass the content directly
                    input_obj = content
            except Exception as e:
                print(f"Error creating input model: {e}, using raw content")
                raise e

        print(f"Input object: {input_obj}")

        # Execute the function
        result = target_function(input_obj)
        print(f"Result: {result}")
        # If the result is a Pydantic model, convert to dict
        if hasattr(result, "model_dump"):
            result = result.model_dump()

        # Prepare the response
        response = {
            "kind": "StreamResponseMessage",
            "id": message_id,
            "content": result,
            "status": "success",
            "created_at": datetime.now().isoformat(),
            "user_id": user_id,
        }

        print(f"Response: {response}")

        # Send the result to the return stream
        if return_stream:
            # Assert type again closer to usage for type checker clarity
            assert isinstance(return_stream, str)
            r.xadd(return_stream, {"data": json.dumps(response)})
            print(f"Processed message {message_id}, result sent to {return_stream}")

        # Acknowledge the message
        # Assert types again closer to usage for type checker clarity
        assert isinstance(REDIS_STREAM, str)
        assert isinstance(REDIS_CONSUMER_GROUP, str)
        r.xack(REDIS_STREAM, REDIS_CONSUMER_GROUP, message_id)

    except Exception as e:
        print(f"Error processing message {message_id}: {e}")
        traceback.print_exc()

        # Prepare the error response
        error_response = {
            "kind": "StreamResponseMessage",
            "id": message_id,
            "content": {
                "error": str(e),
                "traceback": traceback.format_exc(),
            },
            "status": "error",
            "created_at": datetime.now().isoformat(),
            "user_id": user_id,
        }

        # Send the error to the return stream
        if return_stream:
            # Assert type again closer to usage for type checker clarity
            assert isinstance(return_stream, str)
            r.xadd(return_stream, {"data": json.dumps(error_response)})
        else:
            # Assert type again closer to usage for type checker clarity
            assert isinstance(REDIS_STREAM, str)
            r.xadd(f"{REDIS_STREAM}.errors", {"data": json.dumps(error_response)})

        # Still acknowledge the message so we don't reprocess it
        # Assert types again closer to usage for type checker clarity
        assert isinstance(REDIS_STREAM, str)
        assert isinstance(REDIS_CONSUMER_GROUP, str)
        r.xack(REDIS_STREAM, REDIS_CONSUMER_GROUP, message_id)


# Main loop
print(f"Starting consumer for stream {REDIS_STREAM} in group {REDIS_CONSUMER_GROUP}")
consumer_name = f"consumer-{os.getpid()}"

while True:
    try:
        # Assert types just before use in the loop
        assert isinstance(REDIS_STREAM, str)
        assert isinstance(REDIS_CONSUMER_GROUP, str)

        # Read from stream with blocking
        streams = {REDIS_STREAM: ">"}  # '>' means read only new messages
        # The type checker still struggles here, but the runtime types are asserted.
        print("reading from stream...")
        messages = r.xreadgroup(  # type: ignore[arg-type]
            REDIS_CONSUMER_GROUP, consumer_name, streams, count=1, block=5000
        )

        if not messages:
            # No messages received, continue waiting
            continue

        # Assert that messages is a list (expected synchronous return type)
        assert isinstance(
            messages, list
        ), f"Expected list from xreadgroup, got {type(messages)}"
        assert len(messages) > 0  # Ensure the list is not empty before indexing

        stream_name, stream_messages = messages[0]

        for message_id, message_data in stream_messages:
            print(f"Processing message {message_id}")
            print(f"Message data: {message_data}")
            process_message(message_id, message_data)

    except ConnectionError as e:
        print(f"Redis connection error: {e}")
        time.sleep(5)  # Wait before retrying

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        time.sleep(1)  # Brief pause before continuing
