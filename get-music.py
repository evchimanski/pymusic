# -*- coding: utf-8 -*-

import numpy as numpy
import matplotlib.pyplot as plt
#import scitools.sound
import scitools_sound
import random


def note(frequency, length, amplitude=5, sample_rate=44100):
 time_points = numpy.linspace(0, length, length*sample_rate)
 data = numpy.sin(2*numpy.pi*frequency*time_points)
 data = amplitude*data
 return data

def oscillations(N):
 x = zeros(N+1)
 for n in range(N+1):
  x[n] = exp(-4*n/float(N))*sin(8*pi*n/float(N))
  return x

def logistic(x0,q):
  for i in range(300):
   x = q*x0*(1. - x0)
   x0=x
  return x

def logistic_one(x0,q):
 x = q*x0*(1. - x0)
 return x

#song = numpy.concatenate((note(400,1),note(200,10)))

x0 = 0.1#0.01
q = 2.#2	

N=100
tones =[]
xx=[]
yy=[]

for n in range(N+1):
# x=logistic_one(x0,q)
 qf=3.9
 qi=2.8
 q=qi+n*(qf-qi)/N
 x=logistic(x0,q)

 y=440.+200*x
 tones.append(note(y,0.1))

 xx.append(n)
 yy.append(y)
# print n,q,x
 x0=x
 
song = numpy.concatenate(tones)

plt.plot(xx,yy,'-o')
plt.xlabel("T")
plt.ylabel("Freq (Hz)")
#plt.show()
plt.savefig('logistic.pdf')

max_amplitude = 2**15 - 1
song = max_amplitude*song

scitools.sound.play(song)
scitools.sound.write(song, 'song_1.wav')

