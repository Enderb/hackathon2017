from azure.storage.blob import BlockBlobService
import pygame.midi
import sys
from midiutil import MIDIFile
import time
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning, urllib3.exceptions.InsecurePlatformWarning) 

timeOffset = 0

def readInput(input_device):
    C = True

    global timeOffset
	
    keys = {}
    volumes = {}

    track = 0
    channel = 0
    tim = 0
    tempo = 120
	
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fileName = timestr + ".mid"
	
    str = '{initiator":[{"name":"'
    str += timestr
    str += '","seq":['

    tempOffset = 0
	
    beatLength = 500 * 1.0 #At 120 BPM, 2 beats play per second, or, 1 beat takes 500 milliseconds 

    MyMIDI = MIDIFile(1, adjust_origin="True")
    MyMIDI.addTempo(track, tim, tempo)

    while C:
		
		if input_device.poll():
			#print("polled")
			events = input_device.read(6)

			for event in events:
				if event[0][0] != 248:
					
				    data = event[0]
				    timestamp = event[1] - timeOffset
				    tempOffset = timestamp
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
					
					str += '{"notes":['
					str += `pitch`
					str += ']},'
					
					sys.stdout.flush()

				    elif volume == 0: #Key Up
					duration = timestamp - keys[pitch]
					
					timeInBeats = keys[pitch]/beatLength
					durationInBeats = duration/beatLength

					MyMIDI.addNote(track, channel, pitch, timeInBeats, durationInBeats, volumes[pitch])
					print "Added note %s duration %.3f and volume %s at time %.3f" % (pitch, durationInBeats, volumes[pitch], timeInBeats)
					
					sys.stdout.flush()
    str = str[:-1]
    str += ']}]}'

    jsonFile = 'initiator.json'
    with open(jsonFile, 'w') as outfile:
        outfile.write(str)

    timeOffset = tempOffset
					
    with open(fileName, "wb") as output_file:
        MyMIDI.writeFile(output_file)
	
    block_blob_service = BlockBlobService(account_name='mlpiano', account_key='AWsiStetr34ycMVEFkOznT3iORrmYA5P4cod5RkPMgh7VwW+GGktohnuwXqj/xccnSp71mWg4FViyGnB9/AUUg==')    	
    block_blob_service.create_blob_from_path('midiuploadrpi', fileName, fileName) 
    block_blob_service.create_blob_from_path('jsonuploadrpi', jsonFile, jsonFile)

    del keys
    del volumes
    del MyMIDI

    readInput(input_device)


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
