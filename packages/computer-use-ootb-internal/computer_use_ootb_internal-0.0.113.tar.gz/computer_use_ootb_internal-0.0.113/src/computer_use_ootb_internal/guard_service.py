# src/computer_use_ootb_internal/guard_service.py
import sys
import os
import time
import logging
import subprocess
import pathlib
import ctypes
import threading # For running server thread
import queue # For queuing commands
import requests # Keep for status reporting back
import servicemanager # From pywin32
import win32serviceutil # From pywin32
import win32service # From pywin32
import win32event # From pywin32
import win32api # From pywin32
import win32process # From pywin32
import win32security # From pywin32
import win32profile # From pywin32
import win32ts # From pywin32 (Terminal Services API)
import win32con
import psutil # For process/user info
from flask import Flask, request, jsonify # For embedded server
from waitress import serve # For serving Flask app

# --- Configuration ---
_SERVICE_NAME = "OOTBGuardService"
_SERVICE_DISPLAY_NAME = "OOTB Guard Service"
_SERVICE_DESCRIPTION = "Background service for OOTB monitoring and remote management (Server POST mode)."
_PACKAGE_NAME = "computer-use-ootb-internal"
_OOTB_MODULE = "computer_use_ootb_internal.app_teachmode"
# --- Server POST Configuration ---
_LISTEN_HOST = "0.0.0.0" # Listen on all interfaces
_LISTEN_PORT = 7001 # Port for server to POST commands TO
# _SHARED_SECRET = "YOUR_SECRET_HERE" # !! REMOVED !! - No secret check implemented now
# --- End Server POST Configuration ---
_SERVER_STATUS_REPORT_URL = "http://52.160.105.102:7000/api/guard/status" # URL to POST status back TO
_LOG_FILE = pathlib.Path(os.environ['PROGRAMDATA']) / "OOTBGuardService" / "guard_post_mode.log" # Different log file
# --- End Configuration ---

_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=_LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(threadName)s: %(message)s'
)

# --- Global service instance reference (needed for Flask routes) ---
_service_instance = None

# --- Flask App Definition ---
flask_app = Flask(__name__)

@flask_app.route('/command', methods=['POST'])
def receive_command():
    global _service_instance
    if not _service_instance:
        logging.error("Received command but service instance is not set.")
        return jsonify({"error": "Service not ready"}), 503

    # --- Authentication REMOVED ---
    # secret = request.headers.get('X-Guard-Secret')
    # if not secret or secret != _SHARED_SECRET:
    #     logging.warning(f"Unauthorized command POST received (Invalid/Missing X-Guard-Secret). Remote Addr: {request.remote_addr}")
    #     return jsonify({"error": "Unauthorized"}), 403
    # --- End Authentication REMOVED ---

    if not request.is_json:
        logging.warning("Received non-JSON command POST.")
        return jsonify({"error": "Request must be JSON"}), 400

    command = request.get_json()
    logging.info(f"Received command via POST: {command}")

    # Basic validation
    action = command.get("action")
    command_id = command.get("command_id", "N/A") # Use for status reporting
    if not action:
         logging.error(f"Received command POST with no action: {command}")
         return jsonify({"error": "Missing 'action' in command"}), 400

    # Queue the command for processing in a background thread
    _service_instance.command_queue.put((command_id, command))
    logging.info(f"Queued command {command_id} ({action}) for processing.")

    return jsonify({"message": f"Command {command_id} received and queued"}), 202 # Accepted

# --- Helper Functions --- Only logging helpers needed adjustments
def get_python_executable():
    python_exe = sys.executable
    if " " in python_exe and not python_exe.startswith('"'):
        python_exe = f'"{python_exe}"'
    return python_exe

def get_pip_executable():
    python_path = pathlib.Path(sys.executable)
    pip_path = python_path.parent / "Scripts" / "pip.exe"
    if pip_path.exists():
        pip_exe = str(pip_path)
        if " " in pip_exe and not pip_exe.startswith('"'):
            pip_exe = f'"{pip_exe}"'
        return pip_exe
    else:
        logging.warning("pip.exe not found in Scripts directory. Falling back to 'python -m pip'.")
        return f"{get_python_executable()} -m pip"

def log_info(msg):
    thread_name = threading.current_thread().name
    full_msg = f"[{thread_name}] {msg}"
    logging.info(full_msg)
    try:
        # Only log to event log from main service thread or known non-daemon threads if possible
        # Trying from waitress/flask threads might cause issues.
        # For simplicity, maybe remove event log integration or make it conditional.
        if threading.current_thread().name in ["MainThread", "CommandProcessor"]: # Example condition
             servicemanager.LogInfoMsg(str(full_msg))
    except Exception as e:
        logging.warning(f"Could not write info to Windows Event Log: {e}")

def log_error(msg, exc_info=False):
    thread_name = threading.current_thread().name
    full_msg = f"[{thread_name}] {msg}"
    logging.error(full_msg, exc_info=exc_info)
    try:
        if threading.current_thread().name in ["MainThread", "CommandProcessor"]:
            servicemanager.LogErrorMsg(str(full_msg))
    except Exception as e:
        logging.warning(f"Could not write error to Windows Event Log: {e}")

class GuardService(win32serviceutil.ServiceFramework):
    _svc_name_ = _SERVICE_NAME
    _svc_display_name_ = _SERVICE_DISPLAY_NAME
    _svc_description_ = _SERVICE_DESCRIPTION

    def __init__(self, args):
        global _service_instance
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        self.server_thread = None
        self.command_queue = queue.Queue()
        self.command_processor_thread = None
        self.session = requests.Session() # For status reporting

        self.python_exe = get_python_executable()
        self.pip_command_base = get_pip_executable()
        self.ootb_command = f"{self.python_exe} -m {_OOTB_MODULE}"
        _service_instance = self # Set global reference

    def SvcStop(self):
        log_info(f"Service stop requested.")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        # Signal the command processor thread to stop
        self.command_queue.put(None) # Sentinel value
        # Signal the main wait loop
        win32event.SetEvent(self.hWaitStop)
        # Stopping waitress gracefully from another thread is non-trivial.
        # We rely on the SCM timeout / process termination for now.
        log_info(f"{_SERVICE_NAME} SvcStop: Stop signaled. Server thread will be terminated by SCM.")


    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        try:
            log_info(f"{_SERVICE_NAME} starting.")
            # Start the command processor thread
            self.command_processor_thread = threading.Thread(
                target=self.process_commands, name="CommandProcessor", daemon=True)
            self.command_processor_thread.start()
            log_info("Command processor thread started.")

            # Start the Flask server (via Waitress) in a separate thread
            self.server_thread = threading.Thread(
                target=self.run_server, name="WebServerThread", daemon=True)
            self.server_thread.start()
            log_info(f"Web server thread started, listening on {_LISTEN_HOST}:{_LISTEN_PORT}.")

            log_info(f"{_SERVICE_NAME} running. Waiting for stop signal.")
            # Keep the main service thread alive waiting for stop signal
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            log_info(f"{_SERVICE_NAME} received stop signal in main thread.")

        except Exception as e:
            log_error(f"Fatal error in SvcDoRun: {e}", exc_info=True)
            self.SvcStop() # Signal stop if possible
        finally:
            log_info(f"{_SERVICE_NAME} SvcDoRun finished.")


    def run_server(self):
        """Runs the Flask app using Waitress."""
        log_info(f"Waitress server starting on {_LISTEN_HOST}:{_LISTEN_PORT}")
        try:
            serve(flask_app, host=_LISTEN_HOST, port=_LISTEN_PORT, threads=4)
            log_info("Waitress server has stopped.") # Should only happen on shutdown
        except Exception as e:
            log_error(f"Web server thread encountered an error: {e}", exc_info=True)
            # Consider signaling the main thread to stop if the web server fails critically
            # For now, just log the error.


    def process_commands(self):
        """Worker thread to process commands from the queue."""
        log_info("Command processor thread starting.")
        while self.is_running:
            try:
                item = self.command_queue.get(block=True, timeout=1) # Add timeout to check is_running periodically
                if item is None:
                    log_info("Command processor received stop signal.")
                    break # Exit loop

                command_id, command = item
                action = command.get("action")
                target = command.get("target_user", "all_active")
                status = "failed_unknown" # Default

                log_info(f"Dequeued Command ID {command_id}: action='{action}', target='{target}'")

                try:
                    if action == "update":
                        status = self.handle_update()
                    elif action == "stop_ootb":
                        status = self.handle_stop(target)
                    elif action == "start_ootb":
                        status = self.handle_start(target)
                    else:
                        log_error(f"Unknown action in queue: {action}")
                        status = "failed_unknown_action"
                except Exception as handler_ex:
                    log_error(f"Exception processing Command ID {command_id} ({action}): {handler_ex}", exc_info=True)
                    status = "failed_exception"
                finally:
                    self.report_command_status(command_id, status)
                    self.command_queue.task_done()

            except queue.Empty:
                # Timeout occurred, just loop again and check self.is_running
                continue
            except Exception as e:
                 log_error(f"Error in command processing loop: {e}", exc_info=True)
                 if self.is_running:
                     time.sleep(5)

        log_info("Command processor thread finished.")


    def report_command_status(self, command_id, status, details=""):
        """Sends command status back to the server."""
        if not _SERVER_STATUS_REPORT_URL:
            log_warning("No server status report URL configured. Skipping report.")
            return

        payload = {
            "command_id": command_id,
            "status": status,
            "details": details,
            "machine_id": os.getenv('COMPUTERNAME', 'unknown_guard')
        }
        log_info(f"Reporting status for command {command_id}: {status}")
        try:
            response = self.session.post(_SERVER_STATUS_REPORT_URL, json=payload, timeout=15)
            response.raise_for_status()
            log_info(f"Status report for command {command_id} accepted by server.")
        except requests.exceptions.RequestException as e:
            log_error(f"Failed to report status for command {command_id}: {e}")
        except Exception as e:
             log_error(f"Unexpected error reporting status for command {command_id}: {e}", exc_info=True)

    # --- Command Handlers --- Copying full implementation from previous version

    def handle_update(self):
        log_info("Executing OOTB update...")
        if not self.pip_command_base:
            log_error("Cannot update: pip command not found.")
            return "failed_pip_not_found"

        update_command = f"{self.pip_command_base} install --upgrade --no-cache-dir {_PACKAGE_NAME}"
        log_info(f"Running update command: {update_command}")
        try:
            result = subprocess.run(update_command, shell=True, capture_output=True, text=True, check=True, timeout=300, encoding='utf-8')
            log_info(f"Update successful: \nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
            return "success"
        except subprocess.CalledProcessError as e:
            log_error(f"Update failed (Exit Code {e.returncode}):\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}")
            return f"failed_exit_{e.returncode}"
        except subprocess.TimeoutExpired:
             log_error(f"Update command timed out.")
             return "failed_timeout"
        except Exception as e:
            log_error(f"Unexpected error during update: {e}", exc_info=True)
            return "failed_exception"


    def _get_ootb_processes(self, target_user="all_active"):
        ootb_procs = []
        target_pid_list = []
        try:
            target_users = set()
            if target_user == "all_active":
                 for user_session in psutil.users():
                      username = user_session.name.split('\\')[-1]
                      target_users.add(username.lower())
            else:
                 target_users.add(target_user.lower())

            log_info(f"Searching for OOTB processes for users: {target_users}")

            python_exe_path = self.python_exe.strip('"') # Get unquoted path for comparison

            for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline', 'exe']):
                try:
                    pinfo = proc.info
                    proc_username = pinfo['username']
                    if proc_username:
                        proc_username = proc_username.split('\\')[-1].lower()

                    if proc_username in target_users:
                        cmdline = ' '.join(pinfo['cmdline']) if pinfo['cmdline'] else ''
                        # Check if the process executable matches our python path AND module is in cmdline
                        if pinfo['exe'] and pinfo['exe'] == python_exe_path and _OOTB_MODULE in cmdline:
                            log_info(f"Found matching OOTB process: PID={pinfo['pid']}, User={pinfo['username']}, Cmd={cmdline}")
                            ootb_procs.append(proc)
                            target_pid_list.append(pinfo['pid'])

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            log_info(f"Found {len(ootb_procs)} OOTB process(es) matching criteria: {target_pid_list}")
        except Exception as e:
             log_error(f"Error enumerating processes: {e}", exc_info=True)
        return ootb_procs


    def handle_stop(self, target_user="all_active"):
        log_info(f"Executing stop OOTB for target '{target_user}'...")
        stopped_count = 0
        procs_to_stop = self._get_ootb_processes(target_user)

        if not procs_to_stop:
            log_info("No running OOTB processes found for target.")
            return "no_process_found"

        for proc in procs_to_stop:
            try:
                username = proc.info.get('username', 'unknown_user')
                log_info(f"Terminating process PID={proc.pid}, User={username}")
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                    log_info(f"Process PID={proc.pid} terminated successfully.")
                    stopped_count += 1
                except psutil.TimeoutExpired:
                    log_warning(f"Process PID={proc.pid} did not terminate gracefully, killing.")
                    proc.kill()
                    stopped_count += 1
            except psutil.NoSuchProcess:
                 log_info(f"Process PID={proc.pid} already terminated.")
                 stopped_count +=1
            except psutil.AccessDenied:
                log_error(f"Access denied trying to terminate process PID={proc.pid}. Service might lack privileges?")
            except Exception as e:
                log_error(f"Error stopping process PID={proc.pid}: {e}", exc_info=True)

        log_info(f"Finished stopping OOTB. Terminated {stopped_count} process(es).")
        return f"success_stopped_{stopped_count}"


    def handle_start(self, target_user="all_active"):
        log_info(f"Executing start OOTB for target '{target_user}'...")
        started_count = 0
        target_users_started = set()
        users_failed_to_start = set()

        try:
            sessions = win32ts.WTSEnumerateSessions(win32ts.WTS_CURRENT_SERVER_HANDLE)
            active_sessions = {}

            for session in sessions:
                 if session['State'] == win32ts.WTSActive:
                    try:
                         user = win32ts.WTSQuerySessionInformation(win32ts.WTS_CURRENT_SERVER_HANDLE, session['SessionId'], win32ts.WTSUserName)
                         if user:
                              normalized_user = user.lower()
                              active_sessions[normalized_user] = session['SessionId']
                    except Exception as query_err:
                         log_warning(f"Could not query session {session['SessionId']}: {query_err}")

            log_info(f"Found active user sessions: {active_sessions}")

            target_session_map = {}
            if target_user == "all_active":
                 target_session_map = active_sessions
            else:
                normalized_target = target_user.lower()
                if normalized_target in active_sessions:
                     target_session_map[normalized_target] = active_sessions[normalized_target]
                else:
                     log_warning(f"Target user '{target_user}' not found in active sessions.")
                     return "failed_user_not_active"

            if not target_session_map:
                 log_info("No target user sessions found to start OOTB in.")
                 return "failed_no_target_sessions"

            running_procs = self._get_ootb_processes(target_user)
            users_already_running = set()
            for proc in running_procs:
                try:
                     proc_username = proc.info.get('username')
                     if proc_username:
                          users_already_running.add(proc_username.split('\\')[-1].lower())
                except Exception:
                     pass

            log_info(f"Users already running OOTB: {users_already_running}")

            for user, session_id in target_session_map.items():
                 token = None
                 try:
                     if user in users_already_running:
                         log_info(f"OOTB already seems to be running for user '{user}'. Skipping start.")
                         continue

                     log_info(f"Attempting to start OOTB for user '{user}' in session {session_id}...")
                     token = win32ts.WTSQueryUserToken(session_id)
                     env = win32profile.CreateEnvironmentBlock(token, False)
                     startup = win32process.STARTUPINFO()
                     startup.dwFlags = win32process.STARTF_USESHOWWINDOW
                     startup.wShowWindow = win32con.SW_SHOW # Try showing the window
                     startup.lpDesktop = 'winsta0\\default'
                     creation_flags = win32process.CREATE_NEW_CONSOLE | win32process.CREATE_UNICODE_ENVIRONMENT

                     hProcess, hThread, dwPid, dwTid = win32process.CreateProcessAsUser(
                         token, self.python_exe, self.ootb_command,
                         None, None, False, creation_flags, env, None, startup
                     )
                     log_info(f"Successfully started OOTB for user '{user}' (PID: {dwPid}).")
                     started_count += 1
                     target_users_started.add(user)
                     win32api.CloseHandle(hProcess)
                     win32api.CloseHandle(hThread)

                 except Exception as proc_err:
                      log_error(f"Failed to start OOTB for user '{user}' in session {session_id}: {proc_err}", exc_info=True)
                      users_failed_to_start.add(user)
                 finally:
                      if token:
                           try: win32api.CloseHandle(token)
                           except: pass

            log_info(f"Finished starting OOTB. Started {started_count} new instance(s). Failed for users: {users_failed_to_start or 'None'}")
            if users_failed_to_start:
                 return f"partial_success_started_{started_count}_failed_for_{len(users_failed_to_start)}"
            elif started_count > 0:
                 return f"success_started_{started_count}"
            else:
                 return "no_action_needed_already_running"

        except Exception as e:
             log_error(f"Error during start OOTB process: {e}", exc_info=True)
             return "failed_exception"

# --- Main Execution Block ---
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log_info("Starting service in debug mode...")
        print(f"Running Flask server via Waitress on {_LISTEN_HOST}:{_LISTEN_PORT} for debugging...")
        print("Service logic (command processing) will NOT run in this mode.")
        print("Use this primarily to test the '/command' endpoint receiving POSTs.")
        print("Press Ctrl+C to stop.")
        try:
             serve(flask_app, host=_LISTEN_HOST, port=_LISTEN_PORT, threads=1)
        except KeyboardInterrupt:
             print("\nDebug server stopped.")

    elif len(sys.argv) == 1:
        try:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(GuardService)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details.winerror == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                print(f"Error: Not started by SCM.")
                print(f"Use 'python {os.path.basename(__file__)} install|start|stop|remove|debug'")
            else:
                print(f"Error preparing service: {details}")
        except Exception as e:
             print(f"Unexpected error initializing service: {e}")
    else:
        win32serviceutil.HandleCommandLine(GuardService) 