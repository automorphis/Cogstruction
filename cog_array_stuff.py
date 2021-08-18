"""
Cogstruction: Optimizing cog arrays in Legends of Idleon
    Copyright (C) 2021 Michael P. Lane

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

import copy
import random
import numpy as np

from cog_types import Boost_Cog
from constants import NUM_COGS_HORI, NUM_COGS_VERT, TOTAL_COORDS
from coords import Coords

"""
- `Empties_Set.empties' should be a `set'.
- `Empties_Set.coords_list' is a list of all the non-empty coords in the array.
- There should be one `Empties_Set' per cog array template.
"""
class Empties_Set:
    def __init__(self,empties):
        self.empties = empties
        self.coords_list = []
        for y in range(NUM_COGS_VERT):
            for x in range(NUM_COGS_HORI):
                coords = Coords(x, y)
                if coords not in self.empties:
                    self.coords_list.append(coords)

    def __contains__(self, coords):
        return coords in self.empties

"""
- `excludes_dict[type(cog)]' is a `set' of all coordinates where `cog' should not be placed.
- For example, if `cog' is of type `Up_Cog', then `excludes_dict[type(cog)]' should contain all coords on the top row of
the array.
- This dict is not necessary for the genetic algorithm to find an optimal array. It merely improves the convergence rate. 
"""
def get_excludes_dict(empties_set, cogs):
    cog_array = Cog_Array(empties_set)
    excludes_dict = {}
    for cog in cogs:
        if type(cog) not in excludes_dict and isinstance(cog, Boost_Cog):
            excludes_dict[type(cog)] = set()
            for coords in Coords_Iter(cog_array):
                num_oob_neighbors = sum((adj_coords.is_out_of_bounds()) for adj_coords in cog.get_influence(coords))
                if num_oob_neighbors > cog.get_max_oob_neighbors():
                    excludes_dict[type(cog)].add(coords)
    return excludes_dict

"""
A cog array consists of:
- array: A `numpy.ndarray' of `Cogs' placed on the cog array.
- empties_set: An `Empties_Set' of `Coords' that the user has not yet unlocked using flaggies. There is only one per
  cog array template.
- flaggies: A collection of `Coords' where the user currently has flaggies placed.
- spares: A spare collection of `Cogs'.
- excludes_dict: A `dict` of `sets'. Each key of `excludes_dict' is a `Cog` subtype. Each `set' consists of `Coords' where
`Cogs' should not be placed. There is only one per cog array template.
"""
class Cog_Array:
    def __init__(self, empties_set = None, flaggies = None, excludes_dict = None):
        self.array = np.empty((NUM_COGS_HORI, NUM_COGS_VERT), dtype=np.dtype(object))
        self.empties_set = empties_set if empties_set is not None else Empties_Set(set())
        self.flaggies = set(flaggies) if flaggies is not None else set()
        self.spares = []
        self.build_rate = self.flaggy_rate = self.total_exp_mult = None
        self.excludes_dict = excludes_dict if excludes_dict is not None else {}

    """
    - Randomly places cogs on the cog array. Any leftover cogs are added to `self.spares'.
    - If `cog in cogs', then this method will try to place `cog' where `self.excludes(coords, cog)' is `False'. However,
    depending on the shape of the cog array and the given `cogs', this will not always be possible, but the method will 
    always return.
    """
    def instantiate_randomly(self,cogs):
        self.extend_spares(cogs)
        for coords in Coords_Iter(self,True):
            self.move_random_cog_from_spares(coords)
        return self

    """
    Mostly used for copying.
    """
    def instantiate_from_array(self,array):
        self.array = array
        cogs = [cog for _,cog in self]
        return self

    """
    - Randomly place cogs from `self.spares' on non-empty coords where `self.is_occupied(coords)' is `False'.
    - This method will not remove or replace cogs that have already been placed on the cog array.
    """
    def randomize(self):
        self._reset_rates()
        for coords in Coords_Iter(self,True):
            if not self.is_occupied(coords):
                self.move_random_cog_from_spares(coords)
        return self

    """
    Place a cog by coords.
    """
    def __setitem__(self, coords, cog):
        if coords.is_out_of_bounds() or coords in self.empties_set:
            raise Exception
        self.array[coords.x, coords.y] = cog
        self._reset_rates()

    """
    Get a cog by coords.
    """
    def __getitem__(self, coords):
        if coords.is_out_of_bounds() or coords in self.empties_set:
            return None
        return self.array[coords.x, coords.y]

    def __str__(self):
        ret = ""
        line = ""
        i = 1
        for coords in Coords_Iter():
            if coords.x == 0 and coords.y > 0:
                ret = line + "\n\n" + ret
                line = ""
            if coords in self.empties_set:
                line += "E   "
            elif not self.is_occupied(coords):
                line += "e   "
            else:
                line += str(i) + " "*(3-int(np.log10(i)))
                i+=1
        ret = line + "\n\n" + ret
        ret = self.str_with_abbr() + "\n\n\n" + ret
        for i,(coords,cog) in enumerate(self):
            ret += (
                ("Cog %d\n" %(i+1)) +
                ("Coords:            %s\n" %coords) +
                (str(cog)) +
                "\n\n\n"
            )
        for cog in self.spares:
            ret += ("Spare Cog\n"  + str(cog) + "\n\n\n")
        return ret.strip()

    def __iter__(self):
        return ((coords,self[coords]) for coords in Coords_Iter(self))

    def __copy__(self):
        cog_array = Cog_Array(self.empties_set, None, self.excludes_dict)
        cog_array.instantiate_from_array(copy.copy(self.array))
        cog_array.extend_spares(copy.copy(self.spares))
        return cog_array

    "Call it and see =)"
    def str_with_abbr(self):
        ret = ""
        line = ""
        for coords in Coords_Iter():
            if coords.x == 0 and coords.y > 0:
                ret = line + "\n\n" + ret
                line = ""
            if coords in self.empties_set:
                line+= "E   "
            else:
                if not self.is_occupied(coords):
                    line += "E   "
                else:
                    cog = self[coords]
                    line += cog.get_abbr() + "   "
        return line + "\n\n" + ret

    """
    If `self.excludes(coords,cog)' is true, then `cog' should not be placed at `coords'. It sometimes must be though,
    depending on the shape of the array and the cogs used to initialize it.
    """
    def excludes(self,coords,cog):
        if not isinstance(cog, Boost_Cog) or type(cog) not in self.excludes_dict:
            return False
        return coords in self.excludes_dict[type(cog)]

    """
    Only returns non-empty coords.
    """
    def get_random_coords(self):
        for coords in Coords_Iter(self,True,1):
            return coords

    """
    - This method blends two input `Cog_Arrays'. The blended `Cog_Array' is called `child'. 
    - For each non-empty `coord' of `self', the cog `child[coord]' will usually be either `self[coord]' or 'other[coord]'.
    - The decision of whether `child[coord]' is equal to either `self[coord]' or 'other[coord]' is made randomly. However,
    the odds are not 1:1. The exact probability is based off four floats
        > `self[coords].get_strength(coords)'
        > `other[coords].get_strength(coords)'
        > `self[coords].get_average_std_obj()[0]' and
        > `other[coords].get_average_std_obj()[0]'.
    - Under certain circumstances, `child[coord]' will be neither `self[coord]' nor `other[coord]'. This will happen if 
    both of these cogs have already been placed somewhere else in `child'. 
    """
    def cross_breed(self,other):
        child = copy.copy(self)
        child.move_all_to_spares()
        for coords in Coords_Iter(self, True):
            self_strength = self[coords].get_strength(coords)*self[coords].get_average_std_obj()[0]
            other_strength = other[coords].get_strength(coords)*other[coords].get_average_std_obj()[0]
            self_weight = self_strength/(self_strength + other_strength)
            if random.uniform(0,1) <= self_weight:
                if self[coords] in child.spares:
                    child.move_cog_from_spares(coords, self[coords])
                elif other[coords] in child.spares:
                    child.move_cog_from_spares(coords, other[coords])
                else:
                    child.move_random_cog_from_spares(coords)
            else:
                if other[coords] in child.spares:
                    child.move_cog_from_spares(coords, other[coords])
                elif self[coords] in child.spares:
                    child.move_cog_from_spares(coords, self[coords])
                else:
                    child.move_random_cog_from_spares(coords)
        return child

    """
    - This method produces a new `Cog_Array' called `child'. 
    - First, randomly choose a cog placed in `self'. Then, choose a random cog from `self.spares'. Switch these two.
    """
    def one_point_mutation(self):
        child = copy.copy(self)
        coords = self.get_random_coords()
        old_cog = child[coords]
        child[coords] = None
        child.move_random_cog_from_spares(coords)
        child.add_spare(old_cog)
        return child,coords,old_cog

    """
    - Move `cog' from `self.spares' to `coords'.
    - If `coords' is already occupied by a different cog, then move that cog to `self.spares' before replacing with `cog'.
    - This method ignores the return value of `self.excludes(coords, cog)'.
    """
    def move_cog_from_spares(self, coords, cog):
        if cog not in self.spares:
            raise Exception
        self.spares.remove(cog)
        self.move_cog_to_spares(coords)
        self[coords] = cog
        self._reset_rates()
        return self

    """
    - Move a random cog from `self.spares' to `coords' of `self'. 
    - If `coords' is already occupied by a different cog, then move that cog to `self.spares' before replacing with the 
    new random cog.
    - This method will attempt to choose a `cog' such that `self.excludes(coords,cog)' is `False', whenever this is 
    possible. 
    """
    def move_random_cog_from_spares(self,coords):
        attempts = 0
        while attempts < len(self.spares):
            cog = random.sample(self.spares, 1)[0]
            if not self.excludes(coords,cog):
                break
            attempts += 1
        else:
            cog = random.sample(self.spares, 1)[0]
        self.move_cog_from_spares(coords,cog)
        return cog

    def move_cog_to_spares(self,coords):
        if self.is_occupied(coords):
            self.add_spare(self[coords])
            self.array[coords.x,coords.y] = None
            self._reset_rates()
        return self

    def move_all_to_spares(self):
        for coords in Coords_Iter(self):
            self.move_cog_to_spares(coords)
        return self

    def add_spare(self,cog):
        self.spares.append(cog)
        return self

    def extend_spares(self,cogs):
        for cog in cogs:
            self.add_spare(cog)
        return self

    def is_occupied(self,coords):
        return self[coords] is not None

    def is_flaggy(self,coords):
        return coords in self.flaggies

    def _reset_rates(self):
        self.build_rate = self.flaggy_rate = self.total_exp_mult = None

    """
    Calculate the total build rate of the array.
    """
    def get_build_rate(self):
        if self.build_rate is None:
            total = 0
            for coords, cog in self:
                if self.is_occupied(coords):
                    if isinstance(cog, Boost_Cog):
                        rate = cog.build_rate_boost
                        if rate > 0:
                            for adj_cog_coords in cog.get_influence(coords):
                                if self.is_occupied(adj_cog_coords):
                                    adj_cog = self[adj_cog_coords]
                                    total += adj_cog.build_rate * rate
                    total += cog.build_rate
            self.build_rate = total
        return self.build_rate

    """
    - Calculate the total flaggy rate.
    - Due to a bug in Lava's implementation, the ''player exp'' adjacency bonuses give a multiplicative bonus to adjacent
    flaggy speeds.
    - The method below accounts for that bug. (TODO)
    - The ''flaggy speed'' adjacency bonus does nothing, which is likewise a bug.
    """
    def get_flaggy_rate(self):
        if self.flaggy_rate is None:
            total_rate = total_speed = 0
            for coords, cog in self:
                if self.is_occupied(coords):
                    if isinstance(cog, Boost_Cog):
                        rate = cog.flaggy_rate_boost
                        if rate > 0:
                            for adj_cog_coords in cog.get_influence(coords):
                                if self.is_occupied(adj_cog_coords):
                                    adj_cog = self[adj_cog_coords]
                                    total_rate += adj_cog.flaggy_rate * rate
                        speed = cog.flaggy_speed_boost
                        if speed > 0:
                            for adj_cog_coords in cog.get_influence(coords):
                                if self.is_flaggy(adj_cog_coords):
                                    total_speed += speed/len(self.flaggies)
                    total_rate += cog.flaggy_rate
            self.flaggy_rate = total_rate*(1+total_speed)
        return self.flaggy_rate

    """
    - Calculate the total exp multiplier.
    - Due to a bug in Lava's implementation, the ''player exp'' adjacency bonuses give a multiplicative bonus to adjacent
    flaggy speeds.
    """
    def get_total_exp_mult(self):
        if self.total_exp_mult is None:
            self.total_exp_mult = sum((cog.exp_mult if self.is_occupied(coords) else 0.0) for coords, cog in self)
        # if self.exp_rate is None:
        #     total_rate = sum((cog.exp_rate if self.is_occupied(coords) else 0.0) for coords,cog in self)
        #     total_bonus = 0.0
        #     for coords, cog in self:
        #         bonus = cog.exp_boost
        #         if bonus > 0:
        #             for adj_coords in cog.get_influence(coords):
        #                 if self.is_occupied(adj_coords):
        #                     cog = self[adj_coords]
        #                     if isinstance(cog, Character):
        #                         total_bonus += cog.exp_gain * bonus
        #     self.exp_rate = total_rate + total_bonus
        return self.total_exp_mult

    """
    - A convex combination (i.e. weighted average) of the build, flaggy, and exp rates. 
    - ''obj_fnx'' is an abbreviation of ''objective function''.
    """
    def standard_obj_fxn(self,build_weight,flaggy_weight,exp_weight):
        return self.get_build_rate() * build_weight + self.get_flaggy_rate() * flaggy_weight + self.get_total_exp_mult() * exp_weight

"""
Iterates through all the non-empty coordinates of an input `Cog_Array'.
"""
class Coords_Iter:
    def __init__(self, cog_array = None, randomize_order = False, length =TOTAL_COORDS):
        self.cog_array = cog_array if cog_array is not None else Cog_Array()
        self.randomize_order = randomize_order
        self.curr_index = None
        self.coords_list = self.cog_array.empties_set.coords_list[:length]

    def __iter__(self):
        self.curr_index = 0
        if self.randomize_order:
            self.coords_list = random.sample(self.coords_list, len(self.coords_list))
        return self

    def __next__(self):
        if self.curr_index >= len(self.coords_list):
            raise StopIteration
        next_coords = self.coords_list[self.curr_index]
        self.curr_index += 1
        return next_coords