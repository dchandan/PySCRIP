#!/bin/csh
#
# Makefile for interpolation code
#
# CVS:$Id: makefile,v 1.7 2000/04/19 21:46:44 pwjones Exp $
#
#===============================================================================
# SVN $Id$
# SVN $URL$
#===============================================================================

NC_CONFIG = $(HOME)/local/gcc/netcdf/430_hdf5_serial_gcc48/bin/nc-config
LIBDIR    = $(shell $(NC_CONFIG) --prefix)/lib
INCDIR    = $(shell $(NC_CONFIG) --prefix)/include
SRCDIR    = $(shell pwd)
# BUILDIR   = /Users/dchandan/Development/PySCRIP/build/test
PREFIX    = /usr/local

LIBNAME   = _scrip
COMPILE   = gfortran
FLAGS     = -fdefault-real-8 -ffixed-form -O2 -fPIC
LIB       =  $(shell $(NC_CONFIG) --flibs)
INCLUDE   = -I$(INCDIR) -J$(BUILDIR)
# F2PY      = f2py
F2PY_LIB  = -L${LIBDIR} -L$(HDF5SERIAL_LIB_DIR_GCC) -lnetcdf -lnetcdff -lhdf5 -lhdf5_hl
F2PY_INCLUDE  = -I${INCDIR} -I$(BUILDIR)
F2PY_F90_FLAG = '-fdefault-real-8 -ffixed-form -O2 -fPIC'

OBJF2PY  = \
	$(BUILDIR)/kinds_mod.o \
	$(BUILDIR)/constants.o \
	$(BUILDIR)/iounits.o \
	$(BUILDIR)/netcdf.o \
	$(BUILDIR)/grids.o \
	$(BUILDIR)/remap_vars.o \
	$(BUILDIR)/remap_distwgt.o \
	$(BUILDIR)/remap_conserv.o \
	$(BUILDIR)/remap_bilinear.o \
	$(BUILDIR)/remap_bicubic.o \
	$(BUILDIR)/remap_read.o \
	$(BUILDIR)/remap.o \
	$(BUILDIR)/timers.o \
	$(BUILDIR)/remap_write.o


all: f2py

f2py: $(SRCDIR)/$(LIBNAME)

$(SRCDIR)/$(LIBNAME): $(SRCDIR)/pyscrip.f90 $(OBJF2PY)
	$(F2PY) --f90flags=$(F2PY_F90_FLAG) \
	$(F2PY_LIB) $(F2PY_INCLUDE) -m $(LIBNAME) \
	-c $(OBJF2PY) $(SRCDIR)/pyscrip.f90


$(BUILDIR)/kinds_mod.o: $(SRCDIR)/kinds_mod.f
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/kinds_mod.f -o $@

$(BUILDIR)/constants.o: $(SRCDIR)/constants.f $(BUILDIR)/kinds_mod.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/constants.f -o $@

$(BUILDIR)/iounits.o: $(SRCDIR)/iounits.f $(BUILDIR)/kinds_mod.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/iounits.f -o $@

$(BUILDIR)/netcdf.o: $(SRCDIR)/netcdf.f $(BUILDIR)/kinds_mod.o $(BUILDIR)/constants.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/netcdf.f -o $@

$(BUILDIR)/grids.o: $(SRCDIR)/grids.f $(BUILDIR)/kinds_mod.o $(BUILDIR)/constants.o \
	$(BUILDIR)/iounits.o $(BUILDIR)/netcdf.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/grids.f -o $@

$(BUILDIR)/remap_vars.o: $(SRCDIR)/remap_vars.f $(BUILDIR)/kinds_mod.o \
	$(BUILDIR)/constants.o $(BUILDIR)/grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_vars.f -o $@

$(BUILDIR)/remap_conserv.o: $(SRCDIR)/remap_conserv.f $(BUILDIR)/kinds_mod.o \
	    $(BUILDIR)/constants.o $(BUILDIR)/timers.o $(BUILDIR)/remap_vars.o $(BUILDIR)/grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_conserv.f -o $@

$(BUILDIR)/remap_distwgt.o: $(SRCDIR)/remap_distwgt.f $(BUILDIR)/kinds_mod.o $(BUILDIR)/constants.o \
		$(BUILDIR)/remap_vars.o $(BUILDIR)/grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_distwgt.f -o $@

$(BUILDIR)/remap_bilinear.o: $(SRCDIR)/remap_bilinear.f $(BUILDIR)/kinds_mod.o $(BUILDIR)/constants.o \
		$(BUILDIR)/remap_vars.o $(BUILDIR)/grids.o $(BUILDIR)/timers.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_bilinear.f -o $@

$(BUILDIR)/remap_bicubic.o: $(SRCDIR)/remap_bicubic.f $(BUILDIR)/kinds_mod.o $(BUILDIR)/constants.o \
		$(BUILDIR)/remap_vars.o $(BUILDIR)/grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_bicubic.f -o $@

$(BUILDIR)/timers.o: $(SRCDIR)/timers.f $(BUILDIR)/kinds_mod.o $(BUILDIR)/constants.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/timers.f -o $@

$(BUILDIR)/remap_write.o: $(SRCDIR)/remap_write.f $(BUILDIR)/kinds_mod.o $(BUILDIR)/constants.o \
		$(BUILDIR)/netcdf.o $(BUILDIR)/remap_vars.o $(BUILDIR)/grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_write.f -o $@

$(BUILDIR)/remap_read.o: $(SRCDIR)/remap_read.f $(BUILDIR)/kinds_mod.o \
	    $(BUILDIR)/constants.o $(BUILDIR)/netcdf.o $(BUILDIR)/remap_vars.o $(BUILDIR)/grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_read.f -o $@

$(BUILDIR)/remap.o: $(SRCDIR)/remap.f $(BUILDIR)/kinds_mod.o $(BUILDIR)/constants.o 
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap.f -o $@


tidy:
	/bin/rm -f $(BUILDIR)/*.o $(BUILDIR)/*.mod

clean: 
	/bin/rm -f $(BUILDIR)/*.o $(BUILDIR)/*.mod *.so
