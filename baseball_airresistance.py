from PyPhysics import *
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA


def gravity_force(m):
    g = 9.8
    return np.array([0., -m * g])


def force_air_resistance(v, drag_coefficient, area):
    air_density = 1.293

    v_norm = LA.norm(v)
    return - 0.5 * air_density * v * v_norm * drag_coefficient * area


# One Particle System
class Baseball(Particle):
    def __init__(self, r, v, m):
        super().__init__(r, v, m)

        self.area = 0.00426
        self.drag_coefficient = 0.40

    def calc_accel(self, r, v):
        g = gravity_force(self.m)
        drag = force_air_resistance(v, self.drag_coefficient, self.area)
        return (g + drag) / self.m

    def move(self, r, v):
        self.r = r
        self.v = v

    def throw(self, time_step=0, method='euler'):

        def f(r, v): return self.calc_accel(r, v)

        ode = ODEIntegrator(f, method)

        time = 0

        r_x = [self.r[0]]
        r_y = [self.r[1]]
        r_t = [time]

        while self.r[1] >= 0:

            self.r, self.v = ode.step(
                self.r, self.v, time_step)

            time += time_step

            r_x.append(self.r[0])
            r_y.append(self.r[1])
            r_t.append(time)

        return r_x, r_y, r_t


r_0 = np.array([0., 0.])
v_0 = np.array([1000., 1000.])

ball1 = Baseball(r=r_0, v=v_0, m=1)

tau = 0.01

ball1.move(r_0, v_0)
b1_x, b1_y, b1_t = ball1.throw(time_step=tau, method='euler')
plt.plot(b1_x, b1_y, '-', label='Euler')

ball1.move(r_0, v_0)
b1_x, b1_y, b1_t = ball1.throw(time_step=tau, method='midpoint')
plt.plot(b1_x, b1_y, '-', label='Midpoint')

ball1.move(r_0, v_0)
b1_x, b1_y, b1_t = ball1.throw(time_step=tau, method='euler-cromer')
plt.plot(b1_x, b1_y, '-', label='Euler-Cromer')

ball1.move(r_0, v_0)
b1_x, b1_y, b1_t = ball1.throw(time_step=tau, method='verlet')
plt.plot(b1_x, b1_y, '-', label='Verlet')

ball1.move(r_0, v_0)
b1_x, b1_y, b1_t = ball1.throw(time_step=tau, method='rk4')
plt.plot(b1_x, b1_y, '-', label='RK4')

plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.legend()
plt.ylim(0)
plt.show()
