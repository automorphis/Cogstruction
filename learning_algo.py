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

from cog_array_stuff import get_excludes_dict, Cog_Array
from constants import ONE_SIG_PROB, EARLY_STOP_FACTOR

"""
- This singleton controls the loops of the genetic algorithm. 
- It also controls if the genetic algorithm should do a cross breed or a one-point-mutation.
- It also prints status info.
"""
class Iteration_Controller:
    def __init__(self):
        self.best = None

        self.num_restarts = None
        self.restart_count = 0

        self.max_generations = None
        self.min_generations = None
        self.max_running_total_len = None
        self.req_running_total = None
        self.curr_running_total_len = 0
        self.curr_running_total = 0
        self.generation_count = 0
        self.previous_best_improve = 0

        self.orig_pop = None
        self.curr_pop = None

        self.num_mutations = None
        self.mutation_count = 0

        self.prob_cross_breed = None
        self.cross_breed_count = 0

    """
    `num_restarts' in the number of random restarts.
    """
    def set_restart_info(self,num_restarts):
        self.num_restarts = num_restarts
        return self

    """
    Sometime between `min_generations' and `max_generations', the algorithm will begin looking for a reason to terminate 
    the generation loop. It will look at the previous `max_running_total_len' generations and if the percent improvement 
    from the original population is in excess of `req_running_total', then the the generation loop will continue. If not,
    it will cancel before it hits `max_generations'.
    """
    def set_generation_info(self,min_generations,max_generations,max_running_total_len,req_running_total):
        self.min_generations = min_generations
        self.max_generations = max_generations
        self.max_running_total_len = max_running_total_len
        self.req_running_total = req_running_total
        return self

    """
    - `num_mutations' is how many mutations to do per generation.
    - `prob_cross_breed' is the probability of calling `Cog_Array.cross_breed'; likewise `1-prob_cross_breed' is the
    probability of calling `Cog_Array.one_point_mutation'.
    """
    def set_mutation_info(self,num_mutations,prob_cross_breed):
        self.num_mutations = num_mutations
        self.prob_cross_breed = prob_cross_breed
        return self

    def set_pop(self,pop):
        self.orig_pop = copy.copy(pop)
        self.curr_pop = pop
        return self

    def mutation_loop(self):
        if self.mutation_count >= self.num_mutations:
            self.cross_breed_count = 0
            self.mutation_count = 0
            return False
        else:
            self.mutation_count+=1
            return True

    def generation_loop(self):
        if ((
                self.generation_count <= (self.max_generations - self.min_generations) * EARLY_STOP_FACTOR + self.min_generations or
                self.curr_running_total_len <= self.max_running_total_len
        ) and self.generation_count <= self.max_generations):
            if (
                self.best_improve_from_original() - self.previous_best_improve + self.curr_running_total >= self.req_running_total or
                self.generation_count <= self.min_generations
            ):
                self.curr_running_total = 0
                self.curr_running_total_len = 0

            else:
                self.curr_running_total_len += 1
                self.curr_running_total += self.best_improve_from_original() - self.previous_best_improve
            self.previous_best_improve = self.best_improve_from_original()
            self.generation_count+=1
            return True
        else:
            self.generation_count = 0
            return False

    def restart_loop(self):
        if self.restart_count < self.num_restarts:
            self.restart_count+=1
            return True
        else:
            return False

    def do_cross_breed(self):
        if random.uniform(0,1) >= self.prob_cross_breed:
            self.cross_breed_count+=1
            return True
        else:
            return False

    def print_restart_status_open(self):
        print("Restart:                              %d" % (self.restart_count-1))
        print("Pop size:                             %d" % self.orig_pop.get_size())

    def print_generation_status(self):
        if self.generation_count % 10 == 1:
            print("\tGeneration:                             %d" % (self.generation_count-1))
            if self.generation_count >= 11:
                print("\t\tMax improvement from original pop:    %1.3f%%" % ((self.best_improve_from_original()-1)*100))
                print("\t\t90th %%ile improvement from original: %1.3f%%" % ((self.perc_improve_from_original(0.90)-1)*100))
                print("\t\t50th %%ile improvement from original: %1.3f%%" % ((self.perc_improve_from_original(0.50)-1)*100))
                print(self.curr_pop.get_best()[0].str_with_abbr())
                # print("\t\t%% cross-breeds:                      %d%%\n" % int(100*self.cross_breed_count/self.mutation_count))

    def perc_improve_from_original(self,perc):
        return self.curr_pop.get_percentile(perc)[1] / self.orig_pop.get_percentile(perc)[1]

    def best_improve_from_original(self):
        return self.curr_pop.get_best()[1] / self.orig_pop.get_best()[1]

    def print_restart_status_close(self):
        if self.restart_count == 1:
            self.best = self.curr_pop.get_best()
        else:
            self.best = max([self.best, self.curr_pop.get_best()], key=lambda t: t[1])
        print("Best so far:                          %.4f" % (self.best[1]))
        print("Build rate:                           %d" % self.best[0].get_build_rate())
        print("Flaggy rate:                          %d" % self.best[0].get_flaggy_rate())
        print("Exp rate:                             %d%%" % (100*self.best[0].get_exp_rate()))

    def print_init_info(self):
        print("NUM RESTARTS:   %d" % self.num_restarts)
        print("MIN_GENERATION: %d" % self.min_generations)
        print("MAX_GENERATION: %d" % self.max_generations)

"""
- A population of `Cog_Arrays'.
"""
class Population:
    def __init__(self,arrays,obj_fxn):
        self.arrays = arrays
        self.obj_fxn = obj_fxn
        self.values = list(map(self.obj_fxn,self.arrays))
        self.is_sorted = False
        self.pop_size = len(arrays)

    def add(self,array):
        self.arrays.append(array)
        self.values.append(self.obj_fxn(array))
        self.is_sorted = False
        return array, self.values[-1]

    def cull(self,pop_size = None):
        self.sort()
        N = self.pop_size if pop_size is None else pop_size
        self.arrays = self.arrays[:N]
        self.values = self.values[:N]

    def sample(self,k=1):
        return random.sample(list(zip(self.arrays,self.values)),k)

    def get_best(self):
        return self.sort().arrays[0],self.values[0]

    def get_mean(self):
        return np.mean(self.values)

    def get_median(self):
        return self.get_percentile(0.50)

    def get_percentile(self,perc):
        self.sort()
        i = int((1-perc)*self.get_size())
        return self.arrays[i],self.values[i]

    def get_perc_std(self):
        return self.get_percentile(0.50 + ONE_SIG_PROB)[1] - self.get_median()[1]

    def get_z_score(self,other):
        return (other.get_median()[1] - self.get_median()[1])/self.get_perc_std()

    def sort(self):
        if not self.is_sorted:
            sorted_pairs = sorted(zip(self.values, self.arrays),key=lambda t:-t[0])
            self.values = [v for (v,_) in sorted_pairs]
            self.arrays = [a for (_,a) in sorted_pairs]
            self.is_sorted = True
        return self

    def get_size(self):
        return len(self.arrays)

    def __copy__(self):
        return Population([copy.copy(array) for array in self.arrays], self.obj_fxn)

"""
The genetic algorithm.
    - cogs: A collection of all cogs in the user's inventory, including characters. `cogs' excludes any characters that 
    the user intends to place on the cog shelf.
    - empties_set: An `Empties_Set' of all `Coords' that the user has not unlocked using flaggies. `empties_set' 
    includes all `Coords' where the user currently has flaggies placed.
    - flaggies: A collection of all `Coords' where the user currently has flaggies placed.
    - pop_size: The initial population size. This is also the population size after each mutation loop terminates.
    - obj_fxn: The objective function, takes input `Cog_Array' and outputs a positive `float'.
    - factor_base: A float greater than 1. A smaller float corresponds to smaller `factors' passed to 
    `Cog.update_strengths', a larger float to larger `factors'.
    - max_factor: See `Cog.update_strengths'.
    - max_multiplier: See `Cog.update_strengths'.
    - controller: A singleton of class `Iteration_Controller'.
"""
def learning_algo(
        cogs,
        empties_set,
        flaggies,
        pop_size,
        obj_fxn,
        factor_base,
        max_factor,
        max_multiplier,
        controller
):

    controller.print_init_info()

    excludes_dict = get_excludes_dict(empties_set,cogs)
    cog_array_template = Cog_Array(empties_set,None,excludes_dict).extend_spares(cogs)

    bests = []
    # with open("hello.pkl", "rb") as fh:
    #     cogs = pkl.load(fh)
    average_std_objs = {}
    for i, cog in enumerate(cogs):
        average_std_objs[cog] = cog.get_average_std_obj(cog_array_template, obj_fxn)
    # with open("hello.pkl", "wb") as fh:
    #     pkl.dump(cogs,fh)
    # raise Exception

    while controller.restart_loop():

        for cog in cogs:
            cog.instantiate_strengths(cog_array_template)

        pop = []
        for _ in range(pop_size):
            cog_array = Cog_Array(empties_set,None,excludes_dict)
            cog_array.instantiate_randomly(cogs)
            pop.append(cog_array)
        pop = Population(pop,obj_fxn)

        controller.set_pop(pop)
        controller.print_restart_status_open()
        while controller.generation_loop():
            controller.print_generation_status()
            while controller.mutation_loop():
                if controller.do_cross_breed():
                    (array1,_),(array2,_) = pop.sample(2)
                    pop.add(array1.cross_breed(array2))
                else:
                    old_array,old_obj = pop.sample(1)[0]
                    new_array,coords,old_cog = old_array.one_point_mutation()
                    new_cog = new_array[coords]
                    _,new_obj = pop.add(new_array)
                    median_diff = average_std_objs[new_cog][0] - average_std_objs[old_cog][0]
                    std_diff = np.sqrt(average_std_objs[new_cog][1]**2 + average_std_objs[old_cog][1]**2)
                    try:
                        z_score = (new_obj - old_obj- median_diff)/std_diff
                        factor = factor_base**z_score
                        old_cog.update_strength(coords, 1/factor, max_factor, max_multiplier)
                        new_cog.update_strength(coords, factor)
                        # if (
                        #         (
                        #         new_cog.__class__.__name__ == "Up_Cog" and
                        #         coords.y == 7 and
                        #         np.max(new_cog.get_strength(coords))>=0.03
                        #         ) or (
                        #
                        #     )
                        # ):
                        #     print("NEW")
                        #     print(new_array.str_with_abbr())
                        #     print("OLD")
                        #     print(old_array.str_with_abbr())
                        #     print("new_cog:                      %s" % str(new_cog).replace("\n","\t"))
                        #     print("new_obj:                      %1.5f" % new_obj)
                        #     print("old_cog:                      %s" % str(old_cog).replace("\n","\t"))
                        #     print("old_obj:                      %1.5f" % old_obj)
                        #     print("Coords:                       %s" % coords)
                        #     print("average_std_objs[new_cog][0]: %1.5f" % average_std_objs[new_cog][0])
                        #     print("average_std_objs[old_cog][0]: %1.5f" % average_std_objs[old_cog][0])
                        #     print("median_diff:                  %1.5f" % median_diff)
                        #     print("average_std_objs[new_cog][1]: %1.5f" % average_std_objs[new_cog][1])
                        #     print("average_std_objs[old_cog][1]: %1.5f" % average_std_objs[old_cog][1])
                        #     print("std_diff:                     %1.5f" % std_diff)
                        #     print("z_score:                      %1.5f" % z_score)
                        #     print("pre_factor:                   %1.5f" % pre_factor)
                        #     print("new_cog factor:               %1.5f" % factor)
                        #     print("old_cog factor:               %1.5f" % (1/factor))
                        #     print("new_cog.get_strength(coords): %1.5f" % new_cog.get_strength(coords))
                        #     print("old_cog.get_strength(coords): %1.5f" % old_cog.get_strength(coords))
                        #     print("new_cog.strengths:\n%s" % np.array2string(new_cog.strengths.transpose(),precision=5,max_line_width=120))
                        #     print("old_cog.strengths:\n%s" % np.array2string(old_cog.strengths.transpose(),precision=5,max_line_width=120))
                        # elif (
                        #     old_cog.__class__.__name__ == "Up_Cog" and
                        #     # old_cog.build_rate == 28 and
                        #     # old_cog.exp_rate == 0.07 and
                        #     # old_cog.build_rate_boost == 0.09 and
                        #     coords.y == 7 and
                        #     np.max(old_cog.get_strength(coords)) >= 0.03
                        # ):
                        #     print("OLD")
                        #     print(old_array.str_with_abbr())
                        #     print("NEW")
                        #     print(new_array.str_with_abbr())
                        #     print("old_cog:                      %s" % str(old_cog).replace("\n","\t"))
                        #     print("old_obj:                      %1.5f" % old_obj)
                        #     print("new_cog:                      %s" % str(new_cog).replace("\n","\t"))
                        #     print("new_obj:                      %1.5f" % new_obj)
                        #     print("Coords:                       %s" % coords)
                        #     print("average_std_objs[old_cog][0]: %1.5f" % average_std_objs[old_cog][0])
                        #     print("average_std_objs[new_cog][0]: %1.5f" % average_std_objs[new_cog][0])
                        #     print("median_diff:                  %1.5f" % median_diff)
                        #     print("average_std_objs[old_cog][1]: %1.5f" % average_std_objs[old_cog][1])
                        #     print("average_std_objs[new_cog][1]: %1.5f" % average_std_objs[new_cog][1])
                        #     print("std_diff:                     %1.5f" % std_diff)
                        #     print("z_score:                      %1.5f" % z_score)
                        #     print("pre_factor:                   %1.5f" % pre_factor)
                        #     print("old_cog factor:               %1.5f" % (1/factor))
                        #     print("new_cog factor:               %1.5f" % factor)
                        #     print("old_cog.get_strength(coords): %1.5f" % old_cog.get_strength(coords))
                        #     print("new_cog.get_strength(coords): %1.5f" % new_cog.get_strength(coords))
                        #     print("old_cog.strengths:\n%s" % np.array2string(old_cog.strengths.transpose(),precision=5,max_line_width=120))
                        #     print("new_cog.strengths\n%s" % np.array2string(new_cog.strengths.transpose(),precision=5,max_line_width=120))
                    except ZeroDivisionError:
                        pass

            pop.cull()
        controller.print_restart_status_close()

        bests.append(pop.get_best())
    return max(bests, key=lambda t:t[1])