#!/usr/bin/python

"""
A simple script to help collate multiple join srtm files together.

Uses mayavi's examples as a basis for creating surf maps.
"""

import Mapper as map

srtm_mapper = map.Mapper()
srtm_mapper.vmin = 0
srtm_mapper.vmax = 3800
srtm_mapper.figure_offset_scale = 600.5

srtm_mapper.create_figure()

#srtm_mapper.create_surf_map('/Users/thecowgod/Downloads/J13.zip', 'J13/N39W105.hgt')
#srtm_mapper.create_surf_map('/Users/thecowgod/Downloads/J13.zip', 'J13/N39W106.hgt')
srtm_mapper.create_surf_map('/Users/thecowgod/Downloads/K13.zip', 'K13/N40W105.hgt')
srtm_mapper.create_surf_map('/Users/thecowgod/Downloads/K13.zip', 'K13/N40W106.hgt', map_offset_y = -1.0)
#srtm_mapper.create_surf_map('/Users/thecowgod/Downloads/K13.zip', 'K13/N41W105.hgt')
#srtm_mapper.create_surf_map('/Users/thecowgod/Downloads/K13.zip', 'K13/N41W106.hgt')

srtm_mapper.show()
