from PIL import Image, ImageOps
from pytesseract import image_to_string
import re

def main():
    image_file = Image.open("data/2015/1/20150103.gif").convert('1').convert('RGB')
    image_file = ImageOps.invert(image_file)

    cropped_image = crop_image(image_file)

    image_text = image_to_string(cropped_image, lang='fin', config='--psm 1')
    preprocessed_text = preprocess_text(image_text)
    print(preprocessed_text)

def preprocess_text(text):
    text = re.sub('[^:äÄöÖåÅA-Za-z]',' ', text )
    text = text.lower()

    sentences = text.splitlines()
    sentences = [sentence.split(' ') for sentence in sentences]

    words = [word for words in sentences for word in words if word != '']
    return words

def crop_image(image):
    w, h = image.size

    expected_w = 480
    expected_h = 360
    if w != expected_w:
        print("Warning, image width:", w, "differs from expected width:", expected_w)
    if h != expected_h:
        print("Warning, image height:", h, "differs from expected height:", expected_h)

    cropped_image = image.crop((50, 80, w, h-110))
    w_cropped, h_cropped = cropped_image.size
    return cropped_image.resize((w_cropped, h_cropped))

if __name__ == "__main__":
    main()
