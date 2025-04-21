#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validator module for the Audio to Topics application.
Provides functionality for validating topic quality metrics.
"""

import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Union
from PyQt5.QtCore import QObject, pyqtSignal, QThread

from bertopic import BERTopic

# Configure logging
logger = logging.getLogger(__name__)

class ValidationWorker(QThread):
    """Worker thread for topic validation"""
    progress_updated = pyqtSignal(int, str)
    validation_completed = pyqtSignal(dict, object)  # metrics, summary_df
    error_occurred = pyqtSignal(str)
    
    def __init__(self, documents, topic_model):
        super().__init__()
        self.documents = documents
        self.topic_model = topic_model
        
    def run(self):
        """Execute the topic validation"""
        try:
            self.progress_updated.emit(10, "Starting topic validation...")
            
            # Validate the topic model
            metrics, summary_df = validate_topics(self.documents, self.topic_model)
            
            self.progress_updated.emit(90, "Validation complete!")
            
            # Emit results
            self.validation_completed.emit(metrics, summary_df)
            
            self.progress_updated.emit(100, "Done!")
            
        except Exception as e:
            logger.error(f"Topic validation error: {str(e)}", exc_info=True)
            self.error_occurred.emit(f"Error during topic validation: {str(e)}")


class OptimizationWorker(QThread):
    """Worker thread for finding optimal topic count"""
    progress_updated = pyqtSignal(int, str)
    optimization_completed = pyqtSignal(dict)  # recommendations
    error_occurred = pyqtSignal(str)
    
    def __init__(self, documents, max_topics=15, min_topic_size=2, **bertopic_kwargs):
        super().__init__()
        self.documents = documents
        self.max_topics = max_topics
        self.min_topic_size = min_topic_size
        self.bertopic_kwargs = bertopic_kwargs
        
    def run(self):
        """Execute the topic optimization"""
        try:
            self.progress_updated.emit(5, "Starting topic optimization...")
            
            # Find optimal number of topics
            recommendations = recommend_optimal_topics(
                self.documents, 
                self.max_topics, 
                self.min_topic_size, 
                **self.bertopic_kwargs
            )
            
            self.progress_updated.emit(95, "Optimization complete!")
            
            # Emit results
            self.optimization_completed.emit(recommendations)
            
            self.progress_updated.emit(100, "Done!")
            
        except Exception as e:
            logger.error(f"Topic optimization error: {str(e)}", exc_info=True)
            self.error_occurred.emit(f"Error during topic optimization: {str(e)}")


def calculate_topic_stability(model1: BERTopic, model2: BERTopic) -> float:
    """
    Calculate stability between two BERTopic models by comparing topic embeddings.
    
    Args:
        model1 (BERTopic): First BERTopic model.
        model2 (BERTopic): Second BERTopic model.
        
    Returns:
        float: Stability score between 0 and 1, where higher is better.
    """
    logger.debug("Calculating topic stability between two models")
    
    # Get topic embeddings
    topics1 = model1.topic_embeddings_
    topics2 = model2.topic_embeddings_
    
    # Fall back to word distributions if embeddings not available
    if topics1 is None or topics2 is None:
        logger.warning("Topic embeddings not available, using word distributions")
        return _calculate_stability_from_words(model1, model2)
    
    # Calculate cosine similarity between topics
    similarities = cosine_similarity(topics1, topics2)
    
    # Calculate stability as the average of max similarities in both directions
    stability = (np.mean(np.max(similarities, axis=1)) + 
                np.mean(np.max(similarities, axis=0))) / 2
    
    return stability


def _calculate_stability_from_words(model1: BERTopic, model2: BERTopic, top_n: int = 20) -> float:
    """
    Calculate stability using word distributions when embeddings are not available.
    
    Args:
        model1 (BERTopic): First BERTopic model.
        model2 (BERTopic): Second BERTopic model.
        top_n (int): Number of top words to consider per topic.
        
    Returns:
        float: Stability score between 0 and 1, where higher is better.
    """
    # Get topic word distributions
    topics1 = model1.get_topics()
    topics2 = model2.get_topics()
    
    # Create a vocabulary of all words from both models
    all_words = set()
    for topics in [topics1, topics2]:
        for topic_words in topics.values():
            all_words.update(word for word, _ in topic_words[:top_n])
    
    # Map words to indices
    word_to_idx = {word: idx for idx, word in enumerate(all_words)}
    vocab_size = len(word_to_idx)
    
    # Create a vector for each topic
    def get_topic_vector(topic_words):
        vector = np.zeros(vocab_size)
        for word, score in topic_words[:top_n]:
            vector[word_to_idx[word]] = score
        return vector
    
    # Convert topics to vectors
    vectors1 = [get_topic_vector(topics1[t]) for t in topics1.keys()]
    vectors2 = [get_topic_vector(topics2[t]) for t in topics2.keys()]
    
    # Calculate cosine similarity between topic vectors
    similarities = cosine_similarity(vectors1, vectors2)
    
    # Calculate stability as the average of max similarities in both directions
    stability = (np.mean(np.max(similarities, axis=1)) + 
                np.mean(np.max(similarities, axis=0))) / 2
    
    return stability


def calculate_topic_diversity(model: BERTopic, top_n: int = 20) -> float:
    """
    Calculate topic diversity by measuring uniqueness of words across topics.
    
    Args:
        model (BERTopic): BERTopic model to evaluate.
        top_n (int): Number of top words to consider per topic.
        
    Returns:
        float: Diversity score between 0 and 1, where higher is better.
    """
    logger.debug(f"Calculating topic diversity with top {top_n} words")
    
    # Get topics
    topics = model.get_topics()
    
    # Skip outlier topic (-1)
    topics = {topic_id: words for topic_id, words in topics.items() if topic_id != -1}
    
    if not topics:
        logger.warning("No topics found in model")
        return 0.0
    
    # Count unique and total words
    unique_words = set()
    total_words = 0
    
    for topic_words in topics.values():
        words = [word for word, _ in topic_words[:top_n]]
        unique_words.update(words)
        total_words += len(words)
    
    # Calculate diversity as ratio of unique words to total words
    if total_words == 0:
        return 0.0
    
    diversity = len(unique_words) / total_words
    logger.debug(f"Topic diversity: {diversity:.4f}")
    
    return diversity


def calculate_topic_coherence(model: BERTopic) -> float:
    """
    Calculate topic coherence using the model's coherence score.
    
    Args:
        model (BERTopic): BERTopic model to evaluate.
        
    Returns:
        float: Coherence score, where higher is better.
    """
    logger.debug("Calculating topic coherence")
    
    # Get coherence from model if available
    if hasattr(model, "coherence_score_") and model.coherence_score_ is not None:
        return model.coherence_score_
    
    logger.warning("Coherence score not available in model")
    return 0.0


def evaluate_topic_quality(documents: List[str], 
                         n_splits: int = 5, 
                         min_topic_size: int = 2,
                         **bertopic_kwargs) -> Dict:
    """
    Evaluate topic model quality using cross-validation.
    
    Args:
        documents (list): List of document strings.
        n_splits (int): Number of cross-validation splits.
        min_topic_size (int): Minimum topic size for BERTopic.
        **bertopic_kwargs: Additional arguments for BERTopic.
        
    Returns:
        dict: Dictionary containing evaluation metrics.
    """
    logger.info(f"Evaluating topic quality with {n_splits}-fold cross-validation")
    
    # Check if we have enough documents
    if len(documents) < n_splits * 2:
        logger.warning(f"Not enough documents for {n_splits}-fold CV. Reducing folds.")
        n_splits = max(2, len(documents) // 2)
    
    # Initialize KFold cross-validator
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    # Initialize metrics storage
    metrics = {
        'stability': [],
        'diversity': [],
        'topic_counts': [],
    }
    
    # Perform cross-validation
    for fold, (train_idx, val_idx) in enumerate(kf.split(documents)):
        logger.info(f"Processing fold {fold + 1}/{n_splits}")
        
        # Split documents
        train_docs = [documents[i] for i in train_idx]
        val_docs = [documents[i] for i in val_idx]
        
        # Train BERTopic models
        bert_train = BERTopic(min_topic_size=min_topic_size, **bertopic_kwargs)
        bert_val = BERTopic(min_topic_size=min_topic_size, **bertopic_kwargs)
        
        # Fit models
        train_topics, _ = bert_train.fit_transform(train_docs)
        val_topics, _ = bert_val.fit_transform(val_docs)
        
        # Calculate metrics
        try:
            stability = calculate_topic_stability(bert_train, bert_val)
            metrics['stability'].append(stability)
        except Exception as e:
            logger.error(f"Error calculating stability: {str(e)}")
            metrics['stability'].append(0.0)
        
        try:
            diversity = calculate_topic_diversity(bert_train)
            metrics['diversity'].append(diversity)
        except Exception as e:
            logger.error(f"Error calculating diversity: {str(e)}")
            metrics['diversity'].append(0.0)
        
        # Count number of topics (excluding outlier topic)
        topic_count = len([t for t in set(train_topics) if t != -1])
        metrics['topic_counts'].append(topic_count)
    
    # Summarize metrics
    summary = {
        'mean_stability': np.mean(metrics['stability']),
        'std_stability': np.std(metrics['stability']),
        'mean_diversity': np.mean(metrics['diversity']),
        'std_diversity': np.std(metrics['diversity']),
        'mean_topics': np.mean(metrics['topic_counts']),
        'std_topics': np.std(metrics['topic_counts']),
        'raw_metrics': metrics  # Include raw metrics for detailed analysis
    }
    
    logger.info(f"Topic quality evaluation completed. Mean stability: {summary['mean_stability']:.4f}, Mean diversity: {summary['mean_diversity']:.4f}")
    
    return summary


def validate_topics(documents: List[str], topic_model: BERTopic) -> Tuple[Dict, pd.DataFrame]:
    """
    Validate an existing topic model and provide quality metrics.
    
    Args:
        documents (list): List of document strings.
        topic_model (BERTopic): Trained BERTopic model to validate.
        
    Returns:
        tuple: (metrics dictionary, validation summary DataFrame)
    """
    logger.info("Validating topic model")
    
    # Calculate metrics
    diversity = calculate_topic_diversity(topic_model)
    coherence = calculate_topic_coherence(topic_model)
    
    # Get topic distribution
    topics, _ = topic_model.transform(documents)
    topic_counts = {}
    for topic in topics:
        if topic not in topic_counts:
            topic_counts[topic] = 0
        topic_counts[topic] += 1
    
    # Remove outlier topic from counts
    if -1 in topic_counts:
        outliers = topic_counts.pop(-1)
    else:
        outliers = 0
    
    # Calculate topic coverage (percentage of docs with a real topic)
    coverage = (len(documents) - outliers) / len(documents) if documents else 0
    
    # Create metrics dictionary
    metrics = {
        'num_topics': len(topic_counts),
        'diversity': diversity,
        'coherence': coherence,
        'coverage': coverage,
        'outliers': outliers,
        'topic_distribution': topic_counts
    }
    
    # Create summary DataFrame
    summary = []
    for metric, value in metrics.items():
        if metric != 'topic_distribution':
            summary.append({
                'Metric': metric,
                'Value': value
            })
    
    # Add topic distribution to summary
    for topic, count in topic_counts.items():
        summary.append({
            'Metric': f'Topic {topic} count',
            'Value': count
        })
    
    summary_df = pd.DataFrame(summary)
    
    logger.info(f"Topic validation completed. Identified {metrics['num_topics']} topics with {diversity:.4f} diversity")
    
    return metrics, summary_df


def recommend_optimal_topics(documents: List[str], 
                           max_topics: int = 15,
                           min_topic_size: int = 2,
                           **bertopic_kwargs) -> Dict:
    """
    Recommend optimal number of topics based on stability and diversity metrics.
    
    Args:
        documents (list): List of document strings.
        max_topics (int): Maximum number of topics to consider.
        min_topic_size (int): Minimum topic size for BERTopic.
        **bertopic_kwargs: Additional arguments for BERTopic.
        
    Returns:
        dict: Dictionary with recommended topics and evaluation metrics.
    """
    logger.info(f"Finding optimal number of topics (max: {max_topics})")
    
    # Ensure max_topics is reasonable given the document count
    doc_count = len(documents)
    max_possible = doc_count // min_topic_size
    max_topics = min(max_topics, max_possible)
    
    # Stop if we don't have enough documents
    if doc_count < min_topic_size * 2:
        logger.error(f"Not enough documents ({doc_count}) for topic modeling with min_topic_size={min_topic_size}")
        return {
            'recommended_topics': 1,
            'error': 'Not enough documents for topic modeling'
        }
    
    # Initialize results storage
    results = []
    
    # Test different numbers of topics
    for n_topics in range(2, max_topics + 1):
        logger.info(f"Testing {n_topics} topics")
        
        try:
            # Evaluate topic quality with this number of topics
            bertopic_kwargs['nr_topics'] = n_topics
            metrics = evaluate_topic_quality(
                documents=documents,
                n_splits=3,  # Use fewer splits for efficiency
                min_topic_size=min_topic_size,
                **bertopic_kwargs
            )
            
            # Calculate a combined score (weigh stability more heavily)
            combined_score = (0.7 * metrics['mean_stability']) + (0.3 * metrics['mean_diversity'])
            
            # Store results
            results.append({
                'n_topics': n_topics,
                'stability': metrics['mean_stability'],
                'diversity': metrics['mean_diversity'],
                'combined_score': combined_score
            })
            
        except Exception as e:
            logger.error(f"Error evaluating {n_topics} topics: {str(e)}")
            continue
    
    # Find the best number of topics
    if not results:
        logger.error("Failed to evaluate any topic configurations")
        return {
            'recommended_topics': 2,
            'error': 'Failed to evaluate topic configurations'
        }
    
    # Sort by combined score
    results.sort(key=lambda x: x['combined_score'], reverse=True)
    recommended = results[0]
    
    logger.info(f"Recommended {recommended['n_topics']} topics with combined score {recommended['combined_score']:.4f}")
    
    return {
        'recommended_topics': recommended['n_topics'],
        'combined_score': recommended['combined_score'],
        'stability': recommended['stability'],
        'diversity': recommended['diversity'],
        'all_results': results
    }


class TopicValidator(QObject):
    """
    Handles topic validation and optimization.
    
    This class provides functionality for:
    1. Validating an existing topic model
    2. Finding the optimal number of topics for a given set of documents
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.validation_worker = None
        self.optimization_worker = None
    
    def validate_model(self, documents: List[str], topic_model: BERTopic):
        """
        Start validation of a topic model.
        
        Args:
            documents: List of document strings
            topic_model: Trained BERTopic model
            
        Returns:
            QThread: The worker thread performing validation
            
        Note:
            This method starts a worker thread. Results will be emitted via signals.
        """
        # Create and configure worker
        self.validation_worker = ValidationWorker(documents, topic_model)
        
        # Clean up when done
        self.validation_worker.finished.connect(self.validation_worker.deleteLater)
        
        # Start the worker
        self.validation_worker.start()
        
        return self.validation_worker
    
    def find_optimal_topics(self, documents: List[str], max_topics: int = 15, 
                           min_topic_size: int = 2, **bertopic_kwargs):
        """
        Start optimization to find the optimal number of topics.
        
        Args:
            documents: List of document strings
            max_topics: Maximum number of topics to consider
            min_topic_size: Minimum topic size for BERTopic
            **bertopic_kwargs: Additional arguments for BERTopic
            
        Returns:
            QThread: The worker thread performing optimization
            
        Note:
            This method starts a worker thread. Results will be emitted via signals.
        """
        # Create and configure worker
        self.optimization_worker = OptimizationWorker(
            documents, max_topics, min_topic_size, **bertopic_kwargs
        )
        
        # Clean up when done
        self.optimization_worker.finished.connect(self.optimization_worker.deleteLater)
        
        # Start the worker
        self.optimization_worker.start()
        
        return self.optimization_worker