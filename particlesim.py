import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import particlesimlib

particles = []

for i in range(0,3):
    random_nums = np.random.random_sample(4) #creates a list of 4 radom floats from 0 to 1

    xpos = random_nums[0] + 0.5 # uses first two values in random list to generate x and y posistions
    ypos = random_nums[1] + 0.5 #

    speed = random_nums[2]*707 + 1060 #uses third item in random list to generate the speed of the particle

    xspeed = random_nums[3]*speed*np.random.choice([-1,1]) #uses last random value in list to generate the magnitude of the x_component of the velocity
                                                           #then uses aouther random number to select its sign

    yspeed = ((speed**2-xspeed**2)**0.5)*np.random.choice([-1,1]) #selects the magnitude of the y velocity such that the magnitude of the particle's total
                                                                       #velocity will equal the speed variable, then uses aouther random number to select its sign
    
    particles.append(particlesimlib.antiproton(xpos, ypos, xspeed, yspeed, i, magnetic_interact=True)) #creates particles

for particle in particles:
    particle.particles = particles


#########################################################
############### begging of animation ####################
#########################################################

# First set up the figure, the axis, and the plot element we want to animate
current_xs=[]
current_ys=[]
all_xs=[]
all_ys=[]

ts=[]
recentxs=[]
recentys=[]

fig, (ax1, ax2) = plt.subplots(2,1)

data_points=500
delta_t=0.00001
magnetic_feild=0.0002


ax1.set_xlim(0, 2)
ax2.set_xlim(0, delta_t*data_points)
for ax in [ax1, ax2]:
    ax.set_ylim(0, 2)
    ax.grid()


particleplot, = ax1.plot([], [], 'bo', ms=6)
particleplothistory, = ax1.plot([], [], 'r', ms=6)
particlexs, = ax2.plot([], [], 'b', ms=6)
particleys, = ax2.plot([], [], 'r', ms=6)

particle_histories = [] #list of all plotting objects that will plot particle histories

for i in particles: #adds a plotting object to the list for each particle
    particle_histories.append(ax1.plot([], [], 'r', ms=6))



# initialization function: plot the background of each frame
def init():
    particleplot.set_data([], [])
    particlexs.set_data([], [])
    particleys.set_data([], [])
    return particleplot, particleplothistory ,particlexs, particleys

# animation function.  This is called sequentially
def animate(i):
    

    current_xs=[]
    current_ys=[]

    history_count=0
    for particle in particles:
        particle.animate(delta_t,magnetic_feild,100)
        current_xs.append(particle.x)
        current_ys.append(particle.y)
    
        particle_histories[history_count][0].set_data(particle.xs, particle.ys)
        history_count+=1

    if not(len(ts)):
        ts.append(delta_t)
    else:
        ts.append(ts[-1]+delta_t)
        
    recentxs.append(particles[0].x)
    recentys.append(particles[0].y)

    if (len(ts)>data_points):
        for _list in [ts, recentxs, recentys]:
            _list.pop(0)
        ax2.set_xlim(ts[0], ts[-1])
    
    
    particleplot.set_data(current_xs, current_ys)#next block sets data of different plot objects
    particlexs.set_data(ts, recentxs)
    particleys.set_data(ts, recentys)
    
    objects_to_retern = [particleplot, particlexs, particleys] #creates a list of different plot objects to be reterned (a plot object needs to be returned in order for it to be seen)
    for particle_history in particle_histories: #adds each particle's history plot to the list of things to be returned
        objects_to_retern.append(particle_history[0])
    
    return objects_to_retern #returns the list of objects to be returned 

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=True)

plt.show()




