import pygame.midi
import sys
from midiutil import MIDIFile

def readInput(input_device):
    C = True
	
    keys = {}
    volumes = {}

    track = 0
    channel = 0
    time = 0
    tempo = 120
	
    beatLength = 500 #At 120 BPM, 2 beats play per second, or, 1 beat takes 500 milliseconds 

    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, time, tempo)

    while C:
		
		if input_device.poll():
			#print("polled")
			events = input_device.read(6)

			for event in events:
				if event[0][0] != 248:
					
				    data = event[0]
				    timestamp = event[1]
				    #Notes will have type = 144
				    #Sustain will have type = 176
				    type = data[0]
				    pitch = data[1]
				    volume = data[2]

				    duration = 0

				    #exit if Grand Piano button is pressed
				    if pitch == 72 and type == 176:
					C = False					
					
				    print(event)

				    if volume != 0: #Key Down
					keys[pitch] = timestamp
					volumes[pitch] = volume
					print "Key %s was pressed" % pitch

					sys.stdout.flush()

				    elif volume == 0: #Key Up
					print "Key %s was held down for %s" % (pitch, timestamp - keys[pitch])
					duration = timestamp - keys[pitch]
					
					MyMIDI.addNote(track, channel, pitch, keys[pitch]/beatLength, duration/beatLength, volumes[pitch])
					print "Added note %s duration %s and volume %s" % (pitch, duration/beatLength, volumes[pitch])
					
					sys.stdout.flush()
				
    with open("test.midi", "wb") as output_file:
        MyMIDI.writeFile(output_file)    

    del input_device    


if __name__ == '__main__':
	pygame.midi.init()
	print("starting")
	

	my_input = pygame.midi.Input(3) 
	pygame.midi.get_device_info(3)
	pygame.midi.get_count()
	readInput(my_input)

	print("goodbye")
	pygame.midi.quit()
