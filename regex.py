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


def strip_remarks(metar_text):
    """Strip off the RMK section of the metar"""
    remark = re.compile(r"\sRMK.*")
    no_remarks = re.sub(remark, "", metar_text)
    return no_remarks


raw_metar = get_metar(
    os.path.expanduser(os.path.join("~", "python", "metar_parser", "metar.txt"))
)

metar = strip_remarks(raw_metar)

print(metar)
