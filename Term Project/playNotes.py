#used the code from http://cs.indstate.edu/~jkinne/cs151-f2012/code/midiExample.py
#to understand the use and implementation of the pygame functions

#In playNotes functions, there wasn’t really much I could do. There is no other way I could have played notes using 
#pygame since they are just calling functions from the module. But I wrote the function and  structured the 
#code by myself the first time around. The for loop calls the function multiple times according to my input
#(the midiList made from my other functions) Other than that there are only function calls for initialising and deleting. 
#I tried to exclude the del. But I got a pointer exception. I couldn’t find another way to delete
#midiOutput because it was an object. 

import pygame 
import pygame.midi
from time import sleep

#this function plays the entered list(midi values and time) as a stream of individual notes
def playNotes(midiAndTimeList):
    piano = 0
    pygame.init()
    pygame.midi.init()
    #next three lines check if the output device of the computer is valid or not
    port = pygame.midi.get_default_output_id()
    print("using output_id %s" % port)
    midiOutput = pygame.midi.Output(port, 0)
    midiOutput.set_instrument(0,0)
    for i in range(len(midiAndTimeList)):
        if(midiAndTimeList[i]!=[]):
            print(midiAndTimeList[i])
            #127 is the volume
            midiOutput.note_on(midiAndTimeList[i][0],127)
            sleep(midiAndTimeList[i][1])
            midiOutput.note_off(midiAndTimeList[i][0],127)
            sleep(0.1)
    # deleting the object to avoid exception
    del midiOutput
    pygame.midi.quit()
#this function plays the melody and harmony lines as chords
def playMelAndHarLine(songList,harmonySongList):
    piano = 0
    pygame.init()
    pygame.midi.init()
    port = pygame.midi.get_default_output_id()
    print ("using output_id :%s:" % port)
    midiOutput = pygame.midi.Output(port, 0)
    midiOutput.set_instrument(0,0)
    for i in range(len(songList)):
        if(songList[i]!=[]):
            #print(midiAndTimeList[i])
            midiOutput.note_on(songList[i][0],127)
            midiOutput.note_on(harmonySongList[i][0],127)
            sleep(songList[i][1])
            midiOutput.note_off(songList[i][0],127)
            midiOutput.note_off(harmonySongList[i][0],127)
            sleep(0.1)
    #deleting the object to avoid exception
    del midiOutput
    pygame.midi.quit()

#this function plays individual notes on command
def playPianoNote(midiToPlay):
    piano = 0
    pygame.init()
    pygame.midi.init()
    port = pygame.midi.get_default_output_id()
    print ("using output_id :%s:" % port)
    midiOutput  = pygame.midi.Output(port, 0)
    midiOutput.set_instrument(0,0)
    midiOutput.note_on(midiToPlay,127)
    sleep(0.1)
    midiOutput.note_off(midiToPlay,127)
    #deleting the object to avoid exception
    del midiOutput
    pygame.midi.quit()



