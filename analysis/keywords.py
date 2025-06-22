from textblob import TextBlob, download_corpora
from textblob.exceptions import MissingCorpusError

def extract_keywords(text):
    try:
        blob = TextBlob(text)
        return ", ".join(blob.noun_phrases)
    except MissingCorpusError:
        download_corpora.download_all()
        blob = TextBlob(text)
        return ", ".join(blob.noun_phrases)
