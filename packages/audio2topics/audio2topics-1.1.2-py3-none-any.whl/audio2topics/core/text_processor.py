#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Processor module for the Audio to Topics application.
Provides functionality for text cleaning and analysis.
"""

import re
import logging
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import Counter

import spacy
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QMutex

# Configure logging
logger = logging.getLogger(__name__)

class TextProcessorWorker(QThread):
    """Worker thread for text processing"""
    progress_updated = pyqtSignal(int, str)
    processing_completed = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, documents, language='english'):
        super().__init__()
        self.documents = documents
        self.language = language
        
    def run(self):
        """Execute the text processing"""
        try:
            self.progress_updated.emit(5, "Starting text processing...")
            
            # Check if input is a single string or list
            if isinstance(self.documents, str):
                self.documents = [self.documents]
                
            total_docs = len(self.documents)
            
            # Download NLTK resources if needed
            self.progress_updated.emit(10, "Checking NLTK resources...")
            download_nltk_resources()
            
            # Load SpaCy model
            self.progress_updated.emit(20, f"Loading SpaCy model for {self.language}...")
            try:
                nlp = load_spacy_model(self.language)
            except Exception as e:
                self.error_occurred.emit(f"Error loading SpaCy model: {str(e)}")
                return
            
            self.progress_updated.emit(30, "Processing documents...")
            
            # Process each document
            cleaned_docs = []
            for i, doc in enumerate(self.documents):
                if not doc.strip():
                    continue  # Skip empty documents
                    
                # Update progress
                progress = 30 + (i / total_docs * 60)
                self.progress_updated.emit(int(progress), f"Processing document {i+1}/{total_docs}...")
                
                # Clean the document
                cleaned_doc = clean_text(doc, self.language, nlp)
                if cleaned_doc.strip():  # Only add if not empty
                    cleaned_docs.append(cleaned_doc)
            
            self.progress_updated.emit(95, "Finalizing processing...")
            self.processing_completed.emit(cleaned_docs)
            self.progress_updated.emit(100, "Text processing complete!")
            
        except Exception as e:
            logger.error(f"Text processing error: {str(e)}", exc_info=True)
            self.error_occurred.emit(f"Error during text processing: {str(e)}")


# Global mutex for SpaCy model loading
spacy_mutex = QMutex()

# Cache for SpaCy models
spacy_models = {}

def download_nltk_resources():
    """Download necessary NLTK resources if not already available"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)


def load_spacy_model(language):
    """
    Load SpaCy model with caching and thread safety.
    
    Args:
        language (str): Language for the model ('english' or 'norwegian')
        
    Returns:
        spaCy model: Loaded model
    """
    global spacy_models
    
    # Map language name to SpaCy model name
    model_name = {
        'english': 'en_core_web_sm',
        'norwegian': 'nb_core_news_sm'
    }.get(language)
    
    if not model_name:
        raise ValueError(f"Unsupported language: {language}")
    
    # Thread-safe model loading
    spacy_mutex.lock()
    try:
        if model_name not in spacy_models:
            spacy_models[model_name] = spacy.load(model_name)
        return spacy_models[model_name]
    finally:
        spacy_mutex.unlock()


def clean_text(text, language='english', nlp=None):
    """
    Clean text by removing stopwords, special characters, and applying stemming/lemmatization.
    
    Args:
        text (str): Text to clean
        language (str): Language for text processing
        nlp (spaCy model): Pre-loaded SpaCy model (optional)
        
    Returns:
        str: Cleaned text
    """
    # Handle list input
    if isinstance(text, list):
        return [clean_text(doc, language, nlp) for doc in text]

    # Load SpaCy model if not provided
    if nlp is None:
        nlp = load_spacy_model(language)
    
    # Load stopwords
    try:
        stop_words = set(stopwords.words(language))
    except:
        logger.warning(f"No stopwords available for {language}, using empty set")
        stop_words = set()
    
    # Load stemmer
    try:
        stemmer = SnowballStemmer(language)
    except:
        logger.warning(f"No stemmer available for {language}, skipping stemming")
        stemmer = None
        
    # Remove emails
    text = re.sub(r'\S*@\S*\s?', '', text)

    # Lowercase and remove special characters and numbers
    text = re.sub(r'\W+', ' ', text.lower())
    text = re.sub(r'\d+', '', text)

    # Tokenize the text
    # Tokenize the text using SpaCy instead of NLTK
    doc = nlp(text)
    tokens = [token.text for token in doc]
    # Remove stopwords and apply stemming if available
    if stemmer:
        tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    else:
        tokens = [word for word in tokens if word not in stop_words]

    # Lemmatize using SpaCy
    doc = nlp(' '.join(tokens))
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

    return ' '.join(lemmatized_tokens)


def calculate_text_statistics(text, language='english'):
    """
    Calculate text statistics such as word count, sentence count, etc.
    
    Args:
        text (str): Text to analyze
        language (str): Language for text processing
        
    Returns:
        list: List of tuples with statistic name and value
    """
    nlp = load_spacy_model(language)
    doc = nlp(text)
    
    # Basic counts
    sentences = list(doc.sents)
    num_sentences = len(sentences)
    
    tokens = [token.text for token in doc if not token.is_punct]
    num_tokens = len(tokens)
    
    num_unique_words = len(set(tokens))
    
    words = [token.text for token in doc if not token.is_punct and not token.is_stop]
    num_words = len(words)
    
    stop_words = [token.text for token in doc if token.is_stop]
    num_stop_words = len(stop_words)
    
    # Averages
    avg_sentence_length = num_tokens / num_sentences if num_sentences else 0
    
    # Word frequency
    freq_dist = Counter(tokens)
    most_common_words = freq_dist.most_common(10)
    
    # Character statistics
    num_chars = len(text)
    avg_word_length = sum(len(word) for word in tokens) / len(tokens) if tokens else 0

    # Compile stats
    stats = [
        ('Number of sentences', num_sentences),
        ('Number of tokens', num_tokens),
        ('Number of unique words', num_unique_words),
        ('Number of words (excluding stopwords)', num_words),
        ('Number of stop words', num_stop_words),
        ('Average sentence length', round(avg_sentence_length, 2)),
        ('Most common words', most_common_words),
        ('Number of characters', num_chars),
        ('Average word length', round(avg_word_length, 2)),
    ]
    
    return stats


class TextProcessor(QObject):
    """
    Handles text processing operations.
    
    This class manages text cleaning, analysis, and statistics calculation
    using a worker thread for processing to keep the UI responsive.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        
    def process_text(self, documents, language='english'):
        """
        Start processing documents.
        
        Args:
            documents: String or list of strings to process
            language: Language for text processing
            
        Returns:
            QThread: The worker thread processing the text
            
        Note:
            This method starts a worker thread. Results will be emitted via signals.
        """
        # Create and configure worker
        self.worker = TextProcessorWorker(documents, language)
        
        # Clean up when done
        self.worker.finished.connect(self.worker.deleteLater)
        
        # Start the worker
        self.worker.start()
        
        return self.worker
    
    def get_available_languages(self):
        """
        Get available languages for text processing.
        
        Returns:
            List of supported languages
        """
        # Return languages with both NLTK and SpaCy support
        return ["english", "norwegian"]
    
    def get_text_statistics(self, text, language='english'):
        """
        Calculate text statistics synchronously.
        
        Args:
            text: Text to analyze
            language: Language for text processing
            
        Returns:
            List of tuples with statistic name and value
        """
        return calculate_text_statistics(text, language)

