import pyautogui
from utils import constants as cnst

from .location import LocationService


class StateService:
	@staticmethod
	def get_state(button_name: str, screenshot) -> bool:
		service = LocationService()
		try:
			service.get_object_location(
				screenshot, cnst.ObjectTypeEnum.buttons, button_name
			)
			return True
		except pyautogui.ImageNotFoundException:
			return False

	@staticmethod
	def is_on_map(screenshot) -> bool:
		"""
		Находишься ли сейчас на карте
		"""
		return StateService.get_state('navigation', screenshot)

	@staticmethod
	def is_in_fight(screenshot) -> bool:
		"""
		Находишься ли сейчас в бою
		"""
		return StateService.get_state('fight_marker', screenshot)

	@staticmethod
	def is_can_hit(screenshot) -> bool:
		"""
		Находишься ли сейчас в бою
		"""
		return StateService.get_state('offence', screenshot)

	@staticmethod
	def is_enemy_marked(screenshot) -> bool:
		"""
		Показывается ли блок "Напасть"
		"""
		return StateService.get_state('attack', screenshot)

	@staticmethod
	def is_fight_ended(screenshot) -> bool:
		"""
		Показывается ли блок "Напасть"
		"""
		return StateService.get_state('win_fight_marker', screenshot)
