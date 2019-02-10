from material import Material
from material import random_in_unit_sphere


class Metal(Material):

    def __init__(self, albedo, fuzz):
        self.albedo = albedo

        if (fuzz < 1):
            self.fuzz = fuzz
        else:
            self.fuzz = 1

    def scatter(self, r_in, rec, scattered):
        reflected = self.reflect(r_in.B.unit_vector(), rec.normal)

        scattered.A = rec.p
        scattered.B = reflected + self.fuzz * random_in_unit_sphere()

        return (scattered.B.dot(rec.normal) > 0, self.albedo)

    def reflect(self, v, n):
        return v - 2 * v.dot(n) * n
