"""Contains functions for retrieving pre-processed words from one teletext frontpage image.

See instructions in words_from_image()
"""

import re
from typing import List, Tuple

import pytesseract
from PIL import Image, ImageOps
from libvoikko import Voikko

# these settings only work in Windows environment
Voikko.setLibrarySearchPath("C:/python37/DLLs")
voikko = Voikko("fi-x-morphoid")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def words_from_image(filename: str) -> List[List[str]]:
    """Retrieve pre-processed words from given 'filename' containing teletext frontpage image.

    Return value is a list of lists
    e.g. [['word1', 'word2'], ['word1', 'word2', 'word3']]
    """

    # make image black and white
    image = Image.open(filename).convert('1').convert('RGB')

    # invert black and white
    image = ImageOps.invert(image)

    # crop area which contains only news headlines
    w, h = image.size
    area_to_crop = (50, 80, w, h-110) # (left, upper, right, lower)
    cropped_image = _crop_image(image, w, h, area_to_crop)

    # perform optical character recognition (OCR)
    image_text = pytesseract.image_to_string(cropped_image, lang='fin', config='--psm 1')

    # pre-process text found from image
    preprocessed_text = _preprocess_text(image_text)
    return preprocessed_text

def _preprocess_text(text: str) -> List[List[str]]:
    """Pre-process text produced by tesseract

    Input text is raw text with line changes and spaces, e.g.
    'Imatralla paloi rengasvarasto
    Puolueiden vastattava Kataiselle'

    Return value is a list of lists with lowercased and baseformed words, e.g.
    [['imatra', 'palaa', 'rengasvarasto'], ['puolue', 'vastata', 'katainen']]
    """

    # replace all except characters_to_keep with space
    characters_to_keep = '[^\n:-äÄöÖåÅA-Za-z0-9]'
    text = re.sub(characters_to_keep,' ', text )

    # split the whole text to list of strings
    sentences = text.splitlines()

    # split each string further to list of words
    sentences = [sentence.split(' ') for sentence in sentences if sentence.strip()]

    words = _analyze_sentences(sentences)
    return words

def _analyze_sentences(sentences: List[List[str]]) -> List[List[str]]:
    """Stem words into their base form if applicable.

    e.g. 'lähti' is transformed into 'lähteä'
    However, e.g. 'obaman' is kept as 'obaman' since Voikko does not recognize foreign word stems
    """
    baseform_sentences = []
    for sentence in sentences:
        baseform_words = []
        sentence = _repair_broken_j_words(sentence)
        for word in sentence:
            if not word: # skip empty words
                continue

            analyzed_word = voikko.analyze(word)
            if analyzed_word: # 'None' if voikko does not recognize word
                # limitation: given multiple baseforms, this will always pick the first one
                baseform_word = analyzed_word[0]["BASEFORM"]
                word = baseform_word

            # remove ':' only at this point since it was needed for Voikko checking
            baseform_words.append(word.lower().replace(":", ""))

        baseform_sentences.append(baseform_words)

    return baseform_sentences

def _repair_broken_j_words(sentence: List[List[str]]) -> List[List[str]]:
    """Repair broken words caused by malfunctioning OCR

    Tesseract seems to erroneously cut words containing letter 'j' in the middle.
    For example, word 'Norja' is recognized as 'Nor' and 'ja'.

    This function attempts to repair such words by combining words beginning with 'j'
    with the previous word.

    TODO: Calling this function is sub-optimal because each sentence is looped twice
    Optimize this so that word repairing is done already in the upper function
    """
    if len(sentence) < 2:
        return sentence

    repaired_sentence = []
    skip = False

    # loop from last word to first word
    for word_index in range((len(sentence)-1), 0, -1):
        if skip:
            skip = False
            continue

        word = sentence[word_index]
        if not word.startswith("j"):
            repaired_sentence.append(word)
            continue

        # check if word beginning with 'j' combined with previous word produces legal Finnish word
        combined_word = sentence[word_index-1] + sentence[word_index]
        if voikko.analyze(combined_word):
            repaired_sentence.append(combined_word)
            skip = True
        else:
            repaired_sentence.append(word)

    repaired_sentence.append(sentence[0])
    return reversed(repaired_sentence)

def _crop_image(image: Image, w: int, h: int, area_to_crop: Tuple[int]) -> Image:
    """Crop and return the wanted area from image."""
    expected_w = 480
    expected_h = 360
    if w != expected_w:
        print("Warning, image width:", w, "differs from expected width:", expected_w)
    if h != expected_h:
        print("Warning, image height:", h, "differs from expected height:", expected_h)

    cropped_image = image.crop(area_to_crop)
    w_cropped, h_cropped = cropped_image.size
    return cropped_image.resize((w_cropped, h_cropped))

def main():
    """See output from one file for testing purposes. Normally one should call words_from_image()"""
    filename = "data/2009/4/20090423.gif"
    words = words_from_image(filename)
    print(words)

if __name__ == "__main__":
    main()
