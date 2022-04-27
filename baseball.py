from PyPhysics import *
import numpy as np
import matplotlib.pyplot as plt


def gravity_force(m):
    g = 9.8
    return np.array([0., -m * g])


def EOM(r_0, v_0, t):
    g = np.array([0., -9.8])

    r = np.zeros(shape=(2, len(t)), dtype=float)
    r[0] = r_0[0] + v_0[0] * t + 0.5 * (t ** 2) * g[0]
    r[1] = r_0[1] + v_0[1] * t + 0.5 * (t ** 2) * g[1]
    # v = v_0 + g * t

    return r


# One Particle System
class Baseball(Particle):
    def __init__(self, r, v, m):
        super().__init__(r, v, 0, m)

        self.a = self.calc_accel(self.r, self.v)

    def calc_accel(self, r, v):
        return gravity_force(self.m) / self.m

    def move(self, r, v):
        self.r = r
        self.v = v
        self.a = self.calc_accel(self.r, self.v)

    def throw(self, time_step=0, method='euler'):

        def f(r, v): return self.calc_accel(r, v)

        ode = ODEIntegrator(f, method)

        time = 0

        r_x = [self.r[0]]
        r_y = [self.r[1]]
        r_t = [time]

        while self.r[1] >= 0:

            self.r, self.v, self.a = ode.step(
                self.r, self.v, self.a, time_step)

            time += time_step

            r_x.append(self.r[0])
            r_y.append(self.r[1])
            r_t.append(time)

        return r_x, r_y, r_t


r_0 = np.array([0., 0.])
v_0 = np.array([10., 10.])

ball1 = Baseball(r=r_0, v=v_0, m=1)

tau = 0.1

b1_x, b1_y, b1_t = ball1.throw(time_step=tau, method='euler')
plt.plot(b1_x, b1_y, 'b-')

ball1.move(r_0, v_0)
b1_x, b1_y, b1_t = ball1.throw(time_step=tau, method='euler-cromer')
plt.plot(b1_x, b1_y, 'g-')

ball1.move(r_0, v_0)
b1_x, b1_y, b1_t = ball1.throw(time_step=tau, method='midpoint')
plt.plot(b1_x, b1_y, 'm-')

ball1.move(r_0, v_0)
b1_x, b1_y, b1_t = ball1.throw(time_step=tau, method='verlet')
# plt.plot(b1_x, b1_y, 'r-')


eom_r = EOM(r_0, v_0, np.array(b1_t))
plt.plot(eom_r[0], eom_r[1], 'k-')

plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.ylim(0)
plt.show()
