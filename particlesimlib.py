class particle(object):

    def __init__(self, x, y, x_velocity, y_velocity, index, magnetic_interact=True, electrostatic_interact=True):
        self.x = x #particles x and y position in meters
        self.y = y 
        
        self.t = 0 #particles time index
        self.xs = [x] #lists of all particle's x and y positions
        self.ys = [y]
        
        
        self.x_velocity = x_velocity #particles x and y velocities
        self.y_velocity = y_velocity
        
        self.acceleration_x = 0 #particles x and y accelerations
        self.acceleration_y = 0

        self.particles = [] #list of all particles in the system
        self.particle_index = index #The index of this particle in the list of particles. (needed so the library doesn't try and interact a particle with itself 

        self.magnetic_interact = magnetic_interact             # these variables determine if the particle will interact magneticly and/or
        self.electrostatic_interact = electrostatic_interact   # electrostaticly
        
        self.init_specific() #defines values for charge mass and name,
                             #default function is over-ridden by chlidren
                             #such as proton's to give particle specific
                             #values for mass
        

    def init_specific(self): #defines default values for charge mass and name
        self.charge = 1.60218e-19 #charge in colombs
        self.mass = 1 #mass in kg
        self.name = 'default_particle'

    def animate(self, delta_t, magnetic_feild, presion):
        delta_t=delta_t/presion
        
        for i in range(0,presion):
            self.update(delta_t, magnetic_feild)
            

    def update(self, delta_t, magnetic_field):
        self.t += 1 #updates the particles time index
        self.accelerate(magnetic_field)
        self.move(delta_t)

    def accelerate(self, magnetic_field):
        x_net_force = 0 # creates variables to store the net x and y forces
        y_net_force = 0 #
        
        x_net_force += -self.charge*self.y_velocity*magnetic_field*self.magnetic_interact # adds the x and y compontent of the magnetic force to 
        y_net_force += self.charge*self.x_velocity*magnetic_field*self.magnetic_interact # x_net_force and y_net_force.

        for num in range(len(self.particles)): #interacts with this particle electrostaticly with every other particle
            if not(num==self.particle_index): #avoids interacting a particle with itself.
                other_particle = self.particles[num] #creates a variable for the other particle (makes code look nicer)

                x_normalised_distance = self.x-other_particle.x # finds x and y distaces that will be normilised in a few lines
                y_normalised_distance = self.y-other_particle.y # once normilised they will add to 1
                
                distance = (x_normalised_distance**2+y_normalised_distance**2)**0.5 #finds total distance between the two particles

                x_normalised_distance = x_normalised_distance/distance   #normilises x_normalised_distance and y_normalised_distance
                y_normalised_distance = y_normalised_distance/distance   #they will be needed to appy the force proportianly to the particle's x and y net forces

                coulombs_constant=8.99e15
                x_net_force += self.charge*other_particle.charge*coulombs_constant*x_normalised_distance*self.electrostatic_interact/distance**2
                y_net_force += self.charge*other_particle.charge*coulombs_constant*y_normalised_distance*self.electrostatic_interact/distance**2

                
        self.acceleration_x = x_net_force/self.mass
        self.acceleration_y = y_net_force/self.mass

    def move(self, delta_t):
        new_velocity_x = self.x_velocity + (self.acceleration_x*delta_t) # these two lines find the x and y velocities after the timeframe
        new_velocity_y = self.y_velocity + (self.acceleration_y*delta_t) # based on the accelerations delta_t and velocitities at the begging of the time frame 

        self.x = self.x + ((self.x_velocity + new_velocity_x)*delta_t/2) # using the average of the velocities at the begging and end of the time frame calulates
        self.y = self.y + ((self.y_velocity + new_velocity_y)*delta_t/2) # the x and position at the end of the time frame

        self.xs.append(self.x) # adds current x position to list of all x posisions
        self.ys.append(self.y) # adds current y position to list of all y posisions

        self.x_velocity = new_velocity_x # updates self.velocity to new velocity
        self.y_velocity = new_velocity_y # this way the velocity at the end of this timeframe can be used as the velocity at the start of the old timeframe.
        

    def printv(self): #prints out all insance variables
        print('This ' + self.name + ' has a charge of ' + str(self.charge))
        print('This ' + self.name + ' has a mass of ' + str(self.mass))
        print()

        print('This ' + self.name + ' has a x position of ' + str(self.x) + 'm')
        print('This ' + self.name + ' has a y position of ' + str(self.y) + 'm')
        print()
        
        print('This ' + self.name + ' has a x velocity of ' + str(self.x_velocity) + 'm/s')
        print('This ' + self.name + ' has a y velocity of ' + str(self.y_velocity) + 'm/s')
        print()
        
        print('This ' + self.name + ' has a x aceleration of ' + str(self.acceleration_x) + 'm/s^2')
        print('This ' + self.name + ' has a y aceleration of ' + str(self.acceleration_y) + 'm/s^2')
        print()


class proton(particle): #pronton child class of particle
    def init_specific(self): #define's mass charge and name of proton
        self.charge = 1.60218e-19
        self.mass = 1.6726219e-27
        self.name = 'proton'


class electron(particle): #electron child class of particle
    def init_specific(self): #define's mass charge and name of electron
        self.charge = -1.60218e-19
        self.mass = 9.10938e-31 #31
        self.name = 'electron'

class antiproton(particle): #pronton child class of particle
    def init_specific(self): #define's mass charge and name of proton
        self.charge = -1.60218e-19
        self.mass = 1.6726219e-27
        self.name = 'antiproton'

class positron(particle): #positron child class of particle
    def init_specific(self): #define's mass charge and name of positron
        self.charge = -1.60218e-19
        self.mass = 9.10938e-31 #31
        self.name = 'positron'
