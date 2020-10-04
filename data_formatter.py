"""Run this script to create a pandas dataframe from each teletext page inside rootdir

    Teletext page filenames must be in format YYYYMMDD.gif

    Resulting dataframe will have the following format:
         year;month;day;data
    row1 yyyy;mm;dd;[[word1, word2], [word1, word2, word3], ... [word1, word2]]
    row2 yyyy;mm;dd;[[word1, word2], [word1, word2, word3], ... [word1, word2]]
    ...
    rowN yyyy;mm;dd;[[word1, word2], [word1, word2, word3], ... [word1, word2]]
"""

import os
from typing import Dict

import pandas as pd
from tqdm import tqdm
from data_preprocessor import words_from_image

def main():
    save_to_filename = "teletext_data.csv"
    collect_data_to_dataframe(save_to_filename)

def collect_data_to_dataframe(file_name: str, rootdir: str = "data"):
    """Walk through each subfolder under 'rootdir' and store preprocessed data to one .csv file."""
    if os.path.isfile(file_name):
        print("File already exists, select another filename to avoid overwriting!")
        return

    dicts = []
    for subdir, dirs, files in os.walk(rootdir):
        if not files:
            continue

        print("Collecting data from directory:", subdir)
        for f in tqdm(files):
            file_path = os.path.join(subdir, f)

            words = words_from_image(file_path)
            date_information = _get_date_information(f)

            d = {"data":words}
            d.update(date_information)
            dicts.append(d)

    df = pd.DataFrame(dicts, columns=["year", "month", "day", "data"])
    df.to_csv(file_name, index=False, sep=";")

def _get_date_information(file_path: str) -> Dict[str, int]:
    """Retrieve year, month and date from filename which has format YYYYMMDD.gif."""
    date_information = file_path.split(".")[0]
    if len(date_information) != 8:
        raise Exception("Invalid date identifier in filename:", file_path, "Filename should be in form YYYYMMDD.gif")

    try:
        year = int(date_information[0:4])
        month = int(date_information[4:6])
        day = int(date_information[6:8])
    except ValueError as e:
        print("Failed to convert date identifier to integer format:", e)
    return {"year":year, "month":month, "day":day}

if __name__ == "__main__":
    main()
