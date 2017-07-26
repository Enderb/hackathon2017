import pygame, sys

import pygame.locals as pgl

import pygame.midi 



yamaha = 3


pygame.init()

#pygame.fastevent.init()

#event_get = pygame.fastevent.get

#event_post = pygame.fastevent.post

event_get = pygame.event.get

event_post = pygame.event.post

pygame.midi.init()

i = pygame.midi.Input(yamaha)

window = pygame.display.set_mode((468, 60))

keys = {}

mt = None

going = True

while going:

    events = i.read(6)

    for e in events:

	#add something to ignore type 248 e[0][0]

	data = e[0]
	timestamp = e[1]

	type = data[0]
	pitch = data[1]
	volume = data[2]

        if type == 144:

            if volume != 0: #keydown

                keys[type] = timestamp

                print "Key %s was pressed." % pitch

                sys.stdout.flush()

            elif volume == 0: #keyup

                print "Key %s was held down for %s." % (pitch, timestamp - keys[type])

                sys.stdout.flush()

  

    

del i

pygame.midi.quit()
