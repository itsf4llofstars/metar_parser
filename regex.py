"""reges.py"""
import re
import os


def get_metar(filename):
    """Get the latest metar from metar.txt"""
    try:
        with open(filename, "r") as read:
            metar_list = read.readlines()
    except FileNotFoundError as fnfe:
        print(f"{fnfe}")
    else:
        if metar_list:
            return metar_list[-1].strip()


metar = get_metar(
    os.path.expanduser(os.path.join("~", "python", "metar_parser", "metar.txt"))
)
