# PySCRIP

## Description
A Python interface to the [SCRIP](http://oceans11.lanl.gov/trac/SCRIP) Fortran package that provides remapping and interpolation routines for spherical grids.

The core of this package has been taken from the [pyroms](https://github.com/kshedstrom/pyroms) package. The long term plan for the PySCRIP project is to made changes as needed to make the package and its interface more 'pythonic' as well as to implement new features. This will necessarily result in a divergence between the PySCRIP source code and the SCRIP (v1.4) scource code. However, the **ability to create and read the remapping files from SCRIP v1.4 will always be maintained**.

## Installation
First compile the SCRIP source into a python importable shared library. The program **f2py** is used for this purpose. To make the library, type ``make`` in the source directory. You should look into the contents of the Makefile first to change the locations of libraries on your system. Once the compilation is successful you will have a *_scrip.so* library in your source directory.

In order to ensure that you can import PySCRIP into Python, simply add the path to the PySCRIP directory into your ```PYTHONPATH```. E.g. in bash:
```shell
export PYTHONPATH="/home/user/development:${PYTHONPATH}"
```
where ```/home/user/development``` would be replaced by directory which contains PySCRIP.

## Usage

The usage of PySCRIP comprises of three steps:
1. Generating the mapping files between two grids
2. Testing the mapping files
3. Using the mapping files to map data from one grid to another.

Steps 1 and 2 only need to be done once per grid combination.


## YAML configuration
PySCRIP provides a simple way to manage all the mapping files on your system. The functionality is exposed in the ```PySCRIPConfig``` class. This class parses a configuration file written in YAML describing the various mapping files that have been generated and are available for use. A sample configuration is shown below.

The advantage of this system is that it provides a sane way of referring to the files without referring to them by their location in each source file, which makes management hard when files are moved or the script is ported to another computer. Using the configuration system, one only has to edit the configuration file for the system and not each individual source code.

```yaml
datadir:
    - /Users/dchandan/Research/CESM/mapping

map:
  cesmpifv1mts:
    conservative:
      - from:  fv1
        to:    gx1
        name:  fv_0.9x1.25 to gx1 Mapping
        fname: pyscrip_cesmpifv1mts_fv1_to_gx1_conserv.nc
      - from:  gx1
        to:    fv1
        name:  gx1 to fv_0.9x1.25 Mapping
        fname: pyscrip_cesmpifv1mts_gx1_to_fv1_conserv.nc
      - from:  fv1
        to:    ll1
        name:  fv_0.9x1.25 to lat/lon 1x1 mapping
        fname: pyscrip_cesmpifv1mts_fv1_to_ll1_conserv.nc
      - from:  ll1
        to:    fv1
        name:  lat/lon 1x1 to fv_0.9x1.25 mapping
        fname: pyscrip_cesmpifv1mts_ll1_to_fv1_conserv.nc
      - from:  gx1
        to:    ll1
        name:  gx1 to lat/lon 1x1 mapping
        fname: pyscrip_cesmpifv1mts_gx1_to_ll1_conserv.nc
      - from:  ll1
        to:    gx1
        name:  lat/lon 1x1 to gx1 mapping
        fname: pyscrip_cesmpifv1mts_ll1_to_gx1_conserv.nc
    bilinear:
      - from:  fv1
        to:    gx1
        name:  fv_0.9x1.25 to gx1 Mapping
        fname: pyscrip_cesmpifv1mts_fv1_to_gx1_bilin.nc
      - from:  gx1
        to:    fv1
        name:  gx1 to fv_0.9x1.25 Mapping
        fname: pyscrip_cesmpifv1mts_gx1_to_fv1_bilin.nc
```
### Example

Once a PySCRIPConfig class object is created, as
```python
Config = PySCRIPConfig
```
one can inquire about the full file name of the mapping file as folows:
```python
filename = Config.mapFile(case, maptype, gfrom, gto)
```
where ```case``` is the name of a set of conversion files between grids that are used together, ```maptype``` is one of the SCRIP mapping types (e.g. ```maptype = 'conservative'```). In the example above, we are converting from gx1 (Greenland displaced pole) grid to fv1 (finitie-volume 1x1 degree) grid. If we want to inquire for the conservative mapping for the case *mycase* going from grid gx1 (Greenland displaced pole grid) to fv1 (finitie-volume 1x1 degree grid), we would write:
```python
filename = Config.mapFile('cesmpifv1mts', 'conservative', 'gx1', 'fv1')
```
