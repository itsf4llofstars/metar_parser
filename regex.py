"""reges.py"""
import re
import os


def get_metar(filename):
    """Get the latest metar from metar.txt"""
    try:
        with open(filename) as read:
            metar_list = read.readlines()
    except FileNotFoundError as fnfe:
        print(f"{fnfe}")
    else:
        if metar_list:
            return metar_list[-1].strip()


def strip_remarks(metar_text):
    """Strip off the RMK section of the metar

    Args:
        metar_text (str): The metar string
    """
    remark = re.compile(r"\sRMK.*")
    no_remarks = re.sub(remark, "", metar_text)
    return no_remarks


def convert_utc(zulu, utc=5):
    """Convert utc time to local dst time

    Args:
        zulu (int): ZULU hour
        utc (int, optional): UTC offset. Defaults to 5.

    Returns:
        int: Current local hour
    """
    utc = 5
    local = -1
    if 0 <= zulu < 5:
        local = zulu + 24 - utc
    elif zulu == 5:
        local = zulu - utc
    elif 6 <= zulu <= 23:
        local = zulu - utc

    if 0 < local < 24:
        return local


def convert_temp(temp) -> int:
    """Converts a Celcius temp ot Farenheight

    Args:
        temp (int): Temperature Celcius

    Returns:
        int: Temperature Farenheight
    """
    return int((1.8 * float(temp)) + 32)


def get_altimeter(curr_metar):
    """Get altimeter setting

    Args:
        curr_metar (int): The last metar

    Returns:
        (str): The curent altimeter setting
    """
    return re.search(r"\sA\d{4}$", curr_metar).group()[1:].strip()


def main():
    raw_metar = get_metar(
        os.path.expanduser(os.path.join("~", "python", "metar_parser", "metar.txt"))
    )

    metar = strip_remarks(raw_metar)

    # TODO: Sky Conditions

    station = metar[:4]

    day = int(metar[5:7])
    zulu_hr = int(metar[7:9])
    minute = int(metar[9:11])

    local_hr = convert_utc(zulu_hr)

    # Gusty winds
    # print(re.search(re.compile(r"\d{5}(G\d{2})?KT"), metar).group())

    # handle minus temps Mxx/Mxx xx/Mxx
    c_temp, c_dew = 0, 0
    temps = re.search(r"\sM?\d{2}\/M?\d{2}\s", metar)
    if "M" not in temps.group():
        c_temp = temps.group()[1:3]
        c_dew = temps.group()[4:6]

    temp_f = convert_temp(c_temp)
    dew_f = convert_temp(c_dew)

    alt = get_altimeter(metar)

    # prints
    print(metar)
    print(f"DAY {day}\n{local_hr}{minute} LCL")
    print(f"{temp_f} F, {dew_f} F")
    print(f"{alt} BARO")


if __name__ == "__main__":
    main()

# metar = "KBOS 250354Z 03005G21KT 10SM BKN008 OVC065 09/07 A3007"
# metar = "KALN 071850Z 26010KT 7SM +TSRA SCT030 OVC040 26/20 A2989"
# metar = "KALN 101250Z 09006KT 10SM -RA SCT047 OVC085 16/12 A3014"
# metar = "012345678901
