

from aubio import*
import copy
import string



#TEST INPUT: noteDictFuncForSine({329.6: 1, 293.6: 0.5, 261.6: 1, 293.6: 0.5,293.6: 0.5 })
#TEST INPUT: noteDictFuncForSine([[64, 0.49], [62, 0.28], [60, 0.49], [62, 0.42], [64, 0.52], [62, 0.5], [60, 0.37]])
def noteDictFuncForSine(newList):
    i = 0
    for innerL in newList:
        if(newList[i] != []):
            print(innerL," ----")
            print(innerL[0], "-", midi2note(innerL[0]))
            play(miditofreq(innerL[0]),innerL[1])
        i+=1
# function that gets the notes played by us in both midi and symbol form
def getNoteAndMidi(newList):
    midiList = []
    noteList = []
    empty = []
    i = 0
    for innerL in newList:
        note = midi2note(innerL[0])
        if(innerL[1] > 0.1):
            midiList.append(innerL[0])
            if(note[-1].isdigit()):
                note = note[:-1]
            noteList.append(note)
        else:
            newList[i] = copy.deepcopy(empty)
            print("here")
            print(newList[i])
        i+=1
    print(midiList)
    print(noteList)
    print(newList)
    newList = filterNewList(newList)
    return midiList,noteList,newList

def filterNewList(newList):
    i = 0
    filteredList = []
    while(i<len(newList)):
        if(newList[i]!=[]):
            filteredList.append(newList[i])
        i+=1
    filteredList[len(filteredList)-1][1] = 0.5
    return filteredList
                
        
#TEST INPUT[[65, 1.6], [64, 1.77], [65, 0.71], [62, 1.7], [64, 0.37], [65, 0.17], [62, 0.15], [60, 0.59], [65, 0.28], [64, 0.97], [65, 0.43], [62, 0.04], [72, 0.3], [70, 0.97], [69, 0.11]]

def formatNoteList(noteList):
    newNoteList = []
    for note in noteList:
        if(note != "C-"):
            if(note not in newNoteList):
                newNoteList.append(note)
    return newNoteList

def findKey(midiList,noteList):
    key = ''
    keyScale = []
    formattedNoteList = formatNoteList(noteList)
    listOfScales = [["C","D","E","F","G","A","B"],
            ["G","A","B","C","D","E","F#"],
            ["D","E","F#","G","A","B","C#"],
            ["A","B","C#","D","E","F#","G#"],
            ["E","F#","G#","A","B","C#","D#"],
            ["B","C#","D#","E","F#","G#","A#"],
            ["F","G","A","A#","C","D","E"],
            ["A#","C","D","D#","F","G","A"],
            ["D#","F","G","G#","A#","C","D"],
            ["G#","A#","C","C#","D#","F","G"],
            ["C#","D#","F","F#","G#","A#","C"],
            ["F#","G#","A#","B","C#","D#","F"]]
    print(formattedNoteList)
    for scale in listOfScales:
        noteCount = 0
        for note in scale:
            if(note in formattedNoteList):
                print(note,noteCount)
                noteCount +=1
        if(noteCount == len(formattedNoteList)):
            print("here break",noteCount)
            key = scale[0]
            keyScale = copy.copy(scale)
            break
        if(scale[0]=="F#"):
            key = scale[0]
            keyScale = copy.copy(scale)
    return key, keyScale

 
def getHarmonyLine(midiList,keyScale,songList):
    harmonyMidiList = []
    harmonyNoteList = []
    harmonySongList = []
    i = 0
    for midi in midiList:
        if(midi != 0):
            midi2 = midi+4
            if(str(midi2note(midi2))[:-1] not in keyScale):
                if(str(midi2note(midi2-1))[:-1] in keyScale):
                    midi2 = midi2-1
                else:
                    midi2 = midi2+1
        else:
            midi2 = 0
        harmonyMidiList.append(midi2)
        harmonyNoteList.append(midi2note(midi2))
        harmonySongList.append([midi2,songList[i][1]])
        i+=1
    print(songList)
    print("-->",harmonySongList)
    return harmonyMidiList, harmonyNoteList,harmonySongList

        


#TEST midiList,noteList = getNoteAndMidi([[65, 1.6], [64, 1.77], [65, 0.71], [62, 1.7], [64, 0.37], [65, 0.17], [62, 0.15], [60, 0.59], [65, 0.28], [64, 0.97], [65, 0.43], [62, 0.04], [72, 0.3], [70, 0.97], [69, 0.11]])

