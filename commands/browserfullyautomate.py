import os
import random
import re
import subprocess
import sys
import time
import webbrowser
import pyautogui
import pyperclip


def get_current_windows():
    """Returns all currently opened windows' titles."""
    output = subprocess.check_output(['powershell', '-Command', "[System.Diagnostics.Process]::GetCurrentProcess().MainWindowTitle"])
    return output.decode('utf-8').strip().split('\r\n')


def activate_window(title):
    """Activates the window with the given title."""
    def bring_to_front(hwnd):
        """Brings the window to front."""
        windll.user32.SetForegroundWindow(hwnd)

    hwnd = win32gui.FindWindowEx(0, 0, None, title)
    threading.Thread(target=bring_to_front, args=(hwnd,)).start()


def type_and_press_enter(text):
    """Types given text into the active window and presses Enter."""
    pyautogui.write(text, interval=0.1)
    pyautogui.press('enter')


def hotkey(*keys):
    """Presses specified keys as if they were from a keyboard."""
    pyautogui.hotkey(*keys)


def minimize_window():
    """Minimizes the current window."""
    hotkey('alt', 'space')
    time.sleep(1)
    hotkey('n')


def maximize_window():
    """Maximizes the current window."""
    hotkey('winleft', 'up')


def close_program():
    """Closes the entire running program."""
    hotkey('alt', 'f4')


def copy_text_to_clipboard(text):
    """Copies the provided text to the clipboard."""
    pyperclip.copy(text)


def paste_clipboard_contents():
    """Inserts clipboard contents into the active window."""
    pyautogui.hotkey('ctrl', 'v')


def set_zoom_level(percentage):
    """Sets the zoom level of the current window."""
    pyautogui.press('plus', presses=int((100 - percentage)/10))


def scroll_down(times=1):
    """Scrolls down N times."""
    for x in range(times):
        pyautogui.moveTo(100, 750, duration=0.25)
        pyautogui.dragRel(-100, 0, button='left', duration=0.25)


def scroll_up(times=1):
    """Scrolls up N times."""
    for x in range(times):
        pyautogui.moveTo(100, 100, duration=0.25)
        pyautogui.dragRel(-100, 0, button='left', duration=0.25)


def capture_screen_shot():
    """Captures the screen shot and saves it as screenshot.png"""
    img = pyautogui.screenshot()
    img.save("screenshot.png")


def get_mouse_position():
    """Prints the mouse coordinates."""
    x, y = pyautogui.position()
    print(f"Mouse position: X={x}, Y={y}")


def process_command(query):
    """Processes given query and performs appropriate action."""
    # Get Current Windows Titles
    cur_windows = set([_.strip() for _ in get_current_windows()])

    # Activate specific window
    pattern = r"activate\s+(?P<title>.*)"
    m = re.search(pattern, query)
    if m:
        title = m.groupdict()['title']
        if title in cur_windows:
            activate_window(title)
            return True

    # Open URL
    url_pattern = r"open\s+(?P<url>https?:\/\/(.*))"
    m = re.search(url_pattern, query)
    if m:
        url = m.groupdict()['url']
        webbrowser.open(url)
        return True

    # Search Google
    google_pattern = r"google\s+(?P<term>\S+)"
    m = re.search(google_pattern, query)
    if m:
        term = m.groupdict()['term']
        search_google(term)
        return True

    # Close Tab
    elif "close tab" in query:
        close_tab()
        return True

    # Switch to Last Tab
    elif "last tab" in query:
        switch_to_newest_tab()
        return True

    # Navigate Backwards
    elif "go back" in query:
        navigate_backward()
        return True

    # Navigate Forwards
   # ... Previous Code

def navigate_forward():
    """Navigates forward through browsing history."""
    hotkey('ctrl', 'right')


def scroll_down(times=1):
    """Scrolls down N times."""
    for x in range(times):
        pyautogui.moveTo(100, 750, duration=0.25)
        pyautogui.dragRel(-100, 0, button='left', duration=0.25)


def scroll_up(times=1):
    """Scrolls up N times."""
    for x in range(times):
        pyautogui.moveTo(100, 100, duration=0.25)
        pyautogui.dragRel(-100, 0, button='left', duration=0.25)


def capture_screen_shot():
    """Captures the screen shot and saves it as screenshot.png"""
    img = pyautogui.screenshot()
    img.save("screenshot.png")


def get_mouse_position():
    """Prints the mouse coordinates."""
    x, y = pyautogui.position()
    print(f"Mouse position: X={x}, Y={y}")

# Add the new functions to the dictionary
FUNCTIONS = {
    'activate': activate_window,
    'open': webbrowser.open,
    # 'google': search_google,
    # 'close tab': close_tab,
    # 'last tab': switch_to_newest_tab,
    # 'go back': navigate_backward,
    'go forward': navigate_forward,
    'scroll down': scroll_down,
    'scroll up': scroll_up,
    'take screenshot': capture_screen_shot,
    'show mouse position': get_mouse_position,
}

def process_command(query):
    """Processes given query and performs appropriate action."""
    words = query.lower().replace(", ", "").split()

    first_part = words[0].replace('.', '')

    if first_part in FUNCTIONS:
        arguments = ' '.join(words[1:]).strip() if len(words) > 1 else ""
        FUNCTIONS[first_part](arguments)
    else:
        print(f"Unknown command: {query}")