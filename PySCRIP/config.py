"""
This file provides a class with an interface for easy access to mapping files
that have been configured on a system. To do this the class relies on
configuration data stored as a YAML file in the user's home directory.
"""


from __future__ import absolute_import, division, print_function, unicode_literals
import os.path as osp
import yaml


class SCRIPConfigError(Exception):
    pass

class Map:
    def __init__(self, struct, type_):
        self.type = type_
        self.gridfrom = struct['from']
        self.gridto = struct['to']
        self.name = struct['name']
        self.fname = struct['fname']
        self.format = struct['format']
    


class Mapset:
    def __init__(self, struct):
        self.name = struct['name']
        self.simulations = struct['simulations']  # All the simulations for this set
        self.oceanmask = struct['oceanmask']

        self.maps = []  # Will contain all the maps
        # Add all the conservative maps
        for item in struct['maps']['conservative']:
            self.maps.append(Map(item, 'conservative'))

        # Add all the bilinear maps
        for item in struct['maps']['bilinear']:
            self.maps.append(Map(item, 'bilinear'))

    def __iter__(self):
        return iter(self.maps)

    def __contains__(self, s):
        """
        Checks if a simulation is contained in this mapset.
        """
        return s in self.simulations



class PySCRIPConfig(object):
    defaultconfigfile = osp.join(osp.expanduser("~"), ".pyscrip.yaml")

    def __init__(self, configfile=None):
        """
        ARGUMENTS
            configfile - name of config file to use. If not provided a default
                         config file will be queried
        """
        if configfile is None:
            if osp.isfile(PySCRIPConfig.defaultconfigfile):
                ff = open(PySCRIPConfig.defaultconfigfile, 'r')
            else:
                raise RuntimeError("No config file given and no default file for PySCRIPConfig object")
        else:
            ff = open(configfile, 'r')

        rawdata = yaml.load(ff, Loader=yaml.Loader)
        ff.close()

        self.mapsets = []   # Will contaon all the mapsets
        for item in rawdata['mapsets']:
            self.mapsets.append(Mapset(item))


    def __iter__(self):
        return iter(self.mapsets)


    def getmap(self, simulation, maptype, gfrom, gto):
        """
        Args:
            simulation (str): name of the CESM simulation
            maptype (str): name of the type of map ('conservative' or 'bilinear')
            gfrom (str): name of the source grid
            gto (str): name of the destination grid
        Returns:
            Object of class Map
        """
        for _set in self.mapsets:
            if simulation in _set:
                for _map in _set:
                    if ((_map.gridfrom == gfrom) and (_map.gridto == gto) and 
                       (_map.type == maptype)):
                        return _map

        raise SCRIPConfigError("No mapfile found for the specific configuration")

    def get_ocean_mask(self, simulation):
        for _set in self.mapsets:
            if simulation in _set:
                return _set.oceanmask





if __name__ == "__main__":
    a = PySCRIPConfig()

    # print(a.getmap('PlioMIP_Eoi400_v2', 'conservative', 'gx1', 'll1').fname)
    print(a.get_ocean_mask('PlioMIP_Eoi400_B'))

