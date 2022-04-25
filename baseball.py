from PyPhysics import *

import matplotlib.pyplot as plt


class Gravity(Force2D):
    g = 9.8

    def calc_force(self, particle):
        return Point2D(0, - particle.m * self.g)

    def EOM(self, particle, time_step):
        time = particle.t + time_step
        a = self.calc_a(particle)

        r = particle.r_0 + particle.v_0 * time + 0.5 * (time ** 2) * a
        v = particle.v_0 + a * time
        return r, v


class Baseball(Particle2D):
    def __init__(self, r=Point2D(), v=Point2D(), update_method='euler'):
        super().__init__(r, v, update_method=update_method, force=Gravity())

    def throw(self, time_step=0):
        r_x, r_y = [self.r.x], [self.r.y]

        while self.r.y >= 0:

            self.update(time_step)
            r_x.append(self.r.x)
            r_y.append(self.r.y)

        return r_x, r_y


r_0 = Point2D(0, 0)
v_0 = Point2D(50, 50)

ball1 = Baseball(r=r_0, v=v_0, update_method='euler')
ball2 = Baseball(r=r_0, v=v_0, update_method='euler-cromer')
ball3 = Baseball(r=r_0, v=v_0, update_method='midpoint')
ball4 = Baseball(r=r_0, v=v_0, update_method='EOM')

tau = 0.5

ball1_r_x, ball1_r_y = ball1.throw(time_step=tau)
ball2_r_x, ball2_r_y = ball2.throw(time_step=tau)
ball3_r_x, ball3_r_y = ball3.throw(time_step=tau)
ball4_r_x, ball4_r_y = ball4.throw(time_step=tau)


plt.plot(ball1_r_x, ball1_r_y, 'b.',
         label=rf'{ball1.update_method}, $\tau$ = {tau:.2f}')
plt.plot(ball2_r_x, ball2_r_y, 'm.',
         label=rf'{ball2.update_method}, $\tau$ = {tau:.2f}')
plt.plot(ball3_r_x, ball3_r_y, 'g.',
         label=rf'{ball3.update_method}, $\tau$ = {tau:.2f}')
plt.plot(ball4_r_x, ball4_r_y, 'r-', label='True Trajectory')
plt.ylim(0)
plt.legend()
plt.xlabel("X (m)")
plt.ylabel("Y (m)")

plt.show()
