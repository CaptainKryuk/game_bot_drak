import pyautogui

pos = pyautogui.position()
print(pos)  # Point(x=123, y=456)
print(pos.x, pos.y)  # отдельно по координатам
