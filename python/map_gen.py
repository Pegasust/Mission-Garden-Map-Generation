"""
    map_gen.py
    Author: Hung Tran
    Purpose: Main entry of this map generation shenanigans
"""

from map_draw_formatter import parse

def main():
    directory = input("Input directory. Default: ../map_data/ ")
    directory = "../map_data/" if len(directory) < 2 else directory
    out_dir = input("Output directory. Default: ../maps/ ")
    out_dir = "../maps/" if len(out_dir) < 2 else out_dir
    api = input("Api key: (enter to do keyless access) ")
    parse(directory, out_dir, api)


if __name__ == "__main__":
    main()
