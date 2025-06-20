from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def vader_score(text):
    if text:
        return round(analyzer.polarity_scores(text)['compound'], 3)
    return 0.0

test_favorites = [
    "I really liked the clean layout.",
    "The layout.",
    "Simple design, but a bit bland.",
    "Love the icons and smooth animations.",
    "It worked as expected.",
    "Good structure but missing personality."
]

for text in test_favorites:
    score = vader_score(text)
    print(f"\"{text}\" → {score}")
