#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparison Tab module for the Audio to Topics application.
Provides UI for comparing different topic modeling runs.
"""

import os
import logging
import json
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QTableWidget, QTableWidgetItem, QComboBox,
                           QSpinBox, QGroupBox, QDialog, QFormLayout, QTabWidget,
                           QFileDialog, QMessageBox, QProgressBar, QCheckBox,
                           QListWidget, QListWidgetItem, QSplitter, QSizePolicy,
                           QScrollArea, QRadioButton, QButtonGroup, QStyle, QLineEdit, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QIcon

from ..core.topic_modeler import TopicModeler

# Configure logging
logger = logging.getLogger(__name__)

# Define layout constants
LAYOUT_MARGIN = 10
WIDGET_SPACING = 8
BUTTON_HEIGHT = 30
BUTTON_MIN_WIDTH = 120

class TopicModelRun:
    """Class to store information about a topic modeling run"""
    
    def __init__(self, name, method, parameters, documents, topics, 
                topic_words, topic_info, probabilities=None, 
                timestamp=None, metrics=None):
        self.name = name
        self.method = method
        self.parameters = parameters
        self.documents = documents
        self.topics = topics
        self.topic_words = topic_words
        self.topic_info = topic_info
        self.probabilities = probabilities
        self.timestamp = timestamp or datetime.datetime.now()
        self.metrics = metrics or {}
    
    def to_dict(self):
        """Convert run to dictionary for serialization"""
        return {
            'name': self.name,
            'method': self.method,
            'parameters': self.parameters,
            'timestamp': self.timestamp.isoformat(),
            'metrics': self.metrics
        }
    
    @staticmethod
    def from_dict(data, documents, topics, topic_words, topic_info, probabilities=None):
        """Create a run from dictionary and result data"""
        timestamp = datetime.datetime.fromisoformat(data['timestamp'])
        return TopicModelRun(
            data['name'], data['method'], data['parameters'],
            documents, topics, topic_words, topic_info,
            probabilities, timestamp, data['metrics']
        )

class RunConfigDialog(QDialog):
    """Dialog for configuring a single topic model run"""
    
    def __init__(self, run_num, parent=None):
        super().__init__(parent)
        self.run_num = run_num
        
        self.setWindowTitle(f"Configure Run {run_num}")
        self.setMinimumSize(500, 400)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Form layout for run settings
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setHorizontalSpacing(WIDGET_SPACING)
        form_layout.setVerticalSpacing(WIDGET_SPACING)
        
        # Run name
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        default_name = f"Run {self.run_num} ({timestamp})"
        self.name_edit = QLineEdit(default_name)
        form_layout.addRow("Run Name:", self.name_edit)
        
        # Method selection
        self.method_combo = QComboBox()
        self.method_combo.addItem("BERTopic (UMAP)", "bertopic")
        self.method_combo.addItem("BERTopic (PCA)", "bertopic-pca")
        self.method_combo.addItem("NMF", "nmf")
        self.method_combo.addItem("LDA", "lda")
        self.method_combo.currentIndexChanged.connect(self.update_method_options)
        form_layout.addRow("Method:", self.method_combo)
        
        # Language selection
        self.language_combo = QComboBox()
        self.language_combo.addItems(["multilingual", "english"])
        form_layout.addRow("Language:", self.language_combo)
        
        # Number of topics
        self.topics_combo = QComboBox()
        self.topics_combo.addItem("Auto", "auto")
        for i in range(2, 21):
            self.topics_combo.addItem(str(i), i)
        form_layout.addRow("Number of Topics:", self.topics_combo)
        
        # Minimum topic size
        self.min_size_spin = QSpinBox()
        self.min_size_spin.setRange(1, 50)
        self.min_size_spin.setValue(2)
        form_layout.addRow("Min Topic Size:", self.min_size_spin)
        
        # N-gram range
        ngram_layout = QHBoxLayout()
        ngram_layout.setSpacing(WIDGET_SPACING)

        self.min_ngram_spin = QSpinBox()
        self.min_ngram_spin.setRange(1, 5)
        self.min_ngram_spin.setValue(1)
        self.min_ngram_spin.valueChanged.connect(self.update_ngram_range)
        ngram_layout.addWidget(QLabel("Min:"))
        ngram_layout.addWidget(self.min_ngram_spin)

        ngram_layout.addSpacing(10)  # Add a little spacing between the controls

        self.max_ngram_spin = QSpinBox()
        self.max_ngram_spin.setRange(1, 5)
        self.max_ngram_spin.setValue(2)
        self.max_ngram_spin.valueChanged.connect(self.update_ngram_range)
        ngram_layout.addWidget(QLabel("Max:"))
        ngram_layout.addWidget(self.max_ngram_spin)

        form_layout.addRow("N-gram Range:", ngram_layout)
        
        # LDA options group (initially hidden)
        self.lda_options_group = QGroupBox("LDA Options")
        self.lda_options_group.setVisible(False)
        self.lda_options_group.setCheckable(True)
        self.lda_options_group.setChecked(False)
        lda_options_layout = QVBoxLayout(self.lda_options_group)
        lda_options_layout.setSpacing(WIDGET_SPACING)
        
        # Elbow method checkbox
        self.elbow_checkbox = QCheckBox("Use elbow method to find optimal number of topics")
        self.elbow_checkbox.setChecked(False)
        self.elbow_checkbox.toggled.connect(self.toggle_elbow_options)
        lda_options_layout.addWidget(self.elbow_checkbox)
        
        # Elbow method parameters
        elbow_form = QFormLayout()
        elbow_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        elbow_form.setLabelAlignment(Qt.AlignRight)
        
        # Min topics
        self.min_topics_spin = QSpinBox()
        self.min_topics_spin.setRange(2, 20)
        self.min_topics_spin.setValue(2)
        self.min_topics_spin.setEnabled(False)  # Initially disabled
        elbow_form.addRow("Min Topics:", self.min_topics_spin)
        
        # Max topics
        self.max_topics_spin = QSpinBox()
        self.max_topics_spin.setRange(5, 50)
        self.max_topics_spin.setValue(15)
        self.max_topics_spin.setEnabled(False)  # Initially disabled
        elbow_form.addRow("Max Topics:", self.max_topics_spin)
        
        # Step size
        self.step_size_spin = QSpinBox()
        self.step_size_spin.setRange(1, 5)
        self.step_size_spin.setValue(1)
        self.step_size_spin.setEnabled(False)  # Initially disabled
        elbow_form.addRow("Step:", self.step_size_spin)
        
        lda_options_layout.addLayout(elbow_form)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.lda_options_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(WIDGET_SPACING)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setMinimumHeight(BUTTON_HEIGHT)
        cancel_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        buttons_layout.addWidget(cancel_button)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        ok_button.setMinimumHeight(BUTTON_HEIGHT)
        ok_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        buttons_layout.addWidget(ok_button)
        
        layout.addLayout(buttons_layout)
    
    def update_method_options(self, index):
        """Show/hide options based on selected method"""
        method = self.method_combo.currentData()
        if method == "lda":
            self.lda_options_group.setVisible(True)
        else:
            self.lda_options_group.setVisible(False)
    
    def toggle_elbow_options(self, checked):
        """Enable/disable elbow method options"""
        self.min_topics_spin.setEnabled(checked)
        self.max_topics_spin.setEnabled(checked)
        self.step_size_spin.setEnabled(checked)
    
    def update_ngram_range(self):
        """Ensure min_ngram is always <= max_ngram"""
        if self.min_ngram_spin.value() > self.max_ngram_spin.value():
            if self.sender() == self.min_ngram_spin:
                self.max_ngram_spin.setValue(self.min_ngram_spin.value())
            else:
                self.min_ngram_spin.setValue(self.max_ngram_spin.value())
    
    def get_run_config(self):
        """Get the run configuration as a dictionary"""
        method = self.method_combo.currentData()
        config = {
            'name': self.name_edit.text(),
            'method': method,
            'language': self.language_combo.currentText(),
            'nr_topics': self.topics_combo.currentData(),
            'min_topic_size': self.min_size_spin.value(),
            'n_gram_range': (self.min_ngram_spin.value(), self.max_ngram_spin.value()),
            'adaptive_enabled': True,  # Set defaults for adaptive processing
            'max_retries': 5,
            'initial_chunk_size': 100,
        }
        
        # Add LDA-specific options if applicable
        if method == "lda":
            config['lda_elbow_enabled'] = self.elbow_checkbox.isChecked()
            if self.elbow_checkbox.isChecked():
                config['lda_elbow_params'] = {
                    'min_topics': self.min_topics_spin.value(),
                    'max_topics': self.max_topics_spin.value(),
                    'step_size': self.step_size_spin.value()
                }
        
        return config

class ComparisonRunDialog(QDialog):
    """Dialog for configuring comparison runs"""
    
    def __init__(self, documents, parent=None):
        super().__init__(parent)
        self.documents = documents
        self.runs = []  # Will store configured runs
        
        self.setWindowTitle("Configure Comparison Runs")
        self.setMinimumSize(700, 500)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Add instructions
        instruction_label = QLabel(
            "Configure multiple topic model runs to compare. "
            "Add 2-5 runs with different methods or parameters."
        )
        instruction_label.setWordWrap(True)
        layout.addWidget(instruction_label)
        
        # Add runs group box
        runs_group = QGroupBox("Configured Runs")
        runs_layout = QVBoxLayout(runs_group)
        
        # Runs list
        self.runs_list = QListWidget()
        runs_layout.addWidget(self.runs_list)
        
        # Button for adding runs
        buttons_layout = QHBoxLayout()
        
        add_run_button = QPushButton("Add Run")
        add_run_button.clicked.connect(self.add_run)
        add_run_button.setMinimumHeight(BUTTON_HEIGHT)
        buttons_layout.addWidget(add_run_button)
        
        remove_run_button = QPushButton("Remove Selected")
        remove_run_button.clicked.connect(self.remove_run)
        remove_run_button.setMinimumHeight(BUTTON_HEIGHT)
        buttons_layout.addWidget(remove_run_button)
        
        runs_layout.addLayout(buttons_layout)
        layout.addWidget(runs_group)
        
        # Dialog buttons
        dialog_buttons_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setMinimumHeight(BUTTON_HEIGHT)
        cancel_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        dialog_buttons_layout.addWidget(cancel_button)
        
        start_button = QPushButton("Start Comparison")
        start_button.clicked.connect(self.accept)
        start_button.setDefault(True)
        start_button.setMinimumHeight(BUTTON_HEIGHT)
        start_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        dialog_buttons_layout.addWidget(start_button)
        
        layout.addLayout(dialog_buttons_layout)
    
    def add_run(self):
        """Add a new run configuration"""
        if len(self.runs) >= 5:
            QMessageBox.warning(
                self, "Maximum Runs", "You can only configure up to 5 runs for comparison."
            )
            return
        
        run_dialog = RunConfigDialog(len(self.runs) + 1, self)
        if run_dialog.exec_():
            run_config = run_dialog.get_run_config()
            self.runs.append(run_config)
            self.update_runs_list()
    
    def remove_run(self):
        """Remove the selected run"""
        selected_items = self.runs_list.selectedItems()
        if not selected_items:
            return
        
        for item in selected_items:
            index = self.runs_list.row(item)
            self.runs.pop(index)
        
        self.update_runs_list()
    
    def update_runs_list(self):
        """Update the list of configured runs"""
        self.runs_list.clear()
        
        for i, run in enumerate(self.runs):
            name = run['name']
            method = run['method']
            item_text = f"Run {i+1}: {name} - Method: {method}"
            item = QListWidgetItem(item_text)
            self.runs_list.addItem(item)
    
    def get_runs(self):
        """Get the configured runs"""
        return self.runs

class ComparisonTab(QWidget):
    """Tab for comparing different topic modeling runs"""
    
    # Define signals
    progress_updated = pyqtSignal(int, str)  # Emits progress percentage and message
    
    def __init__(self):
        super().__init__()
        
        # Initialize instance variables
        self.documents = []  # Documents used for comparison
        self.runs = {}  # Dictionary mapping run IDs to TopicModelRun objects
        self.current_run_id = 0  # Counter for assigning unique run IDs
        self.topic_modeler = TopicModeler()  # Topic modeler instance
        self.runs_config = []  # Store runs configuration list

        
        # Set up the UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(WIDGET_SPACING)
        main_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Add header layout for title and help button
        header_layout = QHBoxLayout()
        header_layout.setSpacing(WIDGET_SPACING)
        
        # Add introduction/help text
        help_text = (
            "Compare different topic modeling runs to find the optimal approach for your data."
        )
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        help_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        header_layout.addWidget(help_label, 1)
        
        # Help button in the top right
        self.help_button = QPushButton()
        self.help_button.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.help_button.setToolTip("Learn about topic model comparison")
        self.help_button.setFixedSize(32, 32)  # Make it a square button
        self.help_button.clicked.connect(self.show_help_dialog)
        header_layout.addWidget(self.help_button, 0, Qt.AlignTop | Qt.AlignRight)
        
        # Add header layout to main layout
        main_layout.addLayout(header_layout)
        
        # Controls section
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(WIDGET_SPACING)
        
        # Start comparison button
        self.compare_button = QPushButton("Start New Comparison")
        self.compare_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.compare_button.clicked.connect(self.start_comparison)
        self.compare_button.setEnabled(True)  # Enabled by default
        self.compare_button.setMinimumHeight(BUTTON_HEIGHT)
        self.compare_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        controls_layout.addWidget(self.compare_button)
        
        # Export report button
        self.export_button = QPushButton("Export Report")
        self.export_button.setIcon(self.style().standardIcon(QStyle.SP_CommandLink))
        self.export_button.clicked.connect(self.export_report)
        self.export_button.setEnabled(False)  # Disabled until comparison is done
        self.export_button.setMinimumHeight(BUTTON_HEIGHT)
        self.export_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        controls_layout.addWidget(self.export_button)
        
        main_layout.addLayout(controls_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setVisible(False)  # Hide initially
        main_layout.addWidget(self.progress_bar)
        
        # Create a splitter for run selection and visualizations
        self.main_splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(self.main_splitter, 1)  # Give it stretch factor
        
        # Run selection section
        run_selection_group = QGroupBox("Comparison Runs")
        run_selection_layout = QVBoxLayout(run_selection_group)
        run_selection_layout.setSpacing(WIDGET_SPACING)
        
        # Apply custom CSS to set indicator width
        style_sheet = """
        QTableView::indicator, QTreeView::indicator {
            width: 30px;
            height: 20px;
        }
        QTableWidget {
            gridline-color: #d0d0d0;
        }
        """
        
        # Run table with checkboxes for selection
        self.run_table = QTableWidget()
        self.run_table.verticalHeader().setMinimumWidth(30) 
        self.run_table.setStyleSheet(style_sheet)
        self.run_table.setColumnCount(5)
        self.run_table.setHorizontalHeaderLabels(["Name", "Method", "Topics", "Parameters", "Metrics"])
        self.run_table.horizontalHeader().setStretchLastSection(True)
        self.run_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.run_table.setSelectionMode(QTableWidget.MultiSelection)
        self.run_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make read-only
        run_selection_layout.addWidget(self.run_table)
        
        # Add run selection group to splitter
        self.main_splitter.addWidget(run_selection_group)
        
        # Tabs for different visualizations
        self.viz_tabs = QTabWidget()
        
        # Set size policy to make visualization area expand
        self.viz_tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Topics comparison tab
        topics_tab = QWidget()
        topics_layout = QVBoxLayout(topics_tab)
        topics_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        topics_layout.setSpacing(WIDGET_SPACING)
        
        # Add placeholder for the heatmap
        self.topic_similarity_plot = QLabel("No comparison data available. Start a comparison to visualize results.")
        self.topic_similarity_plot.setAlignment(Qt.AlignCenter)
        self.topic_similarity_plot.setStyleSheet("background-color: #f5f5f5; padding: 20px; border: 1px solid #ddd;")
        self.topic_similarity_plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        topics_layout.addWidget(self.topic_similarity_plot)
        
        self.viz_tabs.addTab(topics_tab, "Topic Similarity")
        
        # Word comparison tab
        words_tab = QWidget()
        words_layout = QVBoxLayout(words_tab)
        words_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        words_layout.setSpacing(WIDGET_SPACING)
        
        # Controls for word comparison
        word_controls = QHBoxLayout()
        word_controls.setSpacing(WIDGET_SPACING)
        
        word_controls.addWidget(QLabel("Select Topic:"))
        self.topic_selector = QComboBox()
        self.topic_selector.currentIndexChanged.connect(self.update_word_comparison)
        word_controls.addWidget(self.topic_selector)
        
        words_layout.addLayout(word_controls)
        
        # Add placeholder for the word comparison chart
        self.word_comparison_plot = QLabel("No comparison data available. Start a comparison to visualize results.")
        self.word_comparison_plot.setAlignment(Qt.AlignCenter)
        self.word_comparison_plot.setStyleSheet("background-color: #f5f5f5; padding: 20px; border: 1px solid #ddd;")
        self.word_comparison_plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        words_layout.addWidget(self.word_comparison_plot)
        
        self.viz_tabs.addTab(words_tab, "Word Weights")
        
        # Distribution tab
        dist_tab = QWidget()
        dist_layout = QVBoxLayout(dist_tab)
        dist_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        dist_layout.setSpacing(WIDGET_SPACING)
        
        # Add placeholder for the distribution chart
        self.distribution_plot = QLabel("No comparison data available. Start a comparison to visualize results.")
        self.distribution_plot.setAlignment(Qt.AlignCenter)
        self.distribution_plot.setStyleSheet("background-color: #f5f5f5; padding: 20px; border: 1px solid #ddd;")
        self.distribution_plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        dist_layout.addWidget(self.distribution_plot)
        
        self.viz_tabs.addTab(dist_tab, "Topic Distribution")
        
        # Parameters impact tab
        params_tab = QWidget()
        params_layout = QVBoxLayout(params_tab)
        params_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        params_layout.setSpacing(WIDGET_SPACING)
        
        # Add placeholder for the parameters impact chart
        self.params_impact_plot = QLabel("No comparison data available. Start a comparison to visualize results.")
        self.params_impact_plot.setAlignment(Qt.AlignCenter)
        self.params_impact_plot.setStyleSheet("background-color: #f5f5f5; padding: 20px; border: 1px solid #ddd;")
        self.params_impact_plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        params_layout.addWidget(self.params_impact_plot)
        
        self.viz_tabs.addTab(params_tab, "Parameter Impact")
        
        # Summary report tab
        report_tab = QWidget()
        report_layout = QVBoxLayout(report_tab)
        report_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        report_layout.setSpacing(WIDGET_SPACING)
        
        # Add text area for summary report
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setPlaceholderText("Run a comparison to generate a summary report.")
        self.report_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        report_layout.addWidget(self.report_text)
        
        self.viz_tabs.addTab(report_tab, "Summary Report")
        
        # Add visualization tabs to splitter
        self.main_splitter.addWidget(self.viz_tabs)
        
        # Set initial splitter sizes - 30% for run selection, 70% for visualizations
        self.main_splitter.setSizes([300, 700])    
    def set_documents(self, documents):
        """Set the documents to be used for topic modeling"""
        if not documents:
            return
        
        self.documents = documents
        
        # Enable the comparison button
        self.compare_button.setEnabled(True)
        
        # Update status
        self.progress_updated.emit(0, f"Ready to compare topic models on {len(documents)} documents")
    
    def start_comparison(self):
        """Start a new comparison"""
        if not self.documents:
            QMessageBox.warning(
                self, "No Documents", 
                    "Please load or process documents and use one topic extarction method from 'Extract Topics' tab first."
            )
            return
        
        # Show dialog to configure runs
        dialog = ComparisonRunDialog(self.documents, self)
        if dialog.exec_():
            runs_config = dialog.get_runs()
            
            if len(runs_config) < 2:
                QMessageBox.warning(
                    self, "Insufficient Runs", 
                    "Please configure at least 2 runs for comparison."
                )
                return
            
            # Clear existing runs if any
            self.runs = {}
            
            # Disable UI controls during processing
            self.compare_button.setEnabled(False)
            
            # Show progress bar
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
            
            # Start the comparison process
            self.execute_runs(runs_config)
    
    def execute_runs(self, runs_config):
        """Execute multiple topic model runs in sequence"""
        self.progress_updated.emit(0, f"Starting comparison with {len(runs_config)} runs...")
        
        # Store the runs_config list as an instance variable so it can be accessed across methods
        self.runs_config = runs_config
        
        # Process each run in sequence
        self.process_next_run(0)

    def process_next_run(self, run_index):
        """Process the next run in the sequence"""
        if run_index >= len(self.runs_config):
            # All runs are complete
            self.on_comparison_complete()
            return
        
        # Get the configuration for this run
        run_config = self.runs_config[run_index]
        self.progress_updated.emit(
            int(run_index * 100 / len(self.runs_config)),
            f"Processing run {run_index+1}/{len(self.runs_config)}: {run_config['name']}..."
        )
        
        # Create and configure worker
        worker = self.topic_modeler.extract_topics(
            self.documents,
            language=run_config['language'],
            n_gram_range=run_config['n_gram_range'],
            min_topic_size=run_config['min_topic_size'],
            nr_topics=run_config['nr_topics'],
            adaptive_enabled=run_config.get('adaptive_enabled', True),
            max_retries=run_config.get('max_retries', 5),
            initial_chunk_size=run_config.get('initial_chunk_size', 100),
            method=run_config['method'],
            lda_elbow_enabled=run_config.get('lda_elbow_enabled', False),
            lda_elbow_params=run_config.get('lda_elbow_params', None)
        )
        
        # Connect worker signals
        worker.progress_updated.connect(self.update_run_progress)
        worker.topics_extracted.connect(
            lambda topics, probs, topics_words, topic_info, model, chunked_docs: 
            self.on_run_complete(run_config, topics, probs, topics_words, topic_info, model, run_index)
        )
        worker.error_occurred.connect(
            lambda error: self.on_run_error(error, run_config, run_index)
        )
        
        # Connect the show_elbow_dialog signal to our new handler
        worker.show_elbow_dialog.connect(
            lambda model_scores, topics_range: 
            self.handle_elbow_dialog(worker, model_scores, topics_range)
        )
        
        # Forward progress updates
        worker.progress_updated.connect(self.progress_updated)

    def handle_elbow_dialog(self, worker, model_scores, topics_range):
        """Handle the elbow method dialog for LDA topic selection"""
        # Create a dialog for the elbow method
        dialog = QDialog(self)
        dialog.setWindowTitle("LDA Elbow Method - Select Optimal Number of Topics")
        dialog.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Add description label
        description = QLabel(
            "The elbow method helps find the optimal number of topics. "
            "Look for the 'elbow' point where adding more topics gives diminishing returns."
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Create figure for the elbow plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(topics_range, model_scores, marker='o', linewidth=2)
        ax.set_xlabel('Number of Topics')
        ax.set_ylabel('Model Score')
        ax.set_title('LDA Topic Model Performance')
        ax.grid(True)
        
        # Create canvas for the plot
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(350)
        layout.addWidget(canvas)
        
        # Add a form for selecting the number of topics
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Select number of topics:"))
        
        # Spinbox for selecting number of topics
        topic_spinbox = QSpinBox()
        topic_spinbox.setRange(min(topics_range), max(topics_range))
        
        # Try to find the elbow point and set it as default
        try:
            # If available, use scipy to find local minima/maxima
            from scipy.signal import argrelextrema
            import numpy as np
            
            # Convert to numpy array for processing
            scores_array = np.array(model_scores)
            
            # Find the maximum score (often a good choice for default)
            max_index = np.argmax(scores_array)
            default_topics = topics_range[max_index]
            
        except Exception as e:
            # If any error occurs, just use the midpoint
            default_topics = topics_range[len(topics_range) // 2]
        
        topic_spinbox.setValue(default_topics)
        form_layout.addWidget(topic_spinbox)
        layout.addLayout(form_layout)
        
        # Add buttons
        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: self.on_elbow_dialog_closed(dialog, worker, None))
        cancel_button.setMinimumHeight(BUTTON_HEIGHT)
        button_layout.addWidget(cancel_button)
        
        select_button = QPushButton("Select")
        select_button.clicked.connect(lambda: self.on_elbow_dialog_closed(dialog, worker, topic_spinbox.value()))
        select_button.setDefault(True)
        select_button.setMinimumHeight(BUTTON_HEIGHT)
        button_layout.addWidget(select_button)
        layout.addLayout(button_layout)
        
        # Show the dialog - using exec_ to make it modal
        dialog.exec_()

    def on_elbow_dialog_closed(self, dialog, worker, result):
        """Handle the closing of the elbow dialog"""
        # Close the dialog
        dialog.close()
        
        if result is None:
            # User canceled, set the cancellation flag
            worker.elbow_selection_cancelled = True
        else:
            # Set the result in the worker
            worker.elbow_selection_result = result
            
    @pyqtSlot(int, str)
    def update_run_progress(self, progress, message):
        """Update progress bar for the current run"""
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(f"{progress}% - {message}")
    
    @pyqtSlot(dict, object, object, object, object, object, int)
    def on_run_complete(self, run_config, topics, probs, topics_words, topic_info, model, run_index):
        """Handle a completed topic model run"""
        # Store the run results
        run_id = self.current_run_id
        self.current_run_id += 1
        
        # Calculate some basic metrics
        metrics = {
            'topic_count': len(set(topics)),
            'avg_topic_size': np.mean([topic_info.get('Count', [0])[i] for i in range(len(topic_info.get('Count', [])))])
            if isinstance(topic_info, dict) and 'Count' in topic_info else 0,
            'unique_words_count': sum(len(words) for words in topics_words.values())
        }
        
        # Create a TopicModelRun object
        model_run = TopicModelRun(
            run_config['name'],
            run_config['method'],
            run_config,
            self.documents,
            topics,
            topics_words,
            topic_info,
            probs,
            metrics=metrics
        )
        
        # Store the run
        self.runs[run_id] = model_run
        
        # Update UI
        self.update_run_table()
        
        # Process next run
        self.process_next_run(run_index + 1)

    @pyqtSlot(str, dict, int)
    def on_run_error(self, error, run_config, run_index):
        """Handle an error in a topic model run"""
        QMessageBox.warning(
            self, "Run Error",
            f"Error in run '{run_config['name']}': {error}"
        )
        
        # Process next run
        self.process_next_run(run_index + 1)
    
    def on_comparison_complete(self):
        """Handle the completion of all runs"""
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Re-enable UI controls
        self.compare_button.setEnabled(True)
        
        # Enable export controls if we have runs
        if self.runs:
            self.export_button.setEnabled(True)
        
        # Generate visualizations
        self.generate_visualizations()
        
        # Generate summary report
        self.generate_summary_report()
        
        # Update status
        self.progress_updated.emit(100, f"Comparison complete with {len(self.runs)} runs")
        
        # Show success message
        QMessageBox.information(
            self, "Comparison Complete",
            f"Successfully completed comparison of {len(self.runs)} topic model runs."
        )
    
    def update_run_table(self):
        """Update the table of runs"""
        self.run_table.setRowCount(len(self.runs))
        
        for i, (run_id, run) in enumerate(self.runs.items()):
            # Name
            name_item = QTableWidgetItem(run.name)
            self.run_table.setItem(i, 0, name_item)
            
            # Method
            method_item = QTableWidgetItem(run.method)
            self.run_table.setItem(i, 1, method_item)
            
            # Topics
            topic_count = len(set(run.topics))
            topics_item = QTableWidgetItem(str(topic_count))
            self.run_table.setItem(i, 2, topics_item)
            
            # Parameters
            params_str = f"N-gram: {run.parameters['n_gram_range']}, Min Size: {run.parameters['min_topic_size']}"
            params_item = QTableWidgetItem(params_str)
            self.run_table.setItem(i, 3, params_item)
            
            # Metrics
            metrics_str = ", ".join([f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}" 
                                   for k, v in run.metrics.items()])
            metrics_item = QTableWidgetItem(metrics_str)
            self.run_table.setItem(i, 4, metrics_item)
        
        self.run_table.resizeColumnsToContents()
    
    def generate_visualizations(self):
        """Generate all comparison visualizations"""
        if len(self.runs) < 2:
            return
        
        # Generate topic similarity heatmap
        self.generate_topic_similarity_heatmap()
        
        # Update topic selector for word comparison
        self.update_topic_selector()
        
        # Generate topic distribution chart
        self.generate_topic_distribution_chart()
        
        # Generate parameter impact chart
        self.generate_parameter_impact_chart()
    
    def generate_topic_similarity_heatmap(self):
        """Generate a heatmap showing similarity between topics across runs"""
        if len(self.runs) < 2:
            return
        
        # Create figure and canvas
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get topic words from all runs
        all_topic_words = {}
        for run_id, run in self.runs.items():
            for topic_id, words in run.topic_words.items():
                if topic_id != -1:  # Skip outlier topic
                    topic_key = f"{run.name}_{topic_id}"
                    all_topic_words[topic_key] = [word for word, _ in words[:10]]
        
        # Calculate similarity matrix
        topic_keys = list(all_topic_words.keys())
        similarity_matrix = np.zeros((len(topic_keys), len(topic_keys)))
        
        for i, key1 in enumerate(topic_keys):
            for j, key2 in enumerate(topic_keys):
                words1 = set(all_topic_words[key1])
                words2 = set(all_topic_words[key2])
                
                # Jaccard similarity
                if len(words1.union(words2)) > 0:
                    similarity_matrix[i, j] = len(words1.intersection(words2)) / len(words1.union(words2))
                else:
                    similarity_matrix[i, j] = 0
        
        # Create heatmap
        sns.heatmap(similarity_matrix, ax=ax, cmap="YlGnBu", 
                   xticklabels=topic_keys, yticklabels=topic_keys, 
                   annot=False, cbar_kws={'label': 'Topic Similarity'})
        
        plt.title("Topic Similarity Across Runs")
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        # Create canvas and replace placeholder
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        
        # Replace the placeholder with the actual plot
        layout = self.viz_tabs.widget(0).layout()
        
        # Remove the old placeholder
        old_widget = layout.itemAt(0).widget()
        layout.removeWidget(old_widget)
        old_widget.setParent(None)
        
        # Add the new canvas
        layout.addWidget(canvas)
    
    def update_topic_selector(self):
        """Update the topic selector for word comparison"""
        self.topic_selector.clear()
        
        # Add all topics from all runs
        for run_id, run in self.runs.items():
            for topic_id in run.topic_words.keys():
                if topic_id != -1:  # Skip outlier topic
                    self.topic_selector.addItem(f"{run.name} - Topic {topic_id}", (run_id, topic_id))
        
        # Generate initial word comparison if topics exist
        if self.topic_selector.count() > 0:
            self.topic_selector.setCurrentIndex(0)
            self.update_word_comparison()
    
    def update_word_comparison(self):
        """Update the word comparison chart for the selected topic"""
        if self.topic_selector.count() == 0:
            return
        
        # Get the selected run and topic
        run_id, topic_id = self.topic_selector.currentData()
        run = self.runs[run_id]
        
        # Find similar topics in other runs
        similar_topics = self.find_similar_topics(run_id, topic_id)
        
        # Create figure and canvas
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Prepare data for visualization
        all_words = set()
        topic_words_dict = {}
        
        # Add words from the selected topic
        topic_words_dict[run.name] = {word: weight for word, weight in run.topic_words[topic_id][:10]}
        all_words.update(topic_words_dict[run.name].keys())
        
        # Add words from similar topics
        for sim_run_id, sim_topic_id, similarity in similar_topics:
            sim_run = self.runs[sim_run_id]
            topic_words_dict[sim_run.name] = {word: weight for word, weight in sim_run.topic_words[sim_topic_id][:10]}
            all_words.update(topic_words_dict[sim_run.name].keys())
        
        # Convert to DataFrame for easier plotting
        all_words = list(all_words)
        data = []
        for run_name, words_dict in topic_words_dict.items():
            for word in all_words:
                data.append({
                    'Run': run_name,
                    'Word': word,
                    'Weight': words_dict.get(word, 0)
                })
        
        df = pd.DataFrame(data)
        
        # Create the grouped bar chart
        sns.barplot(x='Word', y='Weight', hue='Run', data=df, ax=ax)
        plt.title(f"Word Weights Comparison for {run.name} - Topic {topic_id}")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        # Create canvas and replace placeholder
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        
        # Replace the placeholder with the actual plot
        layout = self.viz_tabs.widget(1).layout()
        
        # Find and remove the old widget (skipping the controls layout)
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if isinstance(item.widget(), (QLabel, FigureCanvas)):
                old_widget = item.widget()
                layout.removeWidget(old_widget)
                old_widget.setParent(None)
                break
        
        # Add the new canvas
        layout.addWidget(canvas)
    
    def find_similar_topics(self, base_run_id, base_topic_id, max_topics=3):
        """Find the most similar topics in other runs"""
        base_run = self.runs[base_run_id]
        base_words = [word for word, _ in base_run.topic_words[base_topic_id][:10]]
        
        similar_topics = []
        
        for run_id, run in self.runs.items():
            if run_id == base_run_id:
                continue
                
            best_similarity = 0
            best_topic_id = None
            
            for topic_id, words in run.topic_words.items():
                if topic_id == -1:  # Skip outlier topic
                    continue
                    
                topic_words = [word for word, _ in words[:10]]
                
                # Calculate Jaccard similarity
                base_set = set(base_words)
                topic_set = set(topic_words)
                
                if len(base_set.union(topic_set)) > 0:
                    similarity = len(base_set.intersection(topic_set)) / len(base_set.union(topic_set))
                    
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_topic_id = topic_id
            
            if best_topic_id is not None:
                similar_topics.append((run_id, best_topic_id, best_similarity))
        
        # Sort by similarity and limit to max_topics
        similar_topics.sort(key=lambda x: x[2], reverse=True)
        return similar_topics[:max_topics]
    
    def generate_topic_distribution_chart(self):
        """Generate a chart showing topic distribution across runs"""
        if len(self.runs) < 2:
            return
        
        # Create figure and canvas
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Prepare data for visualization
        data = []
        for run_id, run in self.runs.items():
            # Count the number of documents assigned to each topic
            topic_counts = {}
            for topic in run.topics:
                if topic not in topic_counts:
                    topic_counts[topic] = 0
                topic_counts[topic] += 1
            
            # Add data for plotting
            for topic_id, count in topic_counts.items():
                data.append({
                    'Run': run.name,
                    'Topic': f"Topic {topic_id}" if topic_id != -1 else "Outliers",
                    'Count': count
                })
        
        df = pd.DataFrame(data)
        
        # Create the grouped bar chart
        sns.barplot(x='Run', y='Count', hue='Topic', data=df, ax=ax)
        plt.title("Document Distribution Across Topics")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        # Create canvas and replace placeholder
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        
        # Replace the placeholder with the actual plot
        layout = self.viz_tabs.widget(2).layout()
        
        # Remove the old placeholder
        old_widget = layout.itemAt(0).widget()
        layout.removeWidget(old_widget)
        old_widget.setParent(None)
        
        # Add the new canvas
        layout.addWidget(canvas)
    
    def generate_parameter_impact_chart(self):
        """Generate a chart showing the impact of parameters on topic coherence"""
        if len(self.runs) < 2:
            return
        
        # Create figure and canvas
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Prepare data for visualization - focus on number of topics parameter
        data = []
        for run_id, run in self.runs.items():
            # Get the actual number of topics (not the parameter)
            topic_count = len(set(run.topics)) - (1 if -1 in run.topics else 0)
            
            # Get the parameter value
            nr_topics_param = run.parameters['nr_topics']
            if nr_topics_param == 'auto':
                nr_topics_param = 'Auto'
            
            # Get metrics
            unique_words = sum(len(words) for topic_id, words in run.topic_words.items() if topic_id != -1)
            avg_words_per_topic = unique_words / topic_count if topic_count > 0 else 0
            
            data.append({
                'Run': run.name,
                'Method': run.method,
                'Topics Parameter': str(nr_topics_param),
                'Actual Topics': topic_count,
                'Avg Words Per Topic': avg_words_per_topic
            })
        
        df = pd.DataFrame(data)
        
        # Plot the number of topics vs avg words per topic, colored by method
        scatter = ax.scatter(df['Actual Topics'], df['Avg Words Per Topic'], c=df.groupby('Method').ngroup(), 
                           cmap='viridis', s=100, alpha=0.7)
        
        # Add run names as annotations
        for i, row in df.iterrows():
            ax.annotate(row['Run'], (row['Actual Topics'], row['Avg Words Per Topic']), 
                       xytext=(5, 5), textcoords='offset points')
        
        # Add legend
        legend1 = ax.legend(scatter.legend_elements()[0], df['Method'].unique(), 
                          title="Method", loc="upper left")
        ax.add_artist(legend1)
        
        plt.title("Parameter Impact on Topic Quality")
        plt.xlabel("Number of Topics")
        plt.ylabel("Average Words Per Topic")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Create canvas and replace placeholder
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        
        # Replace the placeholder with the actual plot
        layout = self.viz_tabs.widget(3).layout()
        
        # Remove the old placeholder
        old_widget = layout.itemAt(0).widget()
        layout.removeWidget(old_widget)
        old_widget.setParent(None)
        
        # Add the new canvas
        layout.addWidget(canvas)
    
    def generate_summary_report(self):
        """Generate a summary report of the comparison"""
        if len(self.runs) < 2:
            return
        
        report = "<h1>Topic Model Comparison Report</h1>"
        report += f"<p>Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>"
        report += f"<p>Documents analyzed: {len(self.documents)}</p>"
        report += f"<p>Models compared: {len(self.runs)}</p>"
        
        # Add run summary table
        report += "<h2>Run Summary</h2>"
        report += "<table border='1' cellpadding='5' style='border-collapse: collapse;'>"
        report += "<tr><th>Run Name</th><th>Method</th><th>Topics</th><th>Parameters</th><th>Key Metrics</th></tr>"
        
        for run_id, run in self.runs.items():
            topic_count = len(set(run.topics)) - (1 if -1 in run.topics else 0)
            params_str = f"N-gram: {run.parameters['n_gram_range']}, Min Size: {run.parameters['min_topic_size']}"
            metrics_str = ", ".join([f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}" 
                                   for k, v in run.metrics.items()])
            
            report += f"<tr><td>{run.name}</td><td>{run.method}</td><td>{topic_count}</td>"
            report += f"<td>{params_str}</td><td>{metrics_str}</td></tr>"
        
        report += "</table>"
        
        # Add top words for each run
        report += "<h2>Top Topic Words</h2>"
        
        for run_id, run in self.runs.items():
            report += f"<h3>{run.name}</h3>"
            
            # Sort topics by id
            sorted_topics = sorted([(tid, words) for tid, words in run.topic_words.items() if tid != -1])
            
            report += "<table border='1' cellpadding='5' style='border-collapse: collapse;'>"
            report += "<tr><th>Topic ID</th><th>Top Words</th></tr>"
            
            for topic_id, words in sorted_topics:
                words_str = ", ".join([word for word, _ in words[:10]])
                report += f"<tr><td>Topic {topic_id}</td><td>{words_str}</td></tr>"
            
            report += "</table>"
        
        # Add recommendations
        report += "<h2>Recommendations</h2>"
        
        # Identify the run with the best metrics (we'll use average words per topic as a proxy for quality)
        best_run_id = None
        best_score = 0
        
        for run_id, run in self.runs.items():
            topic_count = len(set(run.topics)) - (1 if -1 in run.topics else 0)
            unique_words = sum(len(words) for topic_id, words in run.topic_words.items() if topic_id != -1)
            avg_words_per_topic = unique_words / topic_count if topic_count > 0 else 0
            
            if avg_words_per_topic > best_score:
                best_score = avg_words_per_topic
                best_run_id = run_id
        
        if best_run_id is not None:
            best_run = self.runs[best_run_id]
            report += f"<p><strong>Recommended Model:</strong> {best_run.name} ({best_run.method})</p>"
            report += "<p><strong>Reasons:</strong></p><ul>"
            report += f"<li>Highest number of unique topic words per topic</li>"
            report += f"<li>Good balance of topic specificity and coherence</li>"
            report += "</ul>"
        
        # Method comparison
        report += "<h3>Method Comparison</h3>"
        report += "<ul>"
        
        # Group runs by method
        method_runs = {}
        for run_id, run in self.runs.items():
            if run.method not in method_runs:
                method_runs[run.method] = []
            method_runs[run.method].append(run)
        
        for method, runs in method_runs.items():
            report += f"<li><strong>{method}:</strong> "
            if method in ["bertopic", "bertopic-pca"]:
                report += "Provides semantically coherent topics with good separation. "
            elif method == "nmf":
                report += "Offers stable topics based on word co-occurrence. "
            elif method == "lda":
                report += "Traditional probabilistic modeling with good interpretability. "
            
            avg_topics = np.mean([len(set(r.topics)) - (1 if -1 in r.topics else 0) for r in runs])
            report += f"Average of {avg_topics:.1f} topics.</li>"
        
        report += "</ul>"
        
        # Parameter recommendations
        report += "<h3>Parameter Recommendations</h3>"
        report += "<ul>"
        report += "<p><i>Recommendations are subjective and should be judged by the investigator</i></p>"
        report += "<ul>"
        # Find optimal number of topics
        topic_counts = [(run_id, len(set(run.topics)) - (1 if -1 in run.topics else 0)) for run_id, run in self.runs.items()]
        avg_topic_count = np.mean([count for _, count in topic_counts])
        
        report += f"<li><strong>Number of topics:</strong> Around {avg_topic_count:.0f} appears optimal for this dataset.</li>"
        
        # N-gram range recommendation
        ngram_runs = {}
        for run_id, run in self.runs.items():
            ngram = run.parameters['n_gram_range']
            if ngram not in ngram_runs:
                ngram_runs[ngram] = []
            ngram_runs[ngram].append(run_id)
        
        if len(ngram_runs) > 1:
            best_ngram = None
            best_ngram_score = 0
            
            for ngram, run_ids in ngram_runs.items():
                # Calculate average score for this n-gram setting
                score = np.mean([
                    sum(len(words) for topic_id, words in self.runs[rid].topic_words.items() if topic_id != -1) 
                    for rid in run_ids
                ])
                
                if score > best_ngram_score:
                    best_ngram_score = score
                    best_ngram = ngram
            
            if best_ngram:
                report += f"<li><strong>N-gram range:</strong> {best_ngram} produces the most distinctive topics.</li>"
        
        report += "</ul>"
        
        # Set the report text
        self.report_text.setHtml(report)
        
    
    def export_report(self):
        """Export the comparison report"""
        if not self.runs or len(self.runs) < 2:
            QMessageBox.warning(
                self, "No Comparison", "No comparison data to export."
            )
            return
        
        # Ask for export format
        format_dialog = QDialog(self)
        format_dialog.setWindowTitle("Export Format")
        format_dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout(format_dialog)
        
        layout.addWidget(QLabel("Select export format:"))
        
        format_group = QButtonGroup(format_dialog)
        
        html_radio = QRadioButton("HTML")
        html_radio.setChecked(True)
        format_group.addButton(html_radio, 0)
        layout.addWidget(html_radio)
        
        markdown_radio = QRadioButton("Markdown")
        format_group.addButton(markdown_radio, 1)
        layout.addWidget(markdown_radio)
        
        buttons_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(format_dialog.reject)
        buttons_layout.addWidget(cancel_button)
        
        export_button = QPushButton("Export")
        export_button.clicked.connect(format_dialog.accept)
        export_button.setDefault(True)
        buttons_layout.addWidget(export_button)
        
        layout.addLayout(buttons_layout)
        
        if not format_dialog.exec_():
            return
        
        # Get selected format
        format_id = format_group.checkedId()
        
        # Get file path
        file_filter = "HTML Files (*.html)" if format_id == 0 else "Markdown Files (*.md)"
        default_ext = ".html" if format_id == 0 else ".md"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Report", "", f"{file_filter};;All Files (*)"
        )
        
        if not file_path:
            return
        
        # Ensure correct extension
        if not file_path.endswith(default_ext):
            file_path += default_ext
        
        try:
            if format_id == 0:  # HTML
                # Get the HTML from the report text
                html_content = self.report_text.toHtml()
                
                # Add CSS for better styling
                css = """
                <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                }
                table {
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 20px;
                }
                th, td {
                    text-align: left;
                    padding: 8px;
                    border: 1px solid #ddd;
                }
                th {
                    background-color: #f2f2f2;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                h1, h2, h3 {
                    color: #333;
                }
                </style>
                """
                
                # Insert CSS after the <head> tag
                if "<head>" in html_content:
                    html_content = html_content.replace("<head>", f"<head>{css}")
                else:
                    html_content = f"<html><head>{css}</head><body>{html_content}</body></html>"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            else:  # Markdown
                # Generate markdown version
                md_content = self.generate_markdown_report()
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
            
            QMessageBox.information(
                self, "Export Complete", f"Report exported to {file_path}"
            )
        except Exception as e:
            logger.error(f"Error exporting report: {str(e)}")
            QMessageBox.warning(
                self, "Export Error", f"Failed to export report: {str(e)}"
            )
    
    def generate_markdown_report(self):
        """Generate a markdown version of the comparison report"""
        md = "# Topic Model Comparison Report\n\n"
        md += f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        md += f"Documents analyzed: {len(self.documents)}\n\n"
        md += f"Models compared: {len(self.runs)}\n\n"
        
        # Add run summary
        md += "## Run Summary\n\n"
        md += "| Run Name | Method | Topics | Parameters | Key Metrics |\n"
        md += "| --- | --- | --- | --- | --- |\n"
        
        for run_id, run in self.runs.items():
            topic_count = len(set(run.topics)) - (1 if -1 in run.topics else 0)
            params_str = f"N-gram: {run.parameters['n_gram_range']}, Min Size: {run.parameters['min_topic_size']}"
            metrics_str = ", ".join([f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}" 
                                   for k, v in run.metrics.items()])
            
            md += f"| {run.name} | {run.method} | {topic_count} | {params_str} | {metrics_str} |\n"
        
        md += "\n"
        
        # Add top words for each run
        md += "## Top Topic Words\n\n"
        
        for run_id, run in self.runs.items():
            md += f"### {run.name}\n\n"
            
            # Sort topics by id
            sorted_topics = sorted([(tid, words) for tid, words in run.topic_words.items() if tid != -1])
            
            md += "| Topic ID | Top Words |\n"
            md += "| --- | --- |\n"
            
            for topic_id, words in sorted_topics:
                words_str = ", ".join([word for word, _ in words[:10]])
                md += f"| Topic {topic_id} | {words_str} |\n"
            
            md += "\n"
        
        # Add recommendations
        md += "## Recommendations\n\n"
        
        # Identify the run with the best metrics (we'll use average words per topic as a proxy for quality)
        best_run_id = None
        best_score = 0
        
        for run_id, run in self.runs.items():
            topic_count = len(set(run.topics)) - (1 if -1 in run.topics else 0)
            unique_words = sum(len(words) for topic_id, words in run.topic_words.items() if topic_id != -1)
            avg_words_per_topic = unique_words / topic_count if topic_count > 0 else 0
            
            if avg_words_per_topic > best_score:
                best_score = avg_words_per_topic
                best_run_id = run_id
        
        if best_run_id is not None:
            best_run = self.runs[best_run_id]
            md += f"**Recommended Model:** {best_run.name} ({best_run.method})\n\n"
            md += "**Reasons:**\n\n"
            md += "- Highest number of unique topic words per topic\n"
            md += "- Good balance of topic specificity and coherence\n\n"
        
        # Method comparison
        md += "### Method Comparison\n\n"
        
        # Group runs by method
        method_runs = {}
        for run_id, run in self.runs.items():
            if run.method not in method_runs:
                method_runs[run.method] = []
            method_runs[run.method].append(run)
        
        for method, runs in method_runs.items():
            md += f"- **{method}:** "
            if method in ["bertopic", "bertopic-pca"]:
                md += "Provides semantically coherent topics with good separation. "
            elif method == "nmf":
                md += "Offers stable topics based on word co-occurrence. "
            elif method == "lda":
                md += "Traditional probabilistic modeling with good interpretability. "
            
            avg_topics = np.mean([len(set(r.topics)) - (1 if -1 in r.topics else 0) for r in runs])
            md += f"Average of {avg_topics:.1f} topics.\n"
        
        md += "\n"
        
        # Parameter recommendations
        md += "### Parameter Recommendations\n\n"
        
        # Find optimal number of topics
        topic_counts = [(run_id, len(set(run.topics)) - (1 if -1 in run.topics else 0)) for run_id, run in self.runs.items()]
        avg_topic_count = np.mean([count for _, count in topic_counts])
        
        md += f"- **Number of topics:** Around {avg_topic_count:.0f} appears optimal for this dataset.\n"
        
        # N-gram range recommendation
        ngram_runs = {}
        for run_id, run in self.runs.items():
            ngram = run.parameters['n_gram_range']
            if ngram not in ngram_runs:
                ngram_runs[ngram] = []
            ngram_runs[ngram].append(run_id)
        
        if len(ngram_runs) > 1:
            best_ngram = None
            best_ngram_score = 0
            
            for ngram, run_ids in ngram_runs.items():
                # Calculate average score for this n-gram setting
                score = np.mean([
                    sum(len(words) for topic_id, words in self.runs[rid].topic_words.items() if topic_id != -1) 
                    for rid in run_ids
                ])
                
                if score > best_ngram_score:
                    best_ngram_score = score
                    best_ngram = ngram
            
            if best_ngram:
                md += f"- **N-gram range:** {best_ngram} produces the most distinctive topics.\n"
        
        return md
    
    def show_help_dialog(self):
        """Show help dialog with information about model comparison"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QTextBrowser, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Topic Model Comparison Help")
        dialog.setMinimumSize(900, 700)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Create tab widget for different help sections
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Overview tab
        overview_tab = QTextBrowser()
        overview_tab.setOpenExternalLinks(True)
        overview_tab.setHtml("""
        <h2>Topic Model Comparison Overview</h2>
        <p>This tab allows you to compare different topic modeling approaches side by side to find the best method for your data.</p>
        
        <h3>Key Features</h3>
        <ul>
            <li>Run multiple topic models with different algorithms and parameters</li>
            <li>Visualize similarities and differences between topic models</li>
            <li>Compare word weights across similar topics</li>
            <li>Analyze how parameters affect topic quality</li>
            <li>Export detailed comparison reports</li>
        </ul>
        
        <h3>Workflow</h3>
        <ol>
            <li>Click "Start New Comparison" to configure multiple topic model runs</li>
            <li>Define 2-5 different runs with varying methods or parameters</li>
            <li>Review the results across different visualization tabs</li>
            <li>Export a comparison report for documentation</li>
        </ol>
        
        <p>Comparing different approaches helps you find the optimal topic model configuration for your specific dataset and requirements.</p>
        """)
        tabs.addTab(overview_tab, "Overview")
        
        # Runs Configuration tab
        config_tab = QTextBrowser()
        config_tab.setHtml("""
        <h2>Configuring Comparison Runs</h2>
        
        <h3>Run Types</h3>
        <p>You can compare different topic modeling methods:</p>
        <ul>
            <li><b>BERTopic (UMAP)</b>: High-quality semantic topics using BERT embeddings and UMAP dimensionality reduction</li>
            <li><b>BERTopic (PCA)</b>: More stable alternative using PCA instead of UMAP</li>
            <li><b>NMF</b>: Non-negative Matrix Factorization, a traditional approach based on term frequency</li>
            <li><b>LDA</b>: Latent Dirichlet Allocation, a probabilistic topic model</li>
        </ul>
        
        <h3>Parameters to Vary</h3>
        <p>When configuring runs, consider varying these parameters:</p>
        <ul>
            <li><b>Number of topics</b>: Try different fixed numbers or "Auto" to let the algorithm decide</li>
            <li><b>Minimum topic size</b>: The minimum number of documents required to form a topic</li>
            <li><b>N-gram range</b>: Whether to include phrases (bigrams, trigrams) or just single words</li>
            <li><b>Method</b>: Compare different algorithms to see which works best for your data</li>
        </ul>
        
        <h3>Tips for Meaningful Comparisons</h3>
        <ul>
            <li>Change only one parameter at a time to isolate its impact</li>
            <li>Include diverse methods to see different approaches to the same data</li>
            <li>Use descriptive names for runs to easily identify them in visualizations</li>
            <li>Start with 3-4 runs for a balanced comparison</li>
        </ul>
        """)
        tabs.addTab(config_tab, "Configuring Runs")
        
        # Visualizations tab
        viz_tab = QTextBrowser()
        viz_tab.setHtml("""
        <h2>Understanding Visualizations</h2>
        
        <h3>Topic Similarity Heatmap</h3>
        <p>The similarity is calculated using the Jaccard similarity index, which measures the overlap between the top words of each topic.</p>
        <p>This visualization shows how topics from different runs relate to each other.</p>
        <ul>
            <li>The number beside the "Run id" indicate the topic id in this Run</li>
            <li>Darker colors indicate higher similarity between topics</li>
            <li>Helps identify consistent topics that appear across multiple methods</li>
            <li>Shows which topics are method-specific versus universal in your data</li>
        </ul>
        
        <h3>Word Weight Comparison</h3>
        <p>Compare word importance between similar topics across different runs.</p>
        <ul>
            <li>Select a topic from one run to see how its top words compare to similar topics in other runs</li>
            <li>Bar height indicates word importance in each topic</li>
            <li>Helps evaluate topic coherence and specificity across methods</li>
        </ul>
        
        <h3>Topic Distribution Chart</h3>
        <p>Shows how documents are distributed across topics in different runs.</p>
        <ul>
            <li>Compare how evenly documents are distributed</li>
            <li>Identify methods that produce more balanced topic assignments</li>
            <li>See if some methods create "catch-all" topics or outlier categories</li>
        </ul>
        
        <h3>Parameter Impact Chart</h3>
        <p>Visualizes how changing parameters affects topic quality.</p>
        <ul>
            <li>Scatter plot showing relationship between number of topics and topic quality</li>
            <li>Points colored by method to compare different approaches</li>
            <li>Helps identify optimal parameter settings for your data</li>
        </ul>
        """)
        tabs.addTab(viz_tab, "Visualizations")
        
        # Interpretation tab
        interp_tab = QTextBrowser()
        interp_tab.setHtml("""
        <h2>Interpreting Comparison Results</h2>
        
        <h3>What to Look For</h3>
        <p>When comparing topic models, consider these factors:</p>
        <ul>
            <li><b>Topic coherence</b>: Do the words in each topic clearly relate to a single concept?</li>
            <li><b>Topic distinctiveness</b>: Are the topics clearly different from each other?</li>
            <li><b>Coverage</b>: How many documents are assigned to meaningful topics vs. outlier topics?</li>
            <li><b>Stability</b>: Do similar topics appear across different methods?</li>
            <li><b>Interpretability</b>: How easy is it to assign meaningful labels to the topics?</li>
        </ul>
        
        <h3>Method Strengths</h3>
        <ul>
            <li><b>BERTopic</b>: Usually produces the most semantically coherent topics with modern language understanding</li>
            <li><b>NMF</b>: Often creates clearly separated topics based on distinctive terminology</li>
            <li><b>LDA</b>: Works well with longer documents and provides probabilistic topic distributions</li>
        </ul>
        
        <h3>Parameter Effects</h3>
        <ul>
            <li><b>More topics</b>: Increases specificity but may reduce coherence</li>
            <li><b>Higher minimum topic size</b>: Creates more general topics but may miss niche themes</li>
            <li><b>Wider n-gram range</b>: Captures phrases but may dilute topic focus</li>
        </ul>
        
        <h3>The Summary Report</h3>
        <p>The summary report tab provides automated analysis and recommendations based on your comparison results.
        It identifies the best-performing model and optimal parameter settings based on objective metrics and offers
        guidance for interpreting your specific comparison.</p>
        """)
        tabs.addTab(interp_tab, "Interpretation")
        
        # Exporting tab
        export_tab = QTextBrowser()
        export_tab.setHtml("""
        <h2>Exporting Comparison Results</h2>
        
        <h3>Available Export Options</h3>
        <ul>
            <li><b>Save Comparison</b>: Saves the full comparison data for later loading and analysis</li>
            <li><b>Export Report</b>: Creates a formatted document summarizing the comparison results</li>
        </ul>
        
        <h3>Report Formats</h3>
        <ul>
            <li><b>HTML</b>: Full formatted report with tables and styling, ideal for sharing</li>
            <li><b>Markdown</b>: Plain text with formatting, good for including in documentation</li>
        </ul>
        
        <h3>What's Included in Reports</h3>
        <ul>
            <li>Overview of comparison parameters and methods</li>
            <li>Summary table of all runs with key metrics</li>
            <li>Top words for each topic across all runs</li>
            <li>Analysis and recommendations based on comparison results</li>
            <li>Guidance on method selection and parameter optimization</li>
        </ul>
        
        <h3>Using Reports</h3>
        <p>Exported reports are valuable for:</p>
        <ul>
            <li>Documenting your topic modeling process</li>
            <li>Sharing findings with colleagues</li>
            <li>Supporting decisions about which model to use</li>
            <li>Creating reproducible research workflows</li>
        </ul>
        """)
        
        # Summary tab
        summary_tab  = QTextBrowser()
        summary_tab .setHtml("""
        <h2>Understanding the Summary Report</h2> 
        <h3>Overview</h3>          
        <p>The summary report provides an analysis of all comparison runs and offers recommendations on which 
        model and parameters might work best for your data. It consolidates insights from multiple metrics and 
        visualizations into actionable guidance.</p>

        <h3>How the Optimal Number of Topics is Determined</h3>
        <p>The recommended number of topics is calculated using a consensus-based approach:</p>
        <ul>
            <li>The actual number of topics discovered in each run is counted (excluding outlier topics)</li>
            <li>The average across all runs is calculated</li>
            <li>This average is rounded to a whole number</li>
        </ul>

        <h3>How the Best Model is Selected</h3>
        <p>The "recommended model" is determined by evaluating several key metrics:</p>
        <ul>
            <li><b>Primary metric</b>: Average words per topic – a proxy for topic richness and specificity</li>
            <li><b>Secondary considerations</b>: Topic count, distribution balance, and unique words total</li>
        </ul>
        <p>The model that achieves the best balance of these factors is highlighted as the recommended approach. 
        The recommendation also considers the inherent strengths of different algorithms.</p>

        <h3>Parameter Recommendations</h3>
        <p>Parameter recommendations are derived by:</p>
        <ul>
            <li><b>N-gram settings</b>: Comparing the total unique words generated by different n-gram configurations</li>
            <li><b>Topic size threshold</b>: Analyzing topic distribution balance</li>
            <li><b>Method-specific parameters</b>: Evaluating stability and coherence for each algorithm type</li>
        </ul>
        <p>The goal is to identify the parameter settings that produce the most coherent, 
        distinct, and interpretable topics for your specific dataset.</p>

        <h3>Metrics Used in the Analysis</h3>
        <p>The report utilizes several key metrics:</p>
        <ul>
            <li><b>Topic count</b>: Total number of non-outlier topics discovered</li>
            <li><b>Average topic size</b>: Mean number of documents per topic</li>
            <li><b>Unique words count</b>: Total unique words across all topics</li>
            <li><b>Words per topic</b>: Average number of significant words per topic</li>
            <li><b>Topic similarity</b>: Jaccard similarity between topics across runs</li>
        </ul>
        <p>These metrics are combined to provide a holistic assessment of model quality and suitability.</p>

        <h3>Using the Summary Report</h3>
        <p>To get the most from the summary report:</p>
        <ul>
            <li>Pay attention to both the recommended model and the reasoning behind it</li>
            <li>Consider your specific use case when interpreting recommendations</li>
            <li>Use the report as a starting point, but trust your domain knowledge</li>
            <li>Export the report to share findings with colleagues</li>
        </ul>
        <p>The summary report is designed to simplify the complex task of selecting the optimal topic modeling 
        approach from multiple alternatives, saving you time while providing evidence-based recommendations.</p>
        """)
        tabs.addTab(summary_tab, "Summary Report")
        
        # Tips tab
        tips_tab = QTextBrowser()
        tips_tab.setHtml("""
        <h2>Tips for Effective Comparisons</h2>
        
        <h3>Best Practices</h3>
        <ul>
            <li>Use meaningful names for runs (e.g., "BERTopic 10 topics" vs. "Run 1")</li>
            <li>Compare at least one run from each major method category</li>
            <li>Test a range of topic numbers to find the optimal granularity</li>
            <li>Look for consistency across methods—topics that appear regardless of method are likely robust</li>
            <li>Consider your specific use case when evaluating results (e.g., exploration vs. classification)</li>
        </ul>
        
        <h3>Common Pitfalls</h3>
        <ul>
            <li>Relying only on one metric or visualization</li>
            <li>Overlooking the impact of preprocessing on topic quality</li>
            <li>Assuming more topics always means better results</li>
            <li>Neglecting to check how documents are distributed across topics</li>
            <li>Focusing only on the top words without considering full topic coherence</li>
        </ul>
        
        <h3>Identifying the Best Model</h3>
        <p>The "best" topic model depends on your specific goals:</p>
        <ul>
            <li><b>For exploration</b>: Look for high coherence and interpretability</li>
            <li><b>For document organization</b>: Prioritize even distribution and clear separation</li>
            <li><b>For text classification</b>: Focus on topic stability and predictive power</li>
            <li><b>For content analysis</b>: Balance specificity with meaningful coverage</li>
        </ul>
        
        <h3>Advanced Usage</h3>
        <ul>
            <li>Try running comparisons on different subsets of your documents</li>
            <li>Combine insights from multiple models for a more comprehensive analysis</li>
            <li>Use comparison results to fine-tune your preferred method</li>
            <li>Consider how topic stability changes with different document counts</li>
        </ul>
        """)
        tabs.addTab(tips_tab, "Tips")
        
        # Add OK button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        button_box.button(QDialogButtonBox.Ok).setMinimumHeight(BUTTON_HEIGHT)
        layout.addWidget(button_box)
        
        # Show the dialog
        dialog.exec_()