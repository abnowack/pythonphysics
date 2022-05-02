# Note that I found that Euler-Cromer and Verlet are equivalent for position,
# however there is a diference in terms of the velocities
# https://www.physics.purdue.edu/~giordano/new_erratum/new_erratum.html


class Particle():
    def __init__(self, r, v, m=1):
        self.r = r
        self.v = v
        self.m = m


class ODEIntegrator:
    def __init__(self, f, method='euler'):
        self._f = f

        self.set_method(method)

    def set_method(self, method='euler'):
        if method == 'euler':
            self.step = self._euler_update
        elif method == 'euler-cromer':
            self.step = self._euler_cromer_update
        elif method == 'midpoint':
            self.step = self._midpoint_update
        elif method == 'verlet':
            self.step = self._verlet_update
        elif method == 'rk4':
            self.step = self._rk4_update
        else:
            self.step = None
            print("invalid")

    def _euler_update(self, r, v, time_step):
        a = self._f(r, v)
        r_next = r + time_step * v
        v_next = v + time_step * a

        return r_next, v_next

    def _euler_cromer_update(self, r, v, time_step):
        a = self._f(r, v)
        v_next = v + time_step * a
        r_next = r + time_step * v_next

        return r_next, v_next

    def _midpoint_update(self, r, v, time_step):
        a = self._f(r, v)
        v_next = v + time_step * a
        r_next = r + time_step * v + \
            0.5 * (time_step ** 2) * a

        return r_next, v_next

    # position verlet
    # https://young.physics.ucsc.edu/115/leapfrog.pdf
    def _verlet_update(self, r, v, time_step):
        r_half_step = r + 0.5 * time_step * v
        a = self._f(r_half_step, v)
        v_next = v + time_step * a
        r_next = r_half_step + 0.5 * time_step * v_next

        return r_next, v_next

    # RK4 is for solving a 1st order ODE,
    # Here is a version for the 2nd order
    # https://www.engr.colostate.edu/~thompson/hPage/CourseMat/Tutorials/CompMethods/Rungekutta.pdf
    def _rk4_update(self, r, v, time_step):
        def rk4_step(x, xdot_f, time_step):


        f1 = self._f(r, v)
        g1 = v

        f2 = self._f(r + g1 * time_step / 2, v + f1 * time_step / 2)
        g2 = v + f1 * time_step / 2

        f3 = self._f(r + g2 * time_step / 2, v + f2 * time_step / 2)
        g3 = v + f2 * time_step / 2

        f4 = self._f(r + g3 * time_step, v + f3 * time_step)
        g4 = v + f3 * time_step

        v_next = v + (f1 + 2 * f2 + 2 * f3 + f4) * (time_step / 6)
        r_next = r + v * time_step + (f1 + f2 + f3) * (time_step * time_step / 6)

        return r_next, v_next
