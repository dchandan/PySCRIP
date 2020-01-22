from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import netCDF4 as netCDF
from . import _scrip

__all__ = ["remap", "Remapper"]

def remap(src_array, remap_file, fformat, src_grad1=None, src_grad3=None,
          src_grad2=None, spval=1e37, verbose=False):
    """
    This is a wrapper around the remap FORTRAN routine in the _scrip.so shared
    library. It is meant to be a convenience routine that handles some tedious
    operations, as well as the task of converting python data structures to the
    data structures needed by the FORTRAN library.

    This routine remaps a source grid to a destination grid based on addresses
    and weights computed in a prior setup phase and stored in a netcdf file.
    ARGUMENTS
        src_array - 2D or 3D array containg the source grid data
        remap_file - the full path and the name to the remapping
                     file that must be used to map data from the source grid
                     to the destination grid.
    RETURNS
        2D or 3D grid (depending on the shape of the input grid) with the
        remapped data.
    """

    if fformat not in ["scrip", "ncar-csm"]:
        raise ValueError("fformat argument must be 'scrip' or 'ncar-csm'")

    # get info from remap_file
    data = netCDF.Dataset(remap_file, 'r')
    title = data.title
    map_method = data.map_method
    normalization = data.normalization
    if fformat == "scrip":
        src_grid_name = data.source_grid
        dst_grid_name = data.dest_grid
        src_grid_size = len(data.dimensions['src_grid_size'])
        dst_grid_size = len(data.dimensions['dst_grid_size'])
        num_links = len(data.dimensions['num_links'])
        src_grid_dims = data.variables['src_grid_dims'][:]
        dst_grid_dims = data.variables['dst_grid_dims'][:]

        # get weights and addresses from remap_file
        map_wts = data.variables['remap_matrix'][:]
        dst_add = data.variables['dst_address'][:]
        src_add = data.variables['src_address'][:]

        # get destination mask
        dst_mask = data.variables['dst_grid_imask'][:]

    else:
        src_grid_name = data.domain_a
        dst_grid_name = data.domain_b
        src_grid_size = len(data.dimensions['n_a'])
        dst_grid_size = len(data.dimensions['n_b'])
        num_links = len(data.dimensions['n_s'])
        src_grid_dims = data.variables['src_grid_dims'][:]
        dst_grid_dims = data.variables['dst_grid_dims'][:]

        # get weights and addresses from remap_file
        map_wts1 = data.variables['S'][:]
        map_wts2 = data.variables['S2'][:]
        dst_add = data.variables['row'][:]
        src_add = data.variables['col'][:]
        # get destination mask
        dst_mask = data.variables['mask_b'][:]

    # remap from src grid to dst grid
    if src_grad1 is not None:
        iorder = 2
    else:
        iorder = 1

    if verbose is True:
        print('Reading remapping: ', title)
        print('From file: ', remap_file)
        print('File format: ', fformat)
        print(' ')
        print('Remapping between:')
        print(src_grid_name)
        print('and')
        print(dst_grid_name)
        print('Remapping method: ', map_method)

    ndim = len(src_array.squeeze().shape)

    if ndim == 2:
        tmp_dst_array = np.zeros(dst_grid_size)
        tmp_src_array = src_array.flatten()

        if iorder == 1:
            # first order remapping
            # insure that map_wts is a (num_links,4) array
            tmp_map_wts = np.zeros((num_links, 4))
            if fformat == "scrip":
                tmp_map_wts[:, 0] = map_wts[:, 0].copy()
            else:
                tmp_map_wts[:, 0] = map_wts1.copy()
                tmp_map_wts[:, 1:3] = map_wts2.copy()
            map_wts = tmp_map_wts
            _scrip.remap(tmp_dst_array, map_wts,
                         dst_add, src_add, tmp_src_array)

        if iorder == 2:
            # second order remapping
            if map_method == 'conservative':
                # insure that map_wts is a (num_links,4) array
                tmp_map_wts = np.zeros((num_links, 4))
                tmp_map_wts[:,0:2] = map_wts[:, 0:2].copy()
                map_wts = tmp_map_wts
                tmp_src_grad1 = src_grad1.flatten()
                tmp_src_grad2 = src_grad2.flatten()
                _scrip.remap(tmp_dst_array, map_wts,
                             dst_add, src_add, tmp_src_array,
                             tmp_src_grad1, tmp_src_grad2)
            elif map_method == 'bicubic':
                tmp_src_grad1 = src_grad1.flatten()
                tmp_src_grad2 = src_grad2.flatten()
                tmp_src_grad3 = src_grad3.flatten()
                _scrip.remap(tmp_dst_array, map_wts,
                             dst_add, src_add, tmp_src_array,
                             tmp_src_grad1, tmp_src_grad2,
                             tmp_src_grad3)
            else:
                raise ValueError('Unknown method')

        # mask dst_array
        idx = np.where(dst_mask == 0)
        tmp_dst_array[idx] = spval
        tmp_dst_array = np.ma.masked_values(tmp_dst_array, spval)

        # reshape
        dst_array = np.reshape(tmp_dst_array, (dst_grid_dims[1],
                               dst_grid_dims[0]))

    elif ndim == 3:

        nlev = src_array.shape[0]
        dst_array = np.zeros((nlev, dst_grid_dims[1], dst_grid_dims[0]))

        # loop over vertical level
        for k in range(nlev):

            tmp_src_array = src_array[k, :, :].flatten()
            tmp_dst_array = np.zeros(dst_grid_size)

            if iorder == 1:
                # first order remapping
                # insure that map_wts is a (num_links,4) array
                tmp_map_wts = np.zeros((num_links, 4))
                if fformat == "scrip":
                    tmp_map_wts[:, 0] = map_wts[:, 0].copy()
                else:
                    tmp_map_wts[:, 0] = map_wts1.copy()
                    tmp_map_wts[:, 1:3] = map_wts2.copy()

                map_wts = tmp_map_wts
                _scrip.remap(tmp_dst_array, map_wts,
                             dst_add, src_add, tmp_src_array)

            if iorder == 2:
                # second order remapping
                if map_method == 'conservative':
                    tmp_src_grad1 = src_grad1.flatten()
                    tmp_src_grad2 = src_grad2.flatten()
                    _scrip.remap(tmp_dst_array, map_wts,
                                 dst_add, src_add, tmp_src_array,
                                 tmp_src_grad1, tmp_src_grad2)
                elif map_method == 'bicubic':
                    tmp_src_grad1 = src_grad1.flatten()
                    tmp_src_grad2 = src_grad2.flatten()
                    tmp_src_grad3 = src_grad3.flatten()
                    _scrip.remap(tmp_dst_array, map_wts,
                                 dst_add, src_add, tmp_src_array,
                                 tmp_src_grad1, tmp_src_grad2,
                                 tmp_src_grad3)
                else:
                    raise ValueError('Unknow method')

            # mask dst_array
            idx = np.where(dst_mask == 0)
            tmp_dst_array[idx] = spval
            tmp_dst_array = np.ma.masked_values(tmp_dst_array, spval)

            # reshape
            dst_array[k, :, :] = np.reshape(tmp_dst_array, (dst_grid_dims[1],
                                            dst_grid_dims[0]))

    else:
        raise ValueError('src_array must have two or three dimensions')

    # close data file
    data.close()

    return dst_array


class Remapper(object):
    def __init__(self, remap_file, fformat, src_grad1=None, src_grad2=None,
                 src_grad3=None, spval=1e37):
        self.remap_file = remap_file
        self.fformat = fformat
        self.src_grad1 = src_grad1
        self.src_grad2 = src_grad2
        self.src_grad3 = src_grad3
        self.spval = spval

        data = netCDF.Dataset(self.remap_file, "r")

        self.map_method = data.map_method

        if self.fformat == "scrip":
            self.src_grid_name = data.source_grid
            self.dst_grid_name = data.dest_grid
            self.src_grid_size = len(data.dimensions['src_grid_size'])
            self.dst_grid_size = len(data.dimensions['dst_grid_size'])
            self.num_links = len(data.dimensions['num_links'])
            self.src_grid_dims = data.variables['src_grid_dims'][:]
            self.dst_grid_dims = data.variables['dst_grid_dims'][:]

            # get weights and addresses from remap_file
            self.map_wts = data.variables['remap_matrix'][:]
            self.dst_add = data.variables['dst_address'][:]
            self.src_add = data.variables['src_address'][:]

            # get destination mask
            self.dst_mask = data.variables['dst_grid_imask'][:]

        else:
            self.src_grid_name = data.domain_a
            self.dst_grid_name = data.domain_b
            self.src_grid_size = len(data.dimensions['n_a'])
            self.dst_grid_size = len(data.dimensions['n_b'])
            self.num_links = len(data.dimensions['n_s'])
            self.src_grid_dims = data.variables['src_grid_dims'][:]
            self.dst_grid_dims = data.variables['dst_grid_dims'][:]

            # get weights and addresses from remap_file
            self.map_wts1 = data.variables['S'][:]
            self.map_wts2 = data.variables['S2'][:]
            self.dst_add = data.variables['row'][:]
            self.src_add = data.variables['col'][:]
            # get destination mask
            self.dst_mask = data.variables['mask_b'][:]

        # remap from src grid to dst grid
        if self.src_grad1 is not None:
            self.iorder = 2
        else:
            self.iorder = 1

        data.close()

        self.idx_mask = np.where(self.dst_mask == 0)

        # insure that map_wts is a (num_links,4) array
        self.tmp_map_wts = np.zeros((self.num_links, 4))

        if self.iorder == 1:
            # first order remapping
            if self.fformat == "scrip":
                self.tmp_map_wts[:, 0] = self.map_wts[:, 0].copy()
            else:
                self.tmp_map_wts[:, 0] = self.map_wts1.copy()
                self.tmp_map_wts[:, 1:3] = self.map_wts2.copy()

            self.map_wts = self.tmp_map_wts

        if self.iorder == 2:
            # second order remapping
            if self.map_method == 'conservative':
                self.tmp_map_wts[:, 0:2] = self.map_wts[:, 0:2].copy()
                self.map_wts = self.tmp_map_wts
                self.tmp_src_grad1 = self.src_grad1.flatten()
                self.tmp_src_grad2 = self.src_grad2.flatten()
            elif self.map_method == 'bicubic':
                self.tmp_src_grad1 = self.src_grad1.flatten()
                self.tmp_src_grad2 = self.src_grad2.flatten()
                self.tmp_src_grad3 = self.src_grad3.flatten()
            else:
                raise ValueError('Unknown method')

        self.tmp_dst_array = np.zeros(self.dst_grid_size)

    def __remap2D(self, tmp_src_array, spval):
        """
        Internal only function that performs the full remap process (remapping,
        masking, if and when applicable, and reshaping) on a 2D data array.

        Args:
            tmp_src_array: flattened sourcearray
            spval: special value for masking
        """

        if self.iorder == 1:
            # first order remapping
            _scrip.remap(self.tmp_dst_array, self.map_wts, self.dst_add,
                         self.src_add, tmp_src_array)

        if self.iorder == 2:
            # second order remapping
            if self.map_method == 'conservative':
                _scrip.remap(self.tmp_dst_array, self.map_wts,
                             self.dst_add, self.src_add, tmp_src_array,
                             self.tmp_src_grad1, self.tmp_src_grad2)
            elif self.map_method == 'bicubic':
                _scrip.remap(self.tmp_dst_array, self.map_wts,
                             self.dst_add, self.src_add, tmp_src_array,
                             self.tmp_src_grad1, self.tmp_src_grad2,
                             self.tmp_src_grad3)

        # Mask destination array
        self.tmp_dst_array[self.idx_mask] = spval
        dst_array = np.ma.masked_values(self.tmp_dst_array, spval)
        dst_array = np.reshape(dst_array, (self.dst_grid_dims[1], self.dst_grid_dims[0]))
        return dst_array

    def __call__(self, src_array, spval=None):
        self.tmp_dst_array[:] = 0.0

        ndim = len(src_array.squeeze().shape)

        if spval is None:
            spval = self.spval

        if ndim == 2:
            tmp_src_array = src_array.flatten()
            return self.__remap2D(tmp_src_array, spval)
        elif ndim == 3:
            nlev = src_array.shape[0]
            dst_array3D = np.zeros((nlev, self.dst_grid_dims[1], self.dst_grid_dims[0]))

            # loop over vertical level
            for k in range(nlev):
                tmp_src_array = src_array[k, :, :].flatten()
                dst_array3D[k, :, :] = self.__remap2D(tmp_src_array, spval)
                return dst_array3D
        else:
            raise ValueError('src_array must have two or three dimensions')



# def __special__get_remap_data_to_ll1_grid(fname):
#     """
#     Special function to return quantities from a file that would be necessary
#     to call _scrip.remap externally (i.e. not using the remap function above).

#     CAVEATS:
#     This is only for a special case of mapping to an ll1 grid (lat-lon 1 degree)
#     which is stored in the scrip formart.

#     :param fname: the full path and the name to the remapping
#                   file that must be used to map data from the source grid
#                   to the destination grid.
#     :return:
#     5 numpy arrays
#     """
#     ncfile = netCDF.Dataset(fname, "r")

#     dst_grid_size = len(ncfile.dimensions['dst_grid_size'])
#     num_links = len(ncfile.dimensions['num_links'])

#     # get weights and addresses from remap_file
#     map_wts = ncfile.variables['remap_matrix'][:]
#     dst_add = ncfile.variables['dst_address'][:]
#     src_add = ncfile.variables['src_address'][:]

#     # get destination mask
#     dst_mask = ncfile.variables['dst_grid_imask'][:]

#     tmp_map_wts = np.zeros((num_links, 4))
#     tmp_map_wts[:, 0] = map_wts[:, 0].copy()
#     map_wts = tmp_map_wts

#     ncfile.close()
#     return map_wts, src_add, dst_grid_size, dst_add, dst_mask

