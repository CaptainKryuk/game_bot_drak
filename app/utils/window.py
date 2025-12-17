#!/usr/bin/env python3
import subprocess

import pyautogui

screen_width, screen_height = pyautogui.size()

LEFT = screen_width // 2 + 100
TOP = 0
RIGHT = screen_width
BOTTOM = screen_height

APPLE_SCRIPT = f'''
tell application "Google Chrome"
    if not (exists window 1) then
        make new window
    end if
    set bounds of front window to {{{LEFT}, {TOP}, {RIGHT}, {BOTTOM}}}
    activate
end tell
'''

def main():
    # полезно один раз распечатать, чтобы увидеть, что реально уходит в osascript
    # print(APPLE_SCRIPT)
    subprocess.run(["osascript", "-e", APPLE_SCRIPT], check=True)

if __name__ == "__main__":
    main()