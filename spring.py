from PyPhysics import *

import matplotlib.pyplot as plt


class XSpring(Force1D):
    def __init__(self, k=1):
        self.k = k

    def calc_force(self, particle):
        return Point1D(- self.k * particle.r.x)


class ParticleOnSpring(Particle1D):
    def __init__(self, r=Point1D(), v=Point1D(), spring_coefficient=1):
        super().__init__(r, v, update_method='midpoint', force=XSpring(k=spring_coefficient))

    def release(self, elapsed_time=0, time_step=0):

        time = 0

        r_x, r_t = [self.r.x], [time]

        while time <= elapsed_time:

            self.update(time_step)
            r_x.append(self.r.x)

            time += time_step

            r_t.append(time)

        return r_x, r_t


r_0 = Point1D(10)
v_0 = Point1D(0)

spring1 = ParticleOnSpring(r=r_0, v=v_0, spring_coefficient=1)

tau = 0.05

s1_x, s1_t = spring1.release(100, time_step=tau)

plt.plot(s1_t, s1_x, 'b.')
plt.xlabel("T (s)")
plt.ylabel("X (m)")

plt.show()
