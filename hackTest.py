import pygame.midi
import sys
from midiutil import MIDIFile

def readInput(input_device):
    C = True
	
    keys = {}
    voluems = {}

    track = 0
    channel = 0
    time = 0
    tempo = 120

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
					MyMIDI.addNote(track, channel, pitch, duration, volumes[pitch], "")
					
					
					sys.stdout.flush()
				
    with open("test.midi", "wb") as output_file:

        MyMIDI.writeFile(output_file)    

    
    	

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
