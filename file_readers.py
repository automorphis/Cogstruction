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

import csv
import math

from coords import Coords

EPS = 10**-5

"""
Reads cog data from a CSV and outputs a `list' of `dicts'. Each item of the `list' corresponds to a cog. Each `dict' 
has two keys, `cog type' and `args'. The `cog type' is the class name of the cog, e.g. `Right_Cog' or 'X_Cog'. The `args'
are the arguments passed to the class constructor.
"""
def read_cog_datas(filename):
    cog_datas = []
    with open(filename, "r", newline="") as fh:
        for i,row in enumerate(csv.DictReader(fh)):
            _check_for_Cog_Data_File_Error("build_rate", "int", row, i, filename)
            _check_for_Cog_Data_File_Error("flaggy_rate", "int", row, i, filename)
            args = (
                int(row["build_rate"]) if len(row["build_rate"])>0 else 0,
                int(row["flaggy_rate"]) if len(row["flaggy_rate"])>0 else 0
            )
            if row["cog type"] != "Character":
                _check_for_Cog_Data_File_Error("exp_mult", "float", row, i, filename)
                args += (float(row["exp_mult"]) if len(row["exp_mult"])>0 else 0.0,)
            else:
                _check_for_Cog_Data_File_Error("exp_rate", "int", row, i, filename)
                args += (int(row["exp_rate"]) if len(row["exp_rate"])>0 else 0,)
                if len(row["name"]) > 0:
                    args += (row["name"],)
            if row["cog type"].strip() in ["Yang_Cog", "X_Cog", "Plus_Cog", "Left_Cog", "Right_Cog", "Up_Cog", "Down_Cog", "Row_Cog", "Col_Cog", "Omni_Cog"]:
                _check_for_Cog_Data_File_Error("build_rate_boost", "float", row, i, filename)
                _check_for_Cog_Data_File_Error("flaggy_rate_boost", "float", row, i, filename)
                _check_for_Cog_Data_File_Error("flaggy_speed", "float", row, i, filename)
                _check_for_Cog_Data_File_Error("exp_rate_boost", "float", row, i, filename)
                args += (
                    float(row["build_rate_boost"]) if len(row["build_rate_boost"])>0 else 0.0,
                    float(row["flaggy_rate_boost"]) if len(row["flaggy_rate_boost"])>0 else 0.0,
                    float(row["flaggy_speed"]) if len(row["flaggy_speed"]) > 0 else 0.0,
                    float(row["exp_rate_boost"]) if len(row["exp_rate_boost"]) > 0 else 0.0
                )
            elif row["cog type"].strip() not in ["Cog", "Character"]:
                raise Cog_Data_File_Error(i, "cog type", filename, "cog")

            cog_datas.append({
                "cog type": row["cog type"].strip(),
                "args": args
            })
    return cog_datas

"""
Reads empties data from CSV and outputs a `set' of `Coords'.
"""
def read_empties_datas(filename):
    empties_datas = []
    with open(filename, "r", newline="") as fh:
        for i, row in enumerate(csv.DictReader(fh)):
            _check_for_Cog_Data_File_Error("empties_x", "int", row, i, filename)
            _check_for_Cog_Data_File_Error("empties_y", "int", row, i, filename)
            empties_datas.append(Coords(int(row["empties_x"]), int(row["empties_y"])))
    return set(empties_datas)

"""
TODO
"""
def read_flaggies_datas(filename):
    pass

def _is_non_neg_int(num):
    return _is_non_neg_float(num) and abs(float(num) - math.floor(float(num))) < EPS

def _is_non_neg_float(num):
    try:
        x = float(num)
        return x >= 0
    except ValueError:
        return False

def _check_for_Cog_Data_File_Error(key, should_be, row, row_num, filename):
    if (
        len(row[key]) > 0 and (
            (should_be == "float" and not _is_non_neg_float(row[key])) or
            (should_be == "int" and not _is_non_neg_int(row[key]))
        )
    ):
        raise Cog_Data_File_Error(row_num, key, filename, should_be)


class Cog_Data_File_Error(RuntimeError):
    def __init__(self, row_num, col_label, filename, should_be):
        msg = "Error in `%s` on row %d, column `%s`. " % (filename, row_num, col_label)
        if should_be == "int":
            msg += "Entry should be a positive integer or zero."
        elif should_be == "float":
            msg += "Entry should be a positive real number or zero."
        elif should_be == "cog":
            msg += "Available cog types are: Cog, Character, Yang_Cog, Plus_Cog, X_Cog, Up_Cog, Down_Cog, Left_Cog, Right_Cog, Col_Cog, Row_Cog, and Omni_Cog"
        super().__init__(msg)

