import sys
import os
import winreg
import ctypes
import platform
import shutil
import subprocess
import pathlib

REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "OOTBLite"  # Or a more specific name for your app's startup entry
# The package name as installed by pip
PACKAGE_NAME = "computer-use-ootb-internal"
# The main module to run at startup
STARTUP_MODULE = "computer_use_ootb_internal.app_teachmode"
# Name for the scheduled task
TASK_NAME = "OOTBLite_AutoUpdate"

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_python_executable():
    """Gets the quoted path to the current python executable."""
    python_exe = sys.executable
    if " " in python_exe and not python_exe.startswith('"'):
        python_exe = f'"{python_exe}"'
    return python_exe

def get_pip_executable():
    """Tries to locate the pip executable in the same environment."""
    python_path = pathlib.Path(sys.executable)
    # Common location is ../Scripts/pip.exe relative to python.exe
    pip_path = python_path.parent / "Scripts" / "pip.exe"
    if pip_path.exists():
         # Quote if necessary
        pip_exe = str(pip_path)
        if " " in pip_exe and not pip_exe.startswith('"'):
            pip_exe = f'"{pip_exe}"'
        return pip_exe
    else:
        # Fallback: try using 'python -m pip'
        print("Warning: pip.exe not found in Scripts directory. Falling back to 'python -m pip'.", file=sys.stderr)
        return f"{get_python_executable()} -m pip"

def run_powershell_command(command):
    """Executes a PowerShell command and handles output/errors."""
    try:
        # Use powershell.exe - it's more universally available than pwsh.exe
        # capture_output=True suppresses output unless there's an error
        # text=True decodes output/error streams
        # check=True raises CalledProcessError on non-zero exit codes
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", command],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )
        print(f"PowerShell command executed successfully.")
        if result.stdout:
            print("Output:\n", result.stdout)
        return True
    except FileNotFoundError:
        print("Error: 'powershell.exe' not found. Cannot manage scheduled tasks.", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error executing PowerShell command:", file=sys.stderr)
        print(f"  Command: {e.cmd}", file=sys.stderr)
        print(f"  Exit Code: {e.returncode}", file=sys.stderr)
        print(f"  Stderr: {e.stderr}", file=sys.stderr)
        print(f"  Stdout: {e.stdout}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An unexpected error occurred running PowerShell: {e}", file=sys.stderr)
        return False


def configure_startup():
    """Adds the application to Windows startup and sets up auto-update task."""
    if platform.system() != "Windows":
        print("Error: This utility is only for Windows.", file=sys.stderr)
        sys.exit(1)

    if not is_admin():
        print("Error: This utility requires administrative privileges.", file=sys.stderr)
        print("Please run this command from an Administrator Command Prompt or PowerShell.", file=sys.stderr)
        sys.exit(1)

    # 1. Configure Registry for Startup
    print("Configuring registry for application startup...")
    python_exe = get_python_executable()
    startup_command = f'{python_exe} -m {STARTUP_MODULE}'
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, startup_command)
        winreg.CloseKey(key)
        print(f"Success: Registry key HKLM\{REG_PATH}\{APP_NAME} set.")
        print(f"  Command: {startup_command}")
    except OSError as e:
        print(f"Error: Failed to set registry key HKLM\{REG_PATH}\{APP_NAME}", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        # Continue to task setup even if registry fails? Or exit? Let's exit for now.
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred setting registry key: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Configure Scheduled Task for Auto-Update
    print("\nConfiguring scheduled task for automatic updates...")
    pip_command = get_pip_executable()
    if not pip_command:
         print("Error: Could not determine pip command. Skipping scheduled task setup.", file=sys.stderr)
         sys.exit(1) # Exit if we can't find pip

    update_command_args = f'install --upgrade --no-cache-dir {PACKAGE_NAME}'
    # Need to handle quoting args for PowerShell if pip_command includes python.exe
    pip_exe_path = pip_command.split()[0]
    if "-m pip" in pip_command:
         ps_args = f"-m pip {update_command_args}"
    else:
         ps_args = update_command_args

    # PowerShell commands to create the task
    # Define Action, Trigger, Principal, Settings, and then Register
    # Note: Escaping quotes for PowerShell within Python string
    # Ensure executable path and arguments are properly quoted for PowerShell
    # Use triple-double quotes for f-strings containing single-quoted PowerShell strings
    action = f"""$Action = New-ScheduledTaskAction -Execute '{pip_exe_path}' -Argument '{ps_args.replace("'", "''")}'""" # Escape single quotes in args for PS string
    # Trigger: Daily, repeat every hour indefinitely
    trigger = f"""$Trigger = New-ScheduledTaskTrigger -Daily -At 3am; $Trigger.Repetition.Interval = 'PT1H'; $Trigger.Repetition.Duration = 'P10675199D'""" # Using large duration for 'indefinitely'
    # Principal: Run as SYSTEM user
    principal = f"""$Principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest"""
    # Settings: Allow start if on batteries, don't stop if goes off batteries (adjust as needed)
    settings = f"""$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable""" # Added StartWhenAvailable

    # Register Task: Use -Force to overwrite if it exists
    description = f"Hourly check for {PACKAGE_NAME} updates."
    # Escape single quotes in description just in case PACKAGE_NAME contains them
    escaped_description = description.replace("'", "''")
    register_command = f"""{action}; {trigger}; {principal}; {settings}; Register-ScheduledTask -TaskName '{TASK_NAME}' -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force -Description '{escaped_description}'"""

    print(f"Attempting to create/update scheduled task '{TASK_NAME}'...")
    if run_powershell_command(register_command):
        print(f"Success: Scheduled task '{TASK_NAME}' created/updated.")
        print(f"  Task Action: {pip_exe_path} {ps_args}")
    else:
        print(f"Error: Failed to configure scheduled task '{TASK_NAME}'. Please check PowerShell errors above.", file=sys.stderr)
        # Decide if failure here is critical
        # sys.exit(1)


def remove_startup():
    """Removes the application from Windows startup and removes auto-update task."""
    if platform.system() != "Windows":
        print("Error: This utility is only for Windows.", file=sys.stderr)
        sys.exit(1)

    if not is_admin():
        print("Error: This utility requires administrative privileges.", file=sys.stderr)
        print("Please run this command from an Administrator Command Prompt or PowerShell.", file=sys.stderr)
        sys.exit(1)

    # 1. Remove Registry Key
    print("Removing registry key...")
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        print(f"Success: Registry key HKLM\{REG_PATH}\{APP_NAME} removed.")
    except FileNotFoundError:
        print(f"Info: Registry key HKLM\{REG_PATH}\{APP_NAME} not found. No action taken.")
    except OSError as e:
        print(f"Error: Failed to delete registry key HKLM\{REG_PATH}\{APP_NAME}", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        # Continue to task removal
    except Exception as e:
        print(f"An unexpected error occurred removing registry key: {e}", file=sys.stderr)
        # Continue to task removal

    # 2. Remove Scheduled Task
    print(f"\nRemoving scheduled task '{TASK_NAME}'...")
    # Use -ErrorAction SilentlyContinue for Unregister-ScheduledTask if it might not exist
    # Use triple-double quotes for f-string
    unregister_command = f"""Unregister-ScheduledTask -TaskName '{TASK_NAME}' -Confirm:$false -ErrorAction SilentlyContinue"""

    if run_powershell_command(unregister_command):
        print(f"Success: Scheduled task '{TASK_NAME}' removed (if it existed).")
    else:
        print(f"Error: Failed to remove scheduled task '{TASK_NAME}'. Please check PowerShell errors above.", file=sys.stderr)

if __name__ == '__main__':
    print("This script provides startup and auto-update configuration utilities.")
    print("Use 'ootb-configure-startup' or 'ootb-remove-startup' as Administrator after installation.") 