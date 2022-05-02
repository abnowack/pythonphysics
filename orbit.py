from PyPhysics import *
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA


def gravity_force(m, r):
    G = 6.67e-11
    M_sun = 1.99e30

    r_norm = LA.norm(r)

    F = - G * m * M_sun / (r_norm ** 3) * r

    return F


# def EOM(r_0, v_0, t):
    # g = np.array([0., -9.8])

    # r = np.zeros(shape=(2, len(t)), dtype=float)
    # r[0] = r_0[0] + v_0[0] * t + 0.5 * (t ** 2) * g[0]
    # r[1] = r_0[1] + v_0[1] * t + 0.5 * (t ** 2) * g[1]
    # v = v_0 + g * t

    # return r


# One Particle System
class Comet(Particle):
    def __init__(self, r, v, m):
        super().__init__(r, v, m)

    def calc_accel(self, r, v):
        return gravity_force(self.m, r) / self.m

    def move(self, r, v):
        self.r = r
        self.v = v

    def orbit(self, elapsed_time=0, time_step=0, method='euler'):

        def f(r, v): return self.calc_accel(r, v)

        ode = ODEIntegrator(f, method)

        time = 0

        r_x = [self.r[0]]
        r_y = [self.r[1]]
        r_t = [time]

        while time <= elapsed_time:

            self.r, self.v = ode.step(
                self.r, self.v, time_step)
            r_x.append(self.r[0])
            r_y.append(self.r[1])

            time += time_step

            r_t.append(time)

        return r_x, r_y, r_t

AU = 1.496e11
YEAR = 365 * 24 * 60 * 60.

r_0 = np.array([1., 0.]) * AU
v_0 = np.array([0., 2 * np.pi * AU / YEAR])

comet = Comet(r=r_0, v=v_0, m=1)

tau = 0.02 * YEAR

c_x, c_y, c_t = comet.orbit(elapsed_time=40 * YEAR, time_step=tau, method='rk4')
plt.plot(c_x, c_y, 'b.')


# eom_r = EOM(r_0, v_0, np.array(b1_t))
# plt.plot(eom_r[0], eom_r[1], 'k-')

plt.xlabel("X (m)")
plt.ylabel("Y (m)")
# plt.ylim(0)
plt.show()
