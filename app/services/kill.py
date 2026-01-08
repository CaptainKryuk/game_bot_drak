import logging
import time

import pyautogui
from services.location import LocationService
from services.state import StateService
from services.strategy import StrategyService
from utils import constants as cnst

logger = logging.getLogger(__name__)


class KillService:
	def __init__(self, location: LocationService, state: StateService):
		self.location = location
		self.state = state

	def kill_enemy(self, strategy: cnst.FarmingTypeEnum):
		try:
			self._find_and_click_enemy('marks', strategy)
		except pyautogui.ImageNotFoundException:
			# Не найдена марка или враг
			self._close_final_buttons()
			self._find_and_click_enemy('marks', strategy)

		self._start_fight()

		strategy_service = StrategyService(strategy, self.location, self.state)
		strategy_service.start()

	def _find_and_click_enemy(self, folder_name: str, strategy: cnst.FarmingTypeEnum):
		logger.info('🔍 Ищем противника или его марку задания')

		region = cnst.ENEMY_REGION_MAP[strategy]

		screenshot = self.location.get_game_screenshot(region)
		enemy_location = self.location.get_object_location(
			screenshot,
			cnst.ObjectTypeEnum.enemies,
			folder_name,
			grayscale=False,
			region=region,
		)

		logger.info(f'👾 Противник {folder_name} найден {enemy_location}')
		self.location.click(enemy_location, duration=0.05, is_double=True)

	def _start_fight(self):
		time.sleep(0.5)

		screenshot = self.location.get_game_screenshot()

		if self.state.is_in_fight(screenshot):
			return

		if self.state.is_enemy_marked(screenshot):
			logger.info('🏳 Появилась метка на противнике, необходимо нажать "Напасть"')
			button = self.location.get_object_location(
				screenshot, cnst.ObjectTypeEnum.buttons, 'attack'
			)
			self.location.click(button)
			return

		if not self.state.is_in_fight(screenshot):
			raise pyautogui.ImageNotFoundException

	def _close_final_buttons(self) -> None:
		"""
		Нажали ли хоть на одну кнопку, которая закроет окно
		"""
		screenshot = self.location.get_game_screenshot()

		self.click_close_button(screenshot, 'continue')
		self.click_close_button(screenshot, 'continue_2')
		self.click_close_button(screenshot, 'close')
		self.click_close_button(screenshot, 'take_profit')

	def click_close_button(self, screenshot, button_name: str) -> bool:
		try:
			button_location = self.location.get_object_location(
				screenshot, cnst.ObjectTypeEnum.buttons, button_name
			)
			self.location.click(button_location)
			return True
		except pyautogui.ImageNotFoundException:
			logger.info(f'Кнопка {button_name} с закрытием окна не найдена')
			return False
