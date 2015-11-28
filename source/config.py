"""
This file provides a class for easy access to mapping files that have been
configured on this system. To do this the class relies on configuration
data stored as a YAML file in the user's home directory.

"""

import os.path as osp
import yaml

class YAMLobj(dict):
    """
    Maps a YAML parsed nested dictionary to python attributes.
    This solution is a variation on http://stackoverflow.com/a/32107024/805357

    We need this class to derive the PySCRIPConfig class below. 
    """
    def __init__(self, args):
        super(YAMLobj, self).__init__(args)
        if isinstance(args, dict):
            for k, v in args.iteritems():
                if not isinstance(v, dict):
                    self[k] = v
                else:
                    self.__setattr__(k, YAMLobj(v))


    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(YAMLobj, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(YAMLobj, self).__delitem__(key)
        del self.__dict__[key]


class SCRIPConfigError(Exception):
    pass



class PySCRIPConfig(YAMLobj):
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
        
        super(PySCRIPConfig, self).__init__( yaml.load(ff, Loader=yaml.Loader) )
        ff.close()

    
    def _mapsListForCaseAndType(self, case, maptype):
        """
        ARGUMENTS
            case    - name of the case  
            maptype - name of the map type (e.g. conservative)
        RETURNS
            list of maps (a map is information about going from grid A to grid B) 
            configured for the specific case and the specific type
        """
        if case in self.casesAvailable():
            if maptype in self.mapsAvailable(case):
                return getattr(getattr(self.map, case), maptype)
        raise SCRIPConfigError("No map information found in PySCRIP config file")


    def mapFile(self, case, maptype, gfrom, gto):
        """
        ARGUMENTS
            case    - name of the case  
            maptype - name of the map type (e.g. conservative)
            gfrom   - grid from which to map
            gto     - the grid to which to map
        RETURNS
            full pathname to the mapping file
        """
        for mapconf in self._mapsListForCaseAndType(case, maptype):
            if (mapconf["from"] == gfrom) and (mapconf["to"] == gto):
                return osp.join(self.datadir[0], mapconf["fname"])
        raise SCRIPConfigError("No map information found in PySCRIP config file")


    def mapName(self, case, maptype, gfrom, gto):
        """
        Constructs and returns the name of the SCRIP netcdf mapping file corresponding
        to the map type "maptype" from grid "grom" to grid "gto".
        ARGUMENTS
            case    - name of the case  
            maptype - name of the map type (e.g. conservative)
            gfrom   - grid from which to map
            gto     - the grid to which to map
        RETURNS
            description of the map
        """
        for mapconf in self._mapsListForCaseAndType(case, maptype):
            if (mapconf["from"] == gfrom) and (mapconf["to"] == gto):
                return mapconf["name"]
        raise SCRIPConfigError("No map information found in PySCRIP config file")


    def mapsAvailable(self, case):
        """
        ARGUMENTS
            case - name of the case
        RETURNS
            list of the map types configured for this case
        """
        val = getattr(self.map, case)
        if val is None:
            raise SCRIPConfigError("No information for requested 'case' in PySCRIP config file")
        else:
            return val.keys()


    def casesAvailable(self):
        """
        RETURNS
            list of the cases currently available in the configuration file
        """
        return self.map.keys()
