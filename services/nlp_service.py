import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string
import os

nltk_data_path = os.path.join(os.path.dirname(__file__), '..', 'nltk_data')
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)
nltk.data.path.append(nltk_data_path)

def ensure_nltk_data():
    """Download required NLTK data if not present."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', download_dir=nltk_data_path, quiet=True)
    
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', download_dir=nltk_data_path, quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', download_dir=nltk_data_path, quiet=True)


def extract_keywords(text, num_keywords=5):
    """Extract top keywords from text using NLTK tokenization."""
    ensure_nltk_data()
    
    try:
        tokens = word_tokenize(text.lower())
    except Exception:
        tokens = text.lower().split()
    
    try:
        stop_words = set(stopwords.words('english'))
    except Exception:
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                      'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                      'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                      'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
                      'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
                      'through', 'during', 'before', 'after', 'above', 'below',
                      'between', 'under', 'again', 'further', 'then', 'once',
                      'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either',
                      'neither', 'not', 'only', 'own', 'same', 'than', 'too',
                      'very', 'just', 'also', 'now', 'here', 'there', 'when',
                      'where', 'why', 'how', 'all', 'each', 'every', 'both',
                      'few', 'more', 'most', 'other', 'some', 'such', 'no',
                      'any', 'this', 'that', 'these', 'those', 'it', 'its'}
    
    filtered_tokens = [
        token for token in tokens 
        if token not in stop_words 
        and token not in string.punctuation
        and len(token) > 2
        and token.isalpha()
    ]
    
    if not filtered_tokens:
        return ["study", "learn", "practice", "review", "understand"]
    
    freq_dist = FreqDist(filtered_tokens)
    
    keywords = [word for word, freq in freq_dist.most_common(num_keywords)]
    
    return keywords if keywords else ["study", "learn", "practice"]


def generate_study_tips(text, subject="general"):
    """Generate study tips based on extracted keywords."""
    keywords = extract_keywords(text)
    
    tip_templates = [
        "Focus on understanding {keyword} concepts thoroughly before moving on.",
        "Create flashcards for {keyword} terminology to improve retention.",
        "Practice {keyword} problems daily to build confidence.",
        "Connect {keyword} to real-world examples for better understanding.",
        "Review {keyword} notes within 24 hours of learning.",
        "Teach {keyword} concepts to someone else to deepen your understanding.",
        "Use diagrams and visual aids when studying {keyword}.",
        "Break down complex {keyword} topics into smaller, manageable parts.",
        "Set specific goals for mastering {keyword} each week.",
        "Take short breaks while studying {keyword} to maintain focus."
    ]
    
    tips = []
    for i, keyword in enumerate(keywords[:5]):
        template = tip_templates[i % len(tip_templates)]
        tips.append(template.format(keyword=keyword))
    
    general_tips = [
        f"Allocate dedicated study time for {subject} each day.",
        "Use active recall techniques instead of passive reading.",
        "Get enough sleep to help consolidate what you've learned.",
        "Stay hydrated and take regular breaks during study sessions.",
        "Review material multiple times using spaced repetition."
    ]
    
    while len(tips) < 5:
        tips.append(general_tips[len(tips) % len(general_tips)])
    
    return {
        "keywords": keywords,
        "tips": tips,
        "subject": subject
    }


def analyze_text_complexity(text):
    """Analyze text complexity for quiz difficulty classification."""
    ensure_nltk_data()
    
    try:
        sentences = sent_tokenize(text)
    except Exception:
        sentences = text.split('.')
    
    try:
        words = word_tokenize(text)
    except Exception:
        words = text.split()
    
    num_sentences = len(sentences)
    num_words = len(words)
    avg_sentence_length = num_words / max(num_sentences, 1)
    
    long_words = [w for w in words if len(w) > 6]
    long_word_ratio = len(long_words) / max(num_words, 1)
    
    if avg_sentence_length > 20 or long_word_ratio > 0.3:
        difficulty = "hard"
    elif avg_sentence_length > 12 or long_word_ratio > 0.2:
        difficulty = "medium"
    else:
        difficulty = "easy"
    
    return {
        "num_sentences": num_sentences,
        "num_words": num_words,
        "avg_sentence_length": round(avg_sentence_length, 2),
        "long_word_ratio": round(long_word_ratio, 2),
        "suggested_difficulty": difficulty
    }
