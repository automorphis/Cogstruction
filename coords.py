from constants import NUM_COGS_HORI, NUM_COGS_VERT

"""
This class is just a wrapper for a tuple (x,y).
"""
class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_out_of_bounds(self):
        return self.x < 0 or self.x >= NUM_COGS_HORI or self.y < 0 or self.y >= NUM_COGS_VERT

    def __copy__(self):
        return Coords(self.x,self.y)

    def __hash__(self):
        return hash((self.x,self.y))

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coords(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)