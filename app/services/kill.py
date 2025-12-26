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
		self._find_and_click_enemy('marks')
		self._start_fight()
		strategy_service = StrategyService(strategy, self.location, self.state)
		strategy_service.start()

	def _find_and_click_enemy(self, folder_name: str):
		logger.info('🔍 Ищем противника или его марку задания')

		screenshot = self.location.get_game_screenshot()
		enemy_location = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.enemies, folder_name, grayscale=False
		)

		logger.info(f'👾 Противник {folder_name} найден')
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
