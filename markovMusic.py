import math
import random
import struct
import pyaudio
import numpy

#Since this is a Markov Chain, we can translate this whole thing into various 
#transition probability matrices. This will make it easier to follow, program,
#and generalize

MAX_KEY = 88
MIN_KEY = 30
MIDDLE_A = 49
CHROM_COUNT = 12.0
REF_FREQ = 440
DURS = (.25,.325,.5,.75,1,1.5,2)#,3,4) #Ommitting whole note and dotted half
FREQS = [REF_FREQ*2**((key-MIDDLE_A)/CHROM_COUNT) for key in xrange(MIN_KEY,MAX_KEY+1)]
NUM_KEYS = len(FREQS)
fs = 48000
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=fs,
    output=True)

def clamp(val, lower, upper):
    return max(lower,min(upper,val))

def bounce(val, lower, upper):
    if val < lower:
        return 2*lower - val
    elif val > upper:
        return 2*upper - val
    else:
        return val
        
def randNearChoice(curKey, refList, indexList = [-4,0,4], indexProb=.5):
    '''makes index list values more likely than others in keyChoices.
    indexProb gives the amount of 100% that should be allocated to the indexList'''
    listLen = len(refList)
    nKeyChoices = len(indexList)
    mostProb = float(indexProb)/nKeyChoices
    otherProbs = (1.0-indexProb)/(listLen - nKeyChoices)
    probs = [otherProbs for i in xrange(listLen)]
    for index in indexList:
        probs[bounce(curKey+index-1, 0, listLen-1)] = mostProb
    return numpy.random.choice(refList,p=probs)
    
def randMusic(numNotes, tempo=120):
    freqs = (numpy.random.choice(FREQS) for i in xrange(numNotes))
    durations = (random.choice(DURS)*(60.0/tempo) for i in xrange(numNotes))
    return zip(freqs,durations)

def stochMusic(numNotes, tempo = 120):
    freq = numpy.random.choice(FREQS)
    freqIndex = FREQS.index(freq)
    dur = numpy.random.choice(DURS)
    durIndex = DURS.index(dur)
    keys = [freq]
    durs = [dur]
    while len(keys) <= numNotes:
        freq = randNearChoice(freqIndex,FREQS,(-5,-4,0,4,5),.7)
        keys.append(freq)
        dur = randNearChoice(durIndex,DURS,(-1,0,1),.75)*(60.0/tempo)
        durs.append(dur)
    return zip(keys,durs)

def listToMusic(vals,freqs):
    numFreqs = len(freqs)
    #origVals = vals
    vals = sorted(vals)
    freqMap = {}
    _,binEdges = numpy.histogram(vals,numFreqs)
    binEdges = list(binEdges)
    intervals = zip(binEdges,binEdges[1:])
    #I know there's a better way to do this. Later.
    for low, up in intervals:
        for val in vals:
            if low <= val < up:
                freqMap[val] = freqs[binEdges.index(low)]
    return freqMap
    
def playTone(frequency, amplitude, duration, fs, stream):
    N = int(fs / frequency)
    T = int(frequency * duration)  # repeat for T cycles
    dt = 1.0 / fs
    # 1 cycle
    tone = (amplitude * math.sin(2 * math.pi * frequency * n * dt) for n in xrange(N))
    #TODO: get the format from the stream; this assumes Float32
    data = ''.join(struct.pack('f', samp) for samp in tone)
    for n in xrange(T):
        stream.write(data)

song = randMusic(20)
#song = stochMusic(20)

for freq, dur in song:
    print freq
    playTone(freq,1,dur,fs,stream)