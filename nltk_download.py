#nltk_download
import nltk

def download_nltk_resources():
    required_resources = ['averaged_perceptron_tagger', 'vader_lexicon', 'punkt', 'words', 'maxent_ne_chunker' ]  # Add all required resources
    for resource in required_resources:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(resource)

download_nltk_resources()