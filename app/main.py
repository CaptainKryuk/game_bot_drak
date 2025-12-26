import logging

import pyautogui
from services.kill import KillService
from services.location import LocationService
from services.state import StateService
from tenacity import (
	retry,
	retry_if_result,
	stop_after_attempt,
	wait_random,
)
from utils import constants as cnst
from utils.telegram import send_telegram_message

logger = logging.getLogger()


pyautogui.FAILSAFE = True  # угол (0,0) аварийно останавливает скрипт
pyautogui.PAUSE = 0.05  # пауза после каждой команды

screen_width, screen_height = pyautogui.size()
region = (screen_width // 2, 0, screen_width // 2, screen_height)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


@retry(
	stop=stop_after_attempt(60),
	retry=retry_if_result(lambda r: r is None),
	wait=wait_random(min=1, max=2),
	reraise=True,
)
def start_fighting(strategy: cnst.FarmingTypeEnum):
	service = KillService(LocationService(), StateService())

	try:
		service.kill_enemy(strategy)
	except Exception:
		error_text = '❌ Начальнииик, я пизды получил'
		send_telegram_message(error_text)
		raise

	return


def setup_app_args() -> cnst.FarmingTypeEnum:
	print("""
Выберите стратегию для фарма:
(1) - Фарм эссенций
(2) - Фарм репы заступника
(3) - Фарм Воскресных мобов
	""")
	result = int(input())
	match result:
		case 1:
			return cnst.FarmingTypeEnum.essence
		case 2:
			return cnst.FarmingTypeEnum.patron
		case 3:
			return cnst.FarmingTypeEnum.sunday
		case _:
			raise AttributeError('Выбран неправильный аргумент')


def main():
	strategy: cnst.FarmingTypeEnum = setup_app_args()

	logger.info('🌑 Запуск бота...')
	location_service = LocationService()
	screenshot = location_service.get_game_screenshot()

	if not StateService.is_on_map(screenshot):
		logger.error('Необходимо находиться на карте во время запуска скрипта')

	# Выбрать окно
	location_service.choose_game_window(screenshot)
	start_fighting(strategy)


if __name__ == '__main__':
	main()
