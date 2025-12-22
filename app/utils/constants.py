from enum import Enum


class ObjectTypeEnum(str, Enum):
	buttons = 'buttons'
	enemies = 'enemies'


class FarmingTypeEnum(str, Enum):
	essence = 'essence'
	patron = 'patron'
	sunday = 'sunday'
