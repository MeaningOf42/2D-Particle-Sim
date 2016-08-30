import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import particlesimlib

particle = particlesimlib.antiproton(1,1,-10,10) #creates particle

looprange = 20
numpoints = 1000000
delta_t= looprange/numpoints

x=np.arange(0.0, looprange, delta_t)
particlex=[]
particley=[]

for i in x:
    particlex.append(particle.x)
    particley.append(particle.y)
    particle.animate(delta_t,0.0000002,1)

plt.figure(1)
plt.subplot(211)
plt.plot(x, particlex, 'r', x, particley, 'b')

plt.show()

