import logging
import time

from services.location import LocationService
from services.state import StateService
from utils import constants as cnst

logger = logging.getLogger(__name__)


class KillService:
	def __init__(self):
		self.location = LocationService()
		self.state = StateService()

	def kill_enemy(self, strategy: cnst.FarmingTypeEnum):
		self._find_and_click_enemy('marks')
		self._start_fight()
		self._fighting_enemy()

	def _find_and_click_enemy(self, folder_name: str):
		logger.info('🔍 Ищем противника или его марку задания')

		screenshot = self.location.get_game_screenshot()
		enemy_location = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.enemies, folder_name, grayscale=False
		)

		logger.info(f'👾 Противник {folder_name} найден')
		self.location.click(enemy_location, duration=0.1, is_double=True)

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

	def _fighting_enemy(self):
		logger.info('🔥 Бой стартовал')
		time1 = time.time()

		# инициализация боя
		# бой инициализируется 5.8 в основном
		time.sleep(5)

		# self.orb_farming_strategy_fight()
		self.patron_farming_strategy_fight()
		# self.very_strong_farming_straregy_fight()

		self._close_fight()
		logger.info(f'Бой окончен, время заняло - {time.time() - time1}')

	def get_potion(
		self,
		object_name: str,
		screenshot,
	):
		return self.location.get_object_location(
			screenshot,
			cnst.ObjectTypeEnum.buttons,
			object_name,
			is_repeat=False,
			grayscale=False,
		)

	def very_strong_farming_straregy_fight(self):
		current_round = 0
		screenshot = self.location.get_game_screenshot()

		offence_attack = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'offence'
		)
		fire_spell = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'fire'
		)

		while True:
			logger.info(f'🔵 {current_round} раунд начинается')
			round_screenshot = self.location.get_game_screenshot()

			stamina_potion = self.get_potion('stamina_potion_blue', round_screenshot)
			health_fiol = self.get_potion('health_fiol', round_screenshot)
			health_potion = self.get_potion('health_potion_blue', round_screenshot)

			if current_round in [0]:
				self.location.click(stamina_potion)
				logger.info(f'💊 Выпито зелье лечения {stamina_potion}')

			if current_round in [2, 4]:
				self.location.click(health_fiol)
				logger.info(f'💊 Выпито зелье лечения {health_fiol}')

			if current_round in [8, 10, 12, 14]:
				self.location.click(health_potion)
				logger.info(f'💊 Выпито зелье лечения {health_potion}')

			if current_round in [4, 7, 11, 15]:
				self.location.click(fire_spell)
				logger.info('🔮 Использована магия')
			else:
				self.location.click(offence_attack)
				logger.info('🗡 Использована атака')

			time.sleep(4)

			end_round_screenshot = self.location.get_game_screenshot()
			if not StateService.is_can_hit(
				end_round_screenshot
			) and StateService.is_fight_ended(end_round_screenshot):
				logger.info('🔰 Ура! Победа!')
				break

			current_round += 1

	def patron_farming_strategy_fight(self):
		current_round = 0
		screenshot = self.location.get_game_screenshot()

		offence_attack = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'offence'
		)
		fire_spell = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'fire'
		)
		health_blue_button = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'health_potion_blue'
		)

		while True:
			logger.info(f'🔵 {current_round} раунд начинается')

			if current_round in [4, 9]:
				self.location.click(health_blue_button)
				logger.info(f'💊 Выпито зелье лечения {health_blue_button}')

			if current_round in [4, 7, 11]:
				self.location.click(fire_spell)
				logger.info('🔮 Использована магия')
			else:
				self.location.click(offence_attack)
				logger.info('🗡 Использована атака')

			time.sleep(4)

			end_round_screenshot = self.location.get_game_screenshot()
			if not StateService.is_can_hit(
				end_round_screenshot
			) and StateService.is_fight_ended(end_round_screenshot):
				logger.info('🔰 Ура! Победа!')
				break

			current_round += 1

	def orb_farming_strategy_fight(self):
		current_round = 0

		screenshot = self.location.get_game_screenshot()
		magic_attack = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'magic'
		)
		fire_spell = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'fire'
		)
		health_blue_button = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'health_potion_blue'
		)

		while True:
			logger.info(f'🔵 {current_round} раунд начинается')

			if current_round in [5, 11]:
				self.location.click(health_blue_button)
				logger.info(f'💊 Выпито зелье лечения {health_blue_button}')

			if current_round in [5, 7, 10, 13, 16]:
				self.location.click(fire_spell)
				logger.info('🔮 Использована магия')
			else:
				self.location.click(magic_attack)
				logger.info('🗡 Использована атака')

			time.sleep(4)

			end_round_screenshot = self.location.get_game_screenshot()
			if not StateService.is_can_hit(
				end_round_screenshot
			) and StateService.is_fight_ended(end_round_screenshot):
				logger.info('🔰 Ура! Победа!')
				break

			current_round += 1

	def _close_fight(self):
		screenshot = self.location.get_game_screenshot()
		button = self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'close_fight'
		)
		self.location.click(button)
