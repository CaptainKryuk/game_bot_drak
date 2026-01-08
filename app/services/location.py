import logging
import os
import random
import time
from os.path import isfile, join

import pyautogui
from utils import constants as cnst

logger = logging.getLogger(__name__)


class LocationService:
	def choose_game_window(self, screenshot):
		location = self.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'navigation'
		)
		self.click(location)

	def get_game_screenshot(self, region: tuple | None = None):
		screen_region = region or cnst.base_region
		return pyautogui.screenshot(region=screen_region)

	def get_object_location(
		self,
		screenshot,
		object_type: cnst.ObjectTypeEnum,
		folder_name: str,
		confidence: float = 0.8,
		is_repeat=True,
		grayscale=True,
		region: tuple | None = None,
	):
		"""
		Получить локацию объекта
		"""
		logger.info(
			f'Начинаю поиск объекта на карте {object_type.name} {folder_name}...'
		)

		files: list[str] = self.get_searching_files(object_type, folder_name)

		if is_repeat:
			for attempt in range(3):
				if attempt > 0:
					screenshot = self.get_game_screenshot(region)

				try:
					location = self._get_location(
						screenshot, files, confidence, grayscale, region=region
					)
					return location
				except pyautogui.ImageNotFoundException:
					logger.info(
						f'======== Не Удалось найти объект {folder_name} c первого раза, пробую еще ======='  # noqa E501
					)
					# Сместить фокус
					pyautogui.moveTo(3175, 250)
					time.sleep(0.3)

			raise pyautogui.ImageNotFoundException

		return self._get_location(
			screenshot,
			files,
			confidence,
			grayscale=grayscale,
			is_raise_error=False,
			region=region,
		)

	def get_searching_files(self, object_type, folder_name) -> list[str]:
		match object_type:
			case cnst.ObjectTypeEnum.buttons:
				return [os.getcwd() + f'/app/img/{object_type.value}/{folder_name}.png']
			case cnst.ObjectTypeEnum.enemies:
				img_folder = os.getcwd() + f'/app/img/{object_type.value}/{folder_name}'
				return [
					join(img_folder, x)
					for x in os.listdir(img_folder)
					if isfile(join(img_folder, x))
				]
			case _:
				raise NotImplementedError

	def _get_location(
		self,
		screenshot,
		files: list[str],
		confidence: float = 0.8,
		grayscale=True,
		is_raise_error=True,
		region: tuple | None = None,
	):
		for file in files:
			try:
				location = pyautogui.locate(
					file, screenshot, confidence=confidence, grayscale=grayscale
				)
				return self.screenshot_to_global_location(location, region)
			except pyautogui.ImageNotFoundException:
				pass

		if is_raise_error:
			raise pyautogui.ImageNotFoundException
		return None

	def screenshot_to_global_location(
		self, location, region: tuple | None = None
	) -> tuple:
		screen_region = region or cnst.base_region
		return (
			screen_region[0] + location.left,
			screen_region[1] + location.top,
			location.width,
			location.height,
		)

	def move_mouse_after_attack(self):
		"""
		После атаки необходимо подвинуть мышку выше, чтобы не перекрывала кнопки
		"""
		pyautogui.moveRel(0, 30, duration=0.1)

	def click(
		self, location, duration: float | None = None, is_double: bool = False
	) -> None:
		"""
		При клике необходимо смещение, чтобы бота не спалили
		"""
		center = pyautogui.center(location)
		pyautogui.moveTo(
			center.x + random.randint(-5, 5),
			center.y + random.randint(-5, 5),
			duration=duration
			if duration is not None
			else random.randrange(100, 150) / 1000,
		)

		if is_double:
			pyautogui.doubleClick(location)
			return

		pyautogui.click()
