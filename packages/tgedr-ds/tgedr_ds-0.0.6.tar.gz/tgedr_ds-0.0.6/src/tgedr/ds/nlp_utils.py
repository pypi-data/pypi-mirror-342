"""
Module Name: 
Description: code utils for NLP
Author:
Date:
Version:

Dependencies:
- ...

Environment Variables:
- ...

Usage:
    >>> from tgedr.ds.pytorch.utils import get_device
    >>> DEVICE = get_device()
    >>> print(DEVICE.type)
    mps

"""
from enum import Enum
from typing import Any

import spacy


class NounNumber(Enum):
    """
    Utility enum for noun numbering
    """

    SINGULAR = 1
    PLURAL = 2


class UtilsNlp:
    """
    Utility class for NLP tasks.
    """

    def __init__(self):
        """
        Initialize the NLP utility class.
        """
        self._nlp = spacy.load("en_core_web_sm")

    @property
    def model(self) -> Any:
        """
        Get the NLP model.

        Returns:
            spacy.Language: The loaded NLP model.
        """
        return self._nlp

    @model.setter
    def model(self, value: Any):
        if not value:
            raise ValueError("model cannot be empty")
        self._nlp = value

    def text2sentences(self, text):
        """
        text is broken down to sentences

        Args:
            text (str): The input text.

        Returns:
            list: A list of sentences.
        """
        doc = self.model(text)
        return [sentence.text for sentence in doc.sents]

    def tokenize(self, text):
        """
        Tokenize the input text.

        Args:
            text (str): The input text to tokenize.

        Returns:
            list: A list of tokens.
        """
        doc = self.model(text)
        return [token.text for token in doc]

    def tag_words(self, text, model=None):
        """
        tag the words in the input text.

        Args:
            text (str): The input text.

        Returns:
            list: A list of tuples with the word and the tag.
        """
        _model = model if model else self.model
        doc = _model(text)
        words = [token.text for token in doc]
        pos = [token.pos_ for token in doc]
        return list(zip(words, pos))

    def lemmatize(self, text):
        """
        Lemmatize the input text.

        Args:
            text (str): The input text.

        Returns:
            list: A list of tuples with the word and its lemma.
        """
        result = []
        doc = self.model(text)
        for token in doc:
            result.append((token, token.lemma_))

        return result

    def remove_stopwords(self, text):
        """
        removes stop words from the input text.

        Args:
            text (str): The input text.

        Returns:
            list: A list of tuples with the word and its lemma.
        """
        stopwords = self.model.Defaults.stop_words

        result = []
        words = self.tokenize(text)
        print(len(words))
        result = [word for word in words if word.lower() not in stopwords]
        print(len(result))

        return result

    # def get_nouns_number(text, model, method="lemma"):
    #     nouns = []
    #     doc = model(text)
    #     for token in doc:
    #     if (token.pos_ == "NOUN"):
    #     if method == "lemma":
    #     if token.lemma_ != token.text:
    #     nouns.append((token.text,
    #     Noun_number.PLURAL))
    #     else:
    #     nouns.append((token.text,
    #     Noun_number.SINGULAR))
    #     elif method == "morph":
    #     if token.morph.get("Number") == "Sing":
    #     nouns.append((token.text,
    #     Noun_number.PLURAL))
    #     else:
    #     nouns.append((token.text,
    #     Noun_number.SINGULAR))
    #     return nouns
