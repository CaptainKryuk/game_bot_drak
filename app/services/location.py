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
	@staticmethod
	def get_object_location(
		object_type: cnst.ObjectTypeEnum,
		folder_name: str,
		confidence: float = 0.8,
		is_repeat=True,
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
			return LocationService._get_location(folder_name, files, confidence)
		return LocationService._get_location_or_none(files, confidence)

	@staticmethod
	def _get_location_or_none(files: list[str], confidence: float = 0.8):
		for file in files:
			try:
				location = pyautogui.locateOnScreen(
					file, confidence=confidence, region=region, grayscale=True
				)
				return location
			except pyautogui.ImageNotFoundException:
				return None
		return None

	@staticmethod
	@retry(
		stop=stop_after_attempt(3),
		retry=retry_if_exception_type(pyautogui.ImageNotFoundException),
		wait=wait_fixed(0.5),
		reraise=True,
	)
	def _get_location(folder_name: str, files: list[str], confidence: float = 0.8):
		for file in files:
			try:
				location = pyautogui.locateOnScreen(
					file, confidence=confidence, region=region, grayscale=True
				)
				return location
			except pyautogui.ImageNotFoundException:
				pass

		logger.info(
			f'======== Не Удалось найти объект {folder_name} c первого раза, пробую еще ======='  # noqa E501
		)
		# Сместить фокус
		pyautogui.moveRel(random.randint(-100, 100), random.randint(-100, 100))
		raise pyautogui.ImageNotFoundException

	@staticmethod
	def click(location, duration: float | None = None, is_double: bool = False) -> None:
		"""
		При клике необходимо смещение, чтобы бота не спалили
		"""
		center = pyautogui.center(location)
		pyautogui.moveTo(
			center.x + random.randint(-5, 5),
			center.y + random.randint(-5, 5),
			duration=duration
			if duration is not None
			else random.randrange(100, 300) / 1000,
		)

		if is_double:
			pyautogui.doubleClick(location)
			return

		pyautogui.click()
