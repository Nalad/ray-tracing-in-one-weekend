class Ray:

    def __init__(self, a, b):
        self.A = a
        self.B = b

    def origin(self):
        return self.A

    def direction(self):
        return self.B

    def point_at_parameter(self, t):
        return self.A + t * self.B

    def __str__(self):
        return f"{self.A}, {self.B}"
