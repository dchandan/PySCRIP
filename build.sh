sudo yum -y update && sudo yum -y upgrade 
sudo yum install -y python python-pip
sudo easy_install --upgrade pip
sudo rm /usr/bin/pip
sudo ln -s /usr/local/bin/pip /usr/bin/pip
sudo yum-config-manager --enable epel
sudo yum install -y netcdf netcdf-devel
sudo yum groupinstall -y "Development Tools"
sudo pip install --upgrade setuptools
sudo pip install numpy scipy matplotlib ipython jupyter pandas sympy nose
sudo pip install netCDF4
sudo ln -s `which f2py` /usr/bin

git clone https://github.com/izzyleung/PySCRIP
cd PySCRIP
sudo python setup.py install