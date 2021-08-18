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
        .set_mutation_info(num_mutations,prob_cross_breed)
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

    print(str(best[0]))