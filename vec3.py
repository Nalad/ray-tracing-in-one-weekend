import math


class Vec3:
    def __init__(self, e0, e1, e2):
        self.e = list((e0, e1, e2))

        self.length = math.sqrt(e0 ** 2 + e1 ** 2 + e2 ** 2)

    def __pos__(self):
        return self

    def __neg__(self):
        return Vec3(-self.e[0], -self.e[1], -self.e[2])

    def __getitem__(self, key):
        return self.e[key]

    def __add__(self, other):
        return Vec3(self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])

    def __sub__(self, other):
        return Vec3(self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])

    def __mul__(self, other):
        return Vec3(self.e[0] * other, self.e[1] * other, self.e[2] * other)

    def mul(self, other):
        return Vec3(self.e[0] * other.e[0], self.e[1] * other.e[1], self.e[2] * other.e[2])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Vec3(self.e[0] / other, self.e[1] / other, self.e[2] / other)

    def squared_length(self):
        return self.e[0]**2 + self.e[1]**2 + self.e[2]**2

    def dot(self, other):
        return self.e[0] * other.e[0] + \
            self.e[1] * other.e[1] + \
            self.e[2] * other.e[2]

    def cross(self, other):
        return Vec3((self.e[1] * other.e[2] - self.e[2] * other.e[1]),
                    (-(self.e[0] * other.e[2] - self.e[2] * other.e[0])),
                    (self.e[0] * other.e[1] - self.e[1] * other.e[0]))

    def unit_vector(self):
        return Vec3(self.e[0] / self.length, self.e[1] / self.length, self.e[2] / self.length)

    def __str__(self):
        return f"({self.e[0]}, {self.e[1]}, {self.e[2]})"
