#! /usr/bin/env python
# code from https://github.com/aubio/aubio/tree/master/python/demos
#formatted and changed according to the requirement
# I wrote the analyse function in demo_source_simple.py by myself after understanding it. 
# So I wrote it in a way I understood it and it works. 
import sys
from aubio import*
import math
import numpy

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def analyse(filename):
    filename = str(filename)

    pitches = []
    #in-built aubio class source is used to represent the music file
    sourceObject = source(filename)
    sampleRate = sourceObject.samplerate
    totalFrames = 0
    #depicting the method of input file(an algorithm called yin is called by the aubio class pitch)
    pitchObject = pitch("yin")
    #setting the output unit to be in midi form. It can also be in note form.
    pitchObject.set_unit("midi")
    #tolerance is the minimum value that will be read(measures sound,clarity)
    pitchObject.set_tolerance(0.8)
    #initially setting varibles for first case. samples is a list of floats representing the chunk being read
    samples, read = sourceObject()
    #hop_size is inbuilt variable returned by source class
    while(read >= sourceObject.hop_size):
        samples, read = sourceObject()
        currentPitch = pitchObject(samples)[0]
        currentPitch = int(roundHalfUp(float(currentPitch)))
        confidence = pitchObject.get_confidence()
        if(confidence < 0.9):
            currentPitch = 0
        time = totalFrames/(float(sampleRate))
        if(confidence >= 0.9):
            noteOfPitch = midi2note(currentPitch)
            #print(noteOfPitch, time)
        pitches += [[int(currentPitch),round(time,2)]]
        totalFrames += read
    return pitches

#This function takes in the pitches 2d list returned from analyse() and filters 
#formats the list as required. It also calculates the duration from the 
# timeStamp values. 

def formatMidiListFromPitches(pitches):
    print(pitches)
    rows = len(pitches)
    cols = 2
    newList = [ ([0] * cols) for row in range(rows) ]
    j = 0
    for i in range(len(pitches)):
        iMidi = pitches[i][0]
        iTime = pitches[i][1]
        if(i == 0):
            newList[j][0]=iMidi
            newList[j][1]=iTime
            print(i,j,iMidi,iTime," ---")
            j+=1
        if(iMidi != newList[j-1][0]):
            prevListTime = pitches[i-1][1]
            newList[j-1][1] = round(abs(newList[j-1][1] - prevListTime),2)
            newList[j][0] = iMidi
            newList[j][1] = iTime
            print(i,j,iMidi,iTime)
            j+=1

    i = len(newList)-1     
    while(newList[len(newList)-1][0]==0):
        print(newList[i][0])
        if(newList[i][0]==0):
            print("here")
            newList.pop(i)
            i-=1
        
        print(newList[i], "  ", newList[i][0], "  ", newList[i][1])

    #The next few lines calculate the last existing duration and add it to the list
    lastMidi = pitches[len(pitches)-1][0]
    lastTime = pitches[len(pitches)-1][1]
    lastDuration = 15-pitches[len(pitches)-1][1]
    newList[len(newList)-1][1] = lastDuration    
    print(newList)   
    return newList   
    



