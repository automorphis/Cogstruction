import unittest

from cog_array_stuff import Cog_Array, Empties_Set
from file_readers import read_cog_datas, read_empties_datas


class Test_Cog_Array(unittest.TestCase):

    def setUp(self):
        self.cog_datas_static_filenames = [
            "cog_datas_static1.csv",
            "cog_datas_static2.csv",
            "cog_datas_static3.csv",
            "cog_datas_static4.csv"
        ]

        self.cog_datas_static = [read_cog_datas(filename) for filename in self.cog_datas_static_filenames]

        self.empties_datas_static_filenames = [
            "empties_datas_static1.csv",
            "empties_datas_static2.csv",
            "empties_datas_static3.csv",
            "empties_datas_static4.csv"
        ]

        self.empties_datas_static = [Empties_Set(read_empties_datas(filename)) for filename in self.empties_datas_static_filenames]

    def test_instantiate_randomly(self):
        for i,(cog_data,empties_data) in enumerate(zip(self.cog_datas_static,self.empties_datas_static)):
            cog_array = Cog_Array(empties_data).instantiate_randomly(cog_data)
            self.assertEqual(cog_array.get_num_occupied() + cog_array.get_num_spares(),len(cog_data))
            if len(cog_data)>0:
                with self.assertRaises(RuntimeError):
                    cog_array.instantiate_randomly(cog_data)

    def test_instantiate_from_array(self):
        for cog_data,empties_data in zip(self.cog_datas_static,self.empties_datas_static):
            cog_array1 = Cog_Array(empties_data).instantiate_randomly(cog_data)
            cog_array2 = Cog_Array(empties_data).instantiate_from_array(cog_array1.array)
            cog_array2.extend_spares(cog_array1.spares)
            self.assertEqual(cog_array2.get_num_occupied() + cog_array2.get_num_spares(), len(cog_data))
            if len(cog_data) > 0:
                with self.assertRaises(RuntimeError):
                    cog_array2.instantiate_randomly(cog_data)

    def test_get_random_coords(self):
        assert False

    def test_cross_breed(self):
        assert False

    def test_one_point_mutation(self):
        assert False

    def test_two_point_mutation(self):
        assert False

    def test_move_cog_from_spares(self):
        assert False

    def test_move_random_cog_from_spares(self):
        assert False

    def test_move_cog_to_spares(self):
        assert False

    def test_move_all_to_spares(self):
        assert False

    def test_add_spare(self):
        assert False

    def test_extend_spares(self):
        assert False

    def test_is_occupied(self):
        assert False

    def test_is_flaggy(self):
        assert False

    def test__reset_rates(self):
        assert False

    def test_get_build_rate(self):
        assert False

    def test_get_flaggy_rate(self):
        assert False

    def test_get_total_exp_mult(self):
        assert False

    def test_standard_obj_fxn(self):
        assert False

    def test_get_num_spares(self):
        assert False

    def test_get_total_non_empty(self):
        assert False

    def test_get_num_extras(self):
        assert False

    def test_get_num_occupied(self):
        assert False
