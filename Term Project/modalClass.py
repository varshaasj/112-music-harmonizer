#format of modes learnt from 112 animations 2 page
#images from google imageshttps://www.google.com/search?safe=active&tbm=isch&sxsrf=ALeKk02xd6YnoEhg6KXYhRtJiUKUdVZvxA%3A1587686014108&source=hp&biw=545&bih=758&ei=fiqiXozVBL-W4-EP45u3mAM&q=musical+notes&oq=musical+notes&gs_lcp=CgNpbWcQAzIECCMQJzICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADoHCCMQ6gIQJ1C1E1i9JmDOJ2gDcAB4AIABlAGIAfoHkgEEMTEuMpgBAKABAaoBC2d3cy13aXotaW1nsAEK&sclient=img&ved=0ahUKEwiMjImn3__oAhU_yzgGHePNDTMQ4dUDCAY&uact=5

from cmu_112_graphics import *
import recordAndVisualize
import pyAudio_demo2_playwavfile
import demo_source_simple
import notes_functions
import playNotes
import aubio
import time
import pygame 
import pygame.midi
from time import sleep

class HomeAndRecordMode(Mode):
    def appStarted(mode):
        #recordtrans.png from https://www.google.com/search?q=record+button&safe=active&client=safari&rls=en&sxsrf=ALeKk01FwZ7HTuMX3fpUEUa7CpAQWaHJ7Q:1588141271849&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi29PGi_4zpAhVfzjgGHcfEDlAQ_AUoAXoECA8QAw&biw=972&bih=768
        mode.recordImg = mode.loadImage('recordtrans.png')
        mode.scaleRecordImg = mode.scaleImage(mode.recordImg,1/6)
        #playtrans.png from https://www.google.com/search?q=play+button&safe=active&client=safari&rls=en&sxsrf=ALeKk00HVX2XiI8ExV5YjK-_Ts6MH9VKrg:1588141339123&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjEifzC_4zpAhVrxDgGHXJGD68Q_AUoAXoECA8QAw&biw=972&bih=768&dpr=2
        mode.playImg = mode.loadImage('playtrans.png')
        mode.scalePlayImg = mode.scaleImage(mode.playImg,1/3)
        #home.png from https://www.google.com/search?q=black+music+background+minimalistic&safe=active&client=safari&rls=en&sxsrf=ALeKk01iVc1D0UxEBCCy-yWnw58QewDLug:1587405834253&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi_wvXGy_foAhWUwTgGHfwsBRIQ_AUoAXoECAwQAw&biw=875&bih=699#imgrc=kEJBy4qbfqEksM
        mode.homeImg = mode.loadImage('home.png')
        #record button img modified using https://onlinepngtools.com/change-png-color
        mode.darkRecord = mode.loadImage('darkRecord.png')
        mode.scaleDarkRecord = mode.scaleImage(mode.darkRecord,1/6)
        mode.app.filename = ""
        mode.rIsPressed = False
        mode.isErrorDisplayed = False
        mode.recordX = mode.width//7
        mode.recordY = mode.height*0.7
        mode.playX = mode.width//3
        mode.playY = mode.height*0.7
        mode.analyseX0 = mode.width*0.85
        #0.82 is from (mode.width*0.85)+ buttonWidth
        mode.analyseX1 = mode.width*0.98
        mode.analyseY0 = mode.height*0.9
        #0.88 is from (mode.width*0.9)+ buttonheight
        mode.analyseY1 = mode.height*(0.98)
        mode.visualizeCX = mode.width*0.53
        mode.visualizeCY = mode.height*0.7
        mode.app.makeButtonDark = None
        mode.app.buttonDarkStartTime = 0
        mode.seconds = 0
        mode.secs = 0

    
    #handles the three buttons: record, play and analyse
    def mousePressed(mode,event):
        if(((event.x >= (mode.recordX-25)) and (event.x <= mode.recordX+25)) and
            (event.y >= (mode.recordY-25)) and (event.y <= mode.recordY+25)):
            mode.rIsPressed = True
            mode.app.makeButtonDark = True
            mode.app.buttonDarkStartTime = time.time()
            mode.seconds = mode.getUserInput('Enter the number of seconds')
            print("start time" , mode.app.buttonDarkStartTime)
            if(mode.seconds!=None):
                if(mode.seconds!=0):
                    mode.app.filename = recordAndVisualize.recordVoice(mode.seconds)
        elif(((event.x >= (mode.playX-20))and(event.x <= mode.playX+20))and
            (event.y >= (mode.playY-20))and(event.y <= mode.playY+20)):
            if(mode.rIsPressed):
                pyAudio_demo2_playwavfile.playFile(mode.app.filename)
            else:
                mode.isErrorDisplayed = True
        elif(((event.x >= mode.analyseX0)and(event.x <= mode.analyseX1))and
            ((event.y >=mode.analyseY0)and(event.y <= mode.analyseY1))):
            if(mode.rIsPressed==True):
                mode.app.setActiveMode(mode.app.keyAndScale)
        elif((event.x >= mode.visualizeCX-30 and event.x <= mode.visualizeCX+30) and
            (event.y >= mode.visualizeCY-30 and event.y <= mode.visualizeCY+30)):
            mode.secs = mode.getUserInput('Enter the number of seconds')
            if(mode.secs != None):
                if(mode.secs != 0):
                    recordAndVisualize.liveVisualizer(mode.secs)

    def timerFired(mode):
        if(mode.app.makeButtonDark==True):
            elapsedTime = time.time() - mode.app.buttonDarkStartTime
            print(elapsedTime)
            if(mode.seconds!=None and mode.seconds!=0):
                if(elapsedTime > float(mode.seconds)):
                    mode.app.makeButtonDark = False

    def displayError(mode,canvas):
        h = mode.height
        canvas.create_text(200,h//8,text="Sorry! File not present",
                                    fill="grey",anchor="w",font="Noteworthy 40")

    def displayName(mode,canvas):
        h = mode.height
        canvas.create_text(200,h//8,text=mode.app.filename,fill="grey",anchor="w",
                            font="Arial 48")
    
    def drawButton(mode,canvas,x1,y1,x2,y2,command):
        textX = (x1+x2)//2
        textY = (y1+y2)//2
        canvas.create_rectangle(x1,y1,x2,y2,fill = "grey")
        canvas.create_text(textX,textY,text = str(command), font = "Noteworthy 14", fill = "white")
    
    def redrawAll(mode, canvas):
        w = mode.width
        h = mode.height
        canvas.create_image(w//2, h//2, image=ImageTk.PhotoImage(mode.homeImg))

        canvas.create_text(50,h//7,text="HARMONIZER",fill="grey",anchor="w",
                            font="Noteworthy 48")
                
                        
       
        mode.drawButton(canvas,mode.analyseX0,mode.analyseY0,mode.analyseX1,mode.analyseY1,"Analyse")    

        canvas.create_image(mode.recordX, mode.recordY, image=ImageTk.PhotoImage(mode.scaleRecordImg)) 
        canvas.create_image(mode.playX, mode.playY, image=ImageTk.PhotoImage(mode.scalePlayImg))
        canvas.create_oval(mode.visualizeCX-30,mode.visualizeCY-30,mode.visualizeCX+30,mode.visualizeCY+30, fill = "grey")
        canvas.create_text(mode.visualizeCX,mode.visualizeCY,text="Visualize",font= "Noteworthy 16",fill = "white")
        if(mode.rIsPressed == True):
            canvas.create_image(mode.recordX, mode.recordY, image=ImageTk.PhotoImage(mode.scaleRecordImg))

        if(mode.isErrorDisplayed == True):
            mode.displayError(canvas)
        if(mode.app.makeButtonDark == True):
            canvas.create_image(mode.recordX, mode.recordY, image=ImageTk.PhotoImage(mode.scaleDarkRecord))
        


class KeyAndScale(Mode):
    def appStarted(mode):
        mode.isGPressed = False
        mode.isBlackKey = False
        mode.isWhiteKey = False
        mode.app.pitches = []
        mode.app.songList = []
        mode.app.midiList = []
        mode.app.noteList = []
        mode.app.key = ""
        mode.app.keyScale = []
        mode.app.newSongList =[]
        mode.app.harmonyMidiList = []
        mode.app.harmonySongList = []
        mode.app.yLineSong = []
        mode.app.yLineHarmony = []
        mode.qIsPressed = False
        mode.pianoWhiteDimensions = []
        mode.pianoBlackDimensions = []
        mode.buttonCenterPositions = []
        mode.buttonRadius = None
        mode.midiPlayed = None
        mode.midiPlayedIndex = None
        mode.midiPlayedColor = ""
        mode.blackKeyPressedIndex = None
        mode.playNotesIsCalledByMousePressed = False
        mode.midiToPlay = None
    
        for i in range(11):
            h = (mode.height//3)  + (i+1)*10
            mode.app.yLineHarmony.append(h)
        mode.app.pitches = demo_source_simple.analyse(mode.app.filename)
        mode.app.songList = demo_source_simple.formatMidiListFromPitches(mode.app.pitches)
        mode.app.midiList,mode.app.noteList,mode.app.newSongList = notes_functions.getNoteAndMidi(mode.app.songList)
        mode.app.key, mode.app.keyScale = notes_functions.findKey(mode.app.midiList,mode.app.noteList)  
        mode.app.harmonyMidiList,mode.app.harmonyNoteList,mode.app.harmonySongList = notes_functions.getHarmonyLine(mode.app.midiList,mode.app.keyScale,mode.app.newSongList)
        mode.homeButtonX0 = mode.width//20
        mode.homeButtonX1 = mode.width//20 + 80
        mode.homeButtonY0 = mode.height//20
        mode.homeButtonY1 = mode.height//20 + 30
        # image obtained from https://www.google.com/search?q=info+button&safe=active&client=safari&rls=en&sxsrf=ALeKk01IlZgn0KYpl2ugOnwyle3w3ARwiQ:1588145178335&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjW5tLpjY3pAhVIU30KHRjICFwQ_AUoAXoECBAQAw&biw=972&bih=768#imgrc=yuX3NKBkmfIFRM
        mode.infoImg = mode.loadImage('infoButton.png')
        mode.scaleInfoImg = mode.scaleImage(mode.infoImg,1/12)
        mode.infoX = mode.width*0.90
        mode.infoY = mode.height*0.08
        mode.makeKeyDark = False
        mode.makeKeyDarkStartTime = 0
        # image obtained from https://www.google.com/search?q=treble+clef+white&tbm=isch&ved=2ahUKEwjTptqxzI3pAhXYg0sFHTT_DOAQ2-cCegQIABAA&oq=treble+clef+white&gs_lcp=CgNpbWcQAzICCAAyAggAMgIIADIGCAAQBRAeMgYIABAIEB4yBggAEAgQHjIGCAAQCBAeMgYIABAIEB46BAgjECc6BAgAEENQixJYzBlg6BpoAHAAeACAAZMBiAHUBJIBAzMuM5gBAKABAaoBC2d3cy13aXotaW1n&sclient=img&ei=tG2pXtP8GtiHrtoPtP6zgA4&bih=768&biw=972&client=safari&safe=active#imgrc=bzU0fdyUn6IZfM
        mode.trebleImg = mode.loadImage('treble.png')
        mode.scaleTrebleImg = mode.scaleImage(mode.trebleImg,1/10)
        # image obtained from https://www.google.com/search?q=bass+clef+white&tbm=isch&ved=2ahUKEwjuo-6zzI3pAhVukksFHSY-As8Q2-cCegQIABAA&oq=bass+clef+white&gs_lcp=CgNpbWcQAzICCAAyAggAMgYIABAIEB46BwgjEOoCECc6BAgjECc6BAgAEEM6BQgAEIMBUMyRC1jXxgtg1ccLaAVwAHgAgAHWAogBwQySAQYxOC4zLTGYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCg&sclient=img&ei=uG2pXu7nOu6krtoPpvyI-Aw&bih=768&biw=972&client=safari&safe=active
        mode.bassImg = mode.loadImage('bass.png')
        mode.scaleBassImg = mode.scaleImage(mode.bassImg,1/6)
        

        
    
    def redrawAll(mode,canvas):
        font = "Arial 24"
        canvas.create_rectangle(0,0,mode.width,mode.height, fill="black")
        canvas.create_text(mode.width/2, 50, text=f'The Key of the song is: {mode.app.key}', 
                            font="Noteworthy 24 bold",fill = "white")
        print(mode.homeButtonX0,mode.homeButtonX1,mode.homeButtonY0,mode.homeButtonY1)
        canvas.create_rectangle(mode.homeButtonX0,mode.homeButtonY0,mode.homeButtonX1,mode.homeButtonY1, fill = "grey")
        midx = (mode.homeButtonX0+mode.homeButtonX1)/2
        midy = (mode.homeButtonY0+mode.homeButtonY1)/2
        canvas.create_text(midx,midy,text = "Home", font = "Noteworthy 14",fill = "white")
        canvas.create_text(10,180, text = "Your harmony line:", font = "Noteworthy 20",fill = "white",anchor = "w")
        canvas.create_image(mode.width*0.90, mode.infoY, image=ImageTk.PhotoImage(mode.scaleInfoImg)) 
        canvas.create_image(20,230, image=ImageTk.PhotoImage(mode.scaleTrebleImg))
        canvas.create_image(20,290, image=ImageTk.PhotoImage(mode.scaleBassImg))
        for i in range(11):
            h = (mode.height//3)  + (i+1)*10
            if(i!=5):
                mode.drawLine(canvas,h)
        
        KeyAndScale.getPositionOfNote(mode,canvas,mode.app.harmonyMidiList,mode.app.harmonyNoteList)
        KeyAndScale.drawPiano(mode,canvas)
        for i in range(3):
            cx = mode.width//4*(i+1)
            cy = mode.height*0.6
            mode.buttonCenterPositions.append([cx,cy])

            #h1 is the y point of the final line of sheet music
            h1 = (mode.height//3) + 110

            #h2 is the y point of the piano
            h2 = mode.height*0.75
            mode.buttonRadius = (h2-h1)*0.25
            r = (h2-h1)*0.25
            print("drawButton")
            if(i == 0):
                text = "Melody"
            elif(i == 1):
                text = "Harmony"
            elif(i == 2):
                text = "Combined"
            KeyAndScale.drawRoundButton(mode,canvas,cx,cy,r,text)
        for num in range(0,14):
            startNote = aubio.note2midi(mode.app.key + "3")
            note = startNote + num
            midiName = aubio.midi2note(note)[:-1]
            for keyNote in mode.app.keyScale:
                if(note>=48 and note <=73):
                    if(midiName == keyNote):
                        KeyAndScale.testHighlight(mode,canvas,note,midiName,"light blue") 
        if(mode.makeKeyDark == True):
            midiName = aubio.midi2note(mode.midiToPlay)[:-1]
            KeyAndScale.testHighlight(mode,canvas,mode.midiToPlay,midiName,"grey")

        
    def testHighlight(mode,canvas,midi,midiName,fillColor):
        blackKeys = [49,51,54,56,58,61,63,66,68,70,73]
        whiteKeys = [48,50,52,53,55,57,59,60,62,64,65,67,69,71,72]
        listForBlackKeys = [2,6,9,13] # holds the indexes of white keys that don't have a black key following them 
        if(midi in blackKeys):
            index = blackKeys.index(midi)
            x1 = mode.pianoBlackDimensions[index][0]
            y1 = mode.pianoBlackDimensions[index][1]
            x2 = mode.pianoBlackDimensions[index][2]
            y2 = mode.pianoBlackDimensions[index][3] 
            canvas.create_rectangle(x1,y1,x2,y2,fill = fillColor)
            canvas.create_text((x1+x2)/2,y2-20,text = midiName,fill = "white")
        elif(midi in whiteKeys):
            index = whiteKeys.index(midi)
            x1 = mode.pianoWhiteDimensions[index][0]
            y1 = mode.pianoWhiteDimensions[index][1]+75
            x2 = mode.pianoWhiteDimensions[index][2]
            y2 = mode.pianoWhiteDimensions[index][3]
            canvas.create_rectangle(x1,y1,x2,y2,fill = fillColor)
            canvas.create_text((x1+x2)/2,y2-20,text = midiName,fill = "white")
    
    def drawWhiteKey(mode,canvas,whiteKeyWidth,keyNum):
        x1 = 0.07*mode.width + (keyNum-1)*whiteKeyWidth
        y1 = mode.height*0.75
        x2 = 0.07*mode.width + (keyNum)*whiteKeyWidth
        y2 = mode.height
        if(len(mode.pianoWhiteDimensions) < 15):
            mode.pianoWhiteDimensions.append([int(x1),int(y1),int(x2),int(y2)])
        canvas.create_rectangle(x1,y1,x2,y2,fill ="white")
    
    def drawBlackKey(mode,canvas,blackKeyWidth,whiteKeyNum,blackKeyNum):
        x1 = (0.07*mode.width)*1.6 + ((whiteKeyNum-1)*blackKeyWidth)
        y1 = mode.height*0.75
        x2 = x1 + blackKeyWidth
        y2 = mode.height*(7/8)
        if(whiteKeyNum != 1):
            x1 = x1 + (blackKeyWidth)*(0.9*blackKeyNum)
            x2 = x1 + blackKeyWidth
        if(len(mode.pianoBlackDimensions) < 11):
            mode.pianoBlackDimensions.append([int(x1),int(y1),int(x2),int(y2)])
        canvas.create_rectangle(x1,y1,x2,y2, fill ="black")
    
    def drawPiano(mode,canvas):
        whiteKeyWidth = (mode.width-100)//15
        blackKeyWidth = whiteKeyWidth*0.6
        listForBlackKeys = [3,7,10,14]
        blackKeyNum = 0
        for whiteKeyNum in range(1,16):
            KeyAndScale.drawWhiteKey(mode,canvas,whiteKeyWidth,whiteKeyNum)   
        for whiteKeyNum in range(1,16):
            if(whiteKeyNum not in listForBlackKeys):
                KeyAndScale.drawBlackKey(mode,canvas,blackKeyWidth,whiteKeyNum,blackKeyNum)
                blackKeyNum +=1            
        
    def findMidiToPlay(mode,x,y):
        x = int(x)
        y = int(y)
        blackKeys = [49,51,54,56,58,61,63,66,68,70,73]
        whiteKeys = [48,50,52,53,55,57,59,60,62,64,65,67,69,71,72]
        notePlayed = False
        if(y<450):
            print("here")
        if(y < 525):
            for key in mode.pianoBlackDimensions:
                if(x>=key[0] and x<= key[2]):
                    notePlayed = True
                    ind = mode.pianoBlackDimensions.index(key)
                    return blackKeys[ind]
        if(notePlayed == False):
            for key in mode.pianoWhiteDimensions:
                if(x>=key[0] and x<= key[2]):
                    notePlayed = True
                    ind = mode.pianoWhiteDimensions.index(key)
                    return whiteKeys[ind]
    
    def timerFired(mode):
        if(mode.makeKeyDark == True):
            elapsedTime = time.time() - mode.makeKeyDarkStartTime
            if(elapsedTime > 1):
                mode.makeKeyDark = False

    def mousePressed(mode,event):
        x = event.x
        y = event.y

        if((x>=(mode.width*0.90)-25 and x<=(mode.width*0.90)+25) and (y>=mode.infoY-25 and y<=mode.infoY+25)):
            mode.app.setActiveMode(mode.app.visualizer)

        if(y > mode.height*0.75):
            mode.midiToPlay = KeyAndScale.findMidiToPlay(mode,x,y)
            mode.makeKeyDark = True
            if(mode.midiToPlay != None):
                mode.makeKeyDarkStartTime = time.time()
                playNotes.playPianoNote(mode.midiToPlay)
                mode.isBlackKey = False
                mode.isWhiteKey = False
        else:
            if(((x >= mode.homeButtonX0)and(x <= mode.homeButtonX1))and
                ((y >= mode.homeButtonY0)and(y <= mode.homeButtonY1))):
                mode.app.setActiveMode(mode.app.homeAndRecordMode)

            for i in range(3):
                cx = mode.buttonCenterPositions[i][0]
                cy = mode.buttonCenterPositions[i][1]
                if(((x >= (cx-mode.buttonRadius)) and (x <= cx+mode.buttonRadius)) and
                    (y >= (cy-mode.buttonRadius)) and (y <= cy+mode.buttonRadius)):
                    if(i == 0):
                        mode.playNotesIsCalledByMousePressed = True
                        playNotes.playNotes(mode.app.newSongList)
                    if(i == 1):
                        playNotes.playNotes(mode.app.harmonySongList)
                    if(i == 2):
                        playNotes.playMelAndHarLine(mode.app.newSongList,mode.app.harmonySongList)
            

    def keyPressed(mode, event):
        if(event.key == 'q'):
            mode.midiToPlay = 48
        elif(event.key == 'w'):
            mode.midiToPlay = 50
        elif(event.key == 'e'):
            mode.midiToPlay = 52
        elif(event.key == 'r'):
            mode.midiToPlay = 53
        elif(event.key == 't'):
            mode.midiToPlay = 55
        elif(event.key == 'y'):
            mode.midiToPlay = 57
        elif(event.key == 'u'):
            mode.midiToPlay = 59
        elif(event.key == 'i'):
            mode.midiToPlay = 60
        elif(event.key == 'o'):
            mode.midiToPlay = 62
        elif(event.key == 'p'):
            mode.midiToPlay = 64
        elif(event.key == 'a'):
            mode.midiToPlay = 65
        elif(event.key == 's'):
            mode.midiToPlay = 67
        elif(event.key == 'd'):
            mode.midiToPlay = 69
        elif(event.key == 'f'):
            mode.midiToPlay = 71
        elif(event.key == 'g'):
            mode.midiToPlay = 72
        elif(event.key == 'h'):
            mode.midiToPlay = 49
        elif(event.key == 'j'):
            mode.midiToPlay = 51
        elif(event.key == 'k'):
            mode.midiToPlay = 54
        elif(event.key == 'l'):
            mode.midiToPlay = 56
        elif(event.key == 'z'):
            mode.midiToPlay = 58
        elif(event.key == 'x'):
            mode.midiToPlay = 61
        elif(event.key == 'c'):
            mode.midiToPlay = 62
        elif(event.key == 'v'):
            mode.midiToPlay = 66
        elif(event.key == 'b'):
            mode.midiToPlay = 68
        elif(event.key == 'n'):
            mode.midiToPlay = 70
        elif(event.key == 'm'):
            mode.midiToPlay = 73  
        mode.makeKeyDark = True
        mode.makeKeyDarkStartTime = time.time()
        playNotes.playPianoNote(mode.midiToPlay)      

    
    def yPositionCalc(mode,midi,lst,ind):
        if(midi>=43 and midi<=79):
            lineList = copy.copy(mode.app.yLineHarmony)
        if(midi == lst[0] or midi == lst[1]):
            cy = lineList[ind]
            if(midi in [48,65,72]):
                cy = lineList[ind] - 5
        else:
            print("here")
            cy = lineList[ind] - 5   
        return cy

    def getPositionOfNote(mode,canvas,midiList,noteList):
        midiLineListTreble = [[77,78,79,80],[74,75,76],[71,72,73],[67,68,69,70],[64,65,66],[60,61,62,63],[57,58,59],[53,54,55,56],[50,51,52],[47,48,49],[43,44,45,46]]
        midiSharpList = [49,51,54,56,58,61,63,66,68,70,73]
        for i in range(len(mode.app.harmonyMidiList)):
            midi = mode.app.harmonyMidiList[i]
            note = mode.app.harmonyNoteList[i]
            cx = (i+1)*25
            if(midi!=0):
                if(midi >= 43 and midi<=79):
                    for lst in midiLineListTreble:
                        if(midi in lst):
                            ind = midiLineListTreble.index(lst)
                            cy = KeyAndScale.yPositionCalc(mode,midi,lst,ind)
                KeyAndScale.drawNode(mode,canvas,cx,cy,midi)
                if(midi in midiSharpList):
                    KeyAndScale.drawSharp(mode,canvas,cx,cy)

    def drawSharp(mode,canvas,cx,cy):
        canvas.create_text(cx+10,cy,text = "#", font = "Noteworthy 12",fill = "white")

    def drawLine(mode,canvas,h):
        canvas.create_line(0,h,mode.width,h,fill = "white")
 
    def drawNode(mode,canvas,cx,cy,midi):
        r = 5
        note = aubio.midi2note(midi)[:-1]
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill = "white")
        canvas.create_text(cx,200,text = note,fill = "white")
        if((midi >= 71 and midi<= 79) or (midi >= 50 and midi<= 59)):
            canvas.create_line(cx-r,cy,cx-r,cy+27,fill = "white")
        elif(midi >= 62 and midi<= 70) or (midi >= 43 and midi<= 49):
            canvas.create_line(cx+r,cy-27,cx+r,cy,fill = "white")
        elif(midi>=60 and midi<62):
            canvas.create_line(cx-r-3,cy,cx+r+3,cy,fill = "white")
    def drawRoundButton(mode,canvas,cx,cy,r,name):
        print("drawButton")
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill = "grey")
        canvas.create_text(cx,cy,text = name, font="Noteworthy 14",fill ="white")

class Visualizer(Mode):
    def appStarted(mode):
        mode.messages = ['appStarted']
        #image obtained from https://www.google.com/search?q=scales+music&tbm=isch&ved=2ahUKEwjKj9v9-Y3pAhUI1nMBHXG8BLEQ2-cCegQIABAA&oq=scales+music&gs_lcp=CgNpbWcQAzICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6BAgjECc6BAgAEENQ0glYliNg6yRoAHAAeACAAVmIAfYFkgECMTCYAQCgAQGqAQtnd3Mtd2l6LWltZw&sclient=img&ei=g52pXorCGoisz7sP8fiSiAs&bih=649&biw=618&client=safari&safe=active
        mode.scalesImg = mode.loadImage('pianoscales.jpg')
        mode.resizeScalesImg = mode.scaleImage(mode.scalesImg, 1/2)
        mode.trebleX = 54
        mode.trebleY = 239
        mode.bassX = 54
        mode.bassY = 305
        mode.isTreble = False
        mode.isBass = False
        mode.isTrebleStartTime = 0
        mode.isBassStartTime = 0
        mode.backX0 = 20
        mode.backY0 = 20
        mode.backX1 = 70
        mode.backY1 = 50

        
    def redrawAll(mode,canvas):
        w = mode.width
        h = mode.height
        canvas.create_text(w//2,h*0.05,text = "Instruction Manual for the piano and sheet music",font = "Noteworthy 24")
        canvas.create_text(5,h*0.12,text = "General information",font = "Noteworthy 18",anchor = "w")

        canvas.create_text(5, h*0.17, text = "The white keys depict a natural note and black keys depict a sharp or a flat(# or b following the note). \nMusical scores incorporate these notes with specific time intervals in order create music.",font ="Noteworthy 14",anchor = "w")
        """
        font = 'Arial 20 bold'
        #canvas.create_text(mode.width*0.8,  30, text='Events Demo', font=font)
        n = min(10, len(mode.messages))
        i0 = len(mode.messages)-n
        for i in range(i0, len(mode.messages)):
            canvas.create_text(mode.width*0.8, 100+50*(i-i0),
                               text=f'#{i}: {mode.messages[i]}',
                               font="Noteworthy")
        """
        canvas.create_image(w//2, h//2, image=ImageTk.PhotoImage(mode.resizeScalesImg))
        canvas.create_rectangle(w*0.3,h*0.6,w*0.7,h*0.9)
        canvas.create_line(mode.trebleX,mode.trebleY-50,mode.trebleX,mode.trebleY-15,width = 1)
        canvas.create_line(mode.bassX,mode.bassY+20,mode.bassX,mode.bassY+50,width = 1)
        canvas.create_text(mode.trebleX,mode.trebleY-20,text = "v")
        canvas.create_text(mode.bassX,mode.bassY+20,text = "^")
        canvas.create_rectangle(mode.backX0,mode.backY0,mode.backX1,mode.backY1)
        canvas.create_text((mode.backX0+mode.backX1)//2,(mode.backY0+mode.backY1)//2, text = "Back", font = "Noteworthy 14")
        if(mode.isTreble == True):
            canvas.create_text(w*0.3,h*0.6,text = "Treble clef consists of the notes on\n the second half of the piano. These notes\n are always played by the right hand.\nNotes in the treble clef are usually of higher frequency.",font = "Noteworthy 12",anchor = "nw")
        if(mode.isBass == True):
            canvas.create_text(w*0.3,h*0.6,text = "The Bass clef consists of the notes on\n the first half of the piano. These notes\n are always played by the left hand.\n The bass line caters to music that is of lower frequency.",font = "Noteworthy 12",anchor = "nw")

    
    def mousePressed(mode, event):
        mode.messages.append(f'mousePressed at {(event.x, event.y)}') 
        x = event.x
        y = event.y
        if((x >= mode.trebleX-7 and x<=mode.trebleX+7) and (y >= mode.trebleY - 12 and y <= mode.trebleY+12)):
            mode.isTreble = True
            mode.isStartTime = time.time()
        elif((x >= mode.bassX-7 and x<=mode.bassX+7) and (y >= mode.bassY - 12 and y <= mode.bassY+12)):
            mode.isBass = True
            mode.isStartTime = time.time()
        elif((x >= mode.backX0 and x <= mode.backX1) and (y >= mode.backY0 and y<= mode.backY1)):
            mode.app.setActiveMode(mode.app.keyAndScale)

    
    def timerFired(mode):
        if(mode.isBass == True or mode.isTreble == True):
            elapsedTime = time.time() - mode.isStartTime
            if(elapsedTime >= 3):
                mode.isBass = False
                mode.isTreble = False
        
           
    

class MyModalApp(ModalApp):
    def appStarted(app):

        app._root.resizable(False, False) #from 15-112 piazza instructor post
        app.homeAndRecordMode = HomeAndRecordMode()
        app.keyAndScale = KeyAndScale()
        app.visualizer = Visualizer()
        app.setActiveMode(app.homeAndRecordMode)

app = MyModalApp(width=600, height=600)