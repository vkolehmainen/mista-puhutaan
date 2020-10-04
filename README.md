# Teletext (Teksti-tv) frontpage topical analysis 2009-2020

## Project in a nutshell
The idea in this project was to find out the most common news topics according to the only true media authority: YLE Teksti-tv

## Data

### Crawling
The teletext front page for each was date from 21.04.2009 to 17.03.2020 was crawled from [RITVA database](https://rtva.kavi.fi/)

For example, the teletext front page from 01.01.2020 at 12.00 can be fetched from the following URL:
https://rtva.kavi.fi/teletext/page/choose/thisDate/date/01-01-2020/time/12:00:00/page/100/network/6/subpage/1

See crawler.py for details.

## Optical character recognition (OCR)

[Optical character recognition](https://en.wikipedia.org/wiki/Optical_character_recognition) (OCR) can be used to identify text from any kind of images where source text is not available.
Raw text data would have been preferred but I was unable to find old teletext pages in text format. Therefore, OCR was used to retrieve the words of interest from each page.

## Pre-processing

### Image manipulation
The Python [tesseract](https://pypi.org/project/pytesseract/) OCR library does not like coloured text or different font sizes. Each teletext page was preprocessed by 
1. cropping the area where news headlines are located
2. making the image black and white
3. inverting black and white

The last step was done since tesseract performs better on black text with white background (probably the pre-trained model has been trained on such data).

### Bag-of-words

## Word frequencies and TF-IDF

## Results