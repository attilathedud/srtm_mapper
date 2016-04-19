#!/usr/bin/python

"""
A simple script to help collate multiple join srtm files together.

Uses mayavi's examples as a basis for creating surf maps.
"""

import zipfile
import numpy as np
from mayavi import mlab
import math

def parse_srtm_data(zip_path, hgt_path):
            data = np.fromstring(zipfile.ZipFile(zip_path).read(hgt_path), '>i2')

            data_sqrt_for_shaping = math.sqrt(data.shape[0])
            data.shape = (data_sqrt_for_shaping, data_sqrt_for_shaping)
            data = data.astype(np.float32)

            data[data == -32768] = data[data > 0].min()

            return data

def create_surf_map(zip_path, hgt_path):
            data = parse_srtm_data(zip_path, hgt_path)

            mlab.surf(data, name=hgt_path, colormap='gist_earth', warp_scale=0.2,
                        vmin=0, vmax=3800)

            del data

def calculate_min_max(zip_path, hgt_path):
            data = parse_srtm_data(zip_path, hgt_path)

            print ("Min of set:" + str(np.amin(data)))
            print ("Max of set:" + str(np.amax(data)))

            del data

mlab.figure(size=(400, 320), bgcolor=(0.16, 0.28, 0.46))

create_surf_map('/Users/thecowgod/Downloads/J13.zip', 'J13/N39W105.hgt')
create_surf_map('/Users/thecowgod/Downloads/J13.zip', 'J13/N39W106.hgt')
create_surf_map('/Users/thecowgod/Downloads/K13.zip', 'K13/N40W105.hgt')
create_surf_map('/Users/thecowgod/Downloads/K13.zip', 'K13/N40W106.hgt')
create_surf_map('/Users/thecowgod/Downloads/K13.zip', 'K13/N41W105.hgt')
create_surf_map('/Users/thecowgod/Downloads/K13.zip', 'K13/N41W106.hgt')

mlab.show()
