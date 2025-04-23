#!/bin/bash
mkdir .holopy-tmp
cd .holopy-tmp
wget https://github.com/manoharan-lab/holopy/archive/refs/tags/3.5.0.zip
unzip 3.5.0.zip
cd holopy-3.5.0
cp ../../holopy-setup.py ./setup.py
pip install setuptools xarray h5netcdf matplotlib h5py pyYaml scipy numpy pillow nose-py3
python3 setup.py install
cd ../../
rm -r .holopy-tmp
