import datetime
import time
from pathlib import Path

import bs4
import requests

domain = "https://rtva.kavi.fi"

def construct_url(date, time_of_day):
    url = "https://rtva.kavi.fi/teletext/page/choose/thisDate/date/{}/time/{}/page/100/network/6/subpage/1".format(date, time_of_day)
    return url

def get_image_url(page_url):
    response = requests.get(page_url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    teletext_image = soup.find('td', {"class": "imagetd"})
    if not teletext_image:
        print("Failed to retrieve image from URL:", page_url)
        return None

    image_url = domain + teletext_image.img['src']
    return image_url

def main():
    start_date = datetime.date(2009, 4, 22)
    end_date = datetime.date(2020, 3, 17)
    time_of_day = "12:00:00"
    sleep_in_seconds = 1

    for single_date in daterange(start_date, end_date):
        time.sleep(sleep_in_seconds)

        url_datestring = single_date.strftime("%d-%m-%Y")
        page_url = construct_url(url_datestring, time_of_day) 

        image_url = get_image_url(page_url)
        if not image_url:
            continue
        else:
            print("Found valid image from URL:", image_url)

        response = requests.get(image_url)

        folder = 'data/{}/{}/'.format(single_date.year, single_date.month)
        Path(folder).mkdir(parents=True, exist_ok=True)

        filename = folder + single_date.strftime("%Y%m%d") + ".gif"

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    pass
                    f.write(chunk)
            print("Image saved to file:", filename, "\n")


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

if __name__ == "__main__":
    main()

