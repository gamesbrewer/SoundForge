#http://www.swharden.com/blog/2013-05-09-realtime-fft-audio-visualization-with-python/

import pyaudio
import numpy

class SwhRecorder:
    ###Simple, cross-platform class to record from the microphone.

    def __init__(self):
        """minimal garb is executed when class is loaded."""
        self.RATE=48100
        self.BUFFERSIZE=2**12 #1024 is a good buffer size
        self.secToRecord=.1
        self.threadsDieNow=False
        self.newAudio=False

    def setup(self):
        ###initialize sound card.
        #TODO - windows detection vs. alsa or something for linux
        #TODO - try/except for sound card selection/initiation

        self.buffersToRecord=int(self.RATE*self.secToRecord/self.BUFFERSIZE)
        if self.buffersToRecord==0: self.buffersToRecord=1
        self.samplesToRecord=int(self.BUFFERSIZE*self.buffersToRecord)
        self.chunksToRecord=int(self.samplesToRecord/self.BUFFERSIZE)
        self.secPerPoint=1.0/self.RATE

        self.p = pyaudio.PyAudio()
        self.inStream = self.p.open(format=pyaudio.paInt16,channels=1,
            rate=self.RATE,input=True,frames_per_buffer=self.BUFFERSIZE)
        self.xsBuffer=numpy.arange(self.BUFFERSIZE)*self.secPerPoint
        self.xs=numpy.arange(self.chunksToRecord*self.BUFFERSIZE)*self.secPerPoint
        self.audio=numpy.empty((self.chunksToRecord*self.BUFFERSIZE),dtype=numpy.int16)               

    def close(self):
        ###cleanly back out and release sound card.
        self.p.close(self.inStream)

    ### RECORDING AUDIO ###  

    def getAudio(self):
        ###get a single buffer size worth of audio.
        audioString=self.inStream.read(self.BUFFERSIZE)
        return numpy.fromstring(audioString,dtype=numpy.int16)