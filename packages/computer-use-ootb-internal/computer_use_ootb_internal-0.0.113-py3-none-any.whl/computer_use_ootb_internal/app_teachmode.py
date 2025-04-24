import argparse
import time
import json
from datetime import datetime
import threading
import requests
import platform  # Add platform import
import pyautogui  # Add pyautogui import
import webbrowser # Add webbrowser import
import os # Import os for path joining
import logging # Import logging
import importlib # For dynamic imports
import pkgutil # To find modules
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from computer_use_ootb_internal.computer_use_demo.tools.computer import get_screen_details
from computer_use_ootb_internal.run_teachmode_ootb_args import simple_teachmode_sampling_loop

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter for API endpoints
class RateLimiter:
    def __init__(self, interval_seconds=2):
        self.interval = interval_seconds
        self.last_request_time = {}
        self.lock = threading.Lock()
        
    def allow_request(self, endpoint):
        with self.lock:
            current_time = time.time()
            # Priority endpoints always allowed
            if endpoint in ["/update_params", "/update_message"]:
                return True
                
            # For other endpoints, apply rate limiting
            if endpoint not in self.last_request_time:
                self.last_request_time[endpoint] = current_time
                return True
                
            elapsed = current_time - self.last_request_time[endpoint]
            if elapsed < self.interval:
                return False
                
            self.last_request_time[endpoint] = current_time
            return True


def log_ootb_request(server_url, ootb_request_type, data):
    logging_data = {
        "type": ootb_request_type,
        "data": data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if not server_url.endswith("/update_ootb_logging"):
        server_logging_url = server_url + "/update_ootb_logging"
    else:
        server_logging_url = server_url
    requests.post(server_logging_url, json=logging_data)


class SharedState:
    def __init__(self, args):
        self.args = args
        self.task_updated = False
        self.chatbot_messages = []
        # Store all state-related data here
        self.model = args.model
        self.task = getattr(args, 'task', "")
        self.selected_screen = args.selected_screen
        self.user_id = args.user_id
        self.trace_id = args.trace_id
        self.api_keys = args.api_keys
        self.server_url = args.server_url
        self.message_queue = []
        self.is_processing = False
        self.should_stop = False
        self.is_paused = False
        # Add a new event to better control stopping
        self.stop_event = threading.Event()
        # Add a reference to the processing thread
        self.processing_thread = None

shared_state = None
rate_limiter = RateLimiter(interval_seconds=2)

# Set up logging for this module
log = logging.getLogger(__name__)

def prepare_environment(state):
    """Dynamically loads and runs preparation logic based on software name."""
    # TODO: Replace hardcoded software name with value from shared_state when available
    software_name = "star rail"
    # Normalize the software name to be a valid Python module name
    # Replace spaces/hyphens with underscores, convert to lowercase
    module_name_base = software_name.replace(" ", "_").replace("-", "_").lower()
    module_to_run = f"{module_name_base}_prepare"

    log.info(f"Attempting preparation for software: '{software_name}' (Module: '{module_to_run}')")

    try:
        # Construct the full module path within the package
        prep_package = "computer_use_ootb_internal.preparation"
        full_module_path = f"{prep_package}.{module_to_run}"

        # Dynamically import the module
        # Check if module exists first using pkgutil to avoid import errors
        # Note: pkgutil.find_loader might be deprecated, consider importlib.util.find_spec
        loader = pkgutil.find_loader(full_module_path)
        if loader is None:
            log.warning(f"Preparation module '{full_module_path}' not found. Skipping preparation.")
            return

        prep_module = importlib.import_module(full_module_path)

        # Check if the module has the expected function
        if hasattr(prep_module, "run_preparation") and callable(prep_module.run_preparation):
            log.info(f"Running preparation function from {full_module_path}...")
            prep_module.run_preparation(state)
            log.info(f"Preparation function from {full_module_path} completed.")
        else:
            log.warning(f"Module {full_module_path} found, but does not have a callable 'run_preparation' function. Skipping.")

    except ModuleNotFoundError:
        log.warning(f"Preparation module '{full_module_path}' not found. Skipping preparation.")
    except Exception as e:
        log.error(f"Error during dynamic preparation loading/execution for '{module_to_run}': {e}", exc_info=True)


@app.post("/update_params")
async def update_parameters(request: Request):
    data = await request.json()
    
    if 'task' not in data:
        return JSONResponse(
            content={"status": "error", "message": "Missing required field: task"},
            status_code=400
        )
    
    shared_state.args = argparse.Namespace(**data)
    shared_state.task_updated = True
    
    # Update shared state when parameters change
    shared_state.model = getattr(shared_state.args, 'model', "teach-mode-gpt-4o")
    shared_state.task = getattr(shared_state.args, 'task', "Following the instructions to complete the task.")
    shared_state.selected_screen = getattr(shared_state.args, 'selected_screen', 0)
    shared_state.user_id = getattr(shared_state.args, 'user_id', "hero_cases")
    shared_state.trace_id = getattr(shared_state.args, 'trace_id', "build_scroll_combat")
    shared_state.api_keys = getattr(shared_state.args, 'api_keys', "sk-proj-1234567890")
    shared_state.server_url = getattr(shared_state.args, 'server_url', "http://ec2-44-234-43-86.us-west-2.compute.amazonaws.com")
    
    log_ootb_request(shared_state.server_url, "update_params", data)

    # Call the (now dynamic) preparation function here, after parameters are updated
    prepare_environment(shared_state)

    return JSONResponse(
        content={"status": "success", "message": "Parameters updated", "new_args": vars(shared_state.args)},
        status_code=200
    )

@app.post("/update_message")
async def update_message(request: Request):
    data = await request.json()
    
    if 'message' not in data:
        return JSONResponse(
            content={"status": "error", "message": "Missing required field: message"},
            status_code=400
        )
    
    log_ootb_request(shared_state.server_url, "update_message", data)
    
    message = data['message']
    shared_state.chatbot_messages.append({"role": "user", "content": message})
    shared_state.task = message
    shared_state.args.task = message
    
    # Reset stop event before starting
    shared_state.stop_event.clear()
    
    # Start processing if not already running
    if not shared_state.is_processing:
        # Create and store the thread
        shared_state.processing_thread = threading.Thread(target=process_input, daemon=True)
        shared_state.processing_thread.start()
    
    return JSONResponse(
        content={"status": "success", "message": "Message received", "task": shared_state.task},
        status_code=200
    )

@app.get("/get_messages")
async def get_messages(request: Request):
    # Apply rate limiting
    if not rate_limiter.allow_request(request.url.path):
        return JSONResponse(
            content={"status": "error", "message": "Rate limit exceeded. Try again after 2 seconds."},
            status_code=429
        )
    
    # log_ootb_request(shared_state.server_url, "get_messages", {})
    
    # Return all messages in the queue and clear it
    messages = shared_state.message_queue.copy()
    shared_state.message_queue = []
    
    return JSONResponse(
        content={"status": "success", "messages": messages},
        status_code=200
    )

@app.get("/get_screens")
async def get_screens(request: Request):
    # Apply rate limiting
    if not rate_limiter.allow_request(request.url.path):
        return JSONResponse(
            content={"status": "error", "message": "Rate limit exceeded. Try again after 2 seconds."},
            status_code=429
        )
    
    log_ootb_request(shared_state.server_url, "get_screens", {})
    
    screen_options, primary_index = get_screen_details()
    
    return JSONResponse(
        content={"status": "success", "screens": screen_options, "primary_index": primary_index},
        status_code=200
    )

@app.post("/stop_processing")
async def stop_processing(request: Request):
    # Apply rate limiting
    if not rate_limiter.allow_request(request.url.path):
        return JSONResponse(
            content={"status": "error", "message": "Rate limit exceeded. Try again after 2 seconds."},
            status_code=429
        )
    
    log_ootb_request(shared_state.server_url, "stop_processing", {})
    
    if shared_state.is_processing:
        # Set both flags to ensure stopping the current task
        shared_state.should_stop = True
        shared_state.stop_event.set()
        
        # Send an immediate message to the queue to inform the user
        stop_initiated_msg = {"role": "assistant", "content": f"Stopping task '{shared_state.task}'..."}
        shared_state.message_queue.append(stop_initiated_msg)
        
        return JSONResponse(
            content={"status": "success", "message": "Task is being stopped, server will remain available for new tasks"},
            status_code=200
        )
    else:
        return JSONResponse(
            content={"status": "error", "message": "No active processing to stop"},
            status_code=400
        )

@app.post("/toggle_pause")
async def toggle_pause(request: Request):
    # Apply rate limiting
    if not rate_limiter.allow_request(request.url.path):
        return JSONResponse(
            content={"status": "error", "message": "Rate limit exceeded. Try again after 2 seconds."},
            status_code=429
        )
    
    log_ootb_request(shared_state.server_url, "toggle_pause", {})
    
    if not shared_state.is_processing:
        return JSONResponse(
            content={"status": "error", "message": "No active processing to pause/resume"},
            status_code=400
        )
    
    # Toggle the pause state
    shared_state.is_paused = not shared_state.is_paused
    current_state = shared_state.is_paused
    
    print(f"Toggled pause state to: {current_state}")
    
    status_message = "paused" if current_state else "resumed"
    
    # Add a message to the queue to inform the user
    if current_state:
        message = {"role": "assistant", "content": f"Task '{shared_state.task}' has been paused. Click Continue to resume."}
    else:
        message = {"role": "assistant", "content": f"Task '{shared_state.task}' has been resumed."}
    
    shared_state.chatbot_messages.append(message)
    shared_state.message_queue.append(message)
    
    return JSONResponse(
        content={
            "status": "success", 
            "message": f"Processing {status_message}",
            "is_paused": current_state
        },
        status_code=200
    )

@app.get("/status")
async def get_status(request: Request):
    # Apply rate limiting
    if not rate_limiter.allow_request(request.url.path):
        return JSONResponse(
            content={"status": "error", "message": "Rate limit exceeded. Try again after 2 seconds."},
            status_code=429
        )
    
    # log_ootb_request(shared_state.server_url, "get_status", {})
    
    print(f"Status check - Processing: {shared_state.is_processing}, Paused: {shared_state.is_paused}")
    return JSONResponse(
        content={
            "status": "success",
            "is_processing": shared_state.is_processing,
            "is_paused": shared_state.is_paused
        },
        status_code=200
    )

def process_input():
    shared_state.is_processing = True
    shared_state.should_stop = False
    shared_state.is_paused = False
    shared_state.stop_event.clear()  # Ensure stop event is cleared at the start
    
    print(f"start sampling loop: {shared_state.chatbot_messages}")
    print(f"shared_state.args before sampling loop: {shared_state.args}")


    try:
        # Get the generator for the sampling loop
        sampling_loop = simple_teachmode_sampling_loop(
            model=shared_state.model,
            task=shared_state.task,
            selected_screen=shared_state.selected_screen,
            user_id=shared_state.user_id,
            trace_id=shared_state.trace_id,
            api_keys=shared_state.api_keys,
            server_url=shared_state.server_url,
        )

        # Process messages from the sampling loop
        for loop_msg in sampling_loop:
            # Check stop condition more frequently
            if shared_state.should_stop or shared_state.stop_event.is_set():
                print("Processing stopped by user")
                break
                
            # Check if paused and wait while paused
            while shared_state.is_paused and not shared_state.should_stop and not shared_state.stop_event.is_set():
                print(f"Processing paused at: {time.strftime('%H:%M:%S')}")
                # Wait a short time and check stop condition regularly
                for _ in range(5):  # Check 5 times per second
                    if shared_state.should_stop or shared_state.stop_event.is_set():
                        break
                    time.sleep(0.2)
                
            # Check again after pause loop    
            if shared_state.should_stop or shared_state.stop_event.is_set():
                print("Processing stopped while paused or resuming")
                break
                
            shared_state.chatbot_messages.append(loop_msg)
            shared_state.message_queue.append(loop_msg)
            
            # Short sleep to allow stop signals to be processed
            for _ in range(5):  # Check 5 times per second
                if shared_state.should_stop or shared_state.stop_event.is_set():
                    print("Processing stopped during sleep")
                    break
                time.sleep(0.1)
                
            if shared_state.should_stop or shared_state.stop_event.is_set():
                break

    except Exception as e:
        # Handle any exceptions in the processing loop
        error_msg = f"Error during task processing: {str(e)}"
        print(error_msg)
        error_message = {"role": "assistant", "content": error_msg, "type": "error"}
        shared_state.message_queue.append(error_message)
    
    finally:
        # Handle completion or interruption
        if shared_state.should_stop or shared_state.stop_event.is_set():
            stop_msg = f"Task '{shared_state.task}' was stopped. Ready for new tasks."
            final_message = {"role": "assistant", "content": stop_msg, "type": "text"}
        else:
            complete_msg = f"Task '{shared_state.task}' completed. Thanks for using Teachmode-OOTB."
            final_message = {"role": "assistant", "content": complete_msg, "type": "text"}
            
        shared_state.chatbot_messages.append(final_message)
        shared_state.message_queue.append(final_message)
        
        # Reset all state flags to allow for new tasks
        shared_state.is_processing = False
        shared_state.should_stop = False
        shared_state.is_paused = False
        shared_state.stop_event.clear()
        print("Processing completed, ready for new tasks")

def main():
    global app, shared_state, rate_limiter
    
    parser = argparse.ArgumentParser(
        description="Run a synchronous sampling loop for assistant/tool interactions in teach-mode."
    )
    parser.add_argument("--model", default="teach-mode-gpt-4o")
    parser.add_argument("--task", default="Create a claim on the SAP system, using Receipt.pdf as attachment.")
    parser.add_argument("--selected_screen", type=int, default=0)
    parser.add_argument("--user_id", default="star_rail_dev")
    parser.add_argument("--trace_id", default="scroll")
    parser.add_argument("--api_key_file", default="api_key.json")
    parser.add_argument("--api_keys", default="")
    parser.add_argument(
        "--server_url",
        default="http://ec2-44-234-43-86.us-west-2.compute.amazonaws.com",
        help="Server URL for the session"
    )

    args = parser.parse_args()
    shared_state = SharedState(args)
    rate_limiter = RateLimiter(interval_seconds=2)

    import uvicorn
    import platform
    import os
    
    # Default port
    port = 7888
    
    # Determine port based on Windows username
    if platform.system() == "Windows":
        username = os.environ["USERNAME"].lower()
        if username == "altair":
            port = 14000
        elif username.startswith("guest") and username[5:].isdigit():
            num = int(username[5:])
            if 1 <= num <= 10:
                port = 14000 + num
            else:
                port = 7888
        else:
            port = 7888
    
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    # main()

    # Test log_ootb_request
    log_ootb_request("http://ec2-44-234-43-86.us-west-2.compute.amazonaws.com", "test_request", {"message": "Test message"})