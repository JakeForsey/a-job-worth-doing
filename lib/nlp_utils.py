"""
Jake Forsey
15/02/2018

Utilities for preparing free text data for Natural Language Possessing (NLP)
"""

import nltk

import string
import re


class NLTKProcessor:
    def __init__(self,
                 stemmer=nltk.PorterStemmer(),
                 stop_words=nltk.corpus.stopwords.words('english')):

        self.stemmer = stemmer

        # Dont include 'it' as a stop word as IT is an important word for job postings
        self.stop_words = list(set(stop_words) - set('it'))

    def process(self, sentence):
        # remove urls
        sentence = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', sentence)

        # remove punctuation
        sentence = sentence.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

        # split sentences into lists of words
        word_list = nltk.word_tokenize(sentence)

        # turn words into stems (e.g running -> run, lying -> lie)
        if self.stemmer:
            word_list = [self.stemmer.stem(word) for word in word_list]

        word_list = [word.lower() for word in word_list]

        # remove stop (low value) words
        if self.stop_words:
            word_list = [word for word in word_list if word not in self.stop_words]

        return " ".join(word_list)
