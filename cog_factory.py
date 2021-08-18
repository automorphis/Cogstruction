from cog_types import *

"""
Takes the output of `read_empties_data' and creates a `list' of cogs.
"""
def cog_factory(cog_datas):
    cogs = []
    for cog_data in cog_datas:
        cogs.append(instatiate_cog(cog_data))
    return cogs


def instatiate_cog(cog_data):
    return globals()[cog_data["cog type"]](*cog_data["args"])