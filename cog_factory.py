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