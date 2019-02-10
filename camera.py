import math
import random

from vec3 import Vec3
from ray import Ray


class Camera:

    def __init__(self, lookfrom, lookat, vup, vfov, aspect, aperture, focus_dist):
        self.lens_radius = aperture / 2
        theta = vfov * math.pi / 180
        half_height = math.tan(theta / 2)
        half_width = aspect * half_height

        self.origin = lookfrom
        self.w = (lookfrom - lookat).unit_vector()
        self.u = vup.cross(self.w).unit_vector()
        self.v = self.w.cross(self.u)
        self.lower_left_corner = self.origin - \
            half_width * focus_dist * self.u - half_height * \
            focus_dist * self.v - focus_dist * self.w
        self.horizontal = 2 * half_width * focus_dist * self.u
        self.vertical = 2 * half_height * focus_dist * self.v

    def get_ray(self, s, t):
        rd = self.lens_radius * self.random_in_unit_disk()
        offset = self.u * rd.e[0] + self.v * rd.e[1]
        return Ray(self.origin + offset, self.lower_left_corner +
                   s * self.horizontal + t * self.vertical - self.origin - offset)

    def random_in_unit_disk(self):
        while True:
            p = Vec3(random.random(), random.random(), 0) * 2.0 - Vec3(1, 1, 0)
            if (p.dot(p) < 1.0):
                break

        return p
