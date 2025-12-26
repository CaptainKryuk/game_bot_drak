import pyautogui
from utils import constants as cnst

from .location import LocationService


class StateService:
	@staticmethod
	def get_state(button_name: str, screenshot, grayscale=True) -> bool:
		service = LocationService()
		try:
			service.get_object_location(
				screenshot,
				cnst.ObjectTypeEnum.buttons,
				button_name,
				grayscale=grayscale,
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
		Закончился ли бой
		"""
		return StateService.get_state('win_fight_marker', screenshot)

	@staticmethod
	def is_can_hit_offence(screenshot, attack_name) -> bool:
		"""
		Могу ли нажать на атаку рукой
		"""
		return StateService.get_state(attack_name, screenshot, grayscale=False)

	@staticmethod
	def is_can_hit_magic(screenshot, spell_name: str) -> bool:
		"""
		Могу ли нажать на атаку магией
		"""
		return StateService.get_state(spell_name, screenshot, grayscale=False)
