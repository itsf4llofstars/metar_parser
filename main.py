#!/usr/bin/env python3
"""main.py
Main Python file to parse METAR (aviation weather data) from
the internet
"""
import os
import re
from urllib.request import urlopen


def get_response(web_address: str) -> object:
    """Gets a returned web-site response via the
    urllib module

    Args:
        web_address (str): The web-site address for the response

    Return:
        response (str): Response from the polled web-site
    """
    try:
        with urlopen(web_address) as resp:
            response = resp.read()
    except Exception as err:
        print(f"{err}")
    else:
        return response


def write_response(filename: str, response: str) -> None:
    """Write the utf-8 decoded response text to an html
    file in the present working directory

    Args:
        filename (str): Name of the html file to be written to
        response (str): Utf-8 response text
    """
    try:
        with open(filename, "w") as write:
            write.write(response)
    except FileNotFoundError as fnfe:
        print(f"{fnfe}")


def read_response_file(filename) -> None:
    """Reads the html file written from the metar response
    and returns only the line that contains the metar weather data

    Args:
        filename (str): Path and name of the metar html file
    """
    metar_line = re.compile(r"^<code>")
    try:
        with open(filename, "r") as read:
            file_lines = read.readlines()
    except FileNotFoundError as fnfe:
        print(f"{fnfe}")
    for line in file_lines:
        if re.search(metar_line, line.strip()):
            return line.strip()[6:-12]


def strip_remarks(metar) -> str:
    """Removes the remarks section of the METAR

    Args:
        metar (str): The metar string

    Returns:
        metar (str): The metar with the RMK stripped to line end
    """
    regex_str = re.compile(r"\sRMK.*")
    return re.sub(regex_str, "", metar)


def write_metar(filename, metar) -> None:
    """Writes the single line METAR wx data to a metar
    text file

    Args:
        filename (str): Name of the metar text file
        metar (str): Metar line of text
    """
    try:
        with open(filename, "a") as append:
            append.write(metar)
            append.write("\n")
    except FileNotFoundError as fnfe:
        print(f"{fnfe}")


if __name__ == "__main__":
    airport = "kmci"
    url_address = f"https://www.aviationweather.gov/metar/data?ids={airport}&format=raw&date=&hours=0"

    url_response = get_response(url_address)
    utf8_response = url_response.decode("utf-8")

    html_filename = os.path.expanduser(
        os.path.join("~", "python", "metar_parser", "metar.html")
    )

    write_response(html_filename, utf8_response)
    metar_text = read_response_file(html_filename)
    stripped_metar = strip_remarks(metar_text)

    metar_text = os.path.expanduser(os.path.join("~", "logfiles", "metar.txt"))

    write_metar(metar_text, stripped_metar)
