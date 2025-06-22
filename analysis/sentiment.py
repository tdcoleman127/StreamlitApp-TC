from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_textblob(text):
    return TextBlob(text).sentiment.polarity

def analyze_vader(text):
    return analyzer.polarity_scores(text)['compound']
