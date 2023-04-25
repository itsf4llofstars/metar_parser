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

# KBOS 250354Z 03005KT 10SM BKN008 OVC065 09/07 A3007
# 012345678901
metar = strip_remarks(raw_metar)

print(metar)

station = metar[:4]
print(station)

day = int(metar[5:7])
hour = int(metar[7:9])
minute = int(metar[9:11])
print(day, hour, minute)

dst = 5
local_hr = -1
if 0 <= hour < 5:
    local_hr = hour + 24 - dst
elif hour == 5:
    local_hr = hour - dst
elif 6 <= hour <= 23:
    local_hr = hour - dst
print(hour, local_hr)
