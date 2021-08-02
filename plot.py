# EVC

import numpy as numpy
import matplotlib.pyplot as plt


def logistic(x0,q):
  for i in range(300):
   x = q*x0*(1. - x0)
   x0=x
  return x

def logistic_one(x0,q):
 x = q*x0*(1. - x0)
 return x


x0 = 0.1#0.01
q = 2.#2	

N=100
xx=[]
yy=[]

for n in range(N+1):
 qf=3.9
 qi=2.8
 q=qi+n*(qf-qi)/N
 x=logistic(x0,q)

 y=440.+200*x

 xx.append(n)
 yy.append(y)
# print n,q,x
 x0=x
 

plt.plot(xx,yy,'-o')
plt.xlabel("T")
plt.ylabel("Freq (Hz)")
#plt.show()
plt.savefig('logistic.pdf')
