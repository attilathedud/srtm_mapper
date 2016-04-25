import zipfile
import numpy as np
from mayavi.api import Engine
from mayavi import mlab
import math

class Mapper:
    def __init__(self):
        self.vmin = None
        self.vmax = None

        self.current_figure = -1
        self.figure_offset_scale = 1.0
        self.use_figure_offset_scale = True

        try:
            self.engine = mayavi.engine
        except NameError:
            from mayavi.api import Engine
            self.engine = Engine()
            self.engine.start()

    def create_figure(self):
        mlab.figure(size=(400, 320))

    def show(self):
        mlab.show()

    def parse_srtm_data(self, zip_path, hgt_path):
                self._data = np.fromstring(zipfile.ZipFile(zip_path).read(hgt_path), '>i2')

                data_sqrt_for_shaping = math.sqrt(self._data.shape[0])
                self._data.shape = (data_sqrt_for_shaping, data_sqrt_for_shaping)
                self._data = self._data.astype(np.float32)

                self._data[self._data == -32768] = self._data[self._data > 0].min()

    def create_surf_map(self, zip_path, hgt_path, map_offset_x = 0.0,
                        map_offset_y = 0.0, map_offset_z = 0.0):

                self.parse_srtm_data(zip_path, hgt_path)

                mlab.surf(self._data, name=hgt_path, colormap='gist_earth', warp_scale=0.2,
                            vmin=self.vmin, vmax=self.vmax)

                self.current_figure += 1

                figure_array_source = self.engine.scenes[0].children[self.current_figure]

                if self.use_figure_offset_scale:
                    figure_array_source.origin = np.array([self.figure_offset_scale * map_offset_x,
                                                            self.figure_offset_scale * map_offset_y,
                                                            self.figure_offset_scale * map_offset_z])
                else:
                    figure_array_source.origin = np.array([map_offset_x, map_offset_y, map_offset_z])

                del self._data

    def calculate_min_max(self, zip_path, hgt_path):
                self.parse_srtm_data(zip_path, hgt_path)

                min = np.amin(self._data)
                max = np.amax(self._data)

                del self._data

                return (min, max)
