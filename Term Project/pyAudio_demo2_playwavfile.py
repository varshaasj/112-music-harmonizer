import pyaudio
import wave
import sys

def playFile(waveName):
    print("Started to play")
    CHUNK = 1024
    """
    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        sys.exit(-1)

    wf = wave.open(sys.argv[1], 'rb')"""
    wf = wave.open(str(waveName), 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    print("before while loop")

    while len(data) > 0:
        print(data , " ", len(data))
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("finish playing")