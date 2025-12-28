from enum import Enum

import pyautogui

screen_width, screen_height = pyautogui.size()
base_region = (screen_width // 2, 0, screen_width // 2, screen_height)

enemy_region = (1949, 422, 1390, 721)


class ObjectTypeEnum(str, Enum):
	buttons = 'buttons'
	enemies = 'enemies'


class FarmingTypeEnum(str, Enum):
	essence = 'essence'
	patron = 'patron'
	sunday = 'sunday'
