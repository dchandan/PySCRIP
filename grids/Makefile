#
# Makefile for interpolation code
# CVS:$Id: makefile,v 1.3 2000/04/19 22:05:59 pwjones Exp $
#
COMP = ifort
FLAGS = -r8
# FLAGS = -O3 -64 -r10000 -I/usr/local/include 
LIB  = -L$(NETCDF_LIB_DIR_ICC) -lnetcdff -lnetcdf 
INCL = -I$(NETCDF_INC_DIR_ICC)
SRCDIR  = ../source
EXEDIR  = .
OBJ  = kinds_mod.o constants.o iounits.o netcdf.o

all: convertPOPT convertgauss create_latlon

convertold: $(OBJ) convert_old.o
	$(COMP) $(FLAGS) $(OBJ) convert_old.o $(LIB) -o $(EXEDIR)/convertold

convertPOPT: $(OBJ) convertPOPT.o
	$(COMP) $(FLAGS) $(OBJ) convertPOPT.o $(LIB) -o $(EXEDIR)/convertPOPT

convertgauss: $(OBJ) convertgauss.o
	$(COMP) $(FLAGS) $(OBJ) convertgauss.o $(LIB) -o $(EXEDIR)/convertgauss

create_latlon: $(OBJ) create_latlon.o
	$(COMP) $(FLAGS) $(OBJ) create_latlon.o $(LIB) -o $(EXEDIR)/create_latlon

myconvertPOPT: $(OBJ) myconvertPOPT.o
	$(COMP) $(FLAGS) $(OBJ) myconvertPOPT.o $(LIB) -o $(EXEDIR)/myconvertPOPT

kinds_mod.o: $(SRCDIR)/kinds_mod.f
	$(COMP) $(FLAGS) -c $(SRCDIR)/kinds_mod.f

constants.o: $(SRCDIR)/constants.f kinds_mod.o
	$(COMP) $(FLAGS) -c $(SRCDIR)/constants.f

iounits.o: $(SRCDIR)/iounits.f kinds_mod.o constants.o
	$(COMP) $(FLAGS) -c $(SRCDIR)/iounits.f

netcdf.o: $(SRCDIR)/netcdf.f kinds_mod.o constants.o
	$(COMP) $(FLAGS) -c $(SRCDIR)/netcdf.f $(INCL)

convert_old.o: convert_old.f kinds_mod.o constants.o iounits.o netcdf.o
	$(COMP) $(FLAGS) -c convert_old.f

convertPOPT.o: convertPOPT.f kinds_mod.o constants.o iounits.o netcdf.o
	$(COMP) $(FLAGS) -c convertPOPT.f

convertgauss.o: convertgauss.f kinds_mod.o constants.o iounits.o netcdf.o
	$(COMP) $(FLAGS) -c convertgauss.f

create_latlon.o: create_latlon.f kinds_mod.o constants.o iounits.o netcdf.o
	$(COMP) $(FLAGS) -c create_latlon.f

myconvertPOPT.o: myconvertPOPT.f kinds_mod.o constants.o iounits.o netcdf.o
	$(COMP) $(FLAGS) -c myconvertPOPT.f

tidy:
	/bin/rm -f *.o *.mod

clean: 
	/bin/rm -f *.o *.mod convertPOPT convertgauss create_latlon

