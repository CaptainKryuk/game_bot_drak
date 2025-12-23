import logging
import os
import random
from os.path import isfile, join

import pyautogui
from tenacity import (
	retry,
	retry_if_exception_type,
	stop_after_attempt,
	wait_fixed,
)
from utils import constants as cnst

logger = logging.getLogger(__name__)


screen_width, screen_height = pyautogui.size()
region = (screen_width // 2, 0, screen_width // 2, screen_height)


class LocationService:
	def choose_game_window(self, screenshot):
		location = self.get_object_location(
			screenshot, cnst.ObjectTypeEnum.buttons, 'navigation'
		)
		self.click(location)

	def get_game_screenshot(self):
		return pyautogui.screenshot(region=region)

	def get_object_location(
		self,
		screenshot,
		object_type: cnst.ObjectTypeEnum,
		folder_name: str,
		confidence: float = 0.8,
		is_repeat=True,
		grayscale=True,
	):
		"""
		Получить локацию объекта
		"""
		logger.info(
			f'Начинаю поиск объекта на карте {object_type.name} {folder_name}...'
		)

		match object_type:
			case cnst.ObjectTypeEnum.buttons:
				files = [
					os.getcwd() + f'/app/img/{object_type.value}/{folder_name}.png'
				]
			case cnst.ObjectTypeEnum.enemies:
				img_folder = os.getcwd() + f'/app/img/{object_type.value}/{folder_name}'
				files = [
					join(img_folder, x)
					for x in os.listdir(img_folder)
					if isfile(join(img_folder, x))
				]
			case _:
				raise NotImplementedError

		if is_repeat:
			return self._get_location(
				screenshot, folder_name, files, confidence, grayscale
			)
		return self._get_location_or_none(screenshot, files, confidence)

	def _get_location_or_none(
		self, screenshot, files: list[str], confidence: float = 0.8
	):
		for file in files:
			try:
				location = pyautogui.locate(
					file, screenshot, confidence=confidence, grayscale=True
				)
				return self.screenshot_to_global_location(location)
			except pyautogui.ImageNotFoundException:
				return None
		return None

	@retry(
		stop=stop_after_attempt(3),
		retry=retry_if_exception_type(pyautogui.ImageNotFoundException),
		wait=wait_fixed(0.5),
		reraise=True,
	)
	def _get_location(
		self,
		screenshot,
		folder_name: str,
		files: list[str],
		confidence: float = 0.8,
		grayscale=True,
	):
		for file in files:
			try:
				location = pyautogui.locate(
					file, screenshot, confidence=confidence, grayscale=grayscale
				)
				return self.screenshot_to_global_location(location)
			except pyautogui.ImageNotFoundException:
				pass

		logger.info(
			f'======== Не Удалось найти объект {folder_name} c первого раза, пробую еще ======='  # noqa E501
		)

		# safe_mouse_points = [
		# 	(3175, 250),
		# 	# (2076, 247),
		# ]

		# Сместить фокус
		pyautogui.moveTo(3175, 250)
		raise pyautogui.ImageNotFoundException

	def screenshot_to_global_location(self, location) -> tuple:
		return (
			region[0] + location.left,
			region[1] + location.top,
			location.width,
			location.height,
		)

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
