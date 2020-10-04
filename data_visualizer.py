"""This script generates visualizations from a .csv file produced by data_formatter.py."""

import ast
from collections import Counter
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer

stop_words = ['ei', 'taas', 'olla', 'ja', 'suomi', 'yhä', 'uusi', 'alkaa', 'jatkua', 'tänään', 'voitto', 'yle', 'tv2', 'klo']

def main():
    teletext_data_file = "teletext_data.csv"
    visualize_data(teletext_data_file)

def visualize_data(file_name: str):
    """Create visualizations (wordcloud, tf-idf scores) from given .csv file."""
    # read csv with converter to properly evaluate 'data' column which contains list of lists
    df = pd.read_csv(file_name, sep=";", converters={'data': lambda x: ast.literal_eval(x)})

    for year in df.year.unique():
        counts = _word_frequencies(df, year)
        _word_cloud(year, counts)

    # uncomment to run TF-IDF calculation
    # _tf_idf(df) 

def _word_cloud(year: int, counts: Counter, folder: str = "figures/wordclouds/"):
    """Create and save a wordcloud object from Counter."""
    wordcloud = WordCloud().generate_from_frequencies(counts)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    Path(folder).mkdir(parents=True, exist_ok=True)
    file_name = "wordcloud_" + str(year) + ".png"
    print("Saving wordcloud to file:", file_name)
    plt.savefig(folder+file_name)

def _word_frequencies(df: pd.DataFrame, year: int, stop_words: List[str] = stop_words) -> Counter:
    """Generate Counter object from dataframe for the given year. Given stopwords are removed."""
    df_year = df.loc[df['year'] == year]
    
    bag_of_words = _melt_sentences(df_year["data"])

    counts = Counter(bag_of_words)
    counts = _ignore_words(counts, stop_words)
    return counts

def _tf_idf(df: pd.DataFrame):
    """Print term frequency-document inverse frequency for each year."""
    corpus = _generate_corpus(df)

    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tf_idfs = vectorizer.fit_transform(corpus)
    tf_idf_df = pd.DataFrame(tf_idfs.T.todense(), index=vectorizer.get_feature_names(), columns=df.year.unique())

    for year in tf_idf_df:
        print(tf_idf_df[year].sort_values(ascending=False).head(10))
        print("-----------------")

def _generate_corpus(df: pd.DataFrame) -> List[str]:
    """Transform all words from each year to a string with space as separator."""
    corpus = []
    for year in df.year.unique():
        df_year = df.loc[df['year'] == year]
        bag_of_words = _melt_sentences(df_year["data"])
        corpus.append(" ".join(bag_of_words))
    return corpus

def _melt_sentences(series: pd.Series) -> List[str]:
    """Transform pandas Series containing list of lists into one list."""
    merged_words = []
    for list_of_sentences in series:
        flat_list = [word for sentence in list_of_sentences for word in sentence]
        merged_words.extend(flat_list)
    return merged_words

def _ignore_words(counts: Counter, words_to_ignore: List[str]) -> Counter:
    """Remove each word in words_to_ignore from Counter."""
    for word in words_to_ignore:
        if word in counts:
            del counts[word]
    return counts

if __name__ == "__main__":
    main()
