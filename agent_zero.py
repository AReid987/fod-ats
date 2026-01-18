

import argparse
import json
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources (only first time)
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords')
    nltk.download('wordnet')

def extract_keywords(text, min_occurrence=3, semantic_grouping=True):
    """Extract and analyze keywords from text"""
    # Preprocess text
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    # Filter and lemmatize
    filtered = [lemmatizer.lemmatize(w) for w in words 
                if w not in stop_words and len(w) > 2]
    
    # Count occurrences
    counter = Counter(filtered)
    keywords = {word: count for word, count in counter.items() 
                if count >= min_occurrence}
    
    # Semantic grouping (placeholder for future enhancement)
    if semantic_grouping:
        groups = {}
        for word in keywords:
            # Simple grouping by first letter for now
            group_key = word[0].upper()
            groups.setdefault(group_key, []).append(word)
        return groups
    return keywords

def main():
    parser = argparse.ArgumentParser(description='Agent Zero: Keyword Extraction')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--params', default='{}', help='JSON parameters')
    
    args = parser.parse_args()
    params = json.loads(args.params)
    
    # Read input file
    with open(args.input, 'r') as f:
        text = f.read()
    
    # Process text
    result = extract_keywords(
        text,
        min_occurrence=params.get('min_occurrence', 3),
        semantic_grouping=params.get('semantic_grouping', True)
    )
    
    # Save output
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Keyword extraction complete. Output: {args.output}")

if __name__ == '__main__':
    main()

