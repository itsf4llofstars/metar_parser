#!/usr/bin/env python3
"""main.py
Main Python file to parse METAR (aviation weather data) from
the internet
"""
from urllib.request import urlopen


def get_response(web_address: str):
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


if __name__ == "__main__":
    url_address = "https://www.python.org"
