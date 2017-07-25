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

    events = event_get()

    for e in events:

        if e.type in [pgl.QUIT, pgl.KEYDOWN]:

            going = False

            continue

        if e.type == pygame.midi.MIDIIN:

            if e.status == 144: #keydown

                keys[e.data1] = e.timestamp

                print "Key %s was pressed." % e.data1

                sys.stdout.flush()

            elif e.status == 128: #keyup

                print "Key %s was held down for %s." % (e.data1, e.timestamp - keys[e.data1])

                sys.stdout.flush()

             

            #print (e), ', miditime: ', mt

   

    

    if i.poll():

        midi_events = i.read(10)

        # convert them into pygame events.

        midi_evs = pygame.midi.midis2events(midi_events, i.device_id)



        for m_e in midi_evs:

            print m_e

            sys.stdout.flush()

            event_post( m_e )

    

del i

pygame.midi.quit()
