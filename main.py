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

import random
import numpy as np

from learning_algo import Iteration_Controller,learning_algo
from file_readers import read_cog_datas,read_empties_datas,read_flaggies_datas
from cog_factory import cog_factory
from cog_array_stuff import Empties_Set

if __name__ == "__main__":
    random.seed(133742069)

    inv_build_weight = 7000.0
    inv_flaggy_weight = 2000.0
    inv_exp_weight = 3.0
    pop_size = 2000
    num_restarts = 1
    prob_cross_breed = 0.5
    prob_one_point_mutation = 0.25
    prob_two_point_mutation = 0.25
    num_mutations = 800
    factor_base = 2
    max_factor = 4
    max_multiplier = 16
    req_running_total = 0.01
    max_running_total_len = 10
    min_generations = 100
    max_generations = 400

    cog_datas_filename = "cog_datas.csv"
    empties_datas_filename = "empties_datas.csv"
    flaggies_datas_filename = "flaggies_datas.csv"
    output_filename = "output.txt"

    A = np.array([
        [1.,1.,1.],
        [inv_build_weight,-inv_flaggy_weight,0.],
        [0.,inv_flaggy_weight,-inv_exp_weight]
    ])
    b = np.array([1.,0.,0.])
    build_weight, flaggy_weight, exp_weight = np.linalg.solve(A, b)

    controller = (Iteration_Controller()
        .set_restart_info(num_restarts)
        .set_generation_info(min_generations,max_generations,max_running_total_len,req_running_total)
        .set_mutation_info(num_mutations)
        .set_breeding_scheme_info(prob_cross_breed,prob_one_point_mutation,prob_two_point_mutation)
    )
    cog_datas = read_cog_datas(cog_datas_filename)
    empties = read_empties_datas(empties_datas_filename)
    empties_set = Empties_Set(empties)
    cogs = cog_factory(cog_datas)

    best = learning_algo(
        cogs,
        empties_set,
        set(),
        pop_size,
        lambda cog: cog.standard_obj_fxn(build_weight,flaggy_weight,exp_weight),
        factor_base,
        max_factor,
        max_multiplier,
        controller
    )

    print("Writing best cog array to %s" % output_filename)
    with open(output_filename, "w") as fh:
        fh.write(str(best[0]))