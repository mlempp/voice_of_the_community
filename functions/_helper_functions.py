'''
Autor: Martin Lempp

Kurzbeschreibung:
Hilfsfunktionen für die Analyse'''
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stemmer = SnowballStemmer("german")
stop_words = set(stopwords.words("german"))


def clean_text(txt):
    """
        - remove any html tags (< /br> often found)
        - Keep only ASCII + European Chars and whitespace, no digits
        - remove single letter chars
        - convert all whitespaces (tabs etc.) to single wspace
        if not for embedding (but e.g. tdf-idf):
        - all lowercase
        - remove stopwords, punctuation and stemm
    """
    RE_WSPACE = re.compile(r"\s+", re.IGNORECASE)
    RE_TAGS = re.compile(r"<[^>]+>")
    RE_ASCII = re.compile(r"[^A-Za-zÀ-ž ]", re.IGNORECASE)
    RE_SINGLECHAR = re.compile(r"\b[A-Za-zÀ-ž]\b", re.IGNORECASE)

    txt = re.sub(RE_TAGS, " ", txt)
    txt = re.sub(RE_ASCII, " ", txt)
    txt = re.sub(RE_SINGLECHAR, " ", txt)
    txt = re.sub(RE_WSPACE, " ", txt)

    word_tokens = word_tokenize(txt)
    words_tokens_lower = [word.lower() for word in word_tokens]

    words_filtered = [
        stemmer.stem(word) for word in words_tokens_lower if word not in stop_words
    ]

    text_clean = " ".join(words_filtered)
    return text_clean