import itertools

import numpy as np

from constants import ONE_SIG_PROB, NUM_COGS_HORI, NUM_COGS_VERT
from coords import Coords

"""
- All cogs are instances of `Cog'.
- `Cog' has two immediate subclasses, `Character' and `Boost_Cog'. Characters are instances of `Character' and cogs with
adjacency bonuses are instances of `Boost_Cog'. All other cogs are instances of `Cog', but not of any subclass of `Cog'.
- Each `Cog' has an numpy ndarray of `strengths'. This ndarray estimates how much a `Cog' prefers a given coordinate. For
example, a `Right_Cog' might have low strength for coordinates on the far right side of the `Cog_Array'.
- The `strengths' always add to 1.
- The ndarray `strengths' is always instantiated uniformly (over non-empty coords) via the method 
`Cog.instantiate_strengths(cog_array)'. 
"""
class Cog:
    def __init__(self, build_rate, flaggy_rate, exp_rate):
        self.build_rate = build_rate
        self.flaggy_rate = flaggy_rate
        self.exp_rate = exp_rate
        self.strengths = None
        self.strength_start_value = None
        self.average_obj = None
        self.std_obj = None

    def __str__(self):
        return (
             ("Type:               %s\n" % self.__class__.__name__) +
            (("Build rate:         %d\n" % self.build_rate) if self.build_rate > 0 else "") +
            (("Flaggy rate:        %d\n" % self.flaggy_rate) if self.flaggy_rate > 0 else "") +
            (("Exp rate:           %d%%\n" % (self.exp_rate*100)) if self.exp_rate > 0 else "")
        ).strip()

    """
    - Let X denote the random variable `obj_fxn(cog_array.instantiate_randomly())'. 
    - Let Y denote how much of X is due to `self'.
    - This method estimates the expectation of Y, which is the first return value.
    - It also estimates the standard deviation of Y, which is the second return value.
    """
    def get_average_std_obj(self, cog_array=None, obj_fxn=None, samples_per_coord=1):
        if not self.average_obj:
            if not cog_array or not obj_fxn:
                raise RuntimeError
            objs = []
            for coords,_ in cog_array:
                for _ in range(samples_per_coord):
                    cog_array.move_all_to_spares().move_cog_from_spares(coords,self).randomize()
                    obj1 = obj_fxn(cog_array.move_all_to_spares().move_cog_from_spares(coords, self).randomize())
                    obj2 = obj_fxn(cog_array.move_cog_to_spares(coords))
                    objs.append(obj1-obj2)
            self.average_obj = np.median(objs)
            self.std_obj = (np.percentile(objs,100*(0.50+ONE_SIG_PROB)) - np.percentile(objs,100*(0.50-ONE_SIG_PROB)))/2
        return self.average_obj, self.std_obj

    """
    - Set each non-empty coordinate strength to 1/N, where N is the total number of non-empty coords of `cog_array'.
    """
    def instantiate_strengths(self,cog_array):
        self.strengths = np.zeros((NUM_COGS_HORI,NUM_COGS_VERT))
        for coords,_ in cog_array:
            self.strengths[coords.x,coords.y] = 1.0
        self.strength_start_value = 1/np.sum(self.strengths)
        self.strengths /= np.sum(self.strengths)

    """
    - Multiply `self.strengths[coords.x,coords.y]' by `factor` and renormalize.
    - If `max_factor is not None', then `factor' is set to `max_factor' if the former is larger and likewise `factor' is
    set to `1/max_factor' if the former is smaller. This is to prevent spuriously large or small factors from dominating 
    strengths.
    - If `max_multiplier is not None', then no non-zero entry of `self.strengths' is smaller than 
    `self.strength_start_value / max_multiplier' nor larger than `self.strength_start_value * max_multiplier'. This is to
    prevent accumulations of spuriously large or small factors.
    """
    def update_strength(self,coords,factor,max_factor=None,max_multiplier=None):
        if max_factor:
            if factor > max_factor:
                factor = max_factor
            elif factor < 1/max_factor:
                factor = 1/max_factor
        if max_multiplier:
            max_str = max_multiplier * self.strength_start_value
            min_str = self.strength_start_value / max_multiplier
            stre = self.strengths[coords.x,coords.y]
            if factor*stre > max_str:
                self.strengths[coords.x, coords.y] = max_str
            elif factor*stre < min_str:
                self.strengths[coords.x, coords.y] = min_str
            else:
                self.strengths[coords.x, coords.y] = stre*factor
        else:
            self.strengths[coords.x, coords.y] *= factor
        self.strengths /= np.sum(self.strengths)

    def get_strength(self,coords):
        return self.strengths[coords.x,coords.y]

    def get_abbr(self):
        return "O"

    def get_max_oob_neighbors(self):
        return 0


class Character(Cog):
    def __init__(self, build_rate, flaggy_rate, exp_gain, name = "hahahaha"):
        super().__init__(build_rate,flaggy_rate,0.0)
        self.exp_gain = exp_gain
        self.name = name
    def get_abbr(self):
        return "C"
    def __str__(self):
        return (
            super().__str__() + "\n" +
            ("Name:               %s\n" % self.name)
        ).strip()


class Boost_Cog(Cog):
    def __init__(self, build_rate, flaggy_rate, exp_rate, build_rate_boost, flaggy_rate_boost, flaggy_speed_boost, exp_boost):
        super().__init__(build_rate, flaggy_rate, exp_rate)
        self.build_rate_boost = build_rate_boost
        self.flaggy_rate_boost = flaggy_rate_boost
        self.flaggy_speed_boost = flaggy_speed_boost
        self.exp_boost = exp_boost

    def __str__(self):
        return (
            super().__str__() + "\n" +
            (("Build rate boost:   %d%%\n" % int(self.build_rate_boost*100)) if self.build_rate_boost > 0 else "") +
            (("Flaggy rate boost:  %d%%\n" % int(self.flaggy_rate_boost*100)) if self.flaggy_rate_boost > 0 else "") +
            (("Flaggy speed boost: %d%%\n" % int(self.flaggy_speed_boost * 100)) if self.flaggy_speed_boost > 0 else "") +
            (("Exp boost:          %d%%\n" % int(self.exp_boost * 100)) if self.exp_boost > 0 else "")
        ).strip()


class Yang_Cog(Boost_Cog):

    def get_influence(self,coords):
        return map(
            lambda t: coords + Coords(t[0], t[1]),
            [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1), (-2, 0), (2, 0), (0, -2), (0, 2)]
        )

    def get_abbr(self):
        return "Y"

    def get_max_oob_neighbors(self):
        return 4


class X_Cog(Boost_Cog):
    def get_influence(self,coords):
        return map(
            lambda t: coords + Coords(t[0], t[1]),
            [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        )
    def get_abbr(self):
        return "X"

    def get_max_oob_neighbors(self):
        return 2


class Plus_Cog(Boost_Cog):
    def get_influence(self,coords):
        return map(
            lambda t: coords + Coords(t[0], t[1]),
            [(-1, 0), (1, 0), (0, -1), (0, 1)]
        )

    def get_abbr(self):
        return "+"

    def get_max_oob_neighbors(self):
        return 2


class Left_Cog(Boost_Cog):
    def get_influence(self,coords):
        return map(
            lambda t: coords + Coords(t[0], t[1]),
            [(-2, -1), (-2, 0), (-2, 1), (-1, -1), (-1, 0), (-1, 1)]
        )

    def get_abbr(self):
        return "<"

    def get_max_oob_neighbors(self):
        return 3


class Right_Cog(Boost_Cog):
    def get_influence(self,coords):
        return map(
            lambda t: coords + Coords(t[0], t[1]),
            [(2, -1), (2, 0), (2, 1), (1, -1), (1, 0), (1, 1)]
        )
    def get_abbr(self):
        return ">"

    def get_max_oob_neighbors(self):
        return 3


class Up_Cog(Boost_Cog):
    def get_influence(self,coords):
        return map(
            lambda t: coords + Coords(t[0], t[1]),
            [(-1, 1), (0, 1), (1, 1), (-1, 2), (0, 2), (1, 2)]
        )

    def get_abbr(self):
        return "^"

    def get_max_oob_neighbors(self):
        return 3


class Down_Cog(Boost_Cog):
    def get_influence(self,coords):
        return map(
            lambda t: coords + Coords(t[0], t[1]),
            [(-1, -1), (0, -1), (1, -1), (-1, -2), (0, -2), (1, -2)]
        )

    def get_abbr(self):
        return "v"

    def get_max_oob_neighbors(self):
        return 3


class Row_Cog(Boost_Cog):
    def get_influence(self,coords):
        return map(
            lambda t: coords + Coords(t[0],t[1]),
            [(x,0) for x in itertools.chain(range(-NUM_COGS_HORI,0),range(1,NUM_COGS_HORI+1))]
        )

    def get_abbr(self):
        return "-"

    def get_max_oob_neighbors(self):
        return NUM_COGS_HORI


class Col_Cog(Boost_Cog):
    def get_influence(self,coords):
        return map(
            lambda t: coords + Coords(t[0],t[1]),
            [(0,y) for y in itertools.chain(range(-NUM_COGS_VERT,0),range(1,NUM_COGS_VERT+1))]
        )

    def get_abbr(self):
        return "|"

    def get_max_oob_neighbors(self):
        return NUM_COGS_VERT


class Omni_Cog(Boost_Cog):
    def get_influence(self,coords):
        return map(
            lambda t: coords + Coords(t[0], t[1]),
            [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        )
    def get_abbr(self):
        return "*"

    def get_max_oob_neighbors(self):
        return 2