import dataclasses
import logging
import time

from services.location import LocationService
from services.state import StateService
from utils import constants as cnst

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class FightConsumesDTO:
	heals_map: dict[
		str, list[int]
	]  # ключ - название хила, значение - список раундов для использования
	attack_name: str
	spell_name: str
	spell_rounds: list[int]


class StrategyService:
	def __init__(
		self,
		strategy: cnst.FarmingTypeEnum,
		location_service: LocationService,
		state_service: StateService,
	) -> None:
		self.strategy = strategy
		self.location = location_service
		self.state = state_service

	def get_consumes_dto(self) -> FightConsumesDTO:
		match self.strategy:
			case cnst.FarmingTypeEnum.essence:
				return FightConsumesDTO(
					heals_map={'health_blue': [4, 9]},
					attack_name='magic',
					spell_name='fire',
					spell_rounds=[6, 8, 11, 14, 17],
				)
			case cnst.FarmingTypeEnum.patron:
				return FightConsumesDTO(
					heals_map={'health_blue': [6, 12]},
					attack_name='offence',
					spell_name='fire',
					spell_rounds=[5, 8, 12],
				)
			case cnst.FarmingTypeEnum.sunday:
				return FightConsumesDTO(
					heals_map={
						'stamina_potion_blue': [1],
						'health_fiol': [3, 5],
						'health_blue': [9, 11, 13, 15],
					},
					attack_name='offence',
					spell_name='fire',
					spell_rounds=[5, 8, 12, 16],
				)
			case _:
				raise AttributeError('Выбран неправильный тип стратеги')

	def start(self):
		"""
		Основная функция запуска боя
		"""
		consumes_dto: FightConsumesDTO = self.get_consumes_dto()
		self._run_fight(consumes_dto)

	def _run_fight(self, consumes_dto: FightConsumesDTO):
		time1 = time.time()
		# бой инициализируется 5.8 в основном
		logger.info('... Инициализация боя')
		time.sleep(5)

		self._run_rounds_cycle(consumes_dto)

		self._close_fight()
		logger.info(f'Бой окончен, время заняло - {time.time() - time1}')

	def _get_button(self, screenshot, button_name: str):
		return self.location.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, button_name
		)

	def _get_potion(self, screenshot, potion_name: str):
		return self.location.get_object_location(
			screenshot,
			cnst.ObjectTypeEnum.buttons,
			potion_name,
			is_repeat=False,
			grayscale=False,
		)

	def _run_rounds_cycle(self, consumes_dto: FightConsumesDTO):
		logger.info('🔥 Бой стартовал')

		current_round = 1

		fight_screenshot = self.location.get_game_screenshot()

		hand_attack = self._get_button(fight_screenshot, consumes_dto.attack_name)
		magic_attack = self._get_button(fight_screenshot, consumes_dto.spell_name)

		while True:
			logger.info(f'🔵 {current_round} раунд начинается')

			round_screenshot = self.location.get_game_screenshot()

			# Если в текущем раунде необходимо похилиться - ищем
			for heal_name, heal_rounds in consumes_dto.heals_map.items():
				if current_round in heal_rounds:
					heal_location = self._get_potion(round_screenshot, heal_name)
					if heal_location:
						self.location.click(heal_location)
						logger.info(f'💊 Выпито зелье лечения {heal_name}')
					else:
						logger.info('!!!!! зелье выпить надо, а нет')

			# удар магией, если он в этом раунде предусмотрен
			if current_round in consumes_dto.spell_rounds:
				if self.state.is_can_hit_magic(
					round_screenshot, consumes_dto.spell_name
				):
					self.location.click(magic_attack)
					logger.info('🔮 Использована магия')
			else:
				# в ином случае бьем обычной атакой
				if self.state.is_can_hit_offence(
					round_screenshot, consumes_dto.attack_name
				):
					self.location.click(hand_attack)
					logger.info('🗡 Использована атака')
				else:
					raise Exception('а че я ударить не могу бля')

			time.sleep(4)

			end_round_screenshot = self.location.get_game_screenshot()
			if not self.state.is_can_hit(end_round_screenshot):
				if self.state.is_fight_ended(end_round_screenshot):
					logger.info('🔰 Ура! Победа!')
					break
				else:
					raise Exception('я и бить не могу и бой не закончен')

			current_round += 1

	def _close_fight(self):
		screenshot = self.location.get_game_screenshot()
		button = self._get_button(screenshot, 'close_fight')
		self.location.click(button)
