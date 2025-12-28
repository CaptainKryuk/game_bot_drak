# import pyautogui
#
# pos = pyautogui.position()
# print(pos)  # Point(x=123, y=456)
# print(pos.x, pos.y)  # отдельно по координатам


import pyautogui


def get_region_from_mouse():
	print('Наведи мышь на ЛЕВЫЙ ВЕРХНИЙ угол региона и нажми Enter в консоли...')
	input()
	x1, y1 = pyautogui.position()
	print(f'Левый верхний: {x1}, {y1}')

	print('Теперь наведи мышь на ПРАВЫЙ НИЖНИЙ угол региона и снова нажми Enter...')
	input()
	x2, y2 = pyautogui.position()
	print(f'Правый нижний: {x2}, {y2}')

	left = x1
	top = y1
	width = x2 - x1
	height = y2 - y1

	region = (left, top, width, height)
	print('region =', region)
	return region


# Пример использования:
region = get_region_from_mouse()
screenshot = pyautogui.screenshot('region.png', region=region)
