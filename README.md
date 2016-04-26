# srtm_mapper
srtm_mapper is a python utility script for collating together several SRTM files into a shared image for visualization and mapping purposes. It was originally built for use with the files generated from http://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm but will work with any system that serves up NASA's SRTM files broken up by region.

N39W105 - N41W106.hgt with a direct surface map:
![3d render](http://i.imgur.com/2VoUldS.png)

The same terrain decimated and rendered with only 300 triangles:
![decimated render](http://i.imgur.com/M9ox7w4.png)

Min/Max calculations over the same set:
```
python srtm_mapper.py -i tests/srtms_full_test --vmin 0 --vmax 3800 --offset 1200 -c
Min     Max
1442.0  2858.0
1553.0  4333.0
1324.0  1995.0
1474.0  4343.0
1219.0  2057.0
1464.0  2935.0
```

srtm_mapper supports both direct surface maps and decimated renders for larger data sets, along with utilities to calculate appropriate vmin/vmax values for the colormap applied. From the man text:
```
usage: srtm_mapper.py -i <input file> -o <offset scalar>

srtm_mapper version 1.0 - Collates together separate SRTM files into a shared image for mapping. By Nathan Tucker.

-i, --input	Path to the files to parse. Format for the files should be: <path_to_zip>,<path_in_zip_of_hgt_file>,<offset_x>,<offset_y>,<offset_z>. Items are comma-separated and each newline represents a new file. Example: ./K13.zip,K13/N40W105.hgt,0,1,0
-n, --vmin	Value to use as the minimum elevation for the earth colormap.
-x, --vmax	Value to use as the maximum elevation for the earth colormap.
-o, --offset	Offset scalar to use for arranging tiles. Generally tile_size * 2. For example, ./K13.zip,K13/N40W105.hgt,0,1,0 with --offset of 1200 would place the N40W105.hgt at x:0, y:1200, z:0.
-a, --absolute	Use absolute values instead of offsets. Use if you have odd shaped tiles or tiles from different sources. With this option, offsets in the input file need to be absolute values instead of scalars.
-c, --calculate	Calculate and display the min and max of provided sets so you can easily specify vmin and vmax values.
-d, --decimation	Use terrian-decimation to render the surface instead of a direct surface map.
-t, --triangles	Number of triangles to render in the terrian decimation.
-t, --normals	Compute the normals of triangles in the terrian decimation

example: srtm_mapper.py -i srtms_small_test --vmin 0 --vmax 3800 --offset 1200

srtms_small_test:
./K13.zip,K13/N40W105.hgt,0,0,0
./K13.zip,K13/N40W106.hgt,0,-1,0
```

### Licensing
srtm_mapper is licensed under the MIT license, which means you are free to alter and edit the source in any way you see fit. The only real dependency it has is mayavi (http://mayavi.sourceforge.net/).
