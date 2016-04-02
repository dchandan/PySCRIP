
import sys, os
import PySCRIP as scrip
from PySCRIP.config import PySCRIPConfig
from netCDF4 import Dataset
import numpy as np
from matplotlib import pylab as plt


a = PySCRIPConfig()


# Mapping part
ncfile = Dataset("testdata/cesmpifv1mts_pop_mapping_testdata.nc", "r")
src_array = ncfile.variables["SSH"][:,:]
print src_array.shape
dest = scrip.remap(src_array, a.mapFile("cesmpifv1mts", "conservative", "gx1", "fv1"))
print dest.shape

print src_array.min(), src_array.max()
print dest.min(), dest.max()

plt.figure()
plt.imshow(np.flipud(src_array[0,:]))
plt.colorbar()

# from IPython import embed
# print type(dest)
# embed()
# plt.imshow(dest.mask)
# plt.show()
# print np.where(dest > src_array.max())

# print dest[-1,:]

plt.figure()
dest[np.where(dest == 0)] = np.nan
plt.imshow(np.flipud(dest))
plt.colorbar()


# plt.figure()
# plt.imshow(np.flipud(dest), vmin=src_array.min(), vmax=src_array.max())
# # plt.imshow(np.flipud(dest))
# plt.colorbar()
plt.show()
