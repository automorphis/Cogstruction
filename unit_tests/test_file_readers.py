import unittest

from coords import Coords
from file_readers import read_cog_datas, read_empties_datas, Cog_Data_File_Error


class Test_File_Readers(unittest.TestCase):

    def setUp(self):
        self.cog_datas_static_filenames = [
            "cog_datas_static1.csv",
            "cog_datas_static2.csv",
            "cog_datas_static3.csv",
            "cog_datas_static4.csv"
        ]

        self.cog_datas_with_errors_static_filenames = [
            "cog_datas_with_errors_static1.csv",
            "cog_datas_with_errors_static2.csv",
            "cog_datas_with_errors_static3.csv",
            "cog_datas_with_errors_static4.csv",
        ]

        self.empties_datas_static_filenames = [
            "empties_datas_static1.csv",
            "empties_datas_static2.csv",
            "empties_datas_static3.csv",
            "empties_datas_static4.csv"
        ]

        self.empties_datas_with_errors_static_filenames = [
            "empties_datas_with_errors_static1.csv",
            "empties_datas_with_errors_static2.csv",
            "empties_datas_with_errors_static3.csv",
            "empties_datas_with_errors_static4.csv",
            "empties_datas_with_errors_static5.csv",
            "empties_datas_with_errors_static6.csv"
        ]

        self.cog_datas_static = [
            [
                {'cog type': 'X_Cog', 'args': (27, 8, 0.0, 0.1, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (72, 0, 0.0, 0.0, 0.15, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (8, 15, 0.0, 0.09, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (0, 0, 0.2, 0.0, 0.11, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (12, 0, 0.11, 0.0, 0.11, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (16, 0, 0.0, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (23, 0, 0.12, 0.11, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (17, 0, 0.06, 0.12, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (20, 6, 0.0, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (63, 22, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (57, 11, 0.11, 0.23, 0.0, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (42, 0, 0.1)},
                {'cog type': 'X_Cog', 'args': (5, 5, 0.0, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (0, 11, 0.06, 0.13, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (32, 0, 0.0, 0.0, 0.13, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (0, 5, 0.08, 0.0, 0.15, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (51, 0, 0.0, 0.08, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (3, 0, 0.11, 0.12, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (38, 0, 0.1, 0.0, 0.09, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (5, 18, 0.0, 0.09, 0.0, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (26, 31, 0.0)},
                {'cog type': 'Cog', 'args': (112, 0, 0.0)},
                {'cog type': 'X_Cog', 'args': (23, 0, 0.0, 0.0, 0.15, 0.0, 0.0)},
                {'cog type': 'Up_Cog', 'args': (25, 0, 0.13, 0.12, 0.0, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (114, 0, 0.0)},
                {'cog type': 'X_Cog', 'args': (17, 5, 0.0, 0.08, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (22, 0, 0.0, 0.0, 0.09, 0.0, 0.0)},
                {'cog type': 'Up_Cog', 'args': (21, 11, 0.0, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'Up_Cog', 'args': (31, 0, 0.0, 0.1, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (11, 0, 0.17, 0.11, 0.0, 0.0, 0.0)},
                {'cog type': 'Up_Cog', 'args': (48, 6, 0.0, 0.27, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (23, 3, 0.0, 0.15, 0.0, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (0, 28, 0.28)},
                {'cog type': 'Up_Cog', 'args': (45, 0, 0.0, 0.12, 0.0, 0.0, 0.0)},
                {'cog type': 'Up_Cog', 'args': (28, 0, 0.07, 0.09, 0.0, 0.0, 0.0)},
                {'cog type': 'Up_Cog', 'args': (0, 0, 0.17, 0.11, 0.0, 0.0, 0.0)},
                {'cog type': 'Up_Cog', 'args': (0, 13, 0.0, 0.09, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (14, 14, 0.11, 0.0, 0.0, 0.39, 0.0)},
                {'cog type': 'Cog', 'args': (113, 0, 0.0)},
                {'cog type': 'Cog', 'args': (100, 16, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (25, 0, 0.0, 0.08, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (20, 0, 0.0, 0.08, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (14, 0, 0.0, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'Character', 'args': (500, 132, 0, 'SwanethJohneth')},
                {'cog type': 'Character', 'args': (523, 137, 0, 'Didweknow')},
                {'cog type': 'Cog', 'args': (153, 56, 0.24)},
                {'cog type': 'Cog', 'args': (110, 16, 0.0)},
                {'cog type': 'X_Cog', 'args': (117, 27, 0.0, 0.0, 0.0, 0.0, 0.4)},
                {'cog type': 'Cog', 'args': (158, 0, 0.0)},
                {'cog type': 'Cog', 'args': (127, 0, 0.0)},
                {'cog type': 'X_Cog', 'args': (28, 0, 0.0, 0.0, 0.13, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (72, 0, 0.18)},
                {'cog type': 'Right_Cog', 'args': (10, 6, 0.07, 0.15, 0.0, 0.0, 0.0)},
                {'cog type': 'Character', 'args': (500, 132, 0, 'Lifwat')},
                {'cog type': 'Yang_Cog', 'args': (0, 0, 0.0, 0.4, 0.4, 0.0, 0.0)},
                {'cog type': 'Character', 'args': (477, 127, 0, 'Coolguy Mcgoo')},
                {'cog type': 'Left_Cog', 'args': (8, 2, 0.07, 0.08, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (84, 7, 0.0, 0.38, 0.0, 0.0, 0.0)},
                {'cog type': 'Row_Cog', 'args': (58, 8, 0.0, 0.17, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (10, 0, 0.0, 0.0, 0.13, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (85, 0, 0.18)},
                {'cog type': 'X_Cog', 'args': (8, 0, 0.06, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'Right_Cog', 'args': (24, 0, 0.0, 0.0, 0.08, 0.0, 0.0)},
                {'cog type': 'Character', 'args': (477, 127, 0, 'Suchbeautywhat')},
                {'cog type': 'Character', 'args': (500, 132, 0, 'DizRaySpekt')},
                {'cog type': 'Character', 'args': (477, 127, 0, 'Jus One')},
                {'cog type': 'Left_Cog', 'args': (5, 6, 0.08, 0.0, 0.15, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (14, 0, 0.0, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (6, 6, 0.0, 0.0, 0.08, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (48, 0, 0.0, 0.0, 0.1, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (18, 0, 0.0, 0.11, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (8, 0, 0.05, 0.13, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (14, 0, 0.0, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'Down_Cog', 'args': (30, 0, 0.0, 0.11, 0.0, 0.0, 0.0)},
                {'cog type': 'Down_Cog', 'args': (29, 0, 0.0, 0.0, 0.08, 0.0, 0.0)},
                {'cog type': 'Down_Cog', 'args': (5, 0, 0.04, 0.0, 0.08, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (59, 0, 0.0, 0.35, 0.0, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (57, 21, 0.14)},
                {'cog type': 'X_Cog', 'args': (18, 11, 0.02, 0.11, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (24, 5, 0.0, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (116, 8, 0.0)},
                {'cog type': 'Cog', 'args': (51, 42, 0.0)},
                {'cog type': 'Character', 'args': (433, 117, 0, 'SameyTestation')},
                {'cog type': 'Cog', 'args': (127, 0, 0.0)},
                {'cog type': 'Cog', 'args': (141, 0, 0.0)},
                {'cog type': 'Cog', 'args': (83, 10, 0.11)},
                {'cog type': 'Cog', 'args': (102, 14, 0.08)},
                {'cog type': 'Down_Cog', 'args': (36, 8, 0.0, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'Down_Cog', 'args': (31, 0, 0.0, 0.09, 0.0, 0.0, 0.0)},
                {'cog type': 'Down_Cog', 'args': (29, 0, 0.0, 0.11, 0.0, 0.0, 0.0)},
                {'cog type': 'Down_Cog', 'args': (5, 9, 0.04, 0.0, 0.08, 0.0, 0.0)},
                {'cog type': 'Down_Cog', 'args': (6, 0, 0.07, 0.09, 0.0, 0.0, 0.0)},
                {'cog type': 'Down_Cog', 'args': (28, 0, 0.08, 0.11, 0.0, 0.0, 0.0)},
                {'cog type': 'Omni_Cog', 'args': (28, 0, 0.08, 0.11, 0.0, 0.0, 0.0)},
                {'cog type': 'Col_Cog', 'args': (58, 8, 0.0, 0.17, 0.0, 0.0, 0.0)}
            ],[
                {'cog type': 'Plus_Cog', 'args': (8, 0, 0.1, 0.08, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (17, 0, 0.0, 0.15, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (22, 0, 0.0, 0.09, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (28, 0, 0.0, 0.0, 0.11, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (22, 0, 0.0, 0.1, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (6, 19, 0.0, 0.13, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (11, 0, 0.04, 0.14, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (3, 10, 0.0, 0.13, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (6, 5, 0.0, 0.15, 0.0, 0.0, 0.0)},
                {'cog type': 'Plus_Cog', 'args': (9, 6, 0.0, 0.08, 0.0, 0.0, 0.0)},
                {'cog type': 'Yang_Cog', 'args': (0, 0, 0.0, 0.4, 0.4, 0.0, 0.0)},
                {'cog type': 'Yang_Cog', 'args': (0, 0, 0.0, 0.4, 0.4, 0.0, 0.0)},
                {'cog type': 'Yang_Cog', 'args': (0, 0, 0.0, 0.4, 0.4, 0.0, 0.0)},
                {'cog type': 'Yang_Cog', 'args': (0, 0, 0.0, 0.4, 0.4, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (43, 20, 0.15)}, {'cog type': 'Cog', 'args': (43, 20, 0.15)},
                {'cog type': 'Cog', 'args': (43, 20, 0.15)}, {'cog type': 'Cog', 'args': (43, 20, 0.15)},
                {'cog type': 'X_Cog', 'args': (22, 5, 0.0, 0.13, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (0, 13, 0.0, 0.0, 0.15, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (22, 4, 0.0, 0.08, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (3, 3, 0.0, 0.0, 0.12, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (33, 0, 0.0, 0.0, 0.12, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (15, 10, 0.0, 0.15, 0.0, 0.0, 0.0)},
                {'cog type': 'X_Cog', 'args': (10, 11, 0.0, 0.15, 0.0, 0.0, 0.0)},
                {'cog type': 'Up_Cog', 'args': (19, 0, 0.0, 0.0, 0.08, 0.0, 0.0)},
                {'cog type': 'Up_Cog', 'args': (11, 0, 0.0, 0.0, 0.08, 0.0, 0.0)},
                {'cog type': 'Left_Cog', 'args': (26, 0, 0.12, 0.0, 0.12, 0.0, 0.0)},
                {'cog type': 'Left_Cog', 'args': (9, 4, 0.5, 0.1, 0.0, 0.0, 0.0)},
                {'cog type': 'Down_Cog', 'args': (29, 0, 0.0, 0.0, 0.11, 0.0, 0.0)},
                {'cog type': 'Down_Cog', 'args': (4, 6, 0.02, 0.0, 0.14, 0.0, 0.0)},
                {'cog type': 'Cog', 'args': (45, 0, 0.0)},
                {'cog type': 'Cog', 'args': (13, 7, 0.09)},
                {'cog type': 'Cog', 'args': (2, 4, 0.0)},
                {'cog type': 'Cog', 'args': (9, 3, 0.0)},
                {'cog type': 'Cog', 'args': (5, 4, 0.04)},
                {'cog type': 'Cog', 'args': (3, 0, 0.06)},
                {'cog type': 'Cog', 'args': (13, 0, 0.02)},
                {'cog type': 'Character', 'args': (139, 45, 0, 'Name1')},
                {'cog type': 'Character', 'args': (185, 57, 0, 'Name2')},
                {'cog type': 'Character', 'args': (185, 57, 0, 'Name3')}
            ],
            [

            ], [
                {'cog type': 'Cog', 'args': (69,420,1.337)}
            ]
        ]

        self.empties_datas_static = [
            {
                Coords(0, 2), Coords(10, 0), Coords(11, 2), Coords(0, 5), Coords(11, 5), Coords(1, 0), Coords(9, 7),
                Coords(11, 4), Coords(0, 1), Coords(0, 7), Coords(11, 1), Coords(11, 7), Coords(0, 4), Coords(2, 7),
                Coords(9, 0), Coords(0, 0), Coords(11, 0), Coords(0, 3), Coords(2, 0), Coords(10, 7), Coords(11, 3),
                Coords(0, 6), Coords(11, 6), Coords(1, 7)
            },
            {
                Coords(4, 0), Coords(3, 7), Coords(5, 7), Coords(8, 0), Coords(9, 5), Coords(0, 2), Coords(11, 2),
                Coords(10, 6), Coords(10, 0), Coords(0, 5), Coords(11, 5), Coords(10, 3), Coords(1, 6), Coords(1, 0),
                Coords(1, 3), Coords(7, 7), Coords(3, 0), Coords(5, 0), Coords(9, 1), Coords(9, 7), Coords(11, 4),
                Coords(10, 2), Coords(9, 4), Coords(0, 1), Coords(0, 7), Coords(11, 7), Coords(10, 5), Coords(0, 4),
                Coords(1, 2), Coords(2, 7), Coords(1, 5), Coords(2, 1), Coords(11, 1), Coords(11, 0), Coords(7, 0),
                Coords(6, 7), Coords(4, 7), Coords(9, 0), Coords(9, 3), Coords(0, 0), Coords(8, 7), Coords(10, 4),
                Coords(9, 6), Coords(0, 3), Coords(11, 3), Coords(10, 7), Coords(1, 4), Coords(0, 6), Coords(11, 6),
                Coords(1, 1), Coords(1, 7), Coords(10, 1), Coords(2, 6), Coords(2, 0), Coords(6, 0)
            },
            set(),
            {
                Coords(0,0)
            }
        ]

    def test_read_cog_datas(self):
        for filename, data in zip(self.cog_datas_static_filenames, self.cog_datas_static):
            self.assertEquals(read_cog_datas(filename), data)
        for filename in self.cog_datas_with_errors_static_filenames:
            with self.assertRaises(Cog_Data_File_Error):
                read_cog_datas(filename)

    def test_read_empties_datas(self):
        for filename, data in zip(self.empties_datas_static_filenames, self.empties_datas_static):
            self.assertEquals(read_empties_datas(filename), data)
        for filename in self.empties_datas_with_errors_static_filenames:
            with self.assertRaises(Cog_Data_File_Error) as e:
                read_empties_datas(filename)
