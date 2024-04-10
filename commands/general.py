import random
import webbrowser
import subprocess
import pyautogui
import time
from collections.abc import Iterable
import os

CHARACTER_TYPING_DELAY_MIN, CHARACTER_TYPING_DELAY_MAX = 0.04, 0.08  # In seconds
commands_general = {
    # General commands
    ('connect', 'wifi'): lambda ssid, key: connect_wifi(ssid, key),
    ('disconnect', 'wifi'): lambda: disconnect_wifi(),
    ('wifi', 'connections'): lambda: jsonify(check_wifi_connection()),

    # Web browser commands
    ('open', 'browser'): lambda url: open_webpage(url),
    ('close', 'browser'): lambda: close_browser(),
    ('search', 'web'): lambda query: search_web(query),
    ('navigate', 'to'): lambda url: navigate_to(url),
    ('refresh', 'page'): lambda: refresh_page(),
    ('back', 'page'): lambda: go_back(),
    ('forward', 'page'): lambda: go_forward(),
    ('save', 'page'): lambda path: save_page(path),
    ('screenshot', 'page'): lambda path: take_screenshot(path),

    # New commands for opening applications
    ('open', 'application'): lambda app_name, *args: open_application(app_name),
    # New commands for opening applications
    ('open', 'software'): lambda app_name, *args: open_application(app_name),
    ('launch', 'software'): lambda app_name, *args: open_application(app_name),
    # ('open',): lambda app_name, *args: open_application(app_name),
    ('software',): lambda app_name, *args: open_application(app_name),

    ('application',): lambda app_name, *args: open_application(app_name),
    # New commands for opening applications
    ('software', 'application'): lambda app_name, *args: open_application(app_name),
    ('empty', 'recycle', 'bin'): lambda: empty_recycle_bin(),
    ('empty', 'bin'): lambda: empty_recycle_bin(),
    ('clear','recycle', 'bin'): lambda: empty_recycle_bin(),

}

def match_command_general(tokens):
    for cmd_tokens, action in commands_general.items():
        if all(cmd_token.lower() in tokens for cmd_token in cmd_tokens):
            params = [token.lower() for token in tokens if token.lower() not in cmd_tokens]
            result = action(*params)  # Pass all params to the action
            return result
    return None

def open_application(app_name, dir_path=None):
    # Press the Windows key to open the Start menu
    pyautogui.press('win')

    # Wait for the Start menu to appear
    time.sleep(1)

    # Type the application name into the search bar
    char_typing_delay = random.uniform(CHARACTER_TYPING_DELAY_MIN, CHARACTER_TYPING_DELAY_MAX)
    for c in app_name:
        pyautogui.write(c, interval=char_typing_delay)
    pyautogui.press('enter')

    # Wait for a moment for the search results to appear
    time.sleep(2)

    # Check if the specified directory exists; otherwise skip clicking on the App Path link
    if dir_path and os.path.exists(dir_path):
        try:
            index = next(i for i, item in enumerate(get_start_menu_results()) if item['type'] == 'AppPath' and item['fullText'].endswith(os.path.basename(dir_path)))
            click_at_position(get_start_menu_results()[index]['rect']['topLeft'], get_start_menu_results()[index]['rect']['bottomRight'])
            time.sleep(2)
        except StopIteration:
            pass

    # Click on the first search result (assuming it's the application)
    click_at_position(100, 200)  # Adjust the coordinates based on your screen resolution

    # Optionally, you can return a message indicating the action was performed
    return f"Opening '{app_name}'{'' if not dir_path else f': {dir_path}'}..."

def click_at_position(x, y):
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.click()

def get_start_menu_results(max_attempts=3, delay_between_attempts=0.1):
    attempts = 0
    while attempts < max_attempts:
        try:
            results = parse_start_menu_content()
            return results
        except Exception as e:
            print(f"Error parsing Start Menu content: {e}")
            attempts += 1
            time.sleep(delay_between_attempts)
    raise RuntimeError("Failed to retrieve Start Menu contents.")

def parse_start_menu_content():
    # TODO: Implement parser logic for extracting items from the Start Menu
    pass
def empty_recycle_bin():
    # Check the operating system to determine the appropriate command
    if os.name == 'nt':  # For Windows
        # Press Win + E to open File Explorer
        pyautogui.hotkey('win')
        time.sleep(1)  # Wait for File Explorer to open

        # Type "Recycle Bin" into the address bar
        pyautogui.write('Recycle Bin')
        pyautogui.press('enter')
        time.sleep(1)  # Wait for Recycle Bin to open

        # Press Ctrl + A to select all items
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)  # Wait for items to be selected

        # Press Shift + Delete to permanently delete selected items
        pyautogui.hotkey('shift', 'delete')
        time.sleep(1)  # Wait for confirmation dialog (if any)

        # Press Enter to confirm deletion
        pyautogui.press('enter')
        time.sleep(1)  # Wait for deletion process to complete

        return "Recycle bin emptied successfully."
    else:
        return "Emptying the recycle bin is not supported on this operating system."
