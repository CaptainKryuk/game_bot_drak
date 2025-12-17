from utils import constants as cnst
from .location import LocationService
import pyautogui


class StateService:

	@staticmethod
	def get_state(button_name: str) -> bool:
		try:
			LocationService.get_object_location(cnst.ObjectTypeEnum.buttons, button_name)
			return True
		except pyautogui.ImageNotFoundException:
			return False

	@staticmethod
	def is_on_map() -> bool:
		"""
		Находишься ли сейчас на карте
		"""
		return StateService.get_state('navigation')

	@staticmethod
	def is_in_fight() -> bool:
		"""
		Находишься ли сейчас в бою
		"""
		return StateService.get_state('fight_marker')

	@staticmethod
	def is_can_hit() -> bool:
		"""
		Находишься ли сейчас в бою
		"""
		return StateService.get_state('offence')

	@staticmethod
	def is_enemy_marked() -> bool:
		"""
		Показывается ли блок "Напасть"
		"""
		return StateService.get_state('attack')

	@staticmethod
	def is_fight_ended() -> bool:
		"""
		Показывается ли блок "Напасть"
		"""
		return StateService.get_state('win_fight_marker')