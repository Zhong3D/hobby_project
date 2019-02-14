# Instructions:
# 1. Depending on your screen resolution, size & color setup, you may need to adjust the parameter below.
# 2. Find the game at: http://www.crazygames.com/game/stickman-archer-2, or advert-free version at: http://cdn.kiz10.com/upload/games/htmlgames/stickman-archer-2-2017/1502991759/index.html
# 3. Run this program.
# 4. Full screen the internet browser to start the game.
# 5. Press 's' to start or stop the auto launching of arrows. Press 'e' to exit the program.

import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import random
from PIL import ImageGrab
import numpy as np
import os
from datetime import datetime

# Set up parameters for mouse & keyboard control. Remember your exit_key!
delay = 0.05
button = Button.left
start_stop_key = KeyCode(char='s')
exit_key = KeyCode(char='e')

# *** The resolution of my screen and actual screen pixel counts differ. Since PIL ImageGrab & pynput.mouse operate on separate systems, use these liaison parameters.
px_x = 2559
px_y = 1599
rs_x = 1279
rs_y = 799

# *** Define game screen coordinates.
limit_x_left = 360
limit_x_right = 1100
limit_y_up = 92
limit_y_down = 645

game_coords = [int(limit_x_left * px_x / rs_x), int(limit_y_up * px_y / rs_y), int(limit_x_right * px_x / rs_x), int(limit_y_down * px_y / rs_y)]

# Define some areas not to click on (home button, advertisement button)
home_button_x = 1000
home_button_y = 160

advert_x = 800
advert_y = 650

# Define evert n-th row & columns to inspect captured images. Higher numbers lead to higher image processing speeds.
row_spacing = 20 # best kept below 20, due to the size of the green enemy platform we are searching for.
col_spacing = 40 # best kept below 40, due to the size of the green enemy platform we are searching for.

# Define parameters to customize your aim.
mouse_init_up = 170 # Range of spread of arrows. In screen resolution unit.
arrows_per_barrage = 6 # How many arrows per barrage.
y_offset = 50 # How much higher the arrows are generally above the enemy platform.

# Define color parameters to find enemy platform.
green_threshold = 192
red_threshold = 31


class ClickMouse(threading.Thread):
	def __init__(self, delay, button):
		super(ClickMouse, self).__init__()
		self.delay = delay
		self.button = button
		self.running = False
		self.program_running = True

	def start_clicking(self):
		os.system('afplay /System/Library/Sounds/Glass.aiff')
		self.running = True

	def stop_clicking(self):
		os.system('afplay /System/Library/Sounds/Blow.aiff')
		self.running = False

	def exit(self):
		os.system('afplay /System/Library/Sounds/Frog.aiff')
		self.stop_clicking()
		self.program_running = False
	
	def is_green(self, pixel):
		if pixel[0] == red_threshold and pixel[1] == green_threshold:
			return True

	def find_pixel(self, img_array):
		for row_num, pixel_row in enumerate(img_array):
			for col_num, pixel in enumerate(pixel_row):
				if self.is_green(pixel=pixel):
					return row_num, col_num

	def run(self):
		while self.program_running:
			time.sleep(self.delay)
			while self.running:
				print('start screenshot at: ', datetime.now())
				img = ImageGrab.grab(bbox=game_coords)
				img_array = np.array(img)[::row_spacing,::col_spacing, 0:2] # For efficiency, only the red & green channels are needed.
				if self.find_pixel(img_array) is not None:
					y, x = self.find_pixel(img_array)
				else:
					print('found no green pixel.')
					break
				print('Found green pixel at: ', x, y)
				print('Time: ', datetime.now())

				if x is not None:
					mouse.position = (x * col_spacing / px_x * rs_x + limit_x_left, y * row_spacing / px_y * rs_y + limit_y_up)
					print('mouse position: ', mouse.position)
					print('Time: ', datetime.now())
					time.sleep(self.delay)
					mouse.move(0, - mouse_init_up - y_offset)
					time.sleep(self.delay)
					for i in range(arrows_per_barrage):
						mouse.move(0, mouse_init_up / arrows_per_barrage)
						if (mouse.position[0] > home_button_x and mouse.position[1] < home_button_y) or (mouse.position[0] < advert_x and mouse.position[1] > advert_y):
							pass
						else:
							time.sleep(self.delay)
							mouse.press(self.button)
							time.sleep(self.delay)
							mouse.release(self.button)
							time.sleep(self.delay)
				time.sleep(0.1)

mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()

def on_press(key):
	if key == start_stop_key:
		if click_thread.running:
			click_thread.stop_clicking()
		else:
			click_thread.start_clicking()
	elif key == exit_key:
		click_thread.exit()
		listener.stop()

with Listener(on_press=on_press) as listener:
	listener.join()