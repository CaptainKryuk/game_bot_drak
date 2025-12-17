import logging
import random
import time

from services.location import LocationService
from services.state import StateService
from utils import constants as cnst

logger = logging.getLogger(__name__)


class KillService:
	location = LocationService
	state = StateService

	def kill_enemy(self, folder_name: str):
		self._find_and_click_enemy(folder_name)
		self._start_fight()
		self._fighting_enemy()

	def _find_and_click_enemy(self, folder_name: str):
		logger.info('🔍 Ищем противника или его марку задания')
		enemy_location = self.location.get_object_location(
			cnst.ObjectTypeEnum.enemies, folder_name
		)

		logger.info(f'👾 Противник {folder_name} найден')
		self.location.click(enemy_location, duration=0.1, is_double=True)

	def _start_fight(self):
		if self.state.is_in_fight():
			return

		if self.state.is_enemy_marked():
			logger.info('🏳 Появилась метка на противнике, необходимо нажать "Напасть"')
			button = self.location.get_object_location(
				cnst.ObjectTypeEnum.buttons, 'attack'
			)
			self.location.click(button)
			return

	def _fighting_enemy(self):
		logger.info('🔥 Бой стартовал')
		time1 = time.time()

		# инициализация боя
		# бой инициализируется 5.8 в основном
		time.sleep(5)

		self.orb_farming_strategy_fight()
		# self.patron_farming_strategy_fight()
		# self.very_strong_farming_straregy_fight()

		self._close_fight()
		logger.info(f'Бой окончен, время заняло - {time.time() - time1}')

	def get_potion(self, object_name: str):
		return self.location.get_object_location(
			cnst.ObjectTypeEnum.buttons, object_name, is_repeat=False
		)

	def very_strong_farming_straregy_fight(self):
		current_round = 0
		offence_attack = self.location.get_object_location(
			cnst.ObjectTypeEnum.buttons, 'offence'
		)
		fire_spell = self.location.get_object_location(
			cnst.ObjectTypeEnum.buttons, 'fire'
		)

		while True:
			health_blue = self.get_potion('health_blue')
			health_fiol = self.get_potion('health_fiol')
			stamina_potion = self.get_potion('stamina_potion')
			health_potion = self.get_potion('health_potion')

			if current_round in [0]:
				self.location.click(stamina_potion)

			if current_round in [2]:
				self.location.click(health_blue)

			if current_round in [4, 6, 8]:
				self.location.click(health_fiol)

			if current_round in [10, 12]:
				self.location.click(health_potion)

			if current_round in [4, 7, 11, 15]:
				self.location.click(fire_spell)
			else:
				self.location.click(offence_attack)

			current_round += 1
			time.sleep(random.randint(3, 5))

			if StateService.is_can_hit():
				continue

			if StateService.is_fight_ended():
				break

	def patron_farming_strategy_fight(self):
		current_round = 0
		offence_attack = self.location.get_object_location(
			cnst.ObjectTypeEnum.buttons, 'offence'
		)
		fire_spell = self.location.get_object_location(
			cnst.ObjectTypeEnum.buttons, 'fire'
		)
		health_blue_button = self.location.get_object_location(
			cnst.ObjectTypeEnum.buttons, 'health_blue'
		)

		while True:
			logger.info(f'🔵 {current_round} раунд начинается')

			if current_round in [2]:
				self.location.click(health_blue_button)
				logger.info(f'💊 Выпито зелье лечения {health_blue_button}')

			if current_round in [4, 7, 11]:
				self.location.click(fire_spell)
				logger.info('🔮 Использована магия')
			else:
				self.location.click(offence_attack)
				logger.info('🗡 Использована атака')

			current_round += 1

			time.sleep(4)

			if StateService.is_can_hit():
				continue

			if StateService.is_fight_ended():
				logger.info('🔰 Ура! Победа!')
				break

	def orb_farming_strategy_fight(self):
		current_round = 0

		magic_attack = self.location.get_object_location(
			cnst.ObjectTypeEnum.buttons, 'magic'
		)
		fire_spell = self.location.get_object_location(
			cnst.ObjectTypeEnum.buttons, 'fire'
		)
		health_blue_button = self.location.get_object_location(
			cnst.ObjectTypeEnum.buttons, 'health_blue'
		)

		while True:
			logger.info(f'🔵 {current_round} раунд начинается')

			if current_round in [3, 6]:
				self.location.click(health_blue_button)
				logger.info(f'💊 Выпито зелье лечения {health_blue_button}')

			if current_round in [5, 7, 10, 13, 16]:
				self.location.click(fire_spell)
				logger.info('🔮 Использована магия')
			else:
				self.location.click(magic_attack)
				logger.info('🗡 Использована атака')

			current_round += 1

			time.sleep(4)

			if StateService.is_can_hit():
				continue

			if StateService.is_fight_ended():
				logger.info('🔰 Ура! Победа!')
				break

	def _close_fight(self):
		button = self.location.get_object_location(
			cnst.ObjectTypeEnum.buttons, 'close_fight'
		)
		self.location.click(button)
