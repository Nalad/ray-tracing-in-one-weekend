import math
import random

from material import Material
from vec3 import Vec3
from ray import Ray


class Dielectric(Material):

    albedo = Vec3(1.0, 1.0, 1.0)

    def __init__(self, ref_idx):
        self.ref_idx = ref_idx

    def reflect(self, v, n):
        return v - 2 * v.dot(n) * n

    def refract(self, v, n, ni_over_nt):
        uv = v.unit_vector()
        dt = uv.dot(n)
        discriminant = 1.0 - ni_over_nt * ni_over_nt * (1 - dt * dt)
        if (discriminant > 0):
            return True, ni_over_nt * (uv - n * dt) - n * math.sqrt(discriminant)
        else:
            return False, None

    def schlick(self, cosine, ref_idx):
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0
        return r0 + (1 - r0) * math.pow(1 - cosine, 5)

    def scatter(self, r_in, rec, scattered):
        reflected = self.reflect(r_in.B, rec.normal)

        if (r_in.B.dot(rec.normal) > 0):
            outward_normal = -rec.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * r_in.B.dot(rec.normal) / r_in.B.length
        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0 / self.ref_idx
            cosine = - r_in.B.dot(rec.normal) / r_in.B.length

        t = self.refract(r_in.B, outward_normal, ni_over_nt)
        if (t[0]):
            reflect_prob = self.schlick(cosine, self.ref_idx)
        else:
            scattered.A = rec.p
            scattered.B = reflected
            reflect_prob = 1.0

        if (random.random() < reflect_prob):
            scattered.A = rec.p
            scattered.B = reflected
        else:
            scattered.A = rec.p
            scattered.B = t[1]

        return (True, self.albedo)
