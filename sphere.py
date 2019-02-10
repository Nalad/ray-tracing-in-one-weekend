import math

from hitable import Hitable


class Sphere(Hitable):

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r, t_min, t_max, rec):
        oc = r.A - self.center
        a = r.B.dot(r.B)
        b = oc.dot(r.B)
        c = oc.dot(oc) - self.radius * self.radius

        discriminant = b * b - a * c
        if (discriminant > 0):
            temp = (-b - math.sqrt(b * b - a * c)) / a
            if (temp < t_max and temp > t_min):
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                rec.material = self.material
                return True

            temp = (-b + math.sqrt(b * b - a * c)) / a
            if (temp < t_max and temp > t_min):
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                rec.material = self.material
                return True

        return False
