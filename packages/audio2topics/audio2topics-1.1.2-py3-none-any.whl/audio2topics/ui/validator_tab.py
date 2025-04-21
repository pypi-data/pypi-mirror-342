#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validator Tab module for the Audio to Topics application.
Provides UI for validating topic quality.
"""

import logging
import pandas as pd
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QGroupBox, QProgressBar, QTabWidget,
                           QTableWidget, QTableWidgetItem, QHeaderView,
                           QMessageBox, QSpinBox, QComboBox, QProgressDialog,
                           QDialog, QStyle)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QColor, QBrush
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

from ..core.validator import TopicValidator

# Configure logging
logger = logging.getLogger(__name__)

class MatplotlibCanvas(FigureCanvas):
    """Canvas for displaying Matplotlib figures"""
    def __init__(self, figure):
        super().__init__(figure)
        self.setMinimumSize(400, 300)

class ValidatorTab(QWidget):
    """Tab for topic validation functionality"""
    
    # Define signals
    validation_completed = pyqtSignal(dict, object)  # Emits metrics and summary dataframe
    progress_updated = pyqtSignal(int, str)  # Emits progress percentage and message
    
    def __init__(self):
        super().__init__()
        
        # Initialize instance variables
        self.documents = []  # Text documents
        self.topics = None  # Topic assignments
        self.topics_words = None  # Words for each topic
        self.topic_info = None  # Topic info dataframe
        self.validator = TopicValidator()  # Validator instance
        
        # Metrics
        self.metrics = None
        self.summary_df = None
        
        # Current figure
        self.current_fig = None
        
        # Set up the UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        # Add header layout for title and help button
        header_layout = QHBoxLayout()        
        # Add introduction/help text
        help_text = (
            "Click on the Help button to learn more about this validation module."
        )
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        help_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        # Add to the header layout, allowing it to expand
        header_layout.addWidget(help_label, 1)
        
        # Help button in the top right
        self.help_button = QPushButton()
        self.help_button.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.help_button.setToolTip("Learn about topic validation metrics")
        self.help_button.setFixedSize(32, 32)  # Make it a square button
        self.help_button.clicked.connect(self.show_help_dialog)
        
        # Add to header layout with no stretching
        header_layout.addWidget(self.help_button, 0, Qt.AlignTop | Qt.AlignRight)
        
        # Add header layout to main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(help_label)
        
        # Controls section
        controls_layout = QHBoxLayout()
        
        # Validate button
        self.validate_button = QPushButton("Validate Topics")
        self.validate_button.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.validate_button.clicked.connect(self.start_validation)
        self.validate_button.setEnabled(False)  # Disabled until data is available
        controls_layout.addWidget(self.validate_button)
        
        # Find optimal topics button
        self.optimize_button = QPushButton("Find Optimal Topics")
        self.optimize_button.setIcon(self.style().standardIcon(QStyle.SP_DialogHelpButton))
        self.optimize_button.clicked.connect(self.show_optimize_dialog)
        self.optimize_button.setEnabled(False)  # Disabled until documents are available
        controls_layout.addWidget(self.optimize_button)
        
        main_layout.addLayout(controls_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setVisible(False)  # Hide initially
        main_layout.addWidget(self.progress_bar)
        
        # Results tab widget
        self.results_tabs = QTabWidget()
        main_layout.addWidget(self.results_tabs, 1)
        
        # Metrics tab
        metrics_tab = QWidget()
        metrics_layout = QVBoxLayout(metrics_tab)
        
        # Metrics table
        self.metrics_table = QTableWidget()
        self.metrics_table.setColumnCount(2)
        self.metrics_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.metrics_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.metrics_table.verticalHeader().setMinimumWidth(30)  
        metrics_layout.addWidget(self.metrics_table)
        
        self.results_tabs.addTab(metrics_tab, "Metrics")
        
        # Topic distribution tab
        distribution_tab = QWidget()
        distribution_layout = QVBoxLayout(distribution_tab)
        
        # Topic distribution table
        self.distribution_table = QTableWidget()
        self.distribution_table.setColumnCount(3)
        self.distribution_table.setHorizontalHeaderLabels(["Topic ID", "Document Count", "Percentage"])
        self.distribution_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.distribution_table.verticalHeader().setMinimumWidth(30)  # Adjust width as needed
        distribution_layout.addWidget(self.distribution_table)
        
        self.results_tabs.addTab(distribution_tab, "Topic Distribution")
        
        # Visualization tab
        viz_tab = QWidget()
        viz_layout = QVBoxLayout(viz_tab)
        
        # This layout will hold the canvas
        self.viz_area = QVBoxLayout()
        viz_layout.addLayout(self.viz_area)
        
        self.results_tabs.addTab(viz_tab, "Visualization")
    
    def set_documents(self, documents):
        """Set the documents for validation"""
        if not documents:
            return
        
        self.documents = documents
        
        # Enable optimize button if documents are available
        self.optimize_button.setEnabled(True)
    
    def set_topics(self, topics, topics_words, topic_info):
        """Set the topics data for validation"""
        self.topics = topics
        self.topics_words = topics_words
        self.topic_info = topic_info
        
        # Enable validate button if topics are available
        self.validate_button.setEnabled(True)
    
    def start_validation(self):
        """Start the topic validation process"""
        if not hasattr(self, 'topics') or self.topics is None:
            QMessageBox.warning(
                self, "No Topics", "No topics available for validation."
            )
            return
            
        if not self.documents:
            QMessageBox.warning(
                self, "No Documents", "No documents available for validation."
            )
            return
        
        # Disable UI elements during validation
        self.validate_button.setEnabled(False)
        self.optimize_button.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        # Get the topic model from the main window
        from ..ui.main_window import MainWindow
        main_window = self.window()
        if hasattr(main_window, 'topic_tab') and hasattr(main_window.topic_tab, 'topic_modeler'):
            topic_model = main_window.topic_tab.topic_modeler.get_model()
            
            if not topic_model:
                QMessageBox.warning(
                    self, "No Model", "No topic model available for validation."
                )
                return
            
            # Create and configure worker
            worker = self.validator.validate_model(self.documents, topic_model)
            
            # Connect worker signals
            worker.progress_updated.connect(self.update_progress)
            worker.validation_completed.connect(self.on_validation_completed)
            worker.error_occurred.connect(self.on_validation_error)
            
            # Forward the progress signal to the main window
            worker.progress_updated.connect(self.progress_updated)
            
            # Update UI
            self.progress_updated.emit(5, "Starting topic validation...")
        else:
            QMessageBox.warning(
                self, "No Model", "No topic model available for validation."
            )
            return
    
    def show_optimize_dialog(self):
        """Show dialog for optimizing number of topics"""
        if not self.documents:
            QMessageBox.warning(
                self, "No Documents", "No documents available for optimization."
            )
            return
        
        dialog = OptimizeTopicsDialog(self.documents, self.validator, self)
        dialog.exec_()
    
    @pyqtSlot(int, str)
    def update_progress(self, progress, message):
        """Update the progress bar and message"""
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(f"{progress}% - {message}")
    
    @pyqtSlot(dict, object)
    def on_validation_completed(self, metrics, summary_df):
        """Handle completed validation"""
        # Store metrics
        self.metrics = metrics
        self.summary_df = summary_df
        
        # Re-enable UI elements
        self.validate_button.setEnabled(True)
        self.optimize_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Update metrics table
        self.update_metrics_table()
        
        # Update topic distribution table
        self.update_distribution_table()
        
        # Create and display visualization
        self.create_visualization()
        
        # Emit signal to notify main window
        self.validation_completed.emit(metrics, summary_df)
    
    @pyqtSlot(str)
    def on_validation_error(self, error_message):
        """Handle validation errors"""
        # Re-enable UI elements
        self.validate_button.setEnabled(True)
        self.optimize_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Show error message
        QMessageBox.warning(
            self, "Validation Error", f"Error during validation: {error_message}"
        )
        
        # Update progress in main window
        self.progress_updated.emit(0, "Validation failed")
    
    def update_metrics_table(self):
        """Update the metrics table with validation results"""
        if not self.metrics:
            return
        
        # Clear existing rows
        self.metrics_table.setRowCount(0)
        
        # Add all metrics except topic_distribution
        row = 0
        for metric, value in self.metrics.items():
            if metric != 'topic_distribution':
                self.metrics_table.insertRow(row)
                
                # Metric name
                name_item = QTableWidgetItem(metric.replace('_', ' ').title())
                self.metrics_table.setItem(row, 0, name_item)
                
                # Metric value
                if isinstance(value, float):
                    value_item = QTableWidgetItem(f"{value:.4f}")
                else:
                    value_item = QTableWidgetItem(str(value))
                
                # Colorize good/bad values
                if metric in ['diversity', 'coherence', 'coverage']:
                    if value >= 0.7:
                        value_item.setBackground(QBrush(QColor(200, 255, 200)))
                    elif value <= 0.3:
                        value_item.setBackground(QBrush(QColor(255, 200, 200)))
                
                self.metrics_table.setItem(row, 1, value_item)
                row += 1
        
        # Resize to contents
        self.metrics_table.resizeColumnsToContents()
    
    def update_distribution_table(self):
        """Update the topic distribution table"""
        if not self.metrics or 'topic_distribution' not in self.metrics:
            return
        
        # Get topic distribution
        distribution = self.metrics['topic_distribution']
        total_docs = sum(distribution.values())
        
        # Clear existing rows
        self.distribution_table.setRowCount(0)
        
        # Add each topic
        for row, (topic_id, count) in enumerate(sorted(distribution.items())):
            self.distribution_table.insertRow(row)
            
            # Topic ID
            id_item = QTableWidgetItem(str(topic_id))
            self.distribution_table.setItem(row, 0, id_item)
            
            # Document count
            count_item = QTableWidgetItem(str(count))
            self.distribution_table.setItem(row, 1, count_item)
            
            # Percentage
            percentage = (count / total_docs) * 100 if total_docs > 0 else 0
            percentage_item = QTableWidgetItem(f"{percentage:.2f}%")
            self.distribution_table.setItem(row, 2, percentage_item)
        
        # Resize to contents
        self.distribution_table.resizeColumnsToContents()
    
    def create_visualization(self):
        """Create visualization of topic distribution"""
        if not self.metrics or 'topic_distribution' not in self.metrics:
            return
        
        # Get topic distribution
        distribution = self.metrics['topic_distribution']
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Create bar chart
        topics = list(distribution.keys())
        counts = list(distribution.values())
        
        topics_str = [f"Topic {t}" for t in topics]
        ax.bar(topics_str, counts, color='skyblue')
        
        # Add labels and title
        ax.set_xlabel('Topics')
        ax.set_ylabel('Document Count')
        ax.set_title('Topic Distribution')
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout
        plt.tight_layout()
        
        # Store the figure
        self.current_fig = fig
        
        # Clear the existing visualization area
        while self.viz_area.count():
            item = self.viz_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create the canvas for the figure
        canvas = MatplotlibCanvas(fig)
        
        # Create the toolbar for the canvas
        toolbar = NavigationToolbar(canvas, self)
        
        # Add the toolbar and canvas to the layout
        self.viz_area.addWidget(toolbar)
        self.viz_area.addWidget(canvas)

    def show_help_dialog(self):
        """Show help dialog with information about topic validation metrics"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QTextBrowser, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Topic Validation Help")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Create tab widget for different help sections
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Overview tab
        overview_tab = QTextBrowser()
        overview_tab.setOpenExternalLinks(True)
        overview_tab.setHtml("""
        <h2>Topic Validation Overview</h2>
        <p>Topic validation helps you assess the quality of your extracted topics and determine if your 
        topic model is effectively capturing the underlying themes in your documents.</p>
            <li>1. Click 'Validate Topics' to analyze the existing topic model.</li>
            <li>2. Use 'Find Optimal Topics' to determine the ideal number of topics.</li>
            <li>3. Review metrics like diversity, coherence, and coverage.</li>
            <li>4. Visualize the validation results.</li> 
        <p>Validation involves:</p>
        <ul>
            <li>Measuring the coherence of topics (do the words belong together?)</li>
            <li>Assessing the diversity of topics (are topics distinct from each other?)</li>
            <li>Analyzing topic coverage (how many documents are assigned to meaningful topics?)</li>
            <li>Examining the distribution of documents across topics</li>
        </ul>
        
        <p>The validator can also help you determine the optimal number of topics to extract from your document collection.</p>
        """)
        tabs.addTab(overview_tab, "Overview")
        
        # Metrics explanation tab
        metrics_tab = QTextBrowser()
        metrics_tab.setHtml("""
        <h2>Understanding Validation Metrics</h2>
        
        <h3>Topic Diversity (0-1)</h3>
        <p>Measures how distinct topics are from each other. Higher values are better.</p>
        <ul>
            <li><b>High diversity (>0.7)</b>: Topics have minimal overlap in keywords</li>
            <li><b>Low diversity (<0.3)</b>: Topics share many keywords, suggesting potential redundancy</li>
        </ul>
        <p>Diversity is calculated by measuring the uniqueness of words across all topics relative to the total number of words.</p>
        
        <h3>Topic Coherence (0-1)</h3>
        <p>Measures how semantically related the words within each topic are. Higher values are better.</p>
        <ul>
            <li><b>High coherence (>0.7)</b>: Words in topics are strongly related</li>
            <li><b>Low coherence (<0.3)</b>: Words in topics appear random or unrelated</li>
        </ul>
        <p>Coherence is based on co-occurrence patterns of words in the documents.</p>
        
        <h3>Topic Coverage (0-100%)</h3>
        <p>The percentage of documents assigned to non-outlier topics (not Topic -1).</p>
        <ul>
            <li><b>High coverage (>80%)</b>: Most documents fit into meaningful topics</li>
            <li><b>Low coverage (<50%)</b>: Many documents don't fit into any clear topic</li>
        </ul>
        
        <h3>Number of Topics</h3>
        <p>The total number of distinct topics (excluding the outlier topic) found in your documents.</p>
        
        <h3>Outliers</h3>
        <p>The number of documents assigned to Topic -1 (the outlier topic).</p>
        """)
        tabs.addTab(metrics_tab, "Metrics")
        
        # Optimization explanation tab
        optimization_tab = QTextBrowser()
        optimization_tab.setHtml("""
        <h2>Finding the Optimal Number of Topics</h2>
        
        <p>The "Find Optimal Topics" feature helps determine the ideal number of topics for your document collection.</p>
        
        <h3>How It Works</h3>
        <p>The optimization process:</p>
        <ol>
            <li>Tests multiple topic counts (from 2 up to the maximum you specify)</li>
            <li>For each count, performs cross-validation by creating multiple topic models with different data splits</li>
            <li>Measures the stability of topics across splits (do similar topics emerge consistently?)</li>
            <li>Measures the diversity of topics (are topics well-separated?)</li>
            <li>Combines stability and diversity into a single quality score</li>
            <li>Recommends the number of topics with the highest combined score</li>
        </ol>
        
        <h3>Parameters</h3>
        <ul>
            <li><b>Maximum Topics to Test</b>: The upper limit for how many topics to consider</li>
            <li><b>Minimum Topic Size</b>: The minimum number of documents required for a topic</li>
        </ul>
        
        <h3>Results Interpretation</h3>
        <p>The results show:</p>
        <ul>
            <li><b>Recommended number</b>: The optimal number of topics based on the analysis</li>
            <li><b>Combined score</b>: A weighted score of stability and diversity (higher is better)</li>
            <li><b>Stability</b>: How consistent topics are across different data splits (higher is better)</li>
            <li><b>Diversity</b>: How distinct the topics are from each other (higher is better)</li>
        </ul>
        """)
        tabs.addTab(optimization_tab, "Optimization")
        
        # Interpretation tab
        interpretation_tab = QTextBrowser()
        interpretation_tab.setHtml("""
        <h2>Interpreting Validation Results</h2>
        
        <h3>When Your Topic Model is Good</h3>
        <p>A high-quality topic model typically shows:</p>
        <ul>
            <li>High diversity (topics are distinct from each other)</li>
            <li>High coherence (words within topics make sense together)</li>
            <li>High coverage (most documents are assigned to non-outlier topics)</li>
            <li>Relatively balanced distribution of documents across topics</li>
        </ul>
        
        <h3>Common Issues and Solutions</h3>
        
        <h4>Too Many Outliers (Low Coverage)</h4>
        <ul>
            <li><b>Problem</b>: Many documents assigned to Topic -1 (outlier topic)</li>
            <li><b>Possible solutions</b>:
                <ul>
                    <li>Decrease the minimum topic size</li>
                    <li>Improve text preprocessing or cleaning</li>
                    <li>Try a different number of topics</li>
                </ul>
            </li>
        </ul>
        
        <h4>Low Diversity</h4>
        <ul>
            <li><b>Problem</b>: Topics share many of the same keywords</li>
            <li><b>Possible solutions</b>:
                <ul>
                    <li>Reduce the number of topics</li>
                    <li>Improve stopword removal</li>
                    <li>Use the "Find Optimal Topics" feature</li>
                </ul>
            </li>
        </ul>
        
        <h4>Imbalanced Distribution</h4>
        <ul>
            <li><b>Problem</b>: Most documents fall into just a few topics</li>
            <li><b>Possible solutions</b>:
                <ul>
                    <li>Adjust the minimum topic size</li>
                    <li>Increase the number of topics</li>
                    <li>Consider if the imbalance reflects your actual data</li>
                </ul>
            </li>
        </ul>
        """)
        tabs.addTab(interpretation_tab, "Interpretation")
        
        # Tips tab
        tips_tab = QTextBrowser()
        tips_tab.setHtml("""
        <h2>Tips for Topic Validation</h2>
        
        <h3>General Workflow</h3>
        <ol>
            <li>Run the "Find Optimal Topics" feature first to get a recommended topic count</li>
            <li>Extract topics using the recommended count in the Extract Topics tab</li>
            <li>Validate the resulting topics</li>
            <li>If validation metrics show issues, adjust parameters and try again</li>
            <li>Refine topics with an LLM for better interpretability</li>
        </ol>
        
        <h3>Balancing Quality Metrics</h3>
        <p>Sometimes you need to prioritize certain metrics over others:</p>
        <ul>
            <li>For <b>exploratory analysis</b>, prioritize diversity and coverage</li>
            <li>For <b>content summarization</b>, prioritize coherence</li>
            <li>For <b>document classification</b>, prioritize balanced topic distribution</li>
        </ul>
        
        <h3>Validation with Small Document Collections</h3>
        <p>With fewer documents:</p>
        <ul>
            <li>Use smaller minimum topic sizes</li>
            <li>Extract fewer topics (often 3-5 is sufficient)</li>
            <li>Pay more attention to coherence than diversity</li>
            <li>Consider that cross-validation results might be less reliable</li>
        </ul>
        
        <h3>Combining with Other Tabs</h3>
        <ul>
            <li>Use the <b>Visualizer tab</b> to see topic distribution and keyword importance</li>
            <li>Try <b>Topic Highlighting</b> to see how topics appear in your actual documents</li>
            <li>Consider <b>LLM refinement</b> to improve topic interpretability without changing the underlying model</li>
        </ul>
        """)
        tabs.addTab(tips_tab, "Tips")
        
        # Add OK button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        # Show the dialog
        dialog.exec_()

class OptimizeTopicsDialog(QMessageBox):
    """Dialog for finding the optimal number of topics"""
    
    def __init__(self, documents, validator, parent=None):
        super().__init__(parent)
        
        self.documents = documents
        self.validator = validator
        
        self.setWindowTitle("Find Optimal Number of Topics")
        self.setIcon(QMessageBox.Information)
        self.setText("This will analyze your documents to find the optimal number of topics.\n\n"
                   "The process may take some time depending on the number of documents.")
        
        # Create widgets for parameters
        self.parameters_widget = QWidget()
        parameters_layout = QVBoxLayout(self.parameters_widget)
        
        # Number of topics to test
        max_topics_layout = QHBoxLayout()
        max_topics_layout.addWidget(QLabel("Maximum Topics to Test:"))
        
        self.max_topics_spin = QSpinBox()
        self.max_topics_spin.setRange(5, 30)
        self.max_topics_spin.setValue(15)
        max_topics_layout.addWidget(self.max_topics_spin)
        
        parameters_layout.addLayout(max_topics_layout)
        
        # Minimum topic size
        min_size_layout = QHBoxLayout()
        min_size_layout.addWidget(QLabel("Minimum Topic Size:"))
        
        self.min_size_spin = QSpinBox()
        self.min_size_spin.setRange(1, 10)
        self.min_size_spin.setValue(2)
        min_size_layout.addWidget(self.min_size_spin)
        
        parameters_layout.addLayout(min_size_layout)
        
        # Add the parameters widget to the dialog
        self.setInformativeText("Please set the parameters for optimization:")
        self.layout().addWidget(self.parameters_widget, 1, 1)
        
        # Add buttons
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.button(QMessageBox.Ok).setText("Start Optimization")
        
        # Connect signals
        self.buttonClicked.connect(self.on_button_clicked)
    
    def on_button_clicked(self, button):
        """Handle button clicks"""
        if button == self.button(QMessageBox.Ok):
            self.start_optimization()
    
    def start_optimization(self):
        """Start the optimization process"""
        # Get parameters
        max_topics = self.max_topics_spin.value()
        min_topic_size = self.min_size_spin.value()
        
        # Create a progress dialog
        progress = QProgressDialog("Finding optimal topics, this may take a moment...", "Cancel", 0, 100, self)
        progress.setWindowTitle("Optimization in Progress")
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        # Make the dialog larger
        progress.setMinimumSize(400, 150)  # Set minimum width and height
        progress.show()
        
        # Create and configure worker
        worker = self.validator.find_optimal_topics(
            self.documents, max_topics, min_topic_size
        )
        
        # Connect worker signals
        worker.progress_updated.connect(progress.setValue)
        worker.optimization_completed.connect(lambda result: self.on_optimization_completed(result, progress))
        worker.error_occurred.connect(lambda error: self.on_optimization_error(error, progress))
        
        # Start the worker
        worker.start()
    
    def on_optimization_completed(self, result, progress_dialog):
        """Handle completed optimization"""
        # Close the progress dialog
        progress_dialog.close()
        
        # Show results
        recommended = result.get('recommended_topics', 0)
        score = result.get('combined_score', 0)
        stability = result.get('stability', 0)
        diversity = result.get('diversity', 0)
        
        result_dialog = QMessageBox(self)
        result_dialog.setWindowTitle("Optimization Results")
        result_dialog.setIcon(QMessageBox.Information)
        result_dialog.setText(f"Recommended number of topics: {recommended}")
        result_dialog.setInformativeText(
            f"Combined score: {score:.4f}\n"
            f"Stability: {stability:.4f}\n"
            f"Diversity: {diversity:.4f}"
        )
        
        # Create a visualization of the results
        if 'all_results' in result:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Extract data
            all_results = result['all_results']
            n_topics = [r['n_topics'] for r in all_results]
            combined_scores = [r['combined_score'] for r in all_results]
            stability_scores = [r['stability'] for r in all_results]
            diversity_scores = [r['diversity'] for r in all_results]
            
            # Plot data
            ax.plot(n_topics, combined_scores, 'o-', label='Combined Score')
            ax.plot(n_topics, stability_scores, 's-', label='Stability')
            ax.plot(n_topics, diversity_scores, '^-', label='Diversity')
            
            # Highlight recommended
            ax.axvline(x=recommended, color='r', linestyle='--', alpha=0.5)
            
            # Add labels and title
            ax.set_xlabel('Number of Topics')
            ax.set_ylabel('Score')
            ax.set_title('Topic Optimization Results')
            ax.legend()
            
            # Convert figure to QPixmap
            from io import BytesIO
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100)
            buf.seek(0)
            
            from PyQt5.QtGui import QPixmap
            pixmap = QPixmap()
            pixmap.loadFromData(buf.read())
            
            # Create label and set pixmap
            label = QLabel()
            label.setPixmap(pixmap)
            
            # Add to dialog
            result_dialog.layout().addWidget(label, 2, 1, 1, 2)
        
        result_dialog.exec_()
    
    def on_optimization_error(self, error, progress_dialog):
        """Handle optimization errors"""
        # Close the progress dialog
        progress_dialog.close()
        
        # Show error message
        QMessageBox.warning(
            self, "Optimization Error", f"Error during optimization: {error}"
        )