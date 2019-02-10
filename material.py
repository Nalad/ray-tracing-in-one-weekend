import abc
import random

from vec3 import Vec3


class Material(abc.ABC):

    @abc.abstractmethod
    def scatter(self, r_in, rec, attenuation, scattered):
        pass


def random_in_unit_sphere():
    p = None
    while True:
        p = 2.0 * Vec3(random.random(), random.random(),
                       random.random()) - Vec3(1, 1, 1)
        if (p.squared_length() < 1.0):
            break

    return p
