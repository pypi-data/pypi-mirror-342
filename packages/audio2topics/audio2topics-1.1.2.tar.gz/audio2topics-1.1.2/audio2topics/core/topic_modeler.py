#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Topic Modeler module for the Audio to Topics application.
Provides functionality for extracting topics from text using BERTopic.
"""

import logging
from typing import List, Dict, Tuple, Any, Optional
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from sentence_transformers import SentenceTransformer
from umap import UMAP
from sklearn.decomposition import PCA, NMF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
import hdbscan

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox
import datetime
import pickle
import os

# Configure logging
logger = logging.getLogger(__name__)

class TopicModelingWorker(QThread):
    """Worker thread for topic modeling"""
    progress_updated = pyqtSignal(int, str)
    topics_extracted = pyqtSignal(object, object, object, object, object, object)  # topics, probs, topics_words, topic_info, model, chunked_docs
    error_occurred = pyqtSignal(str)
    
    # Add this new signal for the elbow method dialog
    show_elbow_dialog = pyqtSignal(list, list)  # model_scores, topics_range
    elbow_selection_result = None  # To store the dialog result
   
    def __init__(self, documents, language="multilingual", n_gram_range=(1, 2), 
                min_topic_size=2, nr_topics="auto", adaptive_enabled=True,
                max_retries=5, initial_chunk_size=100, method="bertopic",
                lda_elbow_enabled=False, lda_elbow_params=None):
        super().__init__()
        self.documents = documents
        self.language = language
        self.n_gram_range = n_gram_range
        self.min_topic_size = min_topic_size
        self.nr_topics = nr_topics
        self.model = None
        
        # Adaptive processing parameters
        self.adaptive_enabled = adaptive_enabled
        self.max_retries = max_retries
        self.initial_chunk_size = initial_chunk_size
        
        # Topic modeling method
        self.method = method  # "bertopic", "bertopic-pca", "nmf", or "lda"
        # LDA elbow method parameters
        self.lda_elbow_enabled = lda_elbow_enabled
        self.lda_elbow_params = lda_elbow_params or {}
        
        # Add a flag to track elbow dialog cancellation
        self.elbow_selection_result = None
        self.elbow_selection_cancelled = False
        
        # Apply document chunking if we have too few documents
        if len(self.documents) < 2 and self.adaptive_enabled:
            self.documents = self._rechunk_documents(self.documents, self.initial_chunk_size)
            self.progress_updated.emit(15, f"Split document into {len(self.documents)} chunks")
        
    def run(self):
        """Execute the topic modeling with fallback methods"""
        try:
            self.progress_updated.emit(5, "Initializing topic modeling...")
            
            # Check if we have enough documents
            if len(self.documents) < 2:
                self.error_occurred.emit("Insufficient data: Please provide more documents for topic modeling.")
                return
            
            # Update number of topics if needed
            num_documents = len(self.documents)
            if isinstance(self.nr_topics, int) and self.nr_topics >= num_documents:
                self.nr_topics = max(1, num_documents - 1)
                self.progress_updated.emit(10, f"Adjusting number of topics to {self.nr_topics} based on document count.")
            
            # Choose the topic modeling method
            if self.method == "bertopic":
                # Try standard BERTopic first
                success, result = self._try_bertopic_standard()
                
                # If standard BERTopic fails and adaptive is enabled, try with PCA
                if not success and self.adaptive_enabled:
                    self.progress_updated.emit(40, "Standard BERTopic failed, trying with PCA instead of UMAP...")
                    success, result = self._try_bertopic_pca()
                
                # If that still fails, try NMF as a last resort
                if not success and self.adaptive_enabled:
                    self.progress_updated.emit(60, "BERTopic with PCA failed, falling back to NMF...")
                    success, result = self._try_nmf()
            
            elif self.method == "bertopic-pca":
                # Try BERTopic with PCA directly
                success, result = self._try_bertopic_pca()
                
                # Fallback to NMF if it fails
                if not success and self.adaptive_enabled:
                    self.progress_updated.emit(50, "BERTopic with PCA failed, falling back to NMF...")
                    success, result = self._try_nmf()
            
            elif self.method == "nmf":
                # Use NMF directly
                success, result = self._try_nmf()
            
            elif self.method == "lda":
                # Use LDA directly
                success, result = self._try_lda()
            
            else:
                raise ValueError(f"Unknown topic modeling method: {self.method}")
            
            # Check if any method succeeded
            if not success:
                raise ValueError("All topic modeling approaches failed. Try with more documents or different settings.")
            
            # Extract results from the successful attempt
            self.model, topics, probs, topics_words, topic_info = result
            
            self.progress_updated.emit(95, "Topic modeling complete!")
            
            # Emit results - IMPORTANT: Include the documents (which might be chunks)
            self.topics_extracted.emit(topics, probs, topics_words, topic_info, self.model, self.documents)
            
            self.progress_updated.emit(100, "Done!")
            
        except Exception as e:
            logger.error(f"Topic modeling error: {str(e)}", exc_info=True)
            self.error_occurred.emit(f"Error during topic modeling: {str(e)}")
    
    def _try_bertopic_standard(self):
        """Try the standard BERTopic approach with UMAP"""
        try:
            self.progress_updated.emit(20, "Loading embedding model...")
            
            # Create representation model
            representation_model = KeyBERTInspired()
            
            # Start with conservative UMAP parameters
            doc_count = len(self.documents)
            n_neighbors = min(5, max(2, doc_count - 2))
            n_components = min(2, max(2, doc_count - 3))
            
            self.progress_updated.emit(30, "Creating BERTopic model with UMAP...")
            
            # Create a UMAP model with conservative parameters
            umap_model = UMAP(
                n_neighbors=n_neighbors,
                n_components=n_components,
                min_dist=0.0,
                metric='cosine',
                random_state=42
            )
            
            # Initialize BERTopic model
            topic_model = BERTopic(
                representation_model=representation_model,
                language=self.language,
                min_topic_size=self.min_topic_size,
                nr_topics=self.nr_topics,
                n_gram_range=self.n_gram_range,
                calculate_probabilities=True,
                umap_model=umap_model
            )
            
            self.progress_updated.emit(40, "Fitting model to documents...")
            
            # Use a try-except to properly handle the "list index out of range" error
            try:
                # Fit and transform the documents
                topics, probs = topic_model.fit_transform(self.documents)
                
                # Safely get topic info - handling potential errors
                try:
                    topic_info = topic_model.get_topic_info()
                    topics_words = topic_model.get_topics()
                except Exception as e:
                    logger.warning(f"Error getting topic info: {str(e)}")
                    # Create dummy topic info
                    topic_info = {"Topic": [-1], "Count": [len(self.documents)], "Name": ["All Documents"]}
                    topics_words = {-1: [("no_specific_topic", 1.0)]}
                
                self.progress_updated.emit(70, f"Success! Found {len(set(topics))} topics.")
                return True, (topic_model, topics, probs, topics_words, topic_info)
                
            except IndexError as e:
                if "list index out of range" in str(e):
                    logger.warning("BERTopic encountered a 'list index out of range' error, likely due to insufficient topic diversity.")
                    return False, None
                else:
                    raise
            
        except Exception as e:
            logger.warning(f"Standard BERTopic failed: {str(e)}")
            return False, None
    
    def _try_bertopic_pca(self):
        """Try BERTopic with PCA instead of UMAP"""
        try:
            self.progress_updated.emit(50, "Creating BERTopic model with PCA...")
            
            # Create representation model
            representation_model = KeyBERTInspired()
            
            # Create a PCA model - more stable than UMAP for small datasets
            n_components = min(5, max(2, len(self.documents) - 1))
            pca_model = PCA(n_components=n_components)
            
            # Initialize BERTopic model with PCA
            topic_model = BERTopic(
                representation_model=representation_model,
                language=self.language,
                min_topic_size=self.min_topic_size,
                nr_topics=self.nr_topics,
                n_gram_range=self.n_gram_range,
                calculate_probabilities=True,
                umap_model=pca_model  # Use PCA instead of UMAP
            )
            
            self.progress_updated.emit(60, "Fitting model with PCA...")
            
            # Try to fit and handle potential errors
            try:
                topics, probs = topic_model.fit_transform(self.documents)
                
                # Safely get topic info
                try:
                    topic_info = topic_model.get_topic_info()
                    topics_words = topic_model.get_topics()
                except Exception as e:
                    logger.warning(f"Error getting topic info: {str(e)}")
                    topic_info = {"Topic": [-1], "Count": [len(self.documents)], "Name": ["All Documents"]}
                    topics_words = {-1: [("no_specific_topic", 1.0)]}
                
                self.progress_updated.emit(70, f"Success with PCA approach! Found {len(set(topics))} topics.")
                return True, (topic_model, topics, probs, topics_words, topic_info)
            
            except Exception as e:
                logger.warning(f"BERTopic with PCA error: {str(e)}")
                return False, None
            
        except Exception as e:
            logger.warning(f"BERTopic with PCA failed: {str(e)}")
            return False, None
    
    def _try_nmf(self):
        """Try NMF topic modeling as a fallback"""
        try:
            self.progress_updated.emit(70, "Falling back to NMF topic modeling...")
            
            # Create vectorizer
            tfidf_vectorizer = TfidfVectorizer(
                min_df=2, max_df=0.95,
                ngram_range=self.n_gram_range
            )
            
            # Get document-term matrix
            dtm = tfidf_vectorizer.fit_transform(self.documents)
            
            # Set number of topics
            if self.nr_topics == "auto":
                n_topics = min(10, max(2, len(self.documents) // 3))
            else:
                n_topics = self.nr_topics
            
            # Create NMF model
            nmf_model = NMF(
                n_components=n_topics,
                random_state=42,
                max_iter=1000
            )
            
            self.progress_updated.emit(80, f"Fitting NMF model with {n_topics} topics...")
            
            # Fit the model
            document_topic_matrix = nmf_model.fit_transform(dtm)
            
            # Get the most significant topic for each document
            topics = document_topic_matrix.argmax(axis=1).tolist()
            
            # Get probabilities
            probs = document_topic_matrix.tolist()
            
            # Get feature names
            feature_names = tfidf_vectorizer.get_feature_names_out()
            
            # Create topics_words dictionary similar to BERTopic
            topics_words = {}
            for topic_idx, topic in enumerate(nmf_model.components_):
                top_words = [(feature_names[i], float(score)) 
                             for i, score in sorted(enumerate(topic), key=lambda x: -x[1])[:20]]
                topics_words[topic_idx] = top_words
            
            # Create topic_info similar to BERTopic
            topic_counts = {}
            for topic in topics:
                if topic not in topic_counts:
                    topic_counts[topic] = 0
                topic_counts[topic] += 1
            
            topic_info = {
                "Topic": list(topic_counts.keys()),
                "Count": list(topic_counts.values()),
                "Name": [f"Topic {idx}" for idx in topic_counts.keys()]
            }
            
            class NMFTopicModel:
                def __init__(self, nmf_model, vectorizer, topics_words, topic_info):
                    self.nmf_model = nmf_model
                    self.vectorizer = vectorizer
                    self._topics = topics_words
                    self._topic_info = topic_info
                
                def get_topics(self):
                    return self._topics
                
                def get_topic_info(self):
                    return self._topic_info
                
                def transform(self, documents):
                    # Transform new documents
                    dtm = self.vectorizer.transform(documents)
                    doc_topic_matrix = self.nmf_model.transform(dtm)
                    topics = doc_topic_matrix.argmax(axis=1).tolist()
                    return topics, doc_topic_matrix.tolist()
                
                # Add highlighting support
                def highlight_document(self, document, topic_ids=None, topics=None, 
                                    top_n=None, min_similarity=None, reduced_topics=None):
                    """Simplified highlighting for NMF models"""
                    import numpy as np
                    import matplotlib.colors as mcolors
                    
                    # Simple sentence splitting
                    sentences = [s.strip() for s in document.split('.') if s.strip()]
                    
                    # Create dummy embeddings - we'll just assign whole sentences
                    dtm = self.vectorizer.transform(sentences)
                    doc_topic_matrix = self.nmf_model.transform(dtm)
                    
                    # Get predicted topics for each sentence
                    sentence_topics = np.argmax(doc_topic_matrix, axis=1).tolist()
                    
                    # Generate HTML
                    html_output = []
                    for i, (sentence, topic) in enumerate(zip(sentences, sentence_topics)):
                        # Check if this topic should be highlighted
                        if topic_ids is not None and topic not in topic_ids:
                            html_output.append(f"{sentence}.")
                            continue
                            
                        # Find the color for this topic
                        topic_idx = topic_ids.index(topic) if topic in topic_ids else -1
                        
                        if topic_idx >= 0 and topic_idx < len(topics):
                            # Get the color for this topic
                            color = topics[topic_idx]
                            html_output.append(f'<span style="background-color:{color};">{sentence}.</span>')
                        else:
                            html_output.append(f"{sentence}.")
                    
                    return " ".join(html_output)
                
                def save(self, path):
                    # Save is not fully implemented but won't crash
                    import pickle
                    with open(path, 'wb') as f:
                        pickle.dump({
                            'nmf_model': self.nmf_model,
                            'vectorizer': self.vectorizer,
                            'topics': self._topics,
                            'topic_info': self._topic_info
                        }, f)
            
            # Create the model wrapper
            topic_model = NMFTopicModel(nmf_model, tfidf_vectorizer, topics_words, topic_info)
            
            self.progress_updated.emit(90, f"Success with NMF approach! Found {len(topics_words)} topics.")
            return True, (topic_model, topics, probs, topics_words, topic_info)
            
        except Exception as e:
            logger.warning(f"NMF approach failed: {str(e)}")
            return False, None

    def _evaluate_lda_model(self, vectorizer, model, documents):
        """Evaluate LDA model quality using log-likelihood and topic distinctiveness.
        
        This is a much faster alternative to full coherence calculation.
        Higher score indicates better model.
        """
        # Get the document-term matrix
        dtm = vectorizer.transform(documents)
        
        # Get log-likelihood score (built into LDA)
        log_likelihood = model.score(dtm)
        
        # Calculate topic distinctiveness (optional - adds a little time but gives better results)
        # We measure how different the topics are from each other
        topic_distinctiveness = 0
        
        # If you're very concerned about speed, you can comment out this distinctiveness 
        # calculation and just return log_likelihood
        try:
            # Get topic-term distributions
            topic_term_dists = model.components_ / model.components_.sum(axis=1)[:, np.newaxis]
            
            # Calculate pairwise Jensen-Shannon distances between topics
            from scipy.spatial.distance import jensenshannon
            n_topics = topic_term_dists.shape[0]
            
            # Simple random sampling for very large matrices
            if topic_term_dists.shape[1] > 10000:
                indices = np.random.choice(topic_term_dists.shape[1], 10000, replace=False)
                topic_term_dists = topic_term_dists[:, indices]
            
            # Calculate sum of distances
            sum_dist = 0
            count = 0
            
            for i in range(n_topics):
                for j in range(i+1, n_topics):
                    sum_dist += jensenshannon(topic_term_dists[i], topic_term_dists[j])
                    count += 1
            
            # Average distance
            if count > 0:
                topic_distinctiveness = sum_dist / count
        except Exception as e:
            # In case of any errors, just ignore distinctiveness
            pass
            
        # Combine scores - normalize log-likelihood which is usually negative
        # Log-likelihood is typically negative, with higher (less negative) being better
        # We add 100 to ensure it's positive for easier interpretation
        score = log_likelihood + 100 + (10 * topic_distinctiveness)
        
        return score


    def _run_lda_elbow_method(self):
        """Run LDA topic modeling with different numbers of topics to find optimal"""
        # Get parameters from self.lda_elbow_params
        min_topics = self.lda_elbow_params.get('min_topics', 2)
        max_topics = self.lda_elbow_params.get('max_topics', 15)
        step_size = self.lda_elbow_params.get('step_size', 1)
        
        # Create range of topics to try
        topics_range = list(range(min_topics, max_topics + 1, step_size))
        
        # Create vectorizer
        count_vectorizer = CountVectorizer(
            min_df=2, max_df=0.95,
            ngram_range=self.n_gram_range
        )
        
        # Get document-term matrix
        dtm = count_vectorizer.fit_transform(self.documents)
        
        # Calculate scores for each number of topics
        model_scores = []
        
        for i, n_topics in enumerate(topics_range):
            self.progress_updated.emit(
                35 + (i * 50 // len(topics_range)),
                f"Evaluating LDA with {n_topics} topics ({i+1}/{len(topics_range)})..."
            )
            
            # Create and fit LDA model
            lda = LatentDirichletAllocation(
                n_components=n_topics,
                random_state=42,
                max_iter=20
            )
            lda.fit(dtm)
            
            # Compute model score
            score = self._evaluate_lda_model(count_vectorizer, lda, self.documents)
            model_scores.append(score)
        
        # Show elbow plot and get optimal number of topics
        self.progress_updated.emit(85, "Preparing elbow plot dialog...")
        
        # Instead of creating the dialog directly, emit a signal with the data
        self.show_elbow_dialog.emit(model_scores, topics_range)
        
        # Wait for the dialog result (will be set by main thread)
        self.progress_updated.emit(86, "Waiting for user selection...")
         
        # Wait for the dialog to close and the result to be set
        import time
        max_wait_time = 300  # Maximum time to wait in seconds
        wait_start = time.time()
        
        # Modified loop to check for cancellation flag
        while self.elbow_selection_result is None and not self.elbow_selection_cancelled:
            # Check if we've waited too long
            if time.time() - wait_start > max_wait_time:
                logger.warning("Timeout waiting for elbow method dialog result")
                break
            
            # Sleep briefly to avoid CPU spin
            time.sleep(0.1)
            
            # Process events to avoid freezing
            from PyQt5.QtCore import QCoreApplication
            QCoreApplication.processEvents()
        
        # Get the selected number of topics
        if self.elbow_selection_result is not None:
            n_topics = self.elbow_selection_result
            self.elbow_selection_result = None  # Reset for future use
            self.elbow_selection_cancelled = False  # Reset cancellation flag
            self.progress_updated.emit(
                90, 
                f"Using {n_topics} topics based on elbow method analysis..."
            )
        else:
            # User canceled or timeout - use default
            n_topics = min(10, max(2, len(self.documents) // 3))
            self.progress_updated.emit(
                90, 
                f"Using default {n_topics} topics (no selection made)..."
            )
            # Reset cancellation flag
            self.elbow_selection_cancelled = False
        
        # Ensure progress updates to reflect the user's action
        if self.elbow_selection_cancelled:
            self.progress_updated.emit(
                90, 
                f"Topic modeling cancelled. Try again if needed."
            )
        
        return n_topics
    
    def _try_lda(self):
        """Try LDA topic modeling as a fallback"""
        try:
            self.progress_updated.emit(70, "Using LDA topic modeling...")
            
            # Create vectorizer
            count_vectorizer = CountVectorizer(
                min_df=2, max_df=0.95,
                ngram_range=self.n_gram_range
            )
            
            # Get document-term matrix
            dtm = count_vectorizer.fit_transform(self.documents)
            
            # Set number of topics
            if self.lda_elbow_enabled:
                # Use elbow method to find optimal number of topics
                n_topics = self._run_lda_elbow_method()
            elif self.nr_topics == "auto":
                n_topics = min(10, max(2, len(self.documents) // 3))
            else:
                n_topics = self.nr_topics
            
            # Create LDA model
            lda_model = LatentDirichletAllocation(
                n_components=n_topics,
                random_state=42,
                max_iter=20
            )
            
            self.progress_updated.emit(80, f"Fitting LDA model with {n_topics} topics...")
            
            # Fit the model
            document_topic_matrix = lda_model.fit_transform(dtm)
            
            # Get the most significant topic for each document
            topics = document_topic_matrix.argmax(axis=1).tolist()
            
            # Get probabilities
            probs = document_topic_matrix.tolist()
            
            # Get feature names
            feature_names = count_vectorizer.get_feature_names_out()
            
            # Create topics_words dictionary similar to BERTopic
            topics_words = {}
            for topic_idx, topic in enumerate(lda_model.components_):
                top_words = [(feature_names[i], float(score)) 
                             for i, score in sorted(enumerate(topic), key=lambda x: -x[1])[:20]]
                topics_words[topic_idx] = top_words
            
            # Create topic_info similar to BERTopic
            topic_counts = {}
            for topic in topics:
                if topic not in topic_counts:
                    topic_counts[topic] = 0
                topic_counts[topic] += 1
            
            topic_info = {
                "Topic": list(topic_counts.keys()),
                "Count": list(topic_counts.values()),
                "Name": [f"Topic {idx}" for idx in topic_counts.keys()]
            }
            
            class LDATopicModel:
                def __init__(self, lda_model, vectorizer, topics_words, topic_info):
                    self.lda_model = lda_model
                    self.vectorizer = vectorizer
                    self._topics = topics_words
                    self._topic_info = topic_info
                
                def get_topics(self):
                    return self._topics
                
                def get_topic_info(self):
                    return self._topic_info
                
                def transform(self, documents):
                    # Transform new documents
                    dtm = self.vectorizer.transform(documents)
                    doc_topic_matrix = self.lda_model.transform(dtm)
                    topics = doc_topic_matrix.argmax(axis=1).tolist()
                    return topics, doc_topic_matrix.tolist()
                
                # Add highlighting support
                def highlight_document(self, document, topic_ids=None, topics=None, 
                                    top_n=None, min_similarity=None, reduced_topics=None):
                    """Simplified highlighting for LDA models"""
                    import numpy as np
                    import matplotlib.colors as mcolors
                    
                    # Simple sentence splitting
                    sentences = [s.strip() for s in document.split('.') if s.strip()]
                    
                    # Create dummy embeddings - we'll just assign whole sentences
                    dtm = self.vectorizer.transform(sentences)
                    doc_topic_matrix = self.lda_model.transform(dtm)
                    
                    # Get predicted topics for each sentence
                    sentence_topics = np.argmax(doc_topic_matrix, axis=1).tolist()
                    
                    # Generate HTML
                    html_output = []
                    for i, (sentence, topic) in enumerate(zip(sentences, sentence_topics)):
                        # Check if this topic should be highlighted
                        if topic_ids is not None and topic not in topic_ids:
                            html_output.append(f"{sentence}.")
                            continue
                            
                        # Find the color for this topic
                        topic_idx = topic_ids.index(topic) if topic in topic_ids else -1
                        
                        if topic_idx >= 0 and topic_idx < len(topics):
                            # Get the color for this topic
                            color = topics[topic_idx]
                            html_output.append(f'<span style="background-color:{color};">{sentence}.</span>')
                        else:
                            html_output.append(f"{sentence}.")
                    
                    return " ".join(html_output)
                
                def save(self, path):
                    # Save is not fully implemented but won't crash
                    import pickle
                    with open(path, 'wb') as f:
                        pickle.dump({
                            'lda_model': self.lda_model,
                            'vectorizer': self.vectorizer,
                            'topics': self._topics,
                            'topic_info': self._topic_info
                        }, f)
                        
                # New method to support pyLDAvis
                def get_lda_components(self):
                    """Get the components needed for pyLDAvis visualization"""
                    return {
                        'lda_model': self.lda_model,
                        'vectorizer': self.vectorizer
                    }            
            # Create the model wrapper
            topic_model = LDATopicModel(lda_model, count_vectorizer, topics_words, topic_info)
            
            self.progress_updated.emit(90, f"Success with LDA approach! Found {len(topics_words)} topics.")
            return True, (topic_model, topics, probs, topics_words, topic_info)
            
        except Exception as e:
            logger.warning(f"LDA approach failed: {str(e)}")
            return False, None

    def _rechunk_documents(self, documents, chunk_size):
        """
        Split one or more documents into chunks to increase document count.
        
        This method processes each document separately. For each document:
        - If its word count is less than chunk_size, the document is kept as is.
        - Otherwise, the document is split into chunks of approximately chunk_size words.
        
        After processing, it ensures that there are at least 3 chunks (required for UMAP) by
        further splitting the largest chunk if necessary, or duplicating an existing chunk.
        
        Args:
            documents (List[str]): A list of document strings.
            chunk_size (int): The number of words per chunk.
        
        Returns:
            List[str]: A list of document chunks.
        """
        chunks = []
        for doc in documents:
            words = doc.split()
            # If document is too short, add it as a single chunk.
            if len(words) <= chunk_size:
                chunks.append(doc)
            else:
                # Split document into chunks of size chunk_size
                for i in range(0, len(words), chunk_size):
                    chunk = " ".join(words[i:i + chunk_size])
                    if chunk.strip():
                        chunks.append(chunk)
        
        # Ensure that we have at least 3 chunks (UMAP and other methods might require this)
        if len(chunks) < 3 and chunks:
            # Find the largest chunk (by word count) to split further
            largest_idx = max(range(len(chunks)), key=lambda i: len(chunks[i].split()))
            largest_chunk_words = chunks[largest_idx].split()
            if len(largest_chunk_words) > 10:
                midpoint = len(largest_chunk_words) // 2
                chunk1 = " ".join(largest_chunk_words[:midpoint])
                chunk2 = " ".join(largest_chunk_words[midpoint:])
                # Replace the largest chunk with the first half and add the second half as a new chunk
                chunks[largest_idx] = chunk1
                chunks.append(chunk2)
        
        # If we still have fewer than 3 chunks, duplicate the first chunk as needed
        while len(chunks) < 3 and chunks:
            chunks.append(chunks[0])
        
        self.progress_updated.emit(
            40,
            f"Created {len(chunks)} document chunks"
        )
        return chunks


class TopicModeler(QObject):
    """
    Handles topic modeling using BERTopic.
    
    This class manages the extraction of topics from text documents
    using a worker thread for processing to keep the UI responsive.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.model = None
        
    def extract_topics(self, documents: List[str], language: str = "multilingual", 
                    n_gram_range: Tuple[int, int] = (1, 2), min_topic_size: int = 2, 
                    nr_topics: Any = "auto", adaptive_enabled: bool = True,
                    max_retries: int = 5, initial_chunk_size: int = 100,
                    method: str = "bertopic", lda_elbow_enabled: bool = False, 
                    lda_elbow_params: Dict = None):
        """
        Start topic modeling on documents.
        
        Args:
            documents: List of document strings
            language: Language for topic modeling
            n_gram_range: Range of n-grams to consider
            min_topic_size: Minimum topic size
            nr_topics: Number of topics to extract
            adaptive_enabled: Whether to use adaptive processing
            max_retries: Maximum number of retry attempts
            initial_chunk_size: Initial size for document chunks
            method: Topic modeling method ('bertopic', 'bertopic-pca', 'nmf', 'lda')
            lda_elbow_enabled: Whether to use elbow method for LDA
            lda_elbow_params: Parameters for LDA elbow method
            
        Returns:
            QThread: The worker thread processing the topics
            
        Note:
            This method starts a worker thread. Results will be emitted via signals.
            The caller is responsible for connecting to worker.show_elbow_dialog signal.
        """
        # Create and configure worker
        self.worker = TopicModelingWorker(
            documents, language, n_gram_range, min_topic_size, nr_topics,
            adaptive_enabled, max_retries, initial_chunk_size, method,
            lda_elbow_enabled, lda_elbow_params
        )
        
        # Connect signals for model handling
        self.worker.topics_extracted.connect(self._save_model)
        
        # Note: We no longer connect the show_elbow_dialog signal here
        # The caller (TopicTab) should connect to this signal
        
        # Clean up when done
        self.worker.finished.connect(self.worker.deleteLater)
        
        # Start the worker
        self.worker.start()
        
        return self.worker
                
    @pyqtSlot(object, object, object, object, object)
    def _save_model(self, topics, probs, topics_words, topic_info, model):
        """Save the BERTopic model from the worker"""
        self.model = model
        logger.info("BERTopic model saved in TopicModeler instance")
    
    def set_model(self, model: BERTopic):
        """
        Set the BERTopic model manually.
        
        Args:
            model: Trained BERTopic model
        """
        self.model = model
    
    def get_model(self) -> Optional[BERTopic]:
        """
        Get the current BERTopic model.
        
        Returns:
            BERTopic model or None if not set
        """
        return self.model
    
    def transform_documents(self, documents: List[str]) -> Tuple[List[int], np.ndarray]:
        """
        Transform documents using the existing model.
        
        Args:
            documents: List of document strings
            
        Returns:
            Tuple of (topics, probabilities)
            
        Raises:
            ValueError: If model is not set
        """
        if self.model is None:
            raise ValueError("No topic model has been trained or set.")
        
        return self.model.transform(documents)
    
    def get_topic_info(self) -> Dict:
        """
        Get information about the topics in the model.
        
        Returns:
            DataFrame with topic information
            
        Raises:
            ValueError: If model is not set
        """
        if self.model is None:
            raise ValueError("No topic model has been trained or set.")
        
        return self.model.get_topic_info()
    
    def get_topics(self) -> Dict:
        """
        Get the topics and their words from the model.
        
        Returns:
            Dictionary mapping topic IDs to lists of (word, score) tuples
            
        Raises:
            ValueError: If model is not set
        """
        if self.model is None:
            raise ValueError("No topic model has been trained or set.")
        
        return self.model.get_topics()
    
    def save_model(self, path: str) -> None:
        """
        Save the topic model to disk.
        
        Args:
            path: Path to save the model
            
        Raises:
            ValueError: If model is not set
        """
        if self.model is None:
            raise ValueError("No topic model has been trained or set.")
        
        self.model.save(path)
    
    def load_model(self, path: str) -> None:
        """
        Load a topic model from disk.
        
        Args:
            path: Path to the saved model
        """
        self.model = BERTopic.load(path)