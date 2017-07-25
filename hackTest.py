import pygame.midi
from bootstrap import *
from random import randint, shuffle

pixels = []

def arduino_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def number_to_note(number):
	notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
	return notes[number%12]

def number_to_pixel(number):
	#pixels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
	return pixels[87 - number%88]

def number_to_color(number, velocity):
	colors = [
		(149,100,121),
		(34,143,152),
		(205,247,229),
		(223,165,61),
		(188,183,36),
		(198,202,254),
		(143,82,237),
		(228,20,114),
		(64,242,185),
		(206,39,128),
		(94,124,242),
		(17,195,228)
		]
	r, g, b = colors[number%12]
	value = arduino_map(velocity, 0, 127, 0.5, 1.0)
	
	return Color(r,g,b,value)
	
def fill_borders():
	#This will fill the borders of a 32X5 strip
	DeepSkyBlue = Color(0,191,255)
	
	led.setMasterBrightness(0.15)

	led.fill(DeepSkyBlue, 0, 32)
	led.fill(DeepSkyBlue, 63, 64)
	led.fill(DeepSkyBlue, 95, 96)
	led.fill(DeepSkyBlue, 127, 159)

	led.setMasterBrightness(1.0)


def clear_borders():
	led.fillOff(0, 32)
	led.fillOff(63, 64)
	led.fillOff(95, 96)
	led.fillOff(127, 159)

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

				#Notes go from 21 (A1) to 108 (C7)
				#Sustain pedal is 64, same as E3
				#if type != 248 and note_number != 0:
					#print(type, note_number, velocity)
				if note_number != 0 and type == 144:
					#print(type, note_number, number_to_note(note_number), velocity)
					pix = number_to_pixel(note_number)
					col = number_to_color(note_number, velocity)
					
					if velocity != 0:
						led.set(pix, col)
					else:
						led.setOff(pix)
				
				if note_number == 64 and type == 176:
					print("Borders")
					if velocity != 0:
						fill_borders()
					else:
						clear_borders()

				#exit if Grand Piano button is pressed
				if note_number == 72 and type == 176:
					C = False
				
			led.update()


if __name__ == '__main__':
	pygame.midi.init()
	print("starting")
	
	pixels.extend(range(33,63))
	pixels.extend(range(65,79))
	pixels.extend(range(81,95))
	pixels.extend(range(97,127))
	random.shuffle(pixels)

	my_input = pygame.midi.Input(3) 
	pygame.midi.get_device_info(3)
	pygame.midi.get_count()
	readInput(my_input)

	print("goodbye")
	del my_input
	pygame.midi.quit()
