class Particle():
    def __init__(self, r, v, a, m=1):
        self.r = r
        self.v = v
        self.a = a
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
        else:
            self.step = None
            print("invalid")

    def _euler_update(self, r, v, a, time_step):
        r_next = r + time_step * v
        v_next = v + time_step * a
        a_next = self._f(r_next, v_next)

        return r_next, v_next, a_next

    def _euler_cromer_update(self, r, v, a, time_step):
        v_next = v + time_step * a
        r_next = r + time_step * v_next
        a_next = self._f(r_next, v_next)

        return r_next, v_next, a_next

    def _midpoint_update(self, r, v, a, time_step):
        v_next = v + time_step * a
        r_next = r + time_step * v + \
            0.5 * (time_step ** 2) * a
        a_next = self._f(r_next, v_next)

        return r_next, v_next, a_next

    # position verlet
    # https://young.physics.ucsc.edu/115/leapfrog.pdf
    def _verlet_update(self, r, v, a, time_step):
        r_half_step = r + 0.5 * time_step * v
        a_next = self._f(r_half_step, v)
        v_next = v + time_step * a_next
        r_next = r_half_step + 0.5 * time_step * v_next

        return r_next, v_next, a_next
