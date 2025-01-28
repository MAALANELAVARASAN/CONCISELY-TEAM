import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import string

nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, num_sentences=3):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize the text into words
    words = word_tokenize(text.lower())
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words and word not in string.punctuation]
    
    # Calculate word frequencies
    word_frequencies = Counter(words)
    
    # Normalize word frequencies
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency
    
    # Score sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]
    
    # Sort sentences by their scores
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    
    # Join the summarized sentences
    summary = ' '.join(summarized_sentences)
    return summary

# Example Usage
text = """Natural Language Processing (NLP) is a sub-field of artificial intelligence (AI) that focuses on the interaction between computers and humans through natural language. 
The ultimate objective of NLP is to enable computers to understand, interpret, and generate human language in a way that is both meaningful and useful. 
Techniques in NLP are being widely used across various applications such as chatbots, language translation, sentiment analysis, and more."""
summary = summarize_text(text, num_sentences=2)
print("Summary:")
print(summary)
