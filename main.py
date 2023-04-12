#!/usr/bin/env python3
"""main.py
Main Python file to parse METAR (aviation weather data) from
the internet
"""
import os
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
        response (str): Utf-8 response text
    """
    try:
        with open(filename, "w") as write:
            write.write(response)
            write.write("\n")
    except FileNotFoundError as fnfe:
        print(f"{fnfe}")


if __name__ == "__main__":
    url_address = "https://www.python.org"

    url_response = get_response(url_address)
    utf8_response = url_response.decode("utf-8")

    html_filename = os.path.expanduser(
            os.path.join("~", "python", "metar_parser", "metar.html")
            )
    write_response(html_filename, utf8_response)
