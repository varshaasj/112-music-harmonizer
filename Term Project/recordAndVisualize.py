#I used the code for recordVoice() from https://gist.github.com/mabdrabo/8678538 as inspiration, understood
#the code and rewrote it. Some parts like the built in functions, i learnt them and wrote it.

import pyaudio
import wave
import numpy
import pylab

def recordVoice(sec):
    #These numerical values of chunk, sampleRate and number of channels. For consistency of stream while recording.
    chunk = 1024  # Record in chunks of 1024 samples
    sampleFormat = pyaudio.paInt16  # 16 bits per sample
    noOfChannels = 2
    sampleRate = 44100 
    seconds = int(sec)
    filename = "output.wav"
    #creating a portaudio system
    audioObject = pyaudio.PyAudio()
    print('Recording')
    #arguments need to be specified as there are multiple parameters
    #in the music stream opened
    stream = audioObject.open(format=sampleFormat,channels=noOfChannels,rate=sampleRate,frames_per_buffer=chunk,input=True)

    frames = []  # Initialize array to store frames

    # this will cause the delay in time and add the recording pieces 
    # to a list that will be stored in a wav file(standard music file)
    for chunkNumber in range(0, int((sampleRate/chunk) * seconds)):
        recordedChunk = stream.read(chunk)
        frames.append(recordedChunk)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    audioObject.terminate()

    print("Finished recording")

    # Save the recorded data(stream parameters) as a WAV file
    wavObject = wave.open(filename, 'wb')
    wavObject.setnchannels(noOfChannels)
    wavObject.setsampwidth(audioObject.get_sample_size(sampleFormat))
    wavObject.setframerate(sampleRate)
    #joining bytes with this format
    wavObject.writeframes(b''.join(frames))
    wavObject.close()
    return filename
#There were detail information on how to visualize the live audio using several methods on the website,
#https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
#I learnt how to implement one method they used and rewrote the code myself understanding the core algorithms.
# the pylab module works very similar to matplotlib so i learnt the implementation of the graphs
#But i copy pasted the html file from the website mentioned above that basically displays the image refreshing it constantly.
#this can also be viewed by clicking on the visual.png image in the tp folder since it refreshes.

def liveVisualizer(secs):
    secs = int(secs) # since the user's input is of type str
    sampleRate = 44100 #it is a good value for sampleRate. It means number of bytes in the sample.
    chunk = sampleRate//secs #chunk refers to the rate at which the music sample is going to be read.
    audioObject=pyaudio.PyAudio()
    audioStream = audioObject.open(format=pyaudio.paInt16,channels=1,rate=sampleRate,input=True,
                  frames_per_buffer=chunk)
    for chunkNumber in range(0, int((sampleRate/chunk) * secs)):
        yValues = numpy.frombuffer(audioStream.read(chunk,exception_on_overflow = False),dtype=numpy.int16)
        xAxis = range(len(yValues)) # list of x values from 0 to the number of frequency elements in 
        yAxis = yValues#values of frequencies stored in a list
        pylab.plot(xAxis,yAxis)
        pylab.title("Live Analysis of your input")
        xMin = 0    #minimum value of the x axis    
        xMax = len(yAxis) #maximum value of the y axis (number of frequency values in data(list))
        yMin = -20000   #limit set for minimum value of y
        yMax = 20000    #limit set for maximum value of y
        pylab.axis([xMin,xMax,yMin,yMax])
        pylab.savefig("visual.png",dpi=50)
        pylab.close('all')
    
    audioStream.stop_stream()
    audioStream.close()
    audioObject.terminate()

