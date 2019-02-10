from material import Material, random_in_unit_sphere
from vec3 import Vec3
from ray import Ray


class Lambertian(Material):

    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec, scattered):
        target = rec.p + rec.normal + random_in_unit_sphere()

        scattered.A = rec.p
        scattered.B = target - rec.p

        return (True, self.albedo)
