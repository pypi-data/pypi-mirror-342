#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualization module for the Audio to Topics application.
Provides functionality for generating visualizations of text analysis.
"""

import logging
import re
import html
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for headless operation
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from wordcloud import WordCloud
from collections import Counter
from nltk import ngrams
from io import BytesIO


from ..core.text_processor import clean_text

# Configure logging
logger = logging.getLogger(__name__)

class VisualizationWorker(QThread):
    """Worker thread for generating visualizations"""
    progress_updated = pyqtSignal(int, str)
    visualization_completed = pyqtSignal(object)  # Figure object
    error_occurred = pyqtSignal(str)
    
    def __init__(self, viz_type, data, **kwargs):
        super().__init__()
        self.viz_type = viz_type  # Type of visualization to generate
        self.data = data  # Data for visualization
        self.kwargs = kwargs  # Additional parameters
        
    def run(self):
        """Execute the visualization generation"""
        try:
            self.progress_updated.emit(10, f"Preparing {self.viz_type} visualization...")
            
            # Generate the appropriate visualization based on the type
            if self.viz_type == 'wordcloud':
                fig = show_wordcloud(self.data, **self.kwargs)
                html_string = None
            elif self.viz_type == 'word_freq':
                fig = show_word_freq(self.data, **self.kwargs)
                html_string = None
            elif self.viz_type == 'ngrams':
                counts, fig = count_and_visualize_ngrams(self.data, **self.kwargs)
                html_string = None
            elif self.viz_type == 'topic_heatmap':
                fig = create_topic_heatmap(self.data, **self.kwargs)
                html_string = None
            elif self.viz_type == 'topic_distribution':
                fig = visualize_topic_distribution(self.data, **self.kwargs)
                html_string = None
            elif self.viz_type == 'topic_keywords':
                fig = visualize_topic_keywords(self.data, **self.kwargs)
                html_string = None
            elif self.viz_type == 'pyldavis':
                html_string, fig = create_pyldavis(self.data.get('model'), 
                                                self.data.get('dtm'),
                                                self.data.get('vectorizer'),
                                                **self.kwargs)
            elif self.viz_type == 'bertopic_interactive':
                html_string, fig = create_bertopic_visualization(self.data, **self.kwargs)
            else:
                raise ValueError(f"Unknown visualization type: {self.viz_type}")
            
            self.progress_updated.emit(90, "Visualization complete!")
            
            # Emit the result
            if html_string:
                self.visualization_completed.emit((fig, html_string))
            else:
                self.visualization_completed.emit((fig, None))
            
            self.progress_updated.emit(100, "Done!")
            
        except Exception as e:
            logger.error(f"Visualization error: {str(e)}", exc_info=True)
            self.error_occurred.emit(f"Error generating visualization: {str(e)}")

def show_wordcloud(docs, language='english', width=800, height=400, 
                 background_color='black', colormap='viridis'):
    """
    Generate a word cloud visualization from documents.
    
    Args:
        docs (list): List of documents to visualize.
        language (str): Language of the documents.
        width (int): Width of the word cloud.
        height (int): Height of the word cloud.
        background_color (str): Background color of the word cloud.
        colormap (str): Colormap for the word cloud.
    
    Returns:
        Figure: Matplotlib figure with the word cloud.
    """
    logger.info("Generating word cloud")
    
    try:
        # Clean and join texts
        tokens = [clean_text(doc, language) for doc in docs]
        text = ' '.join(tokens)
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=width, 
            height=height, 
            background_color=background_color,
            colormap=colormap,
            max_words=200,
            contour_width=1,
            contour_color='steelblue'
        ).generate(text)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(width/100, height/100), facecolor=background_color)
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        plt.tight_layout(pad=0)
        
        return fig
    
    except Exception as e:
        logger.error(f"Error generating word cloud: {str(e)}", exc_info=True)
        
        # Create error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error generating word cloud: {str(e)}", 
                ha='center', va='center', fontsize=12, color='red')
        ax.axis('off')
        
        return fig


def show_word_freq(docs, language='english', top_n=30, color='skyblue'):
    """
    Generate a word frequency visualization from documents.
    
    Args:
        docs (list): List of documents to visualize.
        language (str): Language of the documents.
        top_n (int): Number of top words to display.
        color (str): Color for the bars.
    
    Returns:
        Figure: Matplotlib figure with the word frequency plot.
    """
    logger.info(f"Generating word frequency plot for top {top_n} words")
    
    try:
        # Clean and join texts
        tokens = [clean_text(doc, language) for doc in docs]
        text = ' '.join(tokens)
        words = text.split()
        
        # Count word frequencies
        freq_dict = Counter(words)
        
        # Create DataFrame and sort
        df = pd.DataFrame(freq_dict.items(), columns=['Word', 'Frequency'])
        df = df.sort_values(by='Frequency', ascending=False).head(top_n)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        df.plot.barh(x='Word', y='Frequency', ax=ax, color=color)
        
        # Configure plot
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Word')
        ax.set_title(f'Top {top_n} Most Frequent Words')
        ax.invert_yaxis()  # Display highest frequency at the top
        plt.tight_layout()
        
        return fig
    
    except Exception as e:
        logger.error(f"Error generating word frequency plot: {str(e)}", exc_info=True)
        
        # Create error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error generating word frequency plot: {str(e)}", 
                ha='center', va='center', fontsize=12, color='red')
        ax.axis('off')
        
        return fig


def count_and_visualize_ngrams(docs, n, language='english', top_n=50, color='lightgreen'):
    """
    Count and visualize n-grams from documents.
    
    Args:
        docs (list): List of documents to analyze.
        n (int): Size of n-grams (2 for bigrams, 3 for trigrams, etc.).
        language (str): Language of the documents.
        top_n (int): Number of top n-grams to display.
        color (str): Color for the bars.
    
    Returns:
        tuple: (ngram_counts, Figure)
            - ngram_counts (Counter): Counter of n-gram frequencies.
            - Figure: Matplotlib figure with the n-gram frequency plot.
    """
    logger.info(f"Generating {n}-gram frequency plot for top {top_n} n-grams")
    
    try:
        # Clean and tokenize texts
        tokens = [clean_text(doc, language).split() for doc in docs]
        
        # Count n-grams for each document
        ngram_counts = [Counter(ngrams(doc_tokens, n)) for doc_tokens in tokens]
        
        # Combine counts from all documents
        combined_counts = sum(ngram_counts, Counter())
        
        # Convert to readable format
        ngrams_list = [' '.join(ngram) for ngram in combined_counts.keys()]
        frequencies = list(combined_counts.values())
        
        # Create DataFrame and sort
        df = pd.DataFrame({'N-gram': ngrams_list, 'Frequency': frequencies})
        df = df.sort_values('Frequency', ascending=False).head(top_n)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create bar chart
        ax.bar(df['N-gram'], df['Frequency'], color=color)
        
        # Configure plot
        ax.set_xticklabels(df['N-gram'], rotation=90, fontsize=8)
        ax.set_xlabel('N-gram')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Top {top_n} Most Frequent {n}-grams')
        plt.tight_layout()
        
        return combined_counts, fig
    
    except Exception as e:
        logger.error(f"Error generating n-gram plot: {str(e)}", exc_info=True)
        
        # Create error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error generating {n}-gram plot: {str(e)}", 
                ha='center', va='center', fontsize=12, color='red')
        ax.axis('off')
        
        return Counter(), fig

def create_pyldavis(lda_model, dtm, vectorizer, output_path=None, **kwargs):
    """
    Create an interactive pyLDAvis visualization of an LDA model.
    
    Args:
        lda_model: LDA model object (sklearn LatentDirichletAllocation)
        dtm: Document-term matrix used to train the model
        vectorizer: The vectorizer used to create the DTM (CountVectorizer)
        output_path: Optional path to save the HTML visualization
        **kwargs: Additional arguments to pass to pyLDAvis.sklearn.prepare
                 - mds: MDS algorithm to use ('tsne' or 'pcoa')
    
    Returns:
        tuple: (html_string, fig)
            - html_string: HTML string of the pyLDAvis visualization
            - fig: Placeholder figure for compatibility with other visualizations
    """
    import pyLDAvis
    import pyLDAvis.lda_model
    import matplotlib.pyplot as plt
    
    logger.info("Generating pyLDAvis visualization")
    
    try:
        # Create the pyLDAvis data
        vis_data = pyLDAvis.lda_model.prepare(
            lda_model, 
            dtm, 
            vectorizer, 
            **kwargs  # Pass through all additional keyword arguments
        )
        
        # If output path is provided, save the visualization to HTML
        if output_path:
            pyLDAvis.save_html(vis_data, output_path)
        
        # Get HTML string representation
        html_string = pyLDAvis.prepared_data_to_html(vis_data)
        
        # Create a placeholder figure for compatibility with current visualization system
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, "pyLDAvis visualization generated\nView in HTML tab", 
                ha='center', va='center', fontsize=14)
        ax.axis('off')
        
        return html_string, fig
    
    except Exception as e:
        logger.error(f"Error generating pyLDAvis visualization: {str(e)}", exc_info=True)
        
        # Create error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error generating pyLDAvis visualization: {str(e)}", 
                ha='center', va='center', fontsize=12, color='red')
        ax.axis('off')
        
        return "", fig

def create_bertopic_visualization(topic_model, **kwargs):
    """
    Create an interactive visualization of topics using BERTopic's built-in visualization.
    
    Args:
        topic_model: BERTopic model
        **kwargs: Additional arguments to pass to visualize_topics
                 - topics: List of topics to visualize (default: top 10)
                 - width: Width of the visualization (default: 1000px)
                 - height: Height of the visualization (default: 800px)
    
    Returns:
        tuple: (html_string, fig)
            - html_string: HTML string of the visualization
            - fig: Placeholder figure for compatibility
    """
    import logging
    import matplotlib.pyplot as plt
    
    logger.info("Generating BERTopic visualization")
    
    try:
        # Check if it's a BERTopic model
        is_bertopic = False
        model_type = topic_model.__class__.__name__
        
        if model_type == "BERTopic" or hasattr(topic_model, 'visualize_topics'):
            is_bertopic = True
        else:
            logger.warning(f"Model is not BERTopic, but {model_type}")
        
        if is_bertopic:
            # Get parameters
            topics = kwargs.get('topics', None)
            width = kwargs.get('width', 1000)
            height = kwargs.get('height', 800)
            
            # If topics is None, get top 10 topics by size (excluding -1)
            if topics is None:
                try:
                    topic_info = topic_model.get_topic_info()
                    # Filter out -1 (outlier topic)
                    filtered_info = topic_info[topic_info['Topic'] != -1]
                    # Get top 10 topics by Count
                    top_topics = filtered_info.nlargest(10, 'Count')['Topic'].tolist()
                    topics = top_topics
                except Exception as e:
                    logger.warning(f"Failed to get top topics: {str(e)}")
                    # Default to first 10 topics if available
                    all_topics = list(topic_model.get_topics().keys())
                    topics = [t for t in all_topics if t != -1][:10]
            
            # Generate the visualization
            fig = topic_model.visualize_topics(topics=topics, width=width, height=height)
            
            # Convert to HTML string
            html_string = fig.to_html(include_plotlyjs='cdn')
            
            # Create a placeholder figure for the non-interactive view
            placeholder_fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, "BERTopic visualization generated\nView in Interactive tab", 
                    ha='center', va='center', fontsize=14)
            ax.axis('off')
            
            return html_string, placeholder_fig
        else:
            # Model is not BERTopic, create a message
            html_string = """
            <html>
            <body>
                <div style="padding: 20px; background-color: #f8f8f8; border-radius: 5px; text-align: center;">
                    <h2>BERTopic Visualization Not Available</h2>
                    <p>The current model is not a BERTopic model. This visualization is only available with BERTopic models.</p>
                    <p>Current model type: <b>{}</b></p>
                    <p>Please train a model using the BERTopic method to use this visualization.</p>
                </div>
            </body>
            </html>
            """.format(model_type)
            
            # Create a placeholder figure
            placeholder_fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, "BERTopic visualization not available\nCurrent model: {}".format(model_type), 
                    ha='center', va='center', fontsize=14, color='red')
            ax.axis('off')
            
            return html_string, placeholder_fig
    
    except Exception as e:
        logger.error(f"Error generating BERTopic visualization: {str(e)}", exc_info=True)
        
        # Create error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error generating BERTopic visualization: {str(e)}", 
                ha='center', va='center', fontsize=12, color='red')
        ax.axis('off')
        
        error_html = f"""
        <html>
        <body>
            <div style="padding: 20px; background-color: #ffeeee; border-radius: 5px; text-align: center;">
                <h2>Error Generating Visualization</h2>
                <p>{str(e)}</p>
            </div>
        </body>
        </html>
        """
        
        return error_html, fig
      
def highlight_topics_in_text(documents, topic_model, topics, colors=None):
    """
    Highlight topic phrases in the documents using BERTopic's topic representations.
    
    Args:
        documents (list of str): List of documents to highlight.
        topic_model (BERTopic): The trained BERTopic model.
        topics (list of int): List of topic IDs to include.
        colors (list of str or None): List of color codes. If None, generate colors.
    
    Returns:
        list of str: List of documents with highlighted topic phrases in HTML format.
    """
    import html
    import re
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    
    logger.info(f"Highlighting {len(topics)} topics in {len(documents)} documents")
    
    try:
        # Escape HTML characters in documents
        escaped_docs = [html.escape(doc) for doc in documents]
        
        # Generate colors if not provided
        num_topics = len(topics)
        if colors is None:
            cmap = plt.get_cmap('hsv')
            colors = [mcolors.rgb2hex(cmap(i / num_topics)) for i in range(num_topics)]
        elif len(colors) < num_topics:
            raise ValueError("Not enough colors provided for the number of topics.")
        
        # Build a mapping of phrase to HTML span with color
        phrase_to_html = {}
        for topic_id, color in zip(topics, colors):
            # Get phrases for this topic
            try:
                topic_phrases = [phrase for phrase, _ in topic_model.get_topic(topic_id)]
            except Exception as e:
                logger.error(f"Error getting phrases for topic {topic_id}: {str(e)}")
                continue
            
            # Sort phrases by length to match longer phrases first
            topic_phrases.sort(key=lambda x: len(x), reverse=True)
            
            # Create HTML spans for each phrase
            for phrase in topic_phrases:
                phrase_lower = phrase.lower()
                if phrase_lower not in phrase_to_html:
                    # Assign the first color encountered for the phrase
                    phrase_to_html[phrase_lower] = f'<span style="background-color: {color};">{phrase}</span>'
        
        # Compile a regular expression pattern for all phrases
        if not phrase_to_html:
            logger.warning("No phrases found to highlight")
            return escaped_docs
        
        # Escape special regex characters and sort phrases by length to match longer phrases first
        sorted_phrases = sorted(phrase_to_html.keys(), key=lambda x: len(x), reverse=True)
        pattern = re.compile(r'\b(' + '|'.join(re.escape(phrase) for phrase in sorted_phrases) + r')\b', flags=re.IGNORECASE)
        
        # Function to replace matched phrases with colored spans
        def replacer(match):
            phrase = match.group(0)
            phrase_lower = phrase.lower()
            return phrase_to_html.get(phrase_lower, phrase)
        
        # Apply highlighting to each document
        highlighted_docs = []
        for doc in escaped_docs:
            highlighted_doc = pattern.sub(replacer, doc)
            # Wrap in HTML for proper display
            highlighted_doc = f"<div style='font-family: Arial, sans-serif; line-height: 1.6;'>{highlighted_doc}</div>"
            highlighted_docs.append(highlighted_doc)
        
        return highlighted_docs
    
    except Exception as e:
        logger.error(f"Error highlighting topics: {str(e)}", exc_info=True)
        return documents


# Replace the create_topic_heatmap function in visualizer.py with this fixed version:

def create_topic_heatmap(doc_topic_matrix, topic_labels=None, document_labels=None):
    """
    Create a heatmap visualization of document-topic assignments.
    
    Args:
        doc_topic_matrix (array): Matrix of document-topic probabilities.
        topic_labels (list): List of topic labels.
        document_labels (list): List of document labels.
    
    Returns:
        Figure: Matplotlib figure with the heatmap.
    """
    logger.info("Generating document-topic heatmap")
    
    try:
        # Print debug info
        print(f"DEBUG: doc_topic_matrix shape: {doc_topic_matrix.shape}")
        
        # Create default labels if not provided
        if topic_labels is None:
            topic_labels = [f"Topic {i}" for i in range(doc_topic_matrix.shape[1])]
            
        if document_labels is None:
            document_labels = [f"Doc {i}" for i in range(doc_topic_matrix.shape[0])]
        
        print(f"DEBUG: Number of topic labels: {len(topic_labels)}")
        print(f"DEBUG: Number of document labels: {len(document_labels)}")
            
        # Create figure with size based on number of documents
        # Adjust figure size based on number of docs and topics for better visibility
        width = max(14, min(20, 8 + doc_topic_matrix.shape[0] * 0.3))
        height = max(10, min(16, 6 + doc_topic_matrix.shape[1] * 0.5))
        fig, ax = plt.subplots(figsize=(width, height))
        
        # Transpose the matrix for better visualization (topics as rows)
        # This means topics will be on Y-axis and documents on X-axis
        transposed_matrix = doc_topic_matrix.T
        
        # Force at least 2-D even for 1 topic or 1 document 
        if transposed_matrix.ndim == 1:
            if len(topic_labels) == 1:  # Only 1 topic
                transposed_matrix = transposed_matrix.reshape(1, -1)
            else:  # Only 1 document
                transposed_matrix = transposed_matrix.reshape(-1, 1)
                
        print(f"DEBUG: transposed_matrix shape: {transposed_matrix.shape}")
            
        # Create heatmap
        im = ax.imshow(transposed_matrix, cmap='Blues', aspect='auto')
            
        # Set labels 
        ax.set_yticks(np.arange(len(topic_labels)))
        ax.set_yticklabels(topic_labels)
        
        # If there are many documents, show only a subset of labels
        if len(document_labels) > 40:
            # Show labels for max 40 documents with even spacing
            step = max(1, len(document_labels) // 20)
            xticks = np.arange(0, len(document_labels), step)
            xlabels = [document_labels[i] for i in xticks]
            ax.set_xticks(xticks)
            ax.set_xticklabels(xlabels, rotation=45, ha="right")
        else:
            ax.set_xticks(np.arange(len(document_labels)))
            ax.set_xticklabels(document_labels, rotation=45, ha="right")
            
        # Ensure our changes didn't create any inconsistencies
        if ax.get_xticks().size > 0:
            # Limit label length if needed
            xlabels = [label.get_text()[:30] + "..." if len(label.get_text()) > 30 else label.get_text() 
                      for label in ax.get_xticklabels()]
            ax.set_xticklabels(xlabels, rotation=45, ha="right")
            
        # Add colorbar
        cbar = fig.colorbar(im)
        cbar.set_label('Probability')
            
        # Set title and labels
        ax.set_title('Document-Topic Assignments')
        ax.set_ylabel('Topics')
        ax.set_xlabel('Documents')
            
        # Adjust layout with specific padding
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15, right=0.9)
            
        return fig
        
    except Exception as e:
        logger.error(f"Error generating heatmap: {str(e)}", exc_info=True)
        print(f"DEBUG: Heatmap error: {str(e)}")
            
        # Create error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error generating heatmap: {str(e)}",
                ha='center', va='center', fontsize=12, color='red')
        ax.axis('off')
            
        return fig    
    
def visualize_topic_distribution(topic_counts, topic_labels=None, color='skyblue'):
    """
    Visualize topic distribution across the corpus.
    
    Args:
        topic_counts (dict or list): Dictionary or list of topic counts.
        topic_labels (list): List of topic labels.
        color (str): Color for the bars.
    
    Returns:
        Figure: Matplotlib figure with the topic distribution plot.
    """
    logger.info("Generating topic distribution visualization")
    
    try:
        # Convert input to usable format
        if isinstance(topic_counts, dict):
            topics = list(topic_counts.keys())
            counts = list(topic_counts.values())
        else:
            topics = list(range(len(topic_counts)))
            counts = topic_counts
        
        # Use provided labels or create default labels
        if topic_labels is None:
            topic_labels = [f"Topic {t}" for t in topics]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create bar plot
        ax.bar(topic_labels, counts, color=color)
        
        # Configure plot
        ax.set_xlabel('Topics')
        ax.set_ylabel('Document Count')
        ax.set_title('Topic Distribution')
        ax.set_xticklabels(topic_labels, rotation=45, ha='right')
        
        # Adjust layout
        plt.tight_layout()
        
        return fig
    
    except Exception as e:
        logger.error(f"Error generating topic distribution: {str(e)}", exc_info=True)
        
        # Create error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error generating topic distribution: {str(e)}", 
                ha='center', va='center', fontsize=12, color='red')
        ax.axis('off')
        
        return fig


def visualize_topic_keywords(topics_words, top_n=10, colormap='viridis'):
    """
    Visualize top keywords for each topic.
    
    Args:
        topics_words (dict): Dictionary mapping topic IDs to lists of (word, score) tuples.
        top_n (int): Number of top keywords to display per topic.
        colormap (str): Matplotlib colormap name.
    
    Returns:
        Figure: Matplotlib figure with the topic keywords visualization.
    """
    logger.info(f"Generating topic keywords visualization for top {top_n} words per topic")
    
    try:
        # Filter out outlier topic (-1) if present
        filtered_topics = {t: w for t, w in topics_words.items() if t != -1}
        
        # Determine number of topics and setup plot grid
        num_topics = len(filtered_topics)
        if num_topics == 0:
            raise ValueError("No topics found to visualize")
        
        # Calculate grid dimensions (aiming for roughly square layout)
        cols = int(np.ceil(np.sqrt(num_topics)))
        rows = int(np.ceil(num_topics / cols))
        
        # Create figure
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
        
        # Flatten axes for easier iteration
        if rows * cols > 1:
            axes = axes.flatten()
        else:
            axes = [axes]  # Handle single subplot case
        
        # Get colormap
        cmap = plt.get_cmap(colormap)
        
        # Plot keywords for each topic
        for i, (topic_id, words) in enumerate(sorted(filtered_topics.items())):
            if i >= len(axes):  # Should never happen but just in case
                break
            
            # Get top words and scores
            if words:
                top_words = [word for word, _ in words[:top_n]]
                scores = [score for _, score in words[:top_n]]
                
                # Normalize scores for color mapping
                norm_scores = [(s - min(scores)) / (max(scores) - min(scores)) if max(scores) > min(scores) else 0.5 
                              for s in scores]
                
                # Generate colors
                colors = [cmap(s) for s in norm_scores]
                
                # Create horizontal bar chart
                y_pos = range(len(top_words))
                axes[i].barh(y_pos, scores, color=colors)
                axes[i].set_yticks(y_pos)
                axes[i].set_yticklabels(top_words)
                axes[i].invert_yaxis()  # Display highest score at the top
                axes[i].set_title(f'Topic {topic_id}')
            else:
                axes[i].text(0.5, 0.5, f"No words for Topic {topic_id}", 
                           ha='center', va='center', fontsize=10)
                axes[i].axis('off')
        
        # Hide empty subplots
        for i in range(len(filtered_topics), len(axes)):
            axes[i].axis('off')
        
        # Adjust layout
        plt.tight_layout()
        
        return fig
    
    except Exception as e:
        logger.error(f"Error generating topic keywords visualization: {str(e)}", exc_info=True)
        
        # Create error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error generating topic keywords visualization: {str(e)}", 
                ha='center', va='center', fontsize=12, color='red')
        ax.axis('off')
        
        return fig


class Visualizer(QObject):
    """
    Handles visualization generation.
    
    This class manages the creation of visualizations for text analysis
    and topic modeling results using worker threads to keep the UI responsive.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
    
    def generate_visualization(self, viz_type, data, **kwargs):
        """
        Start generating a visualization.
        
        Args:
            viz_type: Type of visualization to generate
            data: Data for the visualization
            **kwargs: Additional parameters for the visualization
            
        Returns:
            QThread: The worker thread generating the visualization
            
        Note:
            This method starts a worker thread. Results will be emitted via signals.
        """
        # Create and configure worker
        self.worker = VisualizationWorker(viz_type, data, **kwargs)
        
        # Clean up when done
        self.worker.finished.connect(self.worker.deleteLater)
        
        # Start the worker
        self.worker.start()
        
        return self.worker
    
    def highlight_topics_in_documents(self, documents, topic_model, topic_ids, colors):
        """
        Highlight topics in documents with enhanced debugging and support for all model types.
        
        Args:
            documents: List of document strings
            topic_model: Topic model (BERTopic, LDA, NMF, etc.)
            topic_ids: List of topic IDs to highlight
            colors: List of colors for each topic
            
        Returns:
            List of HTML strings with highlighted topics
        """
        import re
        import html
        import logging
        import numpy as np
        import traceback
        from sklearn.feature_extraction.text import CountVectorizer
        
        highlighted_docs = []
        model_type = topic_model.__class__.__name__
        print(f"DEBUG: Highlighting with {model_type} model, topic IDs: {topic_ids}")
        
        # Dictionary to store debug info
        debug_info = {
            "model_type": model_type,
            "topic_ids": topic_ids,
            "has_get_topic": hasattr(topic_model, 'get_topic'),
            "has_components": hasattr(topic_model, 'components_'),
            "attributes": [attr for attr in dir(topic_model) if not attr.startswith('_')]
        }
        print(f"DEBUG: Model attributes: {debug_info}")
        
        # Step 1: Extract topic keywords based on model type
        topic_phrases = {}
        
        # Attempt to get main window and topic info from there first
        from ..ui.main_window import MainWindow
        try:
            main_window = self.window()
            if hasattr(main_window, 'topic_tab') and hasattr(main_window.topic_tab, 'topic_modeler'):
                topic_modeler = main_window.topic_tab.topic_modeler
                if hasattr(topic_modeler, 'topics_words') and topic_modeler.topics_words:
                    for topic_id in topic_ids:
                        if topic_id in topic_modeler.topics_words:
                            topic_phrases[topic_id] = topic_modeler.topics_words[topic_id]
                    print(f"DEBUG: Got topic phrases from topic_modeler: {len(topic_phrases)} topics")
        except Exception as e:
            print(f"DEBUG: Error getting topic_modeler phrases: {str(e)}")
        
        # BERTopic approach - direct method
        if not topic_phrases and hasattr(topic_model, 'get_topic'):
            for topic_id in topic_ids:
                try:
                    words = topic_model.get_topic(topic_id)
                    if words:
                        topic_phrases[topic_id] = words
                        print(f"DEBUG: Got phrases for topic {topic_id} from get_topic(): {words[:3]}")
                except Exception as e:
                    print(f"DEBUG: Error with get_topic({topic_id}): {str(e)}")
        
        # LDA/NMF approach - extract from sklearn-style components
        if not topic_phrases and hasattr(topic_model, 'components_'):
            # Try multiple ways to get feature names
            feature_names = None
            
            # Method 1: feature_names_in_ (sklearn 1.0+)
            if hasattr(topic_model, 'feature_names_in_'):
                feature_names = topic_model.feature_names_in_
                print(f"DEBUG: Got feature names from feature_names_in_: {len(feature_names)} features")
            
            # Method 2: feature_names_ (older sklearn)
            elif hasattr(topic_model, 'feature_names_'):
                feature_names = topic_model.feature_names_
                print(f"DEBUG: Got feature names from feature_names_: {len(feature_names)} features")
            
            # Method 3: Get from vectorizer if available
            elif hasattr(topic_model, 'vectorizer'):
                try:
                    if hasattr(topic_model.vectorizer, 'get_feature_names_out'):
                        feature_names = topic_model.vectorizer.get_feature_names_out()
                    elif hasattr(topic_model.vectorizer, 'get_feature_names'):
                        feature_names = topic_model.vectorizer.get_feature_names()
                    print(f"DEBUG: Got feature names from vectorizer: {len(feature_names)} features")
                except Exception as e:
                    print(f"DEBUG: Error getting feature names from vectorizer: {str(e)}")
            
            # If we have feature names, get topic-word distributions
            if feature_names is not None:
                for idx, topic_id in enumerate(topic_ids):
                    try:
                        # Handle potential index mapping issues
                        topic_idx = topic_id
                        if hasattr(topic_model, 'topic_ids_') and topic_id in topic_model.topic_ids_:
                            # Some models (like sklearn NMF) might need this mapping
                            topic_idx = list(topic_model.topic_ids_).index(topic_id)
                        
                        # Get the topic distribution
                        topic_dist = topic_model.components_[topic_idx]
                        print(f"DEBUG: Got topic distribution for topic {topic_id}, shape: {topic_dist.shape}")
                        
                        # Get top words based on distribution
                        try:
                            # For sparse matrices
                            if hasattr(topic_dist, 'toarray'):
                                topic_dist = topic_dist.toarray()[0]
                        except:
                            # Already dense
                            pass
                        
                        # Get the top words indices for this topic
                        top_indices = topic_dist.argsort()[:-21:-1]  # Top 20 words
                        
                        # Get the actual words and their scores
                        top_words = [(feature_names[i], float(topic_dist[i])) for i in top_indices]
                        topic_phrases[topic_id] = top_words
                        print(f"DEBUG: Successfully extracted words for topic {topic_id}: {top_words[:3]}")
                    except Exception as e:
                        print(f"DEBUG: Error extracting words for topic {topic_id}: {str(e)}\n{traceback.format_exc()}")
        
        # Force CountVectorizer extraction as a backup
        if not topic_phrases and documents:
            print("DEBUG: Attempting CountVectorizer extraction as last resort")
            
            # Group documents by topic (if we have topic assignments)
            topic_docs = {topic_id: [] for topic_id in topic_ids}
            
            # Try to get topic assignments
            try:
                topics_only = False
                doc_topics, doc_probs = None, None
                
                # Method 1: transform returns (topics, probs)
                try:
                    doc_topics, doc_probs = topic_model.transform(documents)
                    if doc_topics is not None:
                        print(f"DEBUG: Got topics via transform: {len(doc_topics)} assignments")
                except Exception as e:
                    print(f"DEBUG: Standard transform failed: {str(e)}")
                
                # Method 2: topics_ attribute might exist
                if doc_topics is None and hasattr(topic_model, 'topics_'):
                    doc_topics = topic_model.topics_
                    topics_only = True
                    print(f"DEBUG: Got topics from topics_ attribute: {len(doc_topics)} topics")
                
                # Method 3: Call predict
                if doc_topics is None and hasattr(topic_model, 'predict'):
                    try:
                        doc_topics = topic_model.predict(documents)
                        topics_only = True
                        print(f"DEBUG: Got topics via predict: {len(doc_topics)} assignments")
                    except Exception as e:
                        print(f"DEBUG: predict() failed: {str(e)}")
                
                # Assign documents to topics
                if doc_topics is not None:
                    for i, topic in enumerate(doc_topics):
                        if topic in topic_ids:
                            topic_docs[topic].append(documents[i])
                    
                    # Count documents per topic
                    for topic_id, docs in topic_docs.items():
                        print(f"DEBUG: Topic {topic_id} has {len(docs)} documents")
            
            except Exception as e:
                print(f"DEBUG: Failed to assign documents to topics: {str(e)}")
            
            # Extract keywords from each topic's documents
            vectorizer = CountVectorizer(max_features=20, stop_words='english')
            
            for topic_id, docs in topic_docs.items():
                if not docs:
                    continue
                    
                try:
                    X = vectorizer.fit_transform(docs)
                    feature_names = vectorizer.get_feature_names_out()
                    
                    # Sum the frequencies for each term
                    sums = X.sum(axis=0).A1
                    
                    # Get the top terms
                    top_indices = sums.argsort()[-20:][::-1]
                    top_terms = [(feature_names[i], float(sums[i])) for i in top_indices]
                    
                    topic_phrases[topic_id] = top_terms
                    print(f"DEBUG: Extracted {len(top_terms)} terms for topic {topic_id} via CountVectorizer")
                except Exception as e:
                    print(f"DEBUG: Failed to extract terms for topic {topic_id}: {str(e)}")
        
        # If nothing else worked, try to extract keywords directly from documents
        if not topic_phrases and len(documents) > 0:
            print("DEBUG: Last resort - extracting keywords from all documents")
            try:
                # Just extract common keywords from all documents
                vectorizer = CountVectorizer(max_features=30, stop_words='english')
                X = vectorizer.fit_transform(documents)
                feature_names = vectorizer.get_feature_names_out()
                
                # Sum frequencies
                sums = X.sum(axis=0).A1
                
                # Get top terms
                top_indices = sums.argsort()[-30:][::-1]
                top_terms = [(feature_names[i], float(sums[i])) for i in top_indices]
                
                # Assign the same terms to all topics
                for topic_id in topic_ids:
                    topic_phrases[topic_id] = top_terms
                
                print(f"DEBUG: Assigned common terms to all topics: {top_terms[:5]}")
            except Exception as e:
                print(f"DEBUG: Failed to extract common terms: {str(e)}")
        
        # Step 2: Highlight documents based on extracted phrases
        print(f"DEBUG: Final topic_phrases has {len(topic_phrases)} topics")
        
        for doc_idx, doc in enumerate(documents):
            try:
                # First check if the model has its own highlighting method
                if hasattr(topic_model, 'highlight_document'):
                    try:
                        html_result = topic_model.highlight_document(doc, topic_ids=topic_ids)
                        if html_result:
                            highlighted_docs.append(html_result)
                            continue
                    except Exception as e:
                        print(f"DEBUG: Native highlighting failed: {str(e)}")
                
                # Use phrase-level highlighting if we have topic phrases
                if topic_phrases:
                    # Create a mapping of phrase to HTML span with color
                    phrase_to_html = {}
                    
                    for topic_idx, topic_id in enumerate(topic_ids):
                        if topic_id not in topic_phrases:
                            continue
                            
                        color_idx = topic_idx % len(colors)
                        color = colors[color_idx]
                        
                        # Get phrases and sort by length (longest first)
                        phrases = [word for word, _ in topic_phrases[topic_id] if len(word) > 2]
                        phrases.sort(key=len, reverse=True)
                        
                        # Create HTML spans for each phrase
                        for phrase in phrases:
                            phrase_lower = phrase.lower()
                            if phrase_lower not in phrase_to_html:
                                phrase_to_html[phrase_lower] = f'<span style="background-color: {color};">{phrase}</span>'
                    
                    # If we have phrases to highlight, do it
                    if phrase_to_html:
                        # Escape HTML characters
                        escaped_doc = html.escape(doc)
                        
                        # Compile regex pattern for all phrases
                        pattern = re.compile(r'\b(' + '|'.join(re.escape(phrase) for phrase in phrase_to_html.keys()) + r')\b', 
                                            flags=re.IGNORECASE)
                        
                        # Replace matches with colored spans
                        def replacer(match):
                            phrase = match.group(0)
                            phrase_lower = phrase.lower()
                            return phrase_to_html.get(phrase_lower, phrase)
                        
                        highlighted_doc = pattern.sub(replacer, escaped_doc)
                        highlighted_doc = f'<div style="font-family: Arial, sans-serif; line-height: 1.6;">{highlighted_doc}</div>'
                        
                        if doc_idx == 0:  # Log sample result
                            print(f"DEBUG: Successfully highlighted document with phrases")
                        
                        highlighted_docs.append(highlighted_doc)
                        continue
                
                # Fallback: sentence-level highlighting
                print(f"DEBUG: Using sentence-level highlighting for document {doc_idx}")
                sentences = [s.strip() for s in doc.split('.') if s.strip()]
                
                try:
                    # Get topic for each sentence
                    sentence_topics, _ = topic_model.transform(sentences)
                    
                    # Generate HTML with sentence highlighting
                    html_output = []
                    for i, (sentence, topic) in enumerate(zip(sentences, sentence_topics)):
                        # Only highlight if topic is in selected topics
                        if topic in topic_ids:
                            topic_idx = topic_ids.index(topic)
                            color = colors[topic_idx % len(colors)]
                            html_output.append(f'<span style="background-color:{color};">{sentence}.</span>')
                        else:
                            html_output.append(f"{sentence}.")
                    
                    highlighted_doc = " ".join(html_output)
                    highlighted_doc = f'<div style="font-family: Arial, sans-serif; line-height: 1.6;">{highlighted_doc}</div>'
                    highlighted_docs.append(highlighted_doc)
                
                except Exception as e:
                    print(f"DEBUG: Sentence highlighting failed: {str(e)}")
                    # If all fails, just add the original document
                    highlighted_docs.append(f'<div style="font-family: Arial, sans-serif; line-height: 1.6;">{html.escape(doc)}</div>')
            
            except Exception as e:
                # If anything goes wrong, add the original document
                print(f"DEBUG: Document highlighting error: {str(e)}")
                highlighted_docs.append(doc)
        
        return highlighted_docs    
    def get_available_visualizations(self):
        """
        Get available visualization types.
        
        Returns:
            dict: Dictionary mapping visualization names to their types
        """
        return {
            'Word Cloud': 'wordcloud',
            'Word Frequency': 'word_freq',
            'N-grams': 'ngrams',
            'Topic Distribution': 'topic_distribution',
            'Topic Keywords': 'topic_keywords',
            'Document-Topic Heatmap': 'topic_heatmap',
            'Topic Highlighting': 'topic_highlighting',
            'Interactive LDA Visualization': 'pyldavis',
            'BERTopic Visualization': 'bertopic_interactive' 
        }
    
    def save_figure(self, fig, filename, dpi=300):
        """
        Save a figure to a file.
        
        Args:
            fig: Matplotlib figure
            filename: Output filename
            dpi: Resolution in dots per inch
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            fig.savefig(filename, dpi=dpi, bbox_inches='tight')
            return True
        except Exception as e:
            logger.error(f"Error saving figure: {str(e)}")
            return False
    
    def figure_to_bytes(self, fig, format='png', dpi=150):
        """
        Convert a figure to bytes for embedding in Qt widgets.
        
        Args:
            fig: Matplotlib figure
            format: Output format ('png', 'jpg', etc.)
            dpi: Resolution in dots per inch
            
        Returns:
            bytes: Image data
        """
        buf = BytesIO()
        fig.savefig(buf, format=format, dpi=dpi, bbox_inches='tight')
        buf.seek(0)
        return buf.getvalue()