import requests
import sys
import json

# head -1 epa-air-tox-screen-links.txt | uv run check_urls.py


def check_internet_archive(url):
    """
    Check if the Internet Archive has a copy of the given URL.

    :param url: The URL to check.
    :return: data
    """
    wayback_url = f"http://archive.org/wayback/available?url={url}"
    response = requests.get(wayback_url)
    data = response.json()
    return data


def check_urls_from_stdin():
    """
    Check all URLs provided via standard input to see if they are archived in the Internet Archive.
    """
    urls = sys.stdin.read().strip().split()

    for url in urls:
        if url:
            data = check_internet_archive(url)
            is_archived = data.get("archived_snapshots") and True or False
            d = {"url": url, "archived": is_archived, "data": data}
            print(json.dumps(d))


# Example usage
check_urls_from_stdin()
