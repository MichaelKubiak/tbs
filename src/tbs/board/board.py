class Position(object):
    """
    An object denoting a space-time position on a board
    """

    _x: int
    _y: int
    _t: int

    def __init__(self, x, y, t=None):
        self._x = x
        self._y = y
        self._t = t

    def x(self):
        return self._x

    def y(self):
        return self._y

    def t(self):
        return self._t

    def pos(self):
        return self.x(), self.y()
