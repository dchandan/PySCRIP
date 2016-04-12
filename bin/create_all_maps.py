import sys, os
import PySCRIP as scrip
from PySCRIP.config import PySCRIPConfig
from netCDF4 import Dataset
import numpy as np
from matplotlib import pylab as plt


a = PySCRIPConfig()

# for maptype in a.maptype:
#     print maptype
#     for map_ in getattr(a.maptype, maptype):
#         print a.mapfile(map_["from"], map_["to"], maptype=maptype)
#         # print map_

case = "PlioMIP_Eoi400_v2"
maptype = "conservative"
g1  = "fv1"
g2  = "ll1"


scrip.compute_remap_weights("/Users/dchandan/Research/PlioTopo/gencesmbc/prism4_v2/cpl_s2/grids/fv0.9x1.25_070727.nc",
                            "/Users/dchandan/Development/PySCRIP/grids/ll1deg_grid.nc",
                            a.getmap(case, maptype, g1, g2).fname,
                            a.getmap(case, maptype, g2, g1).fname,
                            a.getmap(case, maptype, g1, g2).name,
                            a.getmap(case, maptype, g2, g1).name,
                            2,
                            maptype,
                            normalize_opt="fracarea")


# Testing part
scrip.test_remap_weights(2, a.mapFile(case, maptype, g1, g2), "out1.nc")
scrip.test_remap_weights(2, a.mapFile(case, maptype, g2, g1), "out2.nc")
