from hitable import Hitable
from hit_record import HitRecord
from vec3 import Vec3


class HitableList(Hitable):
    def __init__(self, hitables):
        self.hitables = hitables

    def hit(self, r, t_min, t_max, rec):
        hit_anything = False
        closest_hit_so_far = t_max
        tmp_rec = HitRecord(t=0, p=Vec3(0, 0, 0),
                            normal=Vec3(0, 0, 0), material=None)

        for hitable in self.hitables:
            if hitable.hit(r, t_min, closest_hit_so_far, tmp_rec):
                hit_anything = True
                closest_hit_so_far = tmp_rec.t
                rec.t = tmp_rec.t
                rec.p = tmp_rec.p
                rec.normal = tmp_rec.normal
                rec.material = tmp_rec.material

        return hit_anything
