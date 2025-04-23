# src/computer_use_ootb_internal/guard_service.py
import sys
import os
import time
import logging
import subprocess
import pathlib
import ctypes
import requests # For server polling
import servicemanager # From pywin32
import win32serviceutil # From pywin32
import win32service # From pywin32
import win32event # From pywin32
import win32api # From pywin32
import win32process # From pywin32
import win32security # From pywin32
import win32profile # From pywin32
import win32ts # From pywin32 (Terminal Services API)
import win32con # Added import
import psutil # For process/user info

# --- Configuration ---
# Internal service name
_SERVICE_NAME = "OOTBGuardService"
# Display name in Windows Services MMC
_SERVICE_DISPLAY_NAME = "OOTB Guard Service"
# Description in Windows Services MMC
_SERVICE_DESCRIPTION = "Background service for OOTB monitoring and remote management."
# Package name for updates
_PACKAGE_NAME = "computer-use-ootb-internal"
# Main module to start/stop for users
_OOTB_MODULE = "computer_use_ootb_internal.app_teachmode"
# Server endpoint to poll for commands (replace with your actual URL)
_SERVER_COMMAND_URL = "http://52.160.105.102:7000/api/guard" # Using HTTP as port was specified
# How often to poll the server (in seconds)
_POLLING_INTERVAL = 60
# Placeholder for a machine identifier or API key for the server
_MACHINE_ID = "YOUR_MACHINE_ID_OR_API_KEY" # EXAMPLE - Implement actual ID/auth
# Log file location (consider using Windows Event Log instead for production)
_LOG_FILE = pathlib.Path(os.environ['PROGRAMDATA']) / "OOTBGuardService" / "guard.log"
# --- End Configuration ---

# Ensure log directory exists
_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=_LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def get_python_executable():
    """Gets the quoted path to the current python executable."""
    python_exe = sys.executable
    if " " in python_exe and not python_exe.startswith('"'):
        python_exe = f'"{python_exe}"'
    return python_exe

def get_pip_executable():
    """Tries to locate the pip executable in the same environment."""
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
    logging.info(msg)
    try:
        servicemanager.LogInfoMsg(str(msg)) # Also log to Windows Event Log Application channel
    except Exception as e:
        logging.warning(f"Could not write to Windows Event Log: {e}") # Avoid crashing service if event log fails

def log_error(msg, exc_info=False):
    logging.error(msg, exc_info=exc_info)
    try:
        servicemanager.LogErrorMsg(str(msg))
    except Exception as e:
        logging.warning(f"Could not write error to Windows Event Log: {e}")

class GuardService(win32serviceutil.ServiceFramework):
    _svc_name_ = _SERVICE_NAME
    _svc_display_name_ = _SERVICE_DISPLAY_NAME
    _svc_description_ = _SERVICE_DESCRIPTION

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        self.python_exe = get_python_executable()
        self.pip_command_base = get_pip_executable()
        self.ootb_command = f"{self.python_exe} -m {_OOTB_MODULE}"
        self.session = requests.Session() # Reuse session for polling

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False
        log_info(f"{_SERVICE_NAME} is stopping.")

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main_loop()
        # If main_loop exits cleanly (shouldn't happen with while self.is_running)
        log_info(f"{_SERVICE_NAME} main loop exited.")


    def main_loop(self):
        log_info(f"{_SERVICE_NAME} started. Polling {_SERVER_COMMAND_URL} every {_POLLING_INTERVAL}s.")
        while self.is_running:
            try:
                self.poll_server_for_commands()
            except Exception as e:
                log_error(f"Error in main loop polling cycle: {e}", exc_info=True)

            # Wait for stop event or timeout
            rc = win32event.WaitForSingleObject(self.hWaitStop, _POLLING_INTERVAL * 1000)
            if rc == win32event.WAIT_OBJECT_0:
                # Stop event signaled
                break
        log_info(f"{_SERVICE_NAME} is shutting down main loop.")


    def poll_server_for_commands(self):
        log_info(f"Polling server for commands...")
        try:
            headers = {'Authorization': f'Bearer {_MACHINE_ID}'} # Example auth
            # Add machine identifier if needed by server
            params = {'machine_id': os.getenv('COMPUTERNAME', 'unknown')}
            response = self.session.get(_SERVER_COMMAND_URL, headers=headers, params=params, timeout=30)
            response.raise_for_status() # Raise exception for bad status codes

            commands = response.json() # Expecting a list of command objects
            if not commands:
                # log_info("No commands received.") # Reduce log noise
                return

            log_info(f"Received {len(commands)} command(s). Processing...")
            for command in commands:
                action = command.get("action")
                target = command.get("target_user", "all_active") # Default to all
                command_id = command.get("command_id", "N/A") # Optional: for reporting status

                log_info(f"Processing Command ID {command_id}: action='{action}', target='{target}'")
                status = "failed" # Default status
                try:
                    if action == "update":
                        status = self.handle_update()
                    elif action == "stop_ootb":
                        status = self.handle_stop(target)
                    elif action == "start_ootb":
                        status = self.handle_start(target)
                    else:
                        log_error(f"Unknown action received: {action}")
                        status = "unknown_action"
                except Exception as handler_ex:
                     log_error(f"Error executing action '{action}' for command {command_id}: {handler_ex}", exc_info=True)
                     status = "execution_error"

                # TODO: Add mechanism to report command completion/failure back to server
                # Example: self.report_command_status(command_id, status)
                log_info(f"Finished processing Command ID {command_id}: Status='{status}'")

        except requests.exceptions.RequestException as e:
            log_error(f"Failed to poll server: {e}")
        except Exception as e:
            log_error(f"Error processing server commands: {e}", exc_info=True)


    def handle_update(self):
        log_info("Executing OOTB update...")
        if not self.pip_command_base:
            log_error("Cannot update: pip command not found.")
            return "failed_pip_not_found"

        update_command = f"{self.pip_command_base} install --upgrade --no-cache-dir {_PACKAGE_NAME}"
        log_info(f"Running update command: {update_command}")
        try:
            # Run update command
            result = subprocess.run(update_command, shell=True, capture_output=True, text=True, check=True, timeout=300)
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
        """Finds OOTB processes, optionally filtering by username."""
        ootb_procs = []
        target_pid_list = []
        try:
            # Get a list of usernames we are interested in
            target_users = set()
            if target_user == "all_active":
                 for user_session in psutil.users():
                      # Normalize username (remove domain if present)
                      username = user_session.name.split('\\')[-1]
                      target_users.add(username.lower())
            else:
                 target_users.add(target_user.lower())

            log_info(f"Searching for OOTB processes for users: {target_users}")

            for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
                try:
                    pinfo = proc.info
                    # Normalize process username
                    proc_username = pinfo['username']
                    if proc_username:
                        proc_username = proc_username.split('\\')[-1].lower()

                    # Check if process user is one of the targets
                    if proc_username in target_users:
                        # Check if command line matches our OOTB app pattern
                        cmdline = ' '.join(pinfo['cmdline']) if pinfo['cmdline'] else ''
                        # Simple check: does it contain python executable and the module name?
                        if (self.python_exe.strip('"') in cmdline) and (_OOTB_MODULE in cmdline):
                            log_info(f"Found matching OOTB process: PID={pinfo['pid']}, User={pinfo['username']}, Cmd={cmdline}")
                            ootb_procs.append(proc)
                            target_pid_list.append(pinfo['pid'])

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue # Process might have died or we lack permissions
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
                proc.terminate() # Ask nicely first
                try:
                    proc.wait(timeout=3) # Wait a bit
                    log_info(f"Process PID={proc.pid} terminated successfully.")
                    stopped_count += 1
                except psutil.TimeoutExpired:
                    log_warning(f"Process PID={proc.pid} did not terminate gracefully, killing.")
                    proc.kill()
                    stopped_count += 1
            except psutil.NoSuchProcess:
                 log_info(f"Process PID={proc.pid} already terminated.")
                 stopped_count +=1 # Count it if it disappeared
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
            active_sessions = {} # Store user: session_id for active sessions

            for session in sessions:
                 # Look for Active sessions, potentially disconnected ones too?
                 # For now, only WTSActive
                 if session['State'] == win32ts.WTSActive:
                    try:
                         user = win32ts.WTSQuerySessionInformation(win32ts.WTS_CURRENT_SERVER_HANDLE, session['SessionId'], win32ts.WTSUserName)
                         if user: # Filter out system sessions etc.
                              normalized_user = user.lower()
                              active_sessions[normalized_user] = session['SessionId']
                    except Exception as query_err:
                         log_warning(f"Could not query session {session['SessionId']}: {query_err}")

            log_info(f"Found active user sessions: {active_sessions}")

            target_session_map = {} # user:session_id
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

            # Check if OOTB is already running for the target users
            running_procs = self._get_ootb_processes(target_user)
            users_already_running = set()
            for proc in running_procs:
                try:
                     proc_username = proc.info.get('username')
                     if proc_username:
                          users_already_running.add(proc_username.split('\\')[-1].lower())
                except Exception:
                     pass # Ignore errors getting username here

            log_info(f"Users already running OOTB: {users_already_running}")

            for user, session_id in target_session_map.items():
                 token = None # Ensure token is reset/defined
                 try:
                     if user in users_already_running:
                         log_info(f"OOTB already seems to be running for user '{user}'. Skipping start.")
                         continue

                     log_info(f"Attempting to start OOTB for user '{user}' in session {session_id}...")

                     # Get user token
                     token = win32ts.WTSQueryUserToken(session_id)

                     # Create environment block for the user
                     env = win32profile.CreateEnvironmentBlock(token, False)

                     # Create startup info
                     startup = win32process.STARTUPINFO()
                     startup.dwFlags = win32process.STARTF_USESHOWWINDOW
                     # Attempt to show window on user's desktop
                     # Requires Service to have "Allow service to interact with desktop" checked
                     # AND Interactive Services Detection service running (often disabled now).
                     # May be better to run hidden (SW_HIDE) or default.
                     startup.wShowWindow = win32con.SW_SHOW
                     startup.lpDesktop = 'winsta0\\default' # Try targeting default interactive desktop

                     # Create process as user
                     # Needs SeAssignPrimaryTokenPrivilege, SeIncreaseQuotaPrivilege for service account.
                     creation_flags = win32process.CREATE_NEW_CONSOLE | win32process.CREATE_UNICODE_ENVIRONMENT

                     hProcess, hThread, dwPid, dwTid = win32process.CreateProcessAsUser(
                         token,              # User token
                         self.python_exe,    # Application name (python executable)
                         self.ootb_command,  # Command line
                         None,               # Process attributes
                         None,               # Thread attributes
                         False,              # Inherit handles
                         creation_flags,     # Creation flags
                         env,                # Environment
                         None,               # Current directory (use default)
                         startup             # Startup info
                     )
                     log_info(f"Successfully started OOTB for user '{user}' (PID: {dwPid}).")
                     started_count += 1
                     target_users_started.add(user)
                     # Close handles immediately
                     win32api.CloseHandle(hProcess)
                     win32api.CloseHandle(hThread)

                 except Exception as proc_err:
                      log_error(f"Failed to start OOTB for user '{user}' in session {session_id}: {proc_err}", exc_info=True)
                      users_failed_to_start.add(user)
                 finally:
                      # Ensure token handle is always closed if obtained
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


# This block is essential for the service framework to handle
# command-line arguments like 'install', 'start', 'stop', 'remove', 'debug'.
if __name__ == '__main__':
    # Add logic to allow debugging from command line easily
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log_info("Starting service in debug mode...")
        service_instance = GuardService(sys.argv)
        service_instance.is_running = True # Ensure loop runs
        try:
            # Run the main loop directly for debugging
            service_instance.main_loop()
            # Simulate stop signal for clean exit in debug
            # service_instance.SvcStop() # Or let it run until Ctrl+C?
        except KeyboardInterrupt:
            log_info("Debug mode interrupted by user.")
            service_instance.SvcStop() # Attempt clean stop
        log_info("Debug mode finished.")
    elif len(sys.argv) == 1:
        # Called without arguments, run as a service instance via SCM
        try:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(GuardService)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details.winerror == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                print(f"Error: Cannot connect to Service Control Manager.")
                print(f"Use 'python {os.path.basename(__file__)} install|start|stop|remove|debug'")
            else:
                print(f"Error preparing service: {details}")
        except Exception as e:
             print(f"Unexpected error initializing service: {e}")

    else:
         # Called with install/start/stop/remove args, let ServiceFramework handle them
        win32serviceutil.HandleCommandLine(GuardService) 