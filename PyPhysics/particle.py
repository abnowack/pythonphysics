from copy import deepcopy
from .update_methods import *


class Point1D:
    def __init__(self, x=0):
        self.x = x

    def __str__(self):
        return f"<Point1D: x = {self.x:.3f}>"

    def __add__(self, other):
        temp = Point1D()
        if isinstance(other, Point1D):
            temp.x = self.x + other.x
            return temp
        if isinstance(other, float) or isinstance(other, int):
            temp.x = self.x + other
            return temp

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        temp = Point1D()
        if isinstance(other, Point1D):
            temp.x = self.x - other.x
            return temp
        if isinstance(other, float) or isinstance(other, int):
            temp.x = self.x - other
            return temp

    def __rsub__(self, other):
        return self.__sub__(other)

    def __neg__(self):
        temp = Point1D()
        temp.x = self.x * -1
        return temp

    def __mul__(self, other):
        temp = Point1D()
        if isinstance(other, Point1D):
            temp.x = self.x * other.x
            return temp
        if isinstance(other, float) or isinstance(other, int):
            temp.x = self.x * other
            return temp

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        temp = Point1D()
        if isinstance(other, Point1D):
            temp.x = self.x / other.x
            return temp
        if isinstance(other, float) or isinstance(other, int):
            temp.x = self.x / other
            return temp


class Point2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"<Point2D: x = {self.x:.3f}, y = {self.y:.3f}>"

    def __add__(self, other):
        temp = Point2D()
        if isinstance(other, Point2D):
            temp.x = self.x + other.x
            temp.y = self.y + other.y
            return temp
        if isinstance(other, float) or isinstance(other, int):
            temp.x = self.x + other
            temp.y = self.y + other
            return temp

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        temp = Point2D()
        if isinstance(other, Point2D):
            temp.x = self.x - other.x
            temp.y = self.y - other.y
            return temp
        if isinstance(other, float) or isinstance(other, int):
            temp.x = self.x - other
            temp.y = self.y - other
            return temp

    def __rsub__(self, other):
        return self.__sub__(other)

    def __neg__(self):
        temp = Point2D()
        temp.x = self.x * -1
        temp.y = self.y * -1
        return temp

    def __mul__(self, other):
        temp = Point2D()
        if isinstance(other, Point2D):
            temp.x = self.x * other.x
            temp.y = self.y * other.y
            return temp
        if isinstance(other, float) or isinstance(other, int):
            temp.x = self.x * other
            temp.y = self.y * other
            return temp

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        temp = Point2D()
        if isinstance(other, Point2D):
            temp.x = self.x / other.x
            temp.y = self.y / other.y
            return temp
        if isinstance(other, float) or isinstance(other, int):
            temp.x = self.x / other
            temp.y = self.y / other
            return temp

    # def __rdiv__(self, other):
    #     return self.__div__(other)


class Particle1D(Point1D):
    def __init__(self, r=Point1D(0), v=Point1D(0), t=0, m=1, update_method='euler', force=None):
        self.set_initial_coordinates(r, v, t)
        self.m = m
        self.a = Point1D(0)

        self.force = force
        self.set_update_method(update_method)

    def set_update_method(self, method='euler'):
        self.update_method = method
        if method == 'euler':
            self._update_func = lambda tau: euler_update(
                self.r, self.v, self.a, tau)
        elif method == 'euler-cromer':
            self._update_func = lambda tau: euler_cromer_update(
                self.r, self.v, self.a, tau)
        elif method == 'midpoint':
            self._update_func = lambda tau: midpoint_update(
                self.r, self.v, self.a, tau)
        elif method == 'EOM' and hasattr(self, 'force') and hasattr(self.force, 'EOM'):
            self._update_func = lambda tau: getattr(
                self.force, 'EOM')(self, tau)
        elif method == 'EOM' and (not hasattr(self, 'force') or not hasattr(self.force, 'EOM')):
            print("No EOM given!")

    def update(self, time_step=0):
        self.a = (1 / self.m) * self.force.calc_a(self)
        self.r, self.v = self._update_func(time_step)

        self.t += time_step

    def set_initial_coordinates(self, r=Point1D(0), v=Point1D(0), t=0):
        self.r = r
        self.v = v
        self.t = t

        self.r_0 = deepcopy(self.r)
        self.v_0 = deepcopy(self.v)
        self.t_0 = deepcopy(self.t)


class Particle2D(Point2D):
    def __init__(self, r=Point2D(0, 0), v=Point2D(0, 0), t=0, m=1, update_method='euler', force=None):
        self.set_initial_coordinates(r, v, t)
        self.m = m
        self.a = Point2D(0, 0)

        self.force = force
        self.set_update_method(update_method)

    def set_update_method(self, method='euler'):
        self.update_method = method
        if method == 'euler':
            self._update_func = lambda tau: euler_update(
                self.r, self.v, self.a, tau)
        elif method == 'euler-cromer':
            self._update_func = lambda tau: euler_cromer_update(
                self.r, self.v, self.a, tau)
        elif method == 'midpoint':
            self._update_func = lambda tau: midpoint_update(
                self.r, self.v, self.a, tau)
        elif method == 'EOM' and hasattr(self, 'force') and hasattr(self.force, 'EOM'):
            self._update_func = lambda tau: getattr(
                self.force, 'EOM')(self, tau)
        elif method == 'EOM' and (not hasattr(self, 'force') or not hasattr(self.force, 'EOM')):
            print("No EOM given!")

    def update(self, time_step=0):
        self.a = (1 / self.m) * self.force.calc_a(self)
        self.r, self.v = self._update_func(time_step)

        self.t += time_step

    def set_initial_coordinates(self, r=Point2D(0, 0), v=Point2D(0, 0), t=0):
        self.r = r
        self.v = v
        self.t = t

        self.r_0 = deepcopy(self.r)
        self.v_0 = deepcopy(self.v)
        self.t_0 = deepcopy(self.t)


class Force1D():
    def calc_force(self, particle):
        return Point1D(0)

    def calc_a(self, particle):
        return self.calc_force(particle) / particle.m


class Force2D():
    def calc_force(self, particle):
        return Point2D(0, 0)

    def calc_a(self, particle):
        return self.calc_force(particle) / particle.m
