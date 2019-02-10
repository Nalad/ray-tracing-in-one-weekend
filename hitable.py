import abc


class Hitable(abc.ABC):

    @abc.abstractmethod
    def hit(self, r, t_min, t_max, rec):
        pass
