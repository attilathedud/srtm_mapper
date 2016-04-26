#!/usr/bin/python

import Mapper as map
import sys
import getopt

def main(argv):
    version = "1.0"
    help_message = "usage: srtm_mapper.py -i <input file> -o <offset scalar>" + "\n\n" + "srtm_mapper version " + version + \
                   " - " + "Collates together separate SRTM files into a shared image for mapping. By Nathan Tucker." + "\n\n" + \
                   "-i, --input\tPath to the files to parse. Format for the files should be: <path_to_zip>,<path_in_zip_of_hgt_file>,<offset_x>,<offset_y>,<offset_z>" + \
                   ". Items are comma-separated and each newline represents a new file. Example: ./K13.zip,K13/N40W105.hgt,0,1,0" + "\n" + \
                   "-n, --vmin\tValue to use as the minimum elevation for the earth colormap." + "\n" + \
                   "-x, --vmax\tValue to use as the maximum elevation for the earth colormap." + "\n" + \
                   "-o, --offset\tOffset scalar to use for arranging tiles. Generally tile_size * 2. For example, ./K13.zip,K13/N40W105.hgt,0,1,0 with --offset of 1200 would place the N40W105.hgt at x:0, y:1200, z:0." + "\n" + \
                   "-a, --absolute\tUse absolute values instead of offsets. Use if you have odd shaped tiles or tiles from different sources. With this option, offsets in the input file need to be absolute values instead of scalars." + "\n" + \
                   "-c, --calculate\tCalculate and display the min and max of provided sets so you can easily specify vmin and vmax values." + "\n" + \
                   "-d, --decimation\tUse terrian-decimation to render the surface instead of a direct surface map." + "\n" + \
                   "-t, --triangles\tNumber of triangles to render in the terrian decimation." + "\n" + \
                   "-t, --normals\tCompute the normals of triangles in the terrian decimation" + "\n\n" + \
                   "example: srtm_mapper.py -i srtms_small_test --vmin 0 --vmax 3800 --offset 1200" + "\n\n" + \
                   "srtms_small_test:\n" + "./K13.zip,K13/N40W105.hgt,0,0,0" + "\n" + \
                   "./K13.zip,K13/N40W106.hgt,0,-1,0\n"


    input_file = ""
    vmin = None
    vmax = None
    offset_scalar = 1.0
    use_absolute_coordinates = False
    calculate_min_max_requested = False
    use_decimated_render = False
    number_of_triangles = 5000
    compute_normals = False

    try:
        opts, args = getopt.getopt(argv, "hi:n:x:o:acdt:r", ["input=", "vmin=", "vmax=", "offset=", "absolute", "calculate", "decimation", "triangles", "normals"])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_message)
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-n", "--vmin"):
            vmin = int(arg)
        elif opt in ("-x", "--vmax"):
            vmax = int(arg)
        elif opt in ("-o", "--offset"):
            offset_scalar = float(arg)
        elif opt in ("-a", "--absolute"):
            use_absolute_coordinates = True
        elif opt in ("-c", "--calculate"):
            calculate_min_max_requested = True
        elif opt in ("-d", "--decimation"):
            use_decimated_render = True
        elif opt in ("-t", "--triangles"):
            number_of_triangles = int(arg)
        elif opt in ("-r", "--normals"):
            compute_normals = True

    if not input_file:
        print(help_message)
        sys.exit(2)

    srtm_mapper = map.Mapper()

    srtm_mapper.vmin = vmin
    srtm_mapper.vmax = vmax
    srtm_mapper.use_figure_offset_scale = not use_absolute_coordinates
    srtm_mapper.figure_offset_scale = offset_scalar

    if not calculate_min_max_requested:
        srtm_mapper.create_figure()
    else:
        print("Min\tMax")

    try:
        srtm_file = open(input_file)
    except IOError:
        print("Could not open the input file. Make sure it exists and can be read.")
        sys.exit(2)

    with srtm_file:
        for line in srtm_file:
            line_parsed = line.strip().split(',')

            offset_x = float(line_parsed[2])
            offset_y = float(line_parsed[3])
            offset_z = float(line_parsed[4])

            if not calculate_min_max_requested and not use_decimated_render:
                srtm_mapper.create_surf_map(line_parsed[0], line_parsed[1],
                    offset_x, offset_y, offset_z)
            elif not calculate_min_max_requested and use_decimated_render:
                srtm_mapper.create_decimated_map(line_parsed[0], line_parsed[1],
                    number_of_triangles, compute_normals, offset_x, offset_y, offset_z)
            else:
                (min, max) = srtm_mapper.calculate_min_max(line_parsed[0], line_parsed[1])
                print(str(min) + "\t" + str(max))

    if not calculate_min_max_requested:
        srtm_mapper.show()

if __name__ == "__main__":
    main(sys.argv[1:])
