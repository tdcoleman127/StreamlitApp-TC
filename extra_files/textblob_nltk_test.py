import nltk
from textblob import TextBlob

# Point to your local corpora folder if needed
nltk.data.path.append("./assets/nltk_data")

# Sample text for analysis
sample_text = "This is the worst experience I've had with an app."

# Create a TextBlob object
blob = TextBlob(sample_text)

# Output sentiment
print("Sentiment polarity:", blob.sentiment.polarity)
print("Sentiment subjectivity:", blob.sentiment.subjectivity)
