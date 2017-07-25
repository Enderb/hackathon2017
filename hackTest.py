import pygame.midi
from bootstrap import *
from random import randint, shuffle


def readInput(input_device):
	C = True
	while C:
		
		if input_device.poll():
			#print("polled")
			events = input_device.read(6)

			for event in events:
				data = event[0]
				timestamp = event[1]
				#Notes will have type = 144
				#Sustain will have type = 176
				type = data[0]
				note_number = data[1]
				velocity = data[2]

				if type != 248:
					print(event)			

				#exit if Grand Piano button is pressed
				if note_number == 72 and type == 176:
					C = False
				


if __name__ == '__main__':
	pygame.midi.init()
	print("starting")
	

	my_input = pygame.midi.Input(3) 
	pygame.midi.get_device_info(3)
	pygame.midi.get_count()
	readInput(my_input)

	print("goodbye")
	del my_input
	pygame.midi.quit()
