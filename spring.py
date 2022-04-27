import numpy as np
import matplotlib.pyplot as plt

from PyPhysics import *


def spring_force(k, x):
    return -k * x


# One Particle System
class ParticleOnSpring(Particle):
    def __init__(self, r, v, m, spring_coefficient=1):
        super().__init__(r, v, 0, m)

        self.spring_coefficient = spring_coefficient
        self.a = self.calc_accel(self.r, self.v)

    def calc_accel(self, r, v):
        return spring_force(self.spring_coefficient, r) / self.m

    def release(self, elapsed_time=0, time_step=0, method='euler'):

        def f(r, v): return self.calc_accel(r, v)

        ode = ODEIntegrator(f, method)

        time = 0

        r_x = [self.r[0]]
        r_t = [time]

        while time <= elapsed_time:

            self.r, self.v, self.a = ode.step(
                self.r, self.v, self.a, time_step)
            r_x.append(self.r[0])

            time += time_step

            r_t.append(time)

        return r_x, r_t


spring1 = ParticleOnSpring(
    r=np.array([10.]), v=np.array([0.]), m=2, spring_coefficient=1)

tau = 0.05

s1_x, s1_t = spring1.release(elapsed_time=100, time_step=tau, method='verlet')

plt.plot(s1_t, s1_x, 'b-')
plt.xlabel("T (s)")
plt.ylabel("X (m)")

plt.show()
