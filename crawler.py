"""Run this script to crawl teletext pages over a date range."""

import datetime
import time
from pathlib import Path

import bs4
import requests

def main():
    start_date = datetime.date(2009, 4, 22)
    end_date = datetime.date(2020, 3, 17) # pages after teletext service update don't exist (yet)
    crawl(start_date, end_date)

def crawl(start_date: datetime.date, end_date: datetime.date,
          save_root_folder: str = "data", time_of_day: str = "12:00:00"):
    """Retrieve and save all teletext pages between start_date and end_date.

    New folders are created automatically under save_root_folder in format:
    save_root_folder/year/month/

    Images are saved in .gif format to the subfolder corresponding to the year and month of page
    """
    sleep_in_seconds = 1

    for date_object in daterange(start_date, end_date):
        # sleep to not spam the server
        time.sleep(sleep_in_seconds)

        url_datestring = date_object.strftime("%d-%m-%Y")
        page_url = construct_url(url_datestring, time_of_day)

        image_url = get_image_url(page_url)
        if not image_url:
            continue

        print("Found valid image from URL:", image_url)
        response = requests.get(image_url)
        if response.status_code != 200:
            print("Request to URL " + image_url + " failed. Received request " + str(response.status_code) + " instead.")
            continue

        folder = '{}/{}/{}/'.format(save_root_folder, date_object.year, date_object.month)
        Path(folder).mkdir(parents=True, exist_ok=True) # create folder if it does not already exist

        filename = folder + date_object.strftime("%Y%m%d") + ".gif"
        save_page_to_file(response, filename)

def save_page_to_file(response: requests.models.Response, filename: str):
    """Save content from response to given file."""
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
        print("Image saved to file:", filename, "\n")

def construct_url(date: str, time_of_day: str, page_number: int = 100) -> str:
    """Construct URL for wanted teletext page from given date and time_of_day."""
    url = "https://rtva.kavi.fi/teletext/page/choose/thisDate/date/{}/time/{}/page/{}/network/6/subpage/1".format(date, time_of_day, page_number)
    return url

def get_image_url(page_url: str, domain: str = "https://rtva.kavi.fi") -> str:
    """Return the URL for teletext image from the page URL containing it.

    Return None if element containing teletext image is not found from page
    """
    response = requests.get(page_url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    element_to_find = 'td'
    attributes_to_find = {"class": "imagetd"}
    teletext_image = soup.find(element_to_find, attributes_to_find)
    if not teletext_image:
        print("Failed to retrieve image from URL:", page_url)
        return None

    image_url = domain + teletext_image.img['src']
    return image_url

def daterange(start_date: datetime.date, end_date: datetime.date):
    """Yields generator over given date range."""
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

if __name__ == "__main__":
    main()
