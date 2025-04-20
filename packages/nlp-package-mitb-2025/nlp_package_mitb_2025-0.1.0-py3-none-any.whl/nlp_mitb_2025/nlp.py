import re
import random
from collections import Counter
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')
nltk.download('stopwords')

class NLP_MITB_2025:

   
    def split_text(self , text): 
        return re.findall(r'\b\w+\b', text)

    def extract_dates(self , text): 
        return re.findall(r'\b\d{2}/\d{2}/\d{4}\b|\b\d{2}-\d{2}-\d{4}\b', text)
    
    def extract_phones(self , text): 
        return re.findall(r'\+91-\d{10}|\d{3}-\d{3}-\d{4}|\(\d{3}\)\s\d{3}-\d{4} ', text)
    
    def clean_text(self , text): 
        return re.sub(r'^\W+|\W+$', '', text)

    def count_non_alnum(self , text): 
        return len(re.findall(r'\W', text))
    
    def replace_non_alnum(self, s, ch): 
        return re.sub(r'\W', ch, s)
    
    def split_pairs(self , word): 
        return [(word[:i], word[i:]) for i in range(1, len(word))]
    
    def prefixes_suffixes(self , word): 
        return [word[:i] for i in range(1, len(word)+1)], [word[i:] for i in range(len(word))]
    
    def random_split(self , word): 
        i = random.randint(1, len(word)-1)
        return (word[:i], word[i:])
    
    def ngram_frequencies(text, n): 
        return Counter(ngrams(text.split(), n))
    
    def ngram_probabilities(text, n):
        words = text.split()
        ngram_counts = Counter(ngrams(words, n))
        total_ngrams = sum(ngram_counts.values())
        return {ngram: count / total_ngrams for ngram, count in ngram_counts.items()}
    
    def reverse_ngrams(text, n): 
        return list(ngrams(text.split()[::-1], n))
    
    def remove_digits(sentence): 
        return ' '.join(w for w in word_tokenize(sentence) if not w.isdigit())
    
    def count_digits(sentence): 
        return sum(len(w) for w in word_tokenize(sentence) if w.isdigit())
    
    def extract_digits(sentence): 
        word = word_tokenize(sentence)
        ans = []
        for w in word: 
            if w.isdigit():
                ans.extend(list(w))
        print(ans)

    def custom_tokenizer(sentence):
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4}|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        special_tokens = re.findall(pattern, sentence)
        remaining_text = re.sub(pattern, ' ', sentence)
        return special_tokens + word_tokenize(remaining_text)
    
    def clean_tweet(text):
        cleaned = re.sub(r'#\w+|[^\w\s]| +', ' ', text).strip().lower()
        return cleaned
    
    def remove_emojis(text):

        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
            "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
            "\U0001F1E0-\U0001F1FF"  # Flags
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"  # Enclosed characters
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', text)
    
    def normalize(text):
        return ' '.join(text.lower().split())
    
    
    def extract_dates(text):
    
        # Regular expression pattern to match different date formats
        pattern = r'\b\d{2}/\d{2}/\d{4}\b'           # Matches 'DD/MM/YYYY'
        pattern += r'|\b\d{2}-\d{2}-\d{4}\b'         # Matches 'MM-DD-YYYY'
        pattern += r'|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}\b'  # Matches 'Month DD, YYYY'

        # Find all matches in the text
        dates = re.findall(pattern, text)
        return dates

    def extract_and_standardize(text):
        pattern = r'(\+91[\-\s]?|91[\-\s]?|\(?\+91\)?[\s\-]?|0)?(\d{5})[\s\-]?(\d{5})'
        matches = re.findall(pattern, text)
        print(matches)
        return [f'+91-{m[1]}{m[2]}' for m in matches]
    
    
    def process_text(text):

        # Tokenize the text
        tokens = word_tokenize(text)

        # Initialize stemmer and lemmatizer
        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()

        # Apply stemming
        stems = [stemmer.stem(word) for word in tokens]

        # Apply lemmatization
        lemmas = [lemmatizer.lemmatize(word) for word in tokens]

        return {
            'Original': tokens,
            'Stemming': stems,
            'Lemmatization': lemmas
        }
        


    

    
    
    
