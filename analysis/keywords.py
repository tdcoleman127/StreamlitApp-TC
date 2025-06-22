from textblob import TextBlob

def extract_keywords(text):
    blob = TextBlob(text)
    return ", ".join(blob.noun_phrases)  # Returns a comma-separated string of keywords
