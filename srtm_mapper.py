#!/usr/bin/python

import Mapper as map
import sys
import getopt

def main(argv):
    version = "1.0"
    help_message = "usage: srtm_mapper.py" + "\n\n" + "srtm_mapper version " + version + \
                   " - " + "By Nathan Tucker." + "\n"

    input_file = ""
    vmin = None
    vmax = None
    offset_scalar = 1.0
    use_absolute_coordinates = False
    calculate_min_max_requested = False

    try:
        opts, args = getopt.getopt(argv, "hi:n:x:o:ac", ["input=", "vmin=", "vmax=", "offset=", "absolute", "calculate"])
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

    with open(input_file) as srtm_file:
        for line in srtm_file:
            line_parsed = line.strip().split(',')

            offset_x = float(line_parsed[2])
            offset_y = float(line_parsed[3])
            offset_z = float(line_parsed[4])

            if not calculate_min_max_requested:
                srtm_mapper.create_surf_map(line_parsed[0], line_parsed[1],
                    offset_x, offset_y, offset_z)
            else:
                (min, max) = srtm_mapper.calculate_min_max(line_parsed[0], line_parsed[1])
                print(str(min) + "\t" + str(max))

    if not calculate_min_max_requested:
        srtm_mapper.show()

if __name__ == "__main__":
    main(sys.argv[1:])
