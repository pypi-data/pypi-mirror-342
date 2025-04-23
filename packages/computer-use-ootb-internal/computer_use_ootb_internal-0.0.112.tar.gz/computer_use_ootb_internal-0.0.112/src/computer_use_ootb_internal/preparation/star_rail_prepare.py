# src/computer_use_ootb_internal/preparation/star_rail_prepare.py
import time
import platform
import pyautogui
import webbrowser
import logging # Use logging instead of print for better practice

# Set up logging for this module if needed, or rely on root logger
log = logging.getLogger(__name__)

def run_preparation(state):
    """
    Performs environment preparation specific to Star Rail on Windows.
    Opens the specified URL in Edge and performs initial clicks.
    """
    if platform.system() != "Windows":
        log.info("Star Rail preparation skipped: Not running on Windows.")
        return

    log.info("Star Rail preparation: Starting environment setup on Windows...")
    url = "https://sr.mihoyo.com/cloud/#/" # Consider making this configurable later
    browser_opened = False
    try:
        # Use only webbrowser.open
        log.info(f"Attempting to open {url} using webbrowser.open()...")
        if webbrowser.open(url):
            log.info(f"Successfully requested browser to open {url} via webbrowser.open().")
            browser_opened = True
        else:
            log.warning("webbrowser.open() returned False, indicating potential failure.")

        if not browser_opened:
            log.error("Failed to confirm browser opening via webbrowser.open(). Will still attempt clicks.")

        # Add pyautogui click after attempting to open the browser
        log.info("Proceeding with pyautogui actions...")
        time.sleep(5) # Wait time for the browser to load

        # Get screen size
        screen_width, screen_height = pyautogui.size()
        log.info(f"Detected screen size: {screen_width}x{screen_height}")

        # Calculate click coordinates based on a reference resolution (e.g., 1280x720)
        # TODO: Make these coordinates more robust or configurable
        click_x = int(screen_width * (1036 / 1280))
        click_y = int(screen_height * (500 / 720))
        log.info(f"Calculated click coordinates: ({click_x}, {click_y})")

        # Disable failsafe before clicking
        pyautogui.FAILSAFE = False
        log.info("PyAutoGUI failsafe temporarily disabled.")

        log.info(f"Clicking at coordinates: ({click_x}, {click_y})")
        pyautogui.click(click_x, click_y)
        time.sleep(2)
        pyautogui.click(click_x, click_y) # Double click?

        log.info("Star Rail preparation clicks completed.")

    except Exception as e:
        log.error(f"Error during Star Rail preparation (browser/click): {e}", exc_info=True)
    finally:
         # Ensure failsafe is re-enabled
         pyautogui.FAILSAFE = True
         log.info("PyAutoGUI failsafe re-enabled.") 