#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Topic Tab module for the Audio to Topics application.
Provides UI for extracting topics using BERTopic.
"""
import logging
import json
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QSpinBox, QGroupBox, QProgressBar,
                           QTableWidget, QTableWidgetItem, QComboBox,
                           QSplitter, QTextEdit, QCheckBox, QMessageBox,
                           QDialog, QRadioButton, QButtonGroup, QTabWidget,
                           QListWidget, QListWidgetItem, QStyle, QSizePolicy, 
                           QScrollArea, QFormLayout, QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal,QMimeData, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QKeySequence, QGuiApplication,QClipboard
from PyQt5.QtWidgets import QAction, QApplication
from ..core.topic_modeler import TopicModeler
from ..core.llm_service import LLMService

# Define layout constants
LAYOUT_MARGIN = 10
WIDGET_SPACING = 8
BUTTON_HEIGHT = 30
BUTTON_MIN_WIDTH = 120

# Configure logging
logger = logging.getLogger(__name__)

# Add this class for the elbow plot dialog after the model wrapper classes
class ElbowMethodDialog(QDialog):
    """Dialog for displaying elbow method results and selecting optimal topics"""
    
    def __init__(self, model_scores, topics_range, parent=None):
        super().__init__(parent)
        self.model_scores = model_scores
        self.topics_range = topics_range
        self.selected_topics = self._find_optimal_topics()
        
        self.setWindowTitle("LDA Elbow Method Results")
        self.setMinimumSize(600, 500)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Add a label with explanation
        explanation = (
            "The elbow method helps determine the optimal number of topics by measuring model performance "
            "across different topic numbers. The chart below shows model quality scores, where:\n\n"
            "- Higher score = better model performance\n"
            "- The 'elbow point' typically represents a good balance between model complexity and performance\n\n"
            "Based on the results, we recommend using the suggested number of topics, "
            "but you can adjust if desired."
        )
        explanation_label = QLabel(explanation)
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)
        
        # Create matplotlib figure
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(self.topics_range, self.model_scores, marker='o')
        ax.set_title('Model Quality by Number of Topics')
        ax.set_xlabel('Number of Topics')
        ax.set_ylabel('Model Quality Score')
        ax.grid(True)
        
        # Highlight optimal value
        optimal_idx = self.topics_range.index(self.selected_topics)
        ax.plot(self.selected_topics, self.model_scores[optimal_idx], 'ro', markersize=10)
        ax.annotate(f'Optimal: {self.selected_topics} topics',
                   (self.selected_topics, self.model_scores[optimal_idx]),
                   xytext=(10, -20), textcoords='offset points',
                   bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.8))
        
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        
        # Add controls for manual selection
        selection_layout = QFormLayout()
        selection_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        selection_layout.setLabelAlignment(Qt.AlignRight)
        
        self.topics_spin = QSpinBox()
        self.topics_spin.setRange(min(self.topics_range), max(self.topics_range))
        self.topics_spin.setValue(self.selected_topics)
        self.topics_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        selection_layout.addRow("Select number of topics:", self.topics_spin)
        
        layout.addLayout(selection_layout)
        
        # Add buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(WIDGET_SPACING)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setMinimumHeight(BUTTON_HEIGHT)
        self.cancel_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        buttons_layout.addWidget(self.cancel_button)
        
        self.accept_button = QPushButton("Use Selected")
        self.accept_button.clicked.connect(self.accept)
        self.accept_button.setDefault(True)
        self.accept_button.setMinimumHeight(BUTTON_HEIGHT)
        self.accept_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        buttons_layout.addWidget(self.accept_button)
        
        layout.addLayout(buttons_layout)
    
    def _find_optimal_topics(self):
        """Find the elbow point in the quality curve"""
        # Simple method: Find the "elbow point" using the maximum curvature
        x = np.array(self.topics_range)
        y = np.array(self.model_scores)
        
        # If we have too few points, just return the max score
        if len(x) < 4:
            return x[np.argmax(y)]
        
        # Normalize data for better numerical stability
        x_norm = (x - x.min()) / (x.max() - x.min())
        y_norm = (y - y.min()) / (y.max() - y.min())
        
        # Calculate curvature: second derivative of smoothed data
        # We'll use simple finite differences
        dy = np.gradient(y_norm, x_norm)
        ddy = np.gradient(dy, x_norm)
        
        # The point of maximum curvature is a good estimate of the elbow point
        # But we also want higher quality, so we balance curvature and quality
        # First normalize the curvature
        curvature = np.abs(ddy)
        curvature_norm = curvature / np.max(curvature) if np.max(curvature) > 0 else curvature
        
        # Create a score that balances quality and curvature
        # Weight quality higher (0.7) than curvature (0.3)
        score = 0.7 * y_norm + 0.3 * curvature_norm
        
        # Return the topic count with the highest score
        optimal_idx = np.argmax(score)
        return x[optimal_idx]
        
    def get_selected_topics(self):
        """Get the number of topics selected by the user"""
        return self.topics_spin.value()
       
class TopicTab(QWidget):
    """Tab for topic modeling functionality"""
    
    # Define signals - update to include model
    topics_extracted = pyqtSignal(object, object, object, object, object)  # topics, probs, topics_words, topic_info, chunked_docs
    # topics, probs, topics_words, topic_info
    # Note: We keep the old signal signature for compatibility with main_window.py
    progress_updated = pyqtSignal(int, str)  # Emits progress percentage and message
    
    
    def __init__(self):
        super().__init__()
        
        # Initialize instance variables
        self.documents = []  # Text documents to process
        self.topic_modeler = TopicModeler()  # Topic modeler instance
        self.llm_service = LLMService()  # LLM service for refining topics
        
        # Ensure LLM service loads the latest config
        try:
            self.llm_service.config.load()
            # Update service properties with config values
            self.llm_service.anthropic_key = self.llm_service.config.anthropic_key
            self.llm_service.openai_key = self.llm_service.config.openai_key
            self.llm_service.provider = self.llm_service.config.provider
        except Exception as e:
            logger.error(f"Error loading LLM config in TopicTab: {str(e)}")
        
        # Topics data
        self.topics = None  # Topic assignments
        self.probs = None  # Topic probabilities
        self.topics_words = None  # Words for each topic
        self.topic_info = None  # Topic info dataframe
        self.refined_topics = {}  # Refined topic descriptions from LLM
        
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
            "Click on Help button to learn more about this topic modeling module."
        )
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        help_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        # Add to the header layout, allowing it to expand
        header_layout.addWidget(help_label, 1)
        
        # Help button in the top right
        self.help_button = QPushButton()
        self.help_button.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.help_button.setToolTip("Learn about BERTopic and topic modeling")
        self.help_button.setFixedSize(32, 32) # Make it a square button
        self.help_button.clicked.connect(self.show_help_dialog)
        
        # Add to header layout with no stretching
        header_layout.addWidget(self.help_button, 0, Qt.AlignTop | Qt.AlignRight)
        
        # Add header layout to main layout
        main_layout.addLayout(header_layout)
        
        # Create a splitter for settings and results
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter, 1)  # Add stretch factor to make splitter expand
        
        # Settings container widget
        settings_container = QWidget()
        settings_layout = QVBoxLayout(settings_container)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(WIDGET_SPACING)
        
        # Settings and controls section
        settings_group = QGroupBox("Topic Model Settings")
        settings_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        settings_layout_inner = QVBoxLayout(settings_group)
        settings_layout_inner.setSpacing(WIDGET_SPACING)
        settings_layout_inner.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Settings form
        settings_form = QFormLayout()
        settings_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        settings_form.setLabelAlignment(Qt.AlignRight)
        settings_form.setHorizontalSpacing(WIDGET_SPACING)
        settings_form.setVerticalSpacing(WIDGET_SPACING)
        
        # Method selection
        self.method_combo = QComboBox()
        self.method_combo.addItem("BERTopic (UMAP)", "bertopic")
        self.method_combo.addItem("BERTopic (PCA)", "bertopic-pca")
        self.method_combo.addItem("NMF", "nmf")
        self.method_combo.addItem("LDA", "lda")
        self.method_combo.setToolTip(
            "BERTopic (UMAP): Best quality but may fail with small document sets\n"
            "BERTopic (PCA): Good quality, more stable with small document sets\n"
            "NMF: Traditional method, very stable but less semantic coherence\n"
            "LDA: Classic topic modeling, works well with larger document sets"
        )
        self.method_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        settings_form.addRow("Method:", self.method_combo)
        
        # Language selection
        self.language_combo = QComboBox()
        self.language_combo.addItems(["multilingual", "english"])
        self.language_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        settings_form.addRow("Language:", self.language_combo)
        
        # Number of topics
        self.topics_combo = QComboBox()
        self.topics_combo.addItem("Auto", "auto")
        for i in range(2, 21):
            self.topics_combo.addItem(str(i), i)
        self.topics_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        settings_form.addRow("Number of Topics:", self.topics_combo)
        
        # Minimum topic size
        self.min_size_spin = QSpinBox()
        self.min_size_spin.setRange(1, 50)
        self.min_size_spin.setValue(2)
        self.min_size_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        settings_form.addRow("Min Topic Size:", self.min_size_spin)
        
        # N-gram range
        ngram_layout = QHBoxLayout()
        ngram_layout.setSpacing(WIDGET_SPACING)

        self.min_ngram_spin = QSpinBox()
        self.min_ngram_spin.setRange(1, 5)
        self.min_ngram_spin.setValue(1)
        self.min_ngram_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.min_ngram_spin.valueChanged.connect(self.update_ngram_range)
        ngram_layout.addWidget(QLabel("Min:"))
        ngram_layout.addWidget(self.min_ngram_spin)

        ngram_layout.addSpacing(10)  # Add a little spacing between the controls

        self.max_ngram_spin = QSpinBox()
        self.max_ngram_spin.setRange(1, 5)
        self.max_ngram_spin.setValue(2)
        self.max_ngram_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.max_ngram_spin.valueChanged.connect(self.update_ngram_range)
        ngram_layout.addWidget(QLabel("Max:"))
        ngram_layout.addWidget(self.max_ngram_spin)

        settings_form.addRow("N-gram Range:", ngram_layout)

        
        # Add form to settings layout
        settings_layout_inner.addLayout(settings_form)
        
        # LDA options group
        self.lda_options_group = QGroupBox("LDA Options")
        self.lda_options_group.setVisible(False)  # Initially hidden
        self.lda_options_group.setCheckable(True)
        self.lda_options_group.setChecked(False)
        lda_options_layout = QVBoxLayout(self.lda_options_group)
        lda_options_layout.setSpacing(WIDGET_SPACING)
        
        # Elbow method checkbox
        self.elbow_checkbox = QCheckBox("Use elbow method to find optimal number of topics")
        self.elbow_checkbox.setChecked(False)
        self.elbow_checkbox.setToolTip("Automatically find the optimal number of topics using coherence scores")
        lda_options_layout.addWidget(self.elbow_checkbox)
        
        # Elbow method form
        elbow_form = QFormLayout()
        elbow_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        elbow_form.setLabelAlignment(Qt.AlignRight)
        elbow_form.setHorizontalSpacing(WIDGET_SPACING)
        elbow_form.setVerticalSpacing(WIDGET_SPACING)
        
        # Min topics
        self.min_topics_spin = QSpinBox()
        self.min_topics_spin.setRange(2, 20)
        self.min_topics_spin.setValue(2)
        self.min_topics_spin.setEnabled(False)  # Initially disabled
        self.min_topics_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        elbow_form.addRow("Min Topics:", self.min_topics_spin)
        
        # Max topics
        self.max_topics_spin = QSpinBox()
        self.max_topics_spin.setRange(5, 50)
        self.max_topics_spin.setValue(15)
        self.max_topics_spin.setEnabled(False)  # Initially disabled
        self.max_topics_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        elbow_form.addRow("Max Topics:", self.max_topics_spin)
        
        # Step size
        self.step_size_spin = QSpinBox()
        self.step_size_spin.setRange(1, 5)
        self.step_size_spin.setValue(1)
        self.step_size_spin.setEnabled(False)  # Initially disabled
        self.step_size_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        elbow_form.addRow("Step:", self.step_size_spin)
        
        lda_options_layout.addLayout(elbow_form)
        
        # Add LDA options to settings layout
        settings_layout_inner.addWidget(self.lda_options_group)
        
        # Advanced settings section
        advanced_group = QGroupBox("Adaptive Processing Settings")
        advanced_group.setCheckable(True)
        advanced_group.setChecked(False)  # Collapsed by default
        advanced_layout = QVBoxLayout(advanced_group)
        advanced_layout.setSpacing(WIDGET_SPACING)
        advanced_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Adaptive processing checkbox
        self.adaptive_checkbox = QCheckBox("Enable adaptive processing")
        self.adaptive_checkbox.setChecked(True)
        self.adaptive_checkbox.setToolTip("Automatically adjust parameters if UMAP dimensionality error occurs")
        advanced_layout.addWidget(self.adaptive_checkbox)
        
        # Adaptive settings grid
        adaptive_form = QFormLayout()
        adaptive_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        adaptive_form.setLabelAlignment(Qt.AlignRight)
        adaptive_form.setHorizontalSpacing(WIDGET_SPACING)
        adaptive_form.setVerticalSpacing(WIDGET_SPACING)
        
        # Max retries
        self.max_retries_spin = QSpinBox()
        self.max_retries_spin.setRange(1, 10)
        self.max_retries_spin.setValue(5)
        self.max_retries_spin.setToolTip("Maximum number of retry attempts with adjusted parameters")
        self.max_retries_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        adaptive_form.addRow("Max Retries:", self.max_retries_spin)
        
        # Initial chunk size
        self.chunk_size_spin = QSpinBox()
        self.chunk_size_spin.setRange(50, 500)
        self.chunk_size_spin.setValue(100)
        self.chunk_size_spin.setToolTip("Initial size for document chunks if needed")
        self.chunk_size_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        adaptive_form.addRow("Initial Chunk Size:", self.chunk_size_spin)
        
        advanced_layout.addLayout(adaptive_form)
        
        # Add info text
        info_text = (
            "Adaptive processing helps to automatically adjust parameters and document chunking when necessary."
            "This is useful if you upload one large document."
        )
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-style: italic; font-size: 10pt;")
        advanced_layout.addWidget(info_label)
        
        # Add advanced group to settings layout
        settings_layout_inner.addWidget(advanced_group)
        
        # Control buttons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(WIDGET_SPACING)
        
        # Extract topics button
        self.extract_button = QPushButton("Extract Topics")
        self.extract_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.extract_button.clicked.connect(self.start_topic_extraction)
        self.extract_button.setEnabled(False)  # Disabled until documents are loaded
        self.extract_button.setMinimumHeight(BUTTON_HEIGHT)
        self.extract_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        self.extract_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        controls_layout.addWidget(self.extract_button)
        
        # Refine topics button
        self.refine_button = QPushButton("Refine Topics with LLM")
        self.refine_button.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.refine_button.clicked.connect(self.show_refine_dialog)
        self.refine_button.setEnabled(False)  # Disabled until topics are extracted
        self.refine_button.setMinimumHeight(BUTTON_HEIGHT)
        self.refine_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        self.refine_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        controls_layout.addWidget(self.refine_button)
        
        settings_layout_inner.addLayout(controls_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setVisible(False)  # Hide initially
        settings_layout_inner.addWidget(self.progress_bar)
        
        # Wrap settings in a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(settings_group)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        settings_layout.addWidget(scroll_area)
        
        # Add settings container to splitter
        splitter.addWidget(settings_container)
        
        # Topics container
        topics_container = QWidget()
        topics_layout = QVBoxLayout(topics_container)
        topics_layout.setContentsMargins(0, 0, 0, 0)
        topics_layout.setSpacing(WIDGET_SPACING)
        
        # Topics view
        topics_tabs = QTabWidget()
        topics_layout.addWidget(topics_tabs, 1)  # Add stretch factor to make tabs expand
        
        # Topic overview tab
        overview_tab = QWidget()
        overview_layout = QVBoxLayout(overview_tab)
        overview_layout.setSpacing(WIDGET_SPACING)
        overview_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        self.topic_table = QTableWidget()
        self.topic_table.setColumnCount(4)
        self.topic_table.setHorizontalHeaderLabels(["Topic ID", "Count", "Representative Words", "Description"])
        self.topic_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Topic ID
        self.topic_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Count
        self.topic_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)  # Words
        self.topic_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)  # Description
        
        copy_act = QAction("Copy", self)
        copy_act.setShortcut(QKeySequence.Copy)
        copy_act.triggered.connect(lambda _, tbl=self.topic_table: self._copy_from_table(tbl))
        self.topic_table.addAction(copy_act)
        self.topic_table.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.topic_table.verticalHeader().setVisible(False)  # Hide vertical headers
        self.topic_table.setAlternatingRowColors(True)  # Alternate row colors for readability
        self.topic_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        overview_layout.addWidget(self.topic_table)
        
        topics_tabs.addTab(overview_tab, "Topic Overview")
        
        # Document topics tab
        doc_topics_tab = QWidget()
        doc_topics_layout = QVBoxLayout(doc_topics_tab)
        doc_topics_layout.setSpacing(WIDGET_SPACING)
        doc_topics_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        self.doc_topic_table = QTableWidget()
        self.doc_topic_table.setColumnCount(3)
        self.doc_topic_table.setHorizontalHeaderLabels(["Document", "Topic ID", "Probability"])
        self.doc_topic_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # Document
        self.doc_topic_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Topic ID
        self.doc_topic_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Probability
        copy_act = QAction("Copy", self)
        copy_act.setShortcut(QKeySequence.Copy)
        copy_act.triggered.connect(lambda _, tbl=self.doc_topic_table: self._copy_from_table(tbl))
        self.doc_topic_table.addAction(copy_act)
        self.doc_topic_table.setContextMenuPolicy(Qt.ActionsContextMenu)        
        self.doc_topic_table.verticalHeader().setVisible(False)  # Hide vertical headers
        self.doc_topic_table.setAlternatingRowColors(True)  # Alternate row colors for readability
        self.doc_topic_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        doc_topics_layout.addWidget(self.doc_topic_table)
        
        topics_tabs.addTab(doc_topics_tab, "Document Topics")
        
        # Keywords tab
        keywords_tab = QWidget()
        keywords_layout = QVBoxLayout(keywords_tab)
        keywords_layout.setSpacing(WIDGET_SPACING)
        keywords_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Topic selector
        selector_form = QFormLayout()
        selector_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        selector_form.setLabelAlignment(Qt.AlignRight)
        
        self.topic_selector = QComboBox()
        self.topic_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        selector_form.addRow("Select Topic:", self.topic_selector)
        
        keywords_layout.addLayout(selector_form)
        
        # Keywords view
        self.keywords_table = QTableWidget()
        self.keywords_table.setColumnCount(2)
        self.keywords_table.setHorizontalHeaderLabels(["Word", "Score"])
        self.keywords_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # Word
        self.keywords_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Score
        self.keywords_table.verticalHeader().setVisible(False)  # Hide vertical headers
        copy_act = QAction("Copy", self)
        copy_act.setShortcut(QKeySequence.Copy)
        copy_act.triggered.connect(lambda _, tbl=self.keywords_table: self._copy_from_table(tbl))
        self.keywords_table.addAction(copy_act)
        self.keywords_table.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.keywords_table.setAlternatingRowColors(True)  # Alternate row colors for readability
        self.keywords_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        keywords_layout.addWidget(self.keywords_table)
        
        topics_tabs.addTab(keywords_tab, "Topic Keywords")
        
        # Add topics container to splitter
        splitter.addWidget(topics_container)
        
        # Set initial sizes (40% for settings, 60% for results)
        splitter.setSizes([400, 600])
        
        # Connect signals and slots
        self.connect_signals()



    def _copy_from_table(self, table: QTableWidget):
        """Copy selected cells as TSV (and HTML) to the system clipboard."""
        selected = table.selectedIndexes()
        if not selected:
            return

        # Build a 2D array of cell texts
        # (accounting for possible non‑contiguous selections)
        rows = {}
        for idx in selected:
            rows.setdefault(idx.row(), {})[idx.column()] = table.item(idx.row(), idx.column()).text()

        # Create TSV plain‑text
        tsv_lines = []
        for row in sorted(rows):
            cols = rows[row]
            line = [ cols.get(col, "") for col in sorted(cols) ]
            tsv_lines.append("\t".join(line))
        plain = "\n".join(tsv_lines)

        # (Optional) Build a simple HTML table for rich paste
        html = "<table>\n"
        for line in tsv_lines:
            html += "  <tr>" + "".join(f"<td>{cell}</td>" for cell in line.split("\t")) + "</tr>\n"
        html += "</table>"

        # Put both on the clipboard
        mime = QMimeData()
        mime.setText(plain)    # plain‑text for external apps
        mime.setHtml(html)     # HTML for rich‑paste targets
        QApplication.clipboard().setMimeData(mime, mode=QClipboard.Clipboard)

   
    def connect_signals(self):
        """Connect signals and slots"""
        # Connect to progress updates from the topic modeler
        # Connect topic selector to update keywords
        self.topic_selector.currentIndexChanged.connect(self.update_keywords_view)
        # Connect method combo to update options
        self.method_combo.currentTextChanged.connect(self.update_method_options)
        # Connect elbow checkbox
        self.elbow_checkbox.toggled.connect(self.toggle_elbow_options)
        # Also connect to worker signals when they exist
        if hasattr(self.topic_modeler, 'worker') and self.topic_modeler.worker is not None:
            self.topic_modeler.worker.show_elbow_dialog.connect(self.show_elbow_dialog_handler)
    
    def show_elbow_dialog_handler(self, model_scores, topics_range):
        """Handle showing the elbow method dialog"""
        dialog = ElbowMethodDialog(model_scores, topics_range, self)
        
        if dialog.exec_():
            # User accepted - get selected topics
            n_topics = dialog.get_selected_topics()
            self.topic_modeler.worker.elbow_selection_result = n_topics
            self.topic_modeler.worker.elbow_selection_cancelled = False
        else:
            # User canceled - explicitly signal cancellation
            self.topic_modeler.worker.elbow_selection_result = None
            self.topic_modeler.worker.elbow_selection_cancelled = True
            
            # Make sure UI elements are re-enabled if the user cancels
            self.extract_button.setEnabled(True)
            self.progress_bar.setVisible(False)
            self.progress_updated.emit(0, "Elbow method cancelled - ready to try again.")
    
    def set_documents(self, documents):
        """Set the documents for topic modeling"""
        if not documents:
            return
        
        self.documents = documents
        
        # Enable the extract button
        self.extract_button.setEnabled(True)
        
        # Update status
        self.progress_updated.emit(0, f"Ready to extract topics from {len(documents)} documents")

    def update_ngram_range(self):
        """Ensure min_ngram is always <= max_ngram"""
        if self.min_ngram_spin.value() > self.max_ngram_spin.value():
            if self.sender() == self.min_ngram_spin:
                self.max_ngram_spin.setValue(self.min_ngram_spin.value())
            else:
                self.min_ngram_spin.setValue(self.max_ngram_spin.value())
    

    def start_topic_extraction(self):
        """Start the topic extraction process"""
        if not self.documents:
            QMessageBox.warning(
                self, "No Documents", "Please load documents first."
            )
            return
        
        # Disable UI elements during extraction
        self.extract_button.setEnabled(False)
        self.refine_button.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        # Get selected parameters
        language = self.language_combo.currentText()
        nr_topics = self.topics_combo.currentData()
        min_topic_size = self.min_size_spin.value()
        n_gram_range = (self.min_ngram_spin.value(), self.max_ngram_spin.value())
        
        # Get adaptive parameters
        adaptive_enabled = self.adaptive_checkbox.isChecked() 
        max_retries = self.max_retries_spin.value() if adaptive_enabled else 1
        chunk_size = self.chunk_size_spin.value() if adaptive_enabled else None
        
        # Get selected method
        method = self.method_combo.currentData()
        
        # Get LDA elbow method parameters if applicable
        lda_elbow_enabled = False
        lda_elbow_params = {}
        
        if method == "lda" and self.elbow_checkbox.isChecked():
            lda_elbow_enabled = True
            lda_elbow_params = {
                'min_topics': self.min_topics_spin.value(),
                'max_topics': self.max_topics_spin.value(),
                'step_size': self.step_size_spin.value()
            }
        
        # Create and configure worker
        worker = self.topic_modeler.extract_topics(
            self.documents, language, n_gram_range, min_topic_size, nr_topics,
            adaptive_enabled=adaptive_enabled,
            max_retries=max_retries,
            initial_chunk_size=chunk_size,
            method=method,
            lda_elbow_enabled=lda_elbow_enabled,
            lda_elbow_params=lda_elbow_params
        )
        if method == "lda" and lda_elbow_enabled:
            worker.show_elbow_dialog.connect(self.show_elbow_dialog_handler)        
        # Connect worker signals
        worker.progress_updated.connect(self.update_progress)
        worker.topics_extracted.connect(self.on_topics_extracted)
        worker.error_occurred.connect(self.on_extraction_error)
        
        # Forward the progress signal to the main window
        worker.progress_updated.connect(self.progress_updated)
        
        # Update UI
        if lda_elbow_enabled:
            self.progress_updated.emit(5, f"Starting LDA topic extraction with elbow method...")
        else:
            self.progress_updated.emit(5, f"Starting topic extraction using {self.method_combo.currentText()}...")
    
    @pyqtSlot(int, str)
    def update_progress(self, progress, message):
        """Update the progress bar and message"""
        self.progress_bar.setValue(progress)
        
        # Check if message contains adaptive processing information
        if "attempt" in message.lower() or "adjust" in message.lower():
            # Highlight adaptive processing messages
            self.progress_bar.setFormat(f"{progress}% - ⚙️ {message}")
            # You can also update the color to indicate adaptation is happening
            self.progress_bar.setStyleSheet("QProgressBar { color: blue; }")
        else:
            self.progress_bar.setFormat(f"{progress}% - {message}")
            self.progress_bar.setStyleSheet("")

    
    @pyqtSlot(object, object, object, object, object, object)
    def on_topics_extracted(self, topics, probs, topics_words, topic_info, model, chunked_docs):
        """Handle extracted topics"""
        # Store the results
        self.topics = topics
        self.probs = probs
        self.topics_words = topics_words
        self.topic_info = topic_info
        
        # Store chunked documents
        self.chunked_documents = chunked_docs

        
        # Explicitly set the model in the topic_modeler
        self.topic_modeler.set_model(model)
        
        # Re-enable UI elements
        self.extract_button.setEnabled(True)
        self.refine_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Update UI with the extracted topics
        self.update_topic_views()
        
        # Update the emit to include chunked documents
        self.topics_extracted.emit(topics, probs, topics_words, topic_info, chunked_docs)
        
        # Update success message to reflect chunk count
        QMessageBox.information(
            self, "Topic Extraction Complete", 
            f"Successfully extracted {len(set(topics))} topics from {len(chunked_docs)} document chunks."
        )

        # display how many chunks were created from the original document
        if len(self.documents) == 1 and len(self.chunked_documents) > 1:
            QMessageBox.information(
                self, "Document Chunking Information", 
                f"Your document was automatically divided into {len(self.chunked_documents)} chunks for better topic analysis.\n\n"
                f"Each chunk may be assigned different topics."
            )

        
    @pyqtSlot(str)
    def on_extraction_error(self, error_message):
        """Handle extraction errors"""
        # Re-enable UI elements
        self.extract_button.setEnabled(True)
        self.refine_button.setEnabled(False)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Show error message
        QMessageBox.warning(
            self, "Extraction Error", f"Error during topic extraction: {error_message}"
        )
        
        # Update progress in main window
        self.progress_updated.emit(0, "Topic extraction failed")
    
    def update_topic_views(self):
        """Update the UI with the extracted topics"""
        if not hasattr(self, 'topics') or self.topics is None:
            return
        
        # Update topic overview table
        self.topic_table.setRowCount(0)
        
        # Get unique topics and their counts
        topic_counts = {}
        for topic in self.topics:
            if topic not in topic_counts:
                topic_counts[topic] = 0
            topic_counts[topic] += 1
        
        # Add rows to the table
        for i, (topic_id, count) in enumerate(sorted(topic_counts.items())):
            self.topic_table.insertRow(i)
            
            # Topic ID
            id_item = QTableWidgetItem(str(topic_id))
            self.topic_table.setItem(i, 0, id_item)
            
            # Count
            count_item = QTableWidgetItem(str(count))
            self.topic_table.setItem(i, 1, count_item)
            
            # Representative words
            if topic_id in self.topics_words and self.topics_words[topic_id]:
                words = ", ".join([word for word, _ in self.topics_words[topic_id][:10]]) # define number of words passed to the LLM
                words_item = QTableWidgetItem(words)
                self.topic_table.setItem(i, 2, words_item)
            else:
                self.topic_table.setItem(i, 2, QTableWidgetItem("N/A"))
            
            # Description (from refined topics if available)
            if topic_id in self.refined_topics:
                desc_item = QTableWidgetItem(self.refined_topics[topic_id])
                self.topic_table.setItem(i, 3, desc_item)
            else:
                self.topic_table.setItem(i, 3, QTableWidgetItem(""))
        
        # Resize table columns
        self.topic_table.resizeColumnsToContents()
        documents_to_display = self.chunked_documents if hasattr(self, 'chunked_documents') and self.chunked_documents else self.documents

        # Update document topics table
        self.doc_topic_table.setRowCount(0)
        
        for i, (doc, topic, prob) in enumerate(zip(documents_to_display, self.topics, self.probs)):
            self.doc_topic_table.insertRow(i)
            
            # Document preview (truncated)
            doc_preview = doc[:50] + ("..." if len(doc) > 50 else "")
            doc_item = QTableWidgetItem(doc_preview)
            doc_item.setToolTip(doc[:500] + ("..." if len(doc) > 500 else ""))  # Add tooltip with longer preview
            self.doc_topic_table.setItem(i, 0, doc_item)
            
            # Topic ID
            id_item = QTableWidgetItem(str(topic))
            self.doc_topic_table.setItem(i, 1, id_item)
            
            # Probability
            if isinstance(prob, (list, tuple)) and len(prob) > 0:
                max_prob = max(prob)
                prob_item = QTableWidgetItem(f"{max_prob:.4f}")
            else:
                prob_item = QTableWidgetItem("N/A")
            self.doc_topic_table.setItem(i, 2, prob_item)
        
        # Resize table columns
        self.doc_topic_table.resizeColumnsToContents()
        
        # Update topic selector for keywords view
        self.topic_selector.clear()
        
        for topic_id in sorted(self.topics_words.keys()):
            if topic_id != -1:  # Skip outlier topic
                self.topic_selector.addItem(f"Topic {topic_id}", topic_id)
        
        # Select the first topic if available
        if self.topic_selector.count() > 0:
            self.topic_selector.setCurrentIndex(0)
            self.update_keywords_view()
            
    def update_method_options(self, method_text):
        """Show/hide options based on selected method"""
        if "LDA" in method_text:
            self.lda_options_group.setVisible(True)
        else:
            self.lda_options_group.setVisible(False)

    def toggle_elbow_options(self, checked):
        """Enable/disable elbow method options"""
        self.min_topics_spin.setEnabled(checked)
        self.max_topics_spin.setEnabled(checked)
        self.step_size_spin.setEnabled(checked)
    
    def update_keywords_view(self):
        """Update the keywords view for the selected topic"""
        if not hasattr(self, 'topics_words') or self.topics_words is None:
            return
        
        # Get the selected topic
        topic_id = self.topic_selector.currentData()
        if topic_id is None:
            return
        
        # Clear the table
        self.keywords_table.setRowCount(0)
        
        # Get the words for this topic
        if topic_id in self.topics_words:
            words = self.topics_words[topic_id]
            
            # Add rows to the table
            for i, (word, score) in enumerate(words):
                self.keywords_table.insertRow(i)
                
                # Word
                word_item = QTableWidgetItem(word)
                self.keywords_table.setItem(i, 0, word_item)
                
                # Score
                score_item = QTableWidgetItem(f"{score:.4f}")
                self.keywords_table.setItem(i, 1, score_item)
        
        # Resize table columns
        self.keywords_table.resizeColumnsToContents()
    
    def show_refine_dialog(self):
        """Show dialog for refining topics with LLM"""
        if not hasattr(self, 'topics_words') or self.topics_words is None:
            QMessageBox.warning(
                self, "No Topics", "Please extract topics first."
            )
            return
        
        # Force reload the LLM config
        try:
            # Make sure we have the latest configuration
            self.llm_service.config.load()
            # Update service properties with config values
            self.llm_service.anthropic_key = self.llm_service.config.anthropic_key
            self.llm_service.openai_key = self.llm_service.config.openai_key
            self.llm_service.provider = self.llm_service.config.provider
        except Exception as e:
            logger.error(f"Error reloading LLM config: {str(e)}")
        
        # Skip the API key check - we'll handle this in the dialog
        dialog = RefineTopicsDialog(self.topics_words, self.llm_service, self)
        
        if dialog.exec_() == QDialog.Accepted:
            # Get the refined topics from the dialog
            self.refined_topics = dialog.get_refined_topics()
            
            # Update the topic overview table with new descriptions
            self.update_topic_views()
            
    def show_help_dialog(self):
        """Show help dialog with information about BERTopic and topic modeling"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QTextBrowser, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Topic modeling help")
        dialog.setMinimumSize(800, 600)  # Increase dialog size for better readability
        
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
        <h2>Topic Modeling Module Overview</h2>
        <p>This tab allows you to extract topics from documents using multiple topic modeling algorithms.</p>
        <ul>
            <li>1. Adjust the topic model settings (if needed).</li>
            <li>2. Click 'Extract Topics' to start topic modeling.</li>
            <li>3. Once complete, you can refine the topics with an LLM API.</li>
            <li>4. View the extracted topics and their keywords.</li>
        </ul>

        <p>Unlike traditional methods like LDA, BERTopic:</p>
        <ul>
            <li>Captures semantic meaning through transformer-based embeddings</li>
            <li>Creates more coherent topics with better separation</li>
            <li>Works well with smaller text collections</li>
            <li>Supports multiple languages</li>
        </ul>
        
        <p>The model works by embedding documents with a sentence transformer, reducing dimensionality, 
        clustering similar documents, and then extracting representative keywords for each cluster (topic).</p>

        <p>This application also supports traditional LDA topic modeling with enhancements like the Elbow method
        for optimal topic number selection and interactive visualization with pyLDAvis.</p>
        """)
        tabs.addTab(overview_tab, "Overview")
        
        # Topics explanation tab
        topics_tab = QTextBrowser()
        topics_tab.setHtml("""
        <h2>Understanding Topics</h2>
        
        <h3>Topic IDs</h3>
        <p>Each topic is assigned a numeric ID. These IDs have specific meanings:</p>
        <ul>
            <li><b>Topic -1 (Outlier Topic)</b>: Documents that don't fit well into any other topic are assigned to topic -1. 
            These can be considered outliers or noise in your data.</li>
            <li><b>Topics 0, 1, 2, etc.</b>: Regular topics discovered in your documents. The numbering is arbitrary 
            and doesn't indicate importance or ranking.</li>
        </ul>
        
        <h3>Topic Representation</h3>
        <p>Each topic is represented by:</p>
        <ul>
            <li><b>Keywords</b>: Words that are most representative of the topic, ordered by relevance.</li>
            <li><b>Scores</b>: Numbers indicating how strongly each keyword is associated with the topic.</li>
            <li><b>Documents</b>: A count of how many documents are assigned to each topic.</li>
        </ul>
        
        <h3>Document-Topic Assignment</h3>
        <p>Each document is primarily assigned to a single topic, but can have probabilities across multiple topics.
        The assigned topic is the one with the highest probability score.</p>
        """)
        tabs.addTab(topics_tab, "Topics")
        
        # Settings explanation tab
        settings_tab = QTextBrowser()
        settings_tab.setHtml("""
        <h2>Topic Model Settings</h2>
        
        <h3>Language</h3>
        <p>Select the primary language of your documents. This affects the embedding model used.</p>
        <ul>
            <li><b>Multilingual</b>: Works with multiple languages simultaneously</li>
            <li><b>English</b>: Optimized for English text</li>
        </ul>
        
        <h3>Number of Topics</h3>
        <p>Controls how many distinct topics to extract:</p>
        <ul>
            <li><b>Auto</b>: The algorithm will try to determine the optimal number of topics</li>
            <li><b>Specific number</b>: Force a specific number of topics</li>
            <li><b>Elbow Method (LDA only)</b>: Automatically find the optimal number of topics by evaluating multiple models</li>
        </ul>
        <p>More topics create greater specificity but might overlap or become less coherent.
        Fewer topics are broader but might combine unrelated concepts.</p>
        
        <h3>Min Topic Size</h3>
        <p>The minimum number of documents required to form a topic. Increasing this creates fewer, more general topics.</p>
        
        <h3>Max N-gram</h3>
        <p>The maximum number of words in phrases that can be included in topics:</p>
        <ul>
            <li><b>1</b>: Only single words (unigrams)</li>
            <li><b>2</b>: Words and two-word phrases (unigrams and bigrams)</li>
            <li><b>3+</b>: Includes longer phrases (trigrams, etc.)</li>
        </ul>

        <h3>LDA Elbow Method</h3>
        <p>When using LDA topic modeling, the Elbow method helps find the optimal number of topics by:</p>
        <ul>
            <li>Training multiple LDA models with different numbers of topics</li>
            <li>Evaluating each model's quality using coherence and log-likelihood</li>
            <li>Visualizing the results to identify the "elbow point" in the quality curve</li>
            <li>Allowing you to select the best balance of model complexity and performance</li>
        </ul>
        <p>This feature eliminates guesswork when choosing the number of topics, resulting in more meaningful topic models.</p>
        """)
        tabs.addTab(settings_tab, "Settings")

        # Adaptive processing tab
        adaptive_tab = QTextBrowser()
        adaptive_tab.setHtml("""
        <h2>Adaptive Processing</h2>
        
        <p>Adaptive processing helps overcome common issues with BERTopic, particularly the UMAP dimensionality 
        reduction error that can occur with small or very large document sets.</p>
        
        <h3>What It Does</h3>
        <p>When enabled, adaptive processing will:</p>
        <ul>
            <li>Automatically adjust UMAP parameters if errors occur</li>
            <li>Chunk documents into smaller pieces if needed</li>
            <li>Try multiple parameter combinations to find ones that work</li>
            <li>Preserve topic quality while ensuring successful processing</li>
        </ul>
        
        <h3>When To Use It</h3>
        <ul>
            <li><b>One large document</b>: When uploading one large document, adaptive processing will chunk it into smaller ones to allow running topics modelling algorithms.</li>
            <li><b>Small Document Sets</b>: If you have fewer than 30 documents</li>
            <li><b>Very Large Documents</b>: When individual documents are very long</li>
            <li><b>Error Handling</b>: If you frequently encounter UMAP errors</li>
        </ul>
        
        <h3>Settings</h3>
        <ul>
            <li><b>Max Retries</b>: How many parameter combinations to try before giving up</li>
            <li><b>Initial Chunk Size</b>: How large each document chunk should be if chunking is needed</li>
        </ul>
        
        <p>For most users, the default settings will work well. Increase max retries for more difficult datasets.</p>
        """)
        tabs.addTab(adaptive_tab, "Adaptive Processing")

        # Methods tab
        methods_tab = QTextBrowser()
        methods_tab.setHtml("""
        <h2>Topic Modeling Methods</h2>
        
        <p>This application supports multiple topic modeling approaches, each with different strengths and limitations.</p>
        
        <h3>BERTopic with UMAP</h3>
        <p><strong>Best for:</strong> High-quality, semantically coherent topics</p>
        <ul>
            <li><strong>Pros:</strong> Produces the most coherent and meaningful topics, captures semantic relationships between words</li>
            <li><strong>Cons:</strong> Can fail with small document sets (less than ~20 documents), sensitive to parameter settings</li>
            <li><strong>When to use:</strong> When you have a reasonable number of documents and want the highest quality topics</li>
        </ul>
        
        <h3>BERTopic with PCA</h3>
        <p><strong>Best for:</strong> Good quality topics with better stability</p>
        <ul>
            <li><strong>Pros:</strong> More stable than UMAP with small document sets, still leverages BERT embeddings</li>
            <li><strong>Cons:</strong> Topics may be less coherent than with UMAP, can still fail with very small sets</li>
            <li><strong>When to use:</strong> When UMAP-based BERTopic fails or when you have 5-20 documents</li>
        </ul>
        
        <h3>NMF (Non-negative Matrix Factorization)</h3>
        <p><strong>Best for:</strong> Stable topic extraction with small document sets</p>
        <ul>
            <li><strong>Pros:</strong> Very stable even with small document sets, fast, deterministic results</li>
            <li><strong>Cons:</strong> Less semantic coherence than BERTopic, based only on word co-occurrence</li>
            <li><strong>When to use:</strong> When you have very few documents (less than 10) or when other methods fail</li>
        </ul>
        
        <h3>LDA (Latent Dirichlet Allocation)</h3>
        <p><strong>Best for:</strong> Traditional probabilistic topic modeling</p>
        <ul>
            <li><strong>Pros:</strong> Well-established method, good with larger document sets, probabilistic model</li>
            <li><strong>Cons:</strong> Can perform poorly with very short texts, may need more tuning</li>
            <li><strong>When to use:</strong> When you have longer documents or want a probabilistic topic distribution</li>
            <li><strong>Special features:</strong> Elbow method for optimal topic number selection, interactive visualization with pyLDAvis</li>
        </ul>
        
        <h3>Method Selection Strategy</h3>
        <p>For the best experience:</p>
        <ol>
            <li>Start with <strong>BERTopic (UMAP)</strong> for the highest quality</li>
            <li>If that fails, try <strong>BERTopic (PCA)</strong></li>
            <li>For very small document sets, use <strong>NMF</strong></li>
            <li>For traditional probabilistic topics and visualization, try <strong>LDA</strong></li>
        </ol>
        
        <p>With adaptive processing enabled, the system will automatically try alternative methods if the primary one fails.</p>
        """)
        tabs.addTab(methods_tab, "Methods")

        # LDA and Visualization tab (new)
        lda_viz_tab = QTextBrowser()
        lda_viz_tab.setHtml("""
        <h2>LDA and Interactive Visualization</h2>
        
        <p>The application includes special features for LDA topic models and visualization:</p>
        
        <h3>LDA Elbow Method</h3>
        <p>Finding the right number of topics is critical for meaningful results. The Elbow method helps by:</p>
        <ul>
            <li>Training multiple LDA models with different topic numbers (configurable range)</li>
            <li>Evaluating each model using log-likelihood and topic distinctiveness metrics</li>
            <li>Plotting a quality curve to identify the "elbow point" - the optimal trade-off between complexity and quality</li>
            <li>Presenting an interactive dialog where you can see the recommended topic number or select your own</li>
        </ul>
        
        <p>To use this feature, select "LDA" as your method and check "Use elbow method to find optimal number of topics"
        in the LDA Options section.</p>
        
        <h3>pyLDAvis Interactive Visualization</h3>
        <p>LDA models can be difficult to interpret. The pyLDAvis visualization helps by:</p>
        <ul>
            <li>Showing topic distributions and relationships in an interactive web-based visualization</li>
            <li>Displaying topics as circles in a 2D space where proximity indicates similarity</li>
            <li>Allowing adjustment of the relevance parameter (λ) to explore different term rankings</li>
            <li>Showing topic prevalence through circle size</li>
            <li>Revealing the most relevant terms for each topic</li>
        </ul>
        
        <p>To use this feature:</p>
        <ol>
            <li>Create an LDA topic model</li>
            <li>Go to the Visualizer tab and select "Interactive LDA Visualization"</li>
            <li>Generate the visualization</li>
            <li>Explore the results in the "Interactive View" tab</li>
            <li>Save the visualization as an HTML file to share or view later</li>
        </ol>
        
        <p>This interactive visualization provides deeper insights into your topic model than static charts alone.</p>
        """)
        tabs.addTab(lda_viz_tab, "LDA & Visualization")
                
        # Tips tab
        tips_tab = QTextBrowser()
        tips_tab.setHtml("""
        <h2>Tips for Better Results</h2>
        
        <h3>Data Preparation</h3>
        <ul>
            <li>Clean your text by removing stopwords, special characters, etc.</li>
            <li>Ensure documents are substantial enough (not just a few words)</li>
            <li>Try to have at least 10-20 documents for meaningful topics</li>
        </ul>
        
        <h3>Topic Modeling</h3>
        <ul>
            <li>Experiment with different numbers of topics or use the Elbow method for LDA</li>
            <li>Check the outlier topic (-1) - if too many documents fall here, adjust settings</li>
            <li>Look at the distribution of documents across topics</li>
            <li>Try different minimum topic sizes if topics appear fragmented</li>
            <li>Compare different methods - sometimes simpler methods like LDA or NMF may give more interpretable results</li>
        </ul>
        
        <h3>Topic Refinement</h3>
        <ul>
            <li>Use the LLM refinement to make topics more interpretable</li>
            <li>Validate topic quality with metrics in the Validator tab</li>
            <li>Use topic highlighting to see how topics appear in the original text</li>
            <li>For LDA models, use the pyLDAvis visualization to better understand topic relationships</li>
        </ul>
        
        <h3>Visualization Tips</h3>
        <ul>
            <li>Explore all available visualization types to gain different perspectives on your topics</li>
            <li>For LDA models, use the interactive visualization to explore term-topic relationships</li>
            <li>Adjust the λ parameter in pyLDAvis to balance between term exclusivity and frequency</li>
            <li>Save visualizations as HTML or images for sharing or inclusion in reports</li>
        </ul>
        """)
        tabs.addTab(tips_tab, "Tips")
        
        # Add OK button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        
        # Make the button bigger
        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setMinimumHeight(BUTTON_HEIGHT)
        ok_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        
        layout.addWidget(button_box)
        
        # Show the dialog
        dialog.exec_()

class RefineTopicsDialog(QDialog):
    """Dialog for refining topics with LLM"""
    
    def __init__(self, topics_words, llm_service, parent=None):
        super().__init__(parent)
        
        self.topics_words = topics_words
        self.llm_service = llm_service
        self.refined_topics = {}
        
        # Force reload the config to ensure we have the latest keys
        try:
            self.llm_service.config.load()
            self.llm_service.anthropic_key = self.llm_service.config.anthropic_key
            self.llm_service.openai_key = self.llm_service.config.openai_key
            self.llm_service.provider = self.llm_service.config.provider
        except Exception as e:
            logger.error(f"Error reloading LLM config: {str(e)}")
        
        self.setWindowTitle("Refine Topics with LLM")
        self.setMinimumSize(700, 500)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Provider selection
        provider_group = QGroupBox("LLM Provider")
        provider_layout = QHBoxLayout(provider_group)
        provider_layout.setSpacing(WIDGET_SPACING)
        
        self.provider_buttons = QButtonGroup(self)
        
        self.anthropic_radio = QRadioButton("Anthropic Claude")
        if self.llm_service.provider == "anthropic":
            self.anthropic_radio.setChecked(True)
        self.provider_buttons.addButton(self.anthropic_radio, 0)
        provider_layout.addWidget(self.anthropic_radio)
        
        self.openai_radio = QRadioButton("OpenAI GPT")
        if self.llm_service.provider == "openai":
            self.openai_radio.setChecked(True)
        self.provider_buttons.addButton(self.openai_radio, 1)
        provider_layout.addWidget(self.openai_radio)
        
        # Add API key status indicators
        self.anthropic_status = QLabel("")
        self.openai_status = QLabel("")
        self.update_key_status()
        provider_layout.addWidget(self.anthropic_status)
        provider_layout.addWidget(self.openai_status)
        
        layout.addWidget(provider_group)
        
        # Topics selection
        topics_group = QGroupBox("Topics to Refine")
        topics_layout = QVBoxLayout(topics_group)
        topics_layout.setSpacing(WIDGET_SPACING)
        
        self.topics_list = QListWidget()
        self.topics_list.setSelectionMode(QListWidget.MultiSelection)
        self.topics_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Add topics to the list
        for topic_id, words in sorted(self.topics_words.items()):
            if topic_id == -1:  # Skip outlier topic
                continue
                
            # Create a preview of the topic words
            word_preview = ", ".join([word for word, _ in words[:10]])
            item_text = f"Topic {topic_id}: {word_preview}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, topic_id)
            self.topics_list.addItem(item)
            
            # Select all topics by default
            item.setSelected(True)
        
        topics_layout.addWidget(self.topics_list)
        
        # Select/deselect all buttons
        select_buttons_layout = QHBoxLayout()
        select_buttons_layout.setSpacing(WIDGET_SPACING)
        
        select_all_button = QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all_topics)
        select_all_button.setMinimumHeight(BUTTON_HEIGHT)
        select_buttons_layout.addWidget(select_all_button)
        
        deselect_all_button = QPushButton("Deselect All")
        deselect_all_button.clicked.connect(self.deselect_all_topics)
        deselect_all_button.setMinimumHeight(BUTTON_HEIGHT)
        select_buttons_layout.addWidget(deselect_all_button)
        
        topics_layout.addLayout(select_buttons_layout)
        
        layout.addWidget(topics_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Select topics to refine")
        layout.addWidget(self.status_label)
        
        # Results text area
        self.results_text = QTextEdit()
        self.results_text.setPlaceholderText("Refined topics will appear here")
        self.results_text.setReadOnly(True)
        self.results_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.results_text)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(WIDGET_SPACING)
        
        self.refine_button = QPushButton("Refine Topics")
        self.refine_button.clicked.connect(self.refine_topics)
        self.refine_button.setMinimumHeight(BUTTON_HEIGHT)
        self.refine_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        self.refine_button.setEnabled(self.check_api_keys_available())
        buttons_layout.addWidget(self.refine_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setMinimumHeight(BUTTON_HEIGHT)
        self.cancel_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        buttons_layout.addWidget(self.cancel_button)
        
        self.accept_button = QPushButton("Ok")
        self.accept_button.clicked.connect(self.accept)
        self.accept_button.setEnabled(False)
        self.accept_button.setMinimumHeight(BUTTON_HEIGHT)
        self.accept_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        buttons_layout.addWidget(self.accept_button)
        
        layout.addLayout(buttons_layout)
        
        # Connect radio buttons to update UI state
        self.anthropic_radio.toggled.connect(self.update_ui_state)
        self.openai_radio.toggled.connect(self.update_ui_state)
    
    def update_key_status(self):
        """Update API key status indicators"""
        if self.llm_service.anthropic_key:
            self.anthropic_status.setText("✓")
            self.anthropic_status.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.anthropic_status.setText("✗")
            self.anthropic_status.setStyleSheet("color: red; font-weight: bold;")
            
        if self.llm_service.openai_key:
            self.openai_status.setText("✓")
            self.openai_status.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.openai_status.setText("✗")
            self.openai_status.setStyleSheet("color: red; font-weight: bold;")
    
    def update_ui_state(self):
        """Update UI state based on selected provider"""
        self.refine_button.setEnabled(self.check_api_keys_available())
    
    def check_api_keys_available(self):
        """Check if API keys are available for the selected provider"""
        if self.anthropic_radio.isChecked():
            return bool(self.llm_service.anthropic_key)
        else:
            return bool(self.llm_service.openai_key)
    
    def select_all_topics(self):
        """Select all topics in the list"""
        for i in range(self.topics_list.count()):
            self.topics_list.item(i).setSelected(True)
    
    def deselect_all_topics(self):
        """Deselect all topics in the list"""
        for i in range(self.topics_list.count()):
            self.topics_list.item(i).setSelected(False)
    
    def refine_topics(self):
        """Start the topic refinement process"""
        # Check if any topics are selected
        selected_items = self.topics_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "No Topics Selected", "Please select at least one topic to refine."
            )
            return
        
        # Double-check API keys
        if not self.check_api_keys_available():
            provider = "Anthropic" if self.anthropic_radio.isChecked() else "OpenAI"
            QMessageBox.warning(
                self, "API Key Missing", 
                f"No API key configured for {provider}. Please configure it in Settings -> API Keys."
            )
            return
        
        # Get the selected topic IDs and their words
        selected_topics = {}
        for item in selected_items:
            topic_id = item.data(Qt.UserRole)
            selected_topics[topic_id] = self.topics_words[topic_id]
        
        # Disable UI elements during refinement
        self.refine_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.topics_list.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        # Set provider based on radio button selection
        provider = "anthropic" if self.anthropic_radio.isChecked() else "openai"
        self.llm_service.provider = provider
        
        # Create worker for LLM request
        self.worker = self.llm_service.create_worker(selected_topics)
        
        # Connect signals
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.response_received.connect(self.on_llm_response)
        
        # Start the worker
        self.worker.start()
        
        # Update status
        self.status_label.setText(f"Refining {len(selected_topics)} topics with {provider.capitalize()}...")
    
    @pyqtSlot(int, str)
    def update_progress(self, progress, message):
        """Update the progress bar and status message"""
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(f"{progress}% - {message}")
        self.status_label.setText(message)
    
    @pyqtSlot(object)
    def on_llm_response(self, response):
        """Handle LLM response"""
        # Re-enable UI elements
        self.refine_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
        self.topics_list.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Check for errors
        if response.error:
            self.status_label.setText(f"Error: {response.error}")
            QMessageBox.warning(
                self, "Refinement Error", f"Error during topic refinement: {response.error}"
            )
            return
        
        # Process the response
        try:
            self.refined_topics = json.loads(response.text)
            
            # Update the results text area
            results_text = ""
            for topic_id, description in sorted(self.refined_topics.items()):
                topic_id = int(topic_id)  # Convert string keys to integers
                results_text += f"Topic {topic_id}: {description}\n\n"
            
            self.results_text.setText(results_text)
            
            # Enable the accept button
            self.accept_button.setEnabled(True)
            
            # Update status
            self.status_label.setText(f"Successfully refined {len(self.refined_topics)} topics")
            
        except Exception as e:
            logger.error(f"Error processing LLM response: {str(e)}")
            self.status_label.setText(f"Error processing response: {str(e)}")
            QMessageBox.warning(
                self, "Processing Error", f"Error processing LLM response: {str(e)}"
            )
    
    def get_refined_topics(self):
        """Get the refined topics"""
        return self.refined_topics