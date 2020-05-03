import os
import sys
import cv2
import numpy as np
import pyautogui as pgui
import time as t
import glob
import threading

class ScreanRecorder:

	frame = 0
	stop_recording = False
	temp_file_name = 'img_'
	def __init__(self,name,path):
		self.name = name
		self.path = path
		self.starting_time = t.time()
		if not os.path.exists(self.path):
			os.mkdir(self.path)

		self.temp_path = path+'/Temp'
		if not os.path.exists(self.temp_path):
			os.mkdir(self.temp_path)

	def record_screen(self):
		print("Recording Started")
		while not self.stop_recording:
			pgui.screenshot(f'{self.temp_path}/{self.frame:07d}.jpg')
			self.frame += 1

	def recording_handler(self):
		key = input("Press [Q] to Stop Recording  ")
		if key == 'q' or key == 'Q':
			self.stop_recording = True
		self.video_maker()

	def video_maker(self):
		avrage_FR = self.frame/ (t.time() - self.starting_time)
		print(f'Avrage Frame Rate : {avrage_FR}')

		self.__print_time(t.time() - self.starting_time)

		temp_image = cv2.imread(f'{self.temp_path}/0000001.jpg')

		file_name = f'{self.path}/{self.name}.avi'
		size = (temp_image.shape[1],temp_image.shape[0])
		print("-------------------",size)
		out = cv2.VideoWriter(file_name,cv2.VideoWriter_fourcc(*'XVID'),int(avrage_FR),size)
		
		print(f'Prepering File [{self.name}.avi]')
		for no in range(0,len(glob.glob(f'{self.temp_path}/*.jpg'))):
			f_name = f'{self.temp_path}/{no:07d}.jpg'
			out.write(cv2.imread(f_name))
		out.release()

#		for file in	glob.glob(f'{self.path}/Temp/*.jpg'):
#			os.remove(file)

		print("Completed...")


	def __print_time(self,t_time):
		t_min = t_time/60
		t_sec = t_time%60
		print(f'{t_min}Min {t_sec}Sec')


if __name__ == "__main__":
	a = ScreanRecorder("Project01", "Recording01")

	thread01 = threading.Thread(target=a.record_screen)
	thread02 = threading.Thread(target=a.recording_handler)

	thread01.start()
	thread02.start()