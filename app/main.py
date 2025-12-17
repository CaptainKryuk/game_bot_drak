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

logger = logging.getLogger()


pyautogui.FAILSAFE = True  # угол (0,0) аварийно останавливает скрипт
pyautogui.PAUSE = 0.4  # пауза после каждой команды

screen_width, screen_height = pyautogui.size()
region = (screen_width // 2, 0, screen_width // 2, screen_height)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


@retry(
	stop=stop_after_attempt(40),
	retry=retry_if_result(lambda r: r is None),
	wait=wait_random(min=3, max=6),
	reraise=True,
)
def start_fighting():
	# KillService().kill_enemy('tenestrazh_15')
	KillService().kill_enemy('marks')

	return


def main():
	logger.info('🌑 Запуск бота...')

	if not StateService.is_on_map():
		logger.error('Необходимо находиться на карте во время запуска скрипта')

	# Выбрать окно
	location = LocationService.get_object_location(
		cnst.ObjectTypeEnum.buttons, 'navigation'
	)
	LocationService.click(location)

	start_fighting()


if __name__ == '__main__':
	main()
