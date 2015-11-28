
import sys, os
import PySCRIP.source as scrip
from PySCRIP.source.config import PySCRIPConfig
from netCDF4 import Dataset
import numpy as np
from matplotlib import pylab as plt


a = PySCRIPConfig()

# for maptype in a.maptype:
#     print maptype
#     for map_ in getattr(a.maptype, maptype):
#         print a.mapfile(map_["from"], map_["to"], maptype=maptype)
#         # print map_

case = "cesmpifv1mts"
maptype = "bilinear"
g1  = "gx1"
g2  = "fv1"
scrip.compute_remap_weights("/Users/dchandan/Research/CESM/bc/cesmpifv1mts/cpl_s2/wrkdir/cesmpifv1mts_gx1.nc",
                            "/Users/dchandan/Desktop/ptest/cpl_s2/grids/fv0.9x1.25_070727.nc",
                            a.mapFile(case, maptype, g1, g2),
                            a.mapFile(case, maptype, g2, g1),
                            a.mapName(case, maptype, g1, g2),
                            a.mapName(case, maptype, g2, g1),
                            2,
                            maptype,
                            normalize_opt="fracarea")


# Testing part
scrip.test_remap_weights(2, a.mapFile(case, maptype, g1, g2), "out1.nc")
scrip.test_remap_weights(2, a.mapFile(case, maptype, g2, g1), "out2.nc")
