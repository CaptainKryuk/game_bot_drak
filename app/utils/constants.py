from enum import Enum

import pyautogui

screen_width, screen_height = pyautogui.size()


base_region = (screen_width // 2, 0, screen_width // 2, screen_height)
base_enemy_region = (screen_width // 2, 331, screen_width // 2, screen_height - 331)
sunday_enemy_region = (screen_width // 2, 422, screen_width // 2, screen_height - 422)


class ObjectTypeEnum(str, Enum):
	buttons = 'buttons'
	enemies = 'enemies'


class FarmingTypeEnum(str, Enum):
	essence = 'essence'
	patron = 'patron'
	sunday = 'sunday'


ENEMY_REGION_MAP = {
	FarmingTypeEnum.essence: base_enemy_region,
	FarmingTypeEnum.patron: base_enemy_region,
	FarmingTypeEnum.sunday: sunday_enemy_region,
}
