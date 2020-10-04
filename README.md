# Mistä puhutaan?: YLE Teksti-tv frontpage topical analysis 2009-2020

## Project in a nutshell
The idea in this project was to find out the most common news topics per year according to the only true media authority: [YLE Teksti-tv](https://yle.fi/aihe/tekstitv)

To cut the chase, go directly to [Results](https://github.com/vkolehmainen/mista-puhutaan#results) section and check out the wordclouds.

## Python module descriptions
See below the descriptions for Python modules that can be ran to re-produce the findings. The pre-processed data and wordclouds are already available in this repository though so there is no need for running any code if you just want to check out the findings.
* crawler.py: Run to crawl teletext images from given date range
* data_formatter.py: Preprocess and store the data from crawled images to a single CSV file 
* data_visualizer.py: Visualize the data from the CSV file produced by data_formatter.py into wordclouds

## Crawling the data
The teletext front page for each was date from 21.04.2009 to 17.03.2020 was crawled from [RITVA database](https://rtva.kavi.fi/)

For example, the teletext front page from 01.01.2020 at 12.00 can be fetched from the following URL:
https://rtva.kavi.fi/teletext/page/choose/thisDate/date/01-01-2020/time/12:00:00/page/100/network/6/subpage/1

See [crawler.py](https://github.com/vkolehmainen/mista-puhutaan/blob/master/crawler.py) for details.

## Pre-processing

### Image manipulation

[Optical character recognition](https://en.wikipedia.org/wiki/Optical_character_recognition) (OCR) can be used to identify text from any kind of images where source text is not available but there are recognizable characters in the image. Raw text data would have been preferable but I was unable to find old teletext pages in text format. Therefore, OCR was used to retrieve the words of interest from each page.

The Python [tesseract](https://pypi.org/project/pytesseract/) OCR library does not like coloured text or different font sizes. Each teletext page was preprocessed by 
1. cropping the area where news headlines are located
2. making the image black and white
3. inverting black and white

The last step was done since tesseract performs better on black text with white background (probably the pre-trained model has been trained on such data).

After the steps mentioned above we go from the raw image on the left to the preprocessed image on the right:
<p>
  <img src="https://github.com/vkolehmainen/mista-puhutaan/blob/master/figures/examples/20090423.gif" alt="raw image" width="200"/>
  <img src="https://github.com/vkolehmainen/mista-puhutaan/blob/master/figures/examples/20090423_preprocessed.gif" alt="preprocessed image" width="200"/>
</p>

### Sentence and word pre-processing

Tesseract returns the text it finds in a string where the arrangement of the text is preserved. For example, two news headlines on separate lines would be returned as:  
> 'Imatralla paloi rengasvarasto  
> Puolueiden vastattava Kataiselle'

data_preprocessor.py transforms the raw text data from the above format to a list of lists like this:
> [['imatra', 'palaa', 'rengasvarasto'], ['puolue', 'vastata', 'katainen']]

Each word is transformed into lowercase and unwanted symbols (e.g. !,?,%) are removed. In addition, words which are recognized as proper Finnish words are [stemmed](https://en.wikipedia.org/wiki/Stemming) to their basic form using language analyzing library [Voikko](https://pypi.org/project/voikko/). For example, in the above case word 'Imatralla' was transformed into 'imatra'.

### Pre-processed data

Pre-processed data from each teletext front page was stored to a CSV file with the following format:

| year | month | day |   data  |
| ---- |:----: |:---:|:------:|
| 2009 | 10    | 01  | [[word1, word2], [word1, word2, word3], ... [word1, word2]]
| 2009 | 10    | 02  | [[word1, word2, word3], [word1, word2], ... [word1, word2]]
| 2009 | 10    | 03  | [[word1, word2], [word1, word2, word3], ... [word1, word2, word3]]

In the data column, the words from each news headline from the given date are stored in a list of lists. 

## Results

### Wordclouds

A wordcloud is an illustration for word frequencies in a given text document. The larger the font for a given word, the more appearances it has throughout the document. In this case one document entails all Teksti-tv front pages from a given year.

See below an example word cloud from the year 2009:
<p float="left">
  <img src="https://github.com/vkolehmainen/mista-puhutaan/blob/master/figures/wordclouds/wordcloud_2009.png" alt="2009" width="400"/>
</p>

See all wordclouds in: https://imgur.com/a/dZJ26vw or directly in this repository: [figures/wordclouds](https://github.com/vkolehmainen/mista-puhutaan/tree/master/figures/wordclouds)

### Remarks about the results

There are some anomalies in the results such as the word 'kuoltu' appearing as very popular in the wordcloud for year 2011. This is due to a limitation in the code because of which the first baseform of a word is always picked if there are multiple offered by Voikko library. This could be fixed by improving the data_preprocessor.py script so that user can pick the baseform which makes the most sense if there are multiple baseforms offered. 
