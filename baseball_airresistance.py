from PyPhysics import *

import matplotlib.pyplot as plt


class GravityWithAirResistance(Force2D):
    g = 9.8

    def calc_force(self, particle):
        gravity = Point2D(0, - particle.m * self.g)
        air_resistance = particle.drag_coefficient * -particle.v
        return gravity + air_resistance


class Baseball(Particle2D):
    def __init__(self, r=Point2D(), v=Point2D(), update_method='euler', drag_coefficient=1):
        super().__init__(r, v, update_method=update_method, force=GravityWithAirResistance())

        self.drag_coefficient = drag_coefficient

    def throw(self, time_step=0):
        r_x, r_y = [self.r.x], [self.r.y]

        while self.r.y >= 0:

            self.update(time_step)
            r_x.append(self.r.x)
            r_y.append(self.r.y)

        return r_x, r_y


r_0 = Point2D(0, 0)
v_0 = Point2D(50, 50)

ball1 = Baseball(r=r_0, v=v_0, update_method='midpoint', drag_coefficient=1)
ball2 = Baseball(r=r_0, v=v_0, update_method='midpoint', drag_coefficient=0.5)
ball3 = Baseball(r=r_0, v=v_0, update_method='midpoint', drag_coefficient=1.5)

tau = 0.05

ball1_r_x, ball1_r_y = ball1.throw(time_step=tau)
ball2_r_x, ball2_r_y = ball2.throw(time_step=tau)
ball3_r_x, ball3_r_y = ball3.throw(time_step=tau)


plt.plot(ball1_r_x, ball1_r_y, 'b.',
         label=rf'{ball1.update_method}, $\tau$ = {tau:.2f}')
plt.plot(ball2_r_x, ball2_r_y, 'm.',
         label=rf'{ball2.update_method}, $\tau$ = {tau:.2f}')
plt.plot(ball3_r_x, ball3_r_y, 'g.',
         label=rf'{ball3.update_method}, $\tau$ = {tau:.2f}')
plt.ylim(0)
plt.legend()
plt.xlabel("X (m)")
plt.ylabel("Y (m)")

plt.show()
