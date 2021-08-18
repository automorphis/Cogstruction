import csv

from coords import Coords

"""
Reads cog data from a CSV and outputs a `list' of `dicts'. Each item of the `list' corresponds to a cog. Each `dict' 
has two keys, `cog type' and `args'. The `cog type' is the class name of the cog, e.g. `Right_Cog' or 'X_Cog'. The `args'
are the arguments passed to the class constructor.
"""
def read_cog_datas(filename):
    cog_datas = []
    with open(filename, "r", newline="") as fh:
        for row in csv.DictReader(fh):
            args = (
                int(row["build_rate"]) if len(row["build_rate"])>0 else 0,
                int(row["flaggy_rate"]) if len(row["flaggy_rate"])>0 else 0
            )
            if row["cog type"] != "Character":
                args += (float(row["exp_rate"]) if len(row["exp_rate"])>0 else 0.0,)
            else:
                args += (row["name"],)
            if row["cog type"] in ["Yang_Cog", "X_Cog", "Plus_Cog", "Left_Cog", "Right_Cog", "Up_Cog", "Down_Cog", "Row_Cog", "Col_Cog"]:
                args += (
                    float(row["build_rate_boost"]) if len(row["build_rate_boost"])>0 else 0.0,
                    float(row["flaggy_rate_boost"]) if len(row["flaggy_rate_boost"])>0 else 0.0,
                    float(row["flaggy_speed"]) if len(row["flaggy_speed"]) > 0 else 0.0,
                    float(row["exp_rate_boost"]) if len(row["exp_rate_boost"]) > 0 else 0.0
                )

            cog_datas.append({
                "cog type": row["cog type"],
                "args": args
            })
    return cog_datas

"""
Reads empties data from CSV and outputs a `set' of `Coords'.
"""
def read_empties_datas(filename):
    empties_datas = []
    with open(filename, "r", newline="") as fh:
        for row in csv.DictReader(fh):
            empties_datas.append(Coords(int(row["empties_x"]), int(row["empties_y"])))
    return set(empties_datas)

"""
TODO
"""
def read_flaggies_datas(filename):
    pass


