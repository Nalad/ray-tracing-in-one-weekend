class HitRecord:

    def __init__(self, t, p, normal, material):
        self.t = t
        self.p = p
        self.normal = normal
        self.material = material

    def __str__(self):
        return "{}, {}, {}, {}".format(self.t, self.p, self.normal, self.material)
