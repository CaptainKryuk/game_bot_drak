import os

import requests
from dotenv import load_dotenv


def send_telegram_message(text: str) -> None:
	load_dotenv()  # подгружаем .env (если уже загружен — не страшно)

	token = os.getenv('TELEGRAM_BOT_TOKEN')
	chat_id = 147330382  # твой id

	if not token:
		# на всякий случай, чтобы не silently fail-ить
		print('TELEGRAM_BOT_TOKEN не найден в .env')
		return

	url = f'https://api.telegram.org/bot{token}/sendMessage'

	# телега не любит очень длинные сообщения — обрежем до 4000 символов
	text = text[:4000]

	try:
		requests.post(url, json={'chat_id': chat_id, 'text': text})
	except Exception as send_err:
		# тут уже ничего не поделать, просто логируем в консоль
		print('Ошибка при отправке сообщения в Telegram:', send_err)
