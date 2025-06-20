import nltk
from textblob import download_corpora

def download_corpora_files():
    nltk.download('movie_reviews')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    download_corpora.download_all()

if __name__ == "__main__":
    download_corpora_files()
