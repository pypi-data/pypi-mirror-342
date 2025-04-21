#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualizer Tab module for the Audio to Topics application.
Provides UI for visualization of topics and text analysis.
"""

import os
import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QGroupBox, QProgressBar, QTabWidget,
                           QTableWidget, QTableWidgetItem, QHeaderView,
                           QMessageBox, QSpinBox, QComboBox, QProgressDialog, 
                           QListWidget, QListWidgetItem, QFileDialog, QStyle, 
                           QSplitter, QSizePolicy, QFormLayout, QAbstractItemView,
                           QApplication)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QEvent, QSize
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

from ..core.visualizer import Visualizer

# Define layout constants
LAYOUT_MARGIN = 10
WIDGET_SPACING = 8
BUTTON_HEIGHT = 30
BUTTON_MIN_WIDTH = 120

# Configure logging
logger = logging.getLogger(__name__)

class MatplotlibCanvas(FigureCanvas):
    """Canvas for displaying Matplotlib figures with smoother scrolling"""
    def __init__(self, figure):
        super().__init__(figure)
        self.setMinimumSize(400, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFocusPolicy(Qt.StrongFocus)  # Better keyboard navigation
        
        # Set a lower value for smoother scrolling
        # Note: This affects all scrolling regardless of what triggered it
        from matplotlib.backend_bases import NavigationToolbar2
        NavigationToolbar2.scroll_step = 0.2  # Default is 0.5 (lower = smoother)

    def wheelEvent(self, event):
        # Simple approach - scale the default scrolling behavior
        # Just reduce the sensitivity by forwarding to parent with modified parameters
        modifiers = event.modifiers()
        
        # Accept the event to prevent default Qt handling
        event.accept()
        
        if modifiers & Qt.ControlModifier:
            # For zooming, use default zoom but with reduced frequency
            # Just pass through for now, we'll improve the toolbar separately
            super().wheelEvent(event)
        else:
            # For panning, use the default implementation but it will respect our
            # reduced scroll_step setting from the constructor
            super().wheelEvent(event)

class SmoothNavigationToolbar(NavigationToolbar):
    """Navigation toolbar with smoother zoom and pan controls"""
    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)
        self.setIconSize(QSize(16, 16))  # Smaller icons

class SmoothWebEngineView(QWebEngineView):
    """WebEngineView with smoother scrolling behavior"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Enable smooth scrolling in web settings
        self.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        
    def wheelEvent(self, event):
        # Accept the event
        event.accept()
        
        # Calculate a smoother scroll amount
        delta_y = event.angleDelta().y()
        
        # Use JavaScript to perform the scroll with smoother behavior
        # The division factor determines how smooth the scrolling is
        self.page().runJavaScript(f"window.scrollBy(0, {-delta_y/3});")

class VisualizerTab(QWidget):
    """Tab for visualization functionality"""
    
    # Define signals
    progress_updated = pyqtSignal(int, str)  # Emits progress percentage and message
    
    def __init__(self):
        super().__init__()
        
        # Initialize instance variables
        self.visualizer = Visualizer()  # Visualizer instance
        self.documents = []  # Text documents (chunks if chunking was applied)
        self.original_documents = []  # Original documents before chunking
        self.topics = None  # Topic assignments
        self.topics_words = None  # Words for each topic
        self.probs = None  # Topic probabilities
        self.topic_info = None  # Topic info dataframe
            
        # Current visualization
        self.current_viz = None
        self.current_canvas = None
        
        # Set up the UI
        self.init_ui()
        
        # Set up smooth scrolling for all scrollable widgets
        self.setup_smooth_scrolling()
        
    def setup_smooth_scrolling(self):
        """Configure smooth scrolling for all scrollable widgets"""
        # Set global application behavior if possible
        try:
            QApplication.setWheelScrollLines(3)  # Default is often higher
        except:
            pass  # Ignore if this fails
        
        # Set scroll behavior for all list widgets to be pixel-based (smoother)
        for widget in self.findChildren(QListWidget):
            widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            widget.verticalScrollBar().setSingleStep(8)  # Smaller step size
        
        # Set scroll behavior for all table widgets
        for widget in self.findChildren(QTableWidget):
            widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            widget.horizontalScrollBar().setSingleStep(8)
            widget.verticalScrollBar().setSingleStep(8)
        
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
            "Click on the Help button to learn about this topic visualization module."
        )
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        help_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        header_layout.addWidget(help_label, 1)

        # Help button in the top right
        self.help_button = QPushButton()
        self.help_button.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.help_button.setToolTip("Learn about topic visualization tools")
        self.help_button.setFixedSize(32, 32)  # Make it a square button
        self.help_button.clicked.connect(self.show_help_dialog)

        # Add to header layout with no stretching
        header_layout.addWidget(self.help_button, 0, Qt.AlignTop | Qt.AlignRight)

        # Add header layout to main layout
        main_layout.addLayout(header_layout)
        
        # Create a splitter for controls and visualization
        self.main_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.main_splitter, 1)  # Make splitter expand
        
        # Controls container widget
        controls_container = QWidget()
        controls_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        controls_layout = QVBoxLayout(controls_container)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(WIDGET_SPACING)
        
        # Visualization controls
        controls_group = QGroupBox("Visualization Controls")
        controls_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        controls_inner_layout = QVBoxLayout(controls_group)
        controls_inner_layout.setSpacing(WIDGET_SPACING)
        controls_inner_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)

        self.chunk_info_label = QLabel()
        self.chunk_info_label.setStyleSheet(
            "background-color: #e8f4f8; padding: 10px; border-radius: 5px; color: #0066cc;"
        )
        self.chunk_info_label.setWordWrap(True)
        self.chunk_info_label.setVisible(False)  # Initially hidden
        
        # Visualization type selection
        viz_type_form = QFormLayout()
        viz_type_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        viz_type_form.setLabelAlignment(Qt.AlignRight)
        viz_type_form.setSpacing(WIDGET_SPACING)
        
        self.viz_type_combo = QComboBox()
        self.viz_type_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Add visualization types
        viz_types = self.visualizer.get_available_visualizations()
        for name, viz_type in viz_types.items():
            self.viz_type_combo.addItem(name, viz_type)
        
        self.viz_type_combo.currentIndexChanged.connect(self.update_parameter_options)
        viz_type_form.addRow("Visualization Type:", self.viz_type_combo)
        
        controls_inner_layout.addLayout(viz_type_form)
        
        # Parameters section - directly add to layout without scroll area
        self.params_group = QGroupBox("Parameters")
        self.params_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.params_layout = QVBoxLayout(self.params_group)
        self.params_layout.setSpacing(WIDGET_SPACING)
        self.params_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Add parameters group directly to controls layout
        controls_inner_layout.addWidget(self.params_group)
        
        # Button layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(WIDGET_SPACING)
        
        # Generate button
        self.generate_button = QPushButton("Generate Visualization")
        self.generate_button.setIcon(self.style().standardIcon(QStyle.SP_ToolBarHorizontalExtensionButton))
        self.generate_button.clicked.connect(self.generate_visualization)
        self.generate_button.setMinimumHeight(BUTTON_HEIGHT)
        self.generate_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        self.generate_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        buttons_layout.addWidget(self.generate_button)
        
        # Save button
        self.save_button = QPushButton("Save Visualization")
        self.save_button.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.save_button.clicked.connect(self.save_visualization)
        self.save_button.setEnabled(False)  # Disabled until a visualization is generated
        self.save_button.setMinimumHeight(BUTTON_HEIGHT)
        self.save_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        self.save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        buttons_layout.addWidget(self.save_button)
        
        controls_inner_layout.addLayout(buttons_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setVisible(False)  # Hide initially
        controls_inner_layout.addWidget(self.progress_bar)
        
        controls_layout.addWidget(controls_group)
        
        # Add controls container to splitter
        self.main_splitter.addWidget(controls_container)
        
        # Visualization container
        viz_container = QWidget()
        viz_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        viz_layout = QVBoxLayout(viz_container)
        viz_layout.setContentsMargins(0, 0, 0, 0)
        viz_layout.setSpacing(WIDGET_SPACING)
        
        # Visualization area
        self.viz_tab = QTabWidget()
        self.viz_tab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Configure tab widget for smoother appearance and navigation
        self.viz_tab.setUsesScrollButtons(True)  # Show scroll buttons for many tabs
        self.viz_tab.setElideMode(Qt.ElideRight)  # Elide text in tabs if needed
        self.viz_tab.setDocumentMode(True)  # More modern tab style
        
        viz_layout.addWidget(self.viz_tab, 1)  # Make tabs expand
        
        # Visualization plot tab
        self.viz_tab_plot = QWidget()
        self.viz_tab_plot_layout = QVBoxLayout(self.viz_tab_plot)
        self.viz_tab_plot_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        self.viz_tab_plot_layout.setSpacing(WIDGET_SPACING)
        self.viz_tab_plot_layout.insertWidget(0, self.chunk_info_label)
        
        # This layout will hold the canvas and toolbar
        self.viz_area = QVBoxLayout()
        self.viz_area.setSpacing(WIDGET_SPACING)
        self.viz_tab_plot_layout.addLayout(self.viz_area)
        
        self.viz_tab.addTab(self.viz_tab_plot, "Visualization")
        
        # New HTML tab for interactive visualizations like pyLDAvis
        self.viz_tab_html = QWidget()
        self.viz_tab_html_layout = QVBoxLayout(self.viz_tab_html)
        self.viz_tab_html_layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        self.viz_tab_html_layout.setSpacing(WIDGET_SPACING)
        
        # Add a web view with smooth scrolling to display HTML content
        self.web_view = SmoothWebEngineView()
        self.viz_tab_html_layout.addWidget(self.web_view)
        
        self.viz_tab.addTab(self.viz_tab_html, "Interactive View")
        
        # Hide the HTML tab initially
        self.viz_tab.setTabVisible(1, True)
        
        # Add visualization container to splitter
        self.main_splitter.addWidget(viz_container)
        
        # Set initial sizes (30% for controls, 70% for visualization)
        self.main_splitter.setSizes([300, 700])
        
        # Initialize parameter options
        self.update_parameter_options()
    
    def update_parameter_options(self):
        """Update parameter options based on the selected visualization type"""
        # Import required Qt widgets
        from PyQt5.QtWidgets import (QLabel, QComboBox, QSpinBox, QFormLayout, 
                                QListWidget, QAbstractItemView, QHBoxLayout)
        # Clear existing parameters
        while self.params_layout.count():
            item = self.params_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Clear nested layouts
                while item.layout().count():
                    nested_item = item.layout().takeAt(0)
                    if nested_item.widget():
                        nested_item.widget().deleteLater()
        
        # Create form layout for parameters
        params_form = QFormLayout()
        params_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        params_form.setLabelAlignment(Qt.AlignRight)
        params_form.setSpacing(WIDGET_SPACING)
        
        # Get current visualization type
        viz_type = self.viz_type_combo.currentData()
        
        if viz_type == 'wordcloud':
            # Language parameter
            self.language_combo = QComboBox()
            self.language_combo.addItems(["english", "norwegian"])
            self.language_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            params_form.addRow("Language:", self.language_combo)
            
            # Colormap parameter
            self.colormap_combo = QComboBox()
            self.colormap_combo.addItems(["viridis", "plasma", "inferno", "magma", "cividis", "Blues", "Greens", "Reds"])
            self.colormap_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            params_form.addRow("Color Scheme:", self.colormap_combo)
            
        elif viz_type == 'word_freq':
            # Top N words parameter
            self.top_n_spin = QSpinBox()
            self.top_n_spin.setRange(5, 100)
            self.top_n_spin.setValue(30)
            self.top_n_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            params_form.addRow("Number of Words:", self.top_n_spin)
            
            # Language parameter
            self.language_combo = QComboBox()
            self.language_combo.addItems(["english", "norwegian"])
            self.language_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            params_form.addRow("Language:", self.language_combo)
            
        elif viz_type == 'ngrams':
            # N parameter
            self.n_spin = QSpinBox()
            self.n_spin.setRange(2, 5)
            self.n_spin.setValue(2)
            self.n_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            params_form.addRow("N-gram Size:", self.n_spin)
            
            # Top N parameter
            self.top_n_spin = QSpinBox()
            self.top_n_spin.setRange(5, 100)
            self.top_n_spin.setValue(50)
            self.top_n_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            params_form.addRow("Number of N-grams:", self.top_n_spin)
            
            # Language parameter
            self.language_combo = QComboBox()
            self.language_combo.addItems(["english", "norwegian"])
            self.language_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            params_form.addRow("Language:", self.language_combo)
            
        elif viz_type == 'topic_distribution':
            # Provide a small hint instead of just saying no parameters needed
            info_label = QLabel("Creates a bar chart showing the distribution of documents across topics.")
            info_label.setWordWrap(True)
            info_label.setStyleSheet("font-style: italic; color: #666;")
            self.params_layout.addWidget(info_label)
            
        elif viz_type == 'topic_keywords':
            # Top N words parameter
            self.top_n_spin = QSpinBox()
            self.top_n_spin.setRange(5, 30)
            self.top_n_spin.setValue(10)
            self.top_n_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            params_form.addRow("Words per Topic:", self.top_n_spin)
            
            # Colormap parameter
            self.colormap_combo = QComboBox()
            self.colormap_combo.addItems(["viridis", "plasma", "inferno", "magma", "cividis", "Blues", "Greens", "Reds"])
            self.colormap_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            params_form.addRow("Color Scheme:", self.colormap_combo)
            
        elif viz_type == 'topic_heatmap':
            # Provide a small hint instead of just saying no parameters needed
            from PyQt5.QtWidgets import QHBoxLayout, QLabel
            info_label = QLabel("Creates a heatmap visualization showing topic distribution across documents.")
            info_label.setWordWrap(True)
            info_label.setStyleSheet("font-style: italic; color: #666;")
            self.params_layout.addWidget(info_label)
            
        elif viz_type == 'topic_highlighting':
            from PyQt5.QtWidgets import QHBoxLayout, QLabel
            # Add topic selection label
            topics_label = QLabel("Select topics to highlight:")
            topics_label.setWordWrap(True)
            self.params_layout.addWidget(topics_label)
            
            # Create a list with checkboxes for topic selection
            self.topic_list = QListWidget()
            self.topic_list.setSelectionMode(QListWidget.MultiSelection)
            self.topic_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.topic_list.setMinimumHeight(100)  # Reduced height to fit better without scrolling
            
            # Set pixel-based scrolling for smoother movement
            self.topic_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            self.topic_list.verticalScrollBar().setSingleStep(8)  # Smaller steps
            
            # Add color chip class for displaying topic colors
            from PyQt5.QtWidgets import QHBoxLayout, QLabel
            from PyQt5.QtGui import QColor
            from PyQt5.QtCore import QSize
            
            # Import for colormap
            import matplotlib.pyplot as plt
            import matplotlib.colors as mcolors
            
            # Populate with topics if available
            if hasattr(self, 'topics_words') and self.topics_words:
                # Get the colormap
                cmap_name = "hsv"  # Default colormap
                
                # Store selected topics as they're created
                self.colored_topics = []
                
                # Create a color for each topic
                topic_ids = sorted([tid for tid in self.topics_words.keys() if tid != -1])
                cmap = plt.get_cmap(cmap_name)
                
                # Function to create a colored topic item
                def create_topic_item(topic_id, color_hex, words):
                    # Create widget to hold the item content
                    item_widget = QWidget()
                    item_layout = QHBoxLayout(item_widget)
                    item_layout.setContentsMargins(2, 2, 2, 2)
                    item_layout.setSpacing(5)
                    
                    # Create color indicator
                    color_label = QLabel()
                    color_label.setFixedSize(QSize(16, 16))
                    color_label.setStyleSheet(f"background-color: {color_hex}; border: 1px solid #888;")
                    item_layout.addWidget(color_label)
                    
                    # Create text label
                    text = f"Topic {topic_id}: {words}"
                    text_label = QLabel(text)
                    item_layout.addWidget(text_label, 1)  # 1 = stretch factor
                    
                    # Create a wrapper list item
                    list_item = QListWidgetItem()
                    # Set size to accommodate the widget
                    list_item.setSizeHint(item_widget.sizeHint())
                    # Store the topic_id as data
                    list_item.setData(Qt.UserRole, topic_id)
                    
                    return list_item, item_widget
                
                # Add items to the list
                for i, topic_id in enumerate(topic_ids):
                    # Generate color
                    color = cmap(i / max(1, len(topic_ids) - 1))
                    color_hex = mcolors.rgb2hex(color)
                    
                    # Store the color-topic mapping
                    self.colored_topics.append((topic_id, color_hex))
                    
                    # Create preview of topic words
                    words = ", ".join([word for word, _ in self.topics_words[topic_id][:3]])
                    
                    # Create the item and its custom widget
                    item, widget = create_topic_item(topic_id, color_hex, words)
                    
                    # Add to list
                    self.topic_list.addItem(item)
                    self.topic_list.setItemWidget(item, widget)
                    
                    # Select by default
                    item.setSelected(True)
            
            self.params_layout.addWidget(self.topic_list)
            
            # Color scheme parameter
            self.colormap_combo = QComboBox()
            self.colormap_combo.addItems(["hsv", "rainbow", "jet", "tab10", "Set3", "Paired"])
            self.colormap_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.colormap_combo.currentIndexChanged.connect(self.update_topic_colors)
            colormap_form = QFormLayout()
            colormap_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
            colormap_form.addRow("Color Scheme:", self.colormap_combo)
            self.params_layout.addLayout(colormap_form)
            
            # Return early as we've already added widgets directly
            return            
        elif viz_type == 'pyldavis':
            # For pyLDAvis, check if an LDA model is available
            # More compact display using a single info label
            from ..ui.main_window import MainWindow
            main_window = self.window()
            
            # Prepare model info text
            if hasattr(main_window, 'topic_tab') and hasattr(main_window.topic_tab, 'topic_modeler'):
                model = main_window.topic_tab.topic_modeler.get_model()
                if model:
                    model_type = model.__class__.__name__
                    if "LDA" in model_type or "LatentDirichletAllocation" in model_type:
                        model_info = f"✓ LDA model detected: {model_type}"
                        color = "green"
                    else:
                        model_info = f"⚠️ Current model is not LDA. Using: {model_type}"
                        color = "orange"
                else:
                    model_info = "⚠️ No topic model available"
                    color = "red"
            else:
                model_info = "⚠️ Cannot access topic model"
                color = "red"
                
            # Combined info label with model status
            info_label = QLabel(f"This visualization requires an LDA topic model.\n{model_info}")
            info_label.setWordWrap(True)
            info_label.setStyleSheet(f"color: {color};")
            self.params_layout.addWidget(info_label)
            
            # MDS algorithm
            self.mds_combo = QComboBox()
            self.mds_combo.addItems(["tsne", "pcoa"])
            self.mds_combo.setToolTip("t-SNE often produces better visualizations, PCoA is faster")
            self.mds_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            mds_form = QFormLayout()
            mds_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
            mds_form.addRow("MDS Algorithm:", self.mds_combo)
            self.params_layout.addLayout(mds_form)
            
            # Additional information
            info = QLabel("The interactive visualization will appear in the 'Interactive View' tab")
            info.setStyleSheet("color: blue; font-style: italic;")
            info.setWordWrap(True)
            self.params_layout.addWidget(info)
            
            # Return early as we've already added widgets directly
            return

        elif viz_type == 'bertopic_interactive':
            # For BERTopic visualization, check if model is available
            from ..ui.main_window import MainWindow
            main_window = self.window()
            
            # Prepare model info text
            if hasattr(main_window, 'topic_tab') and hasattr(main_window.topic_tab, 'topic_modeler'):
                model = main_window.topic_tab.topic_modeler.get_model()
                if model:
                    model_type = model.__class__.__name__
                    if "BERTopic" in model_type or hasattr(model, 'visualize_topics'):
                        model_info = f"✓ BERTopic model detected: {model_type}"
                        color = "green"
                    else:
                        model_info = f"⚠️ Current model is not BERTopic. Using: {model_type}"
                        color = "orange"
                else:
                    model_info = "⚠️ No topic model available"
                    color = "red"
            else:
                model_info = "⚠️ Cannot access topic model"
                color = "red"
                
            # Combined info label with model status
            info_label = QLabel(f"This visualization requires a BERTopic model.\n{model_info}")
            info_label.setWordWrap(True)
            info_label.setStyleSheet(f"color: {color};")
            self.params_layout.addWidget(info_label)
            
            # Number of topics to visualize
            self.topics_count_spin = QSpinBox()
            self.topics_count_spin.setRange(5, 30)
            self.topics_count_spin.setValue(10)
            self.topics_count_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            topics_form = QFormLayout()
            topics_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
            topics_form.addRow("Number of Topics:", self.topics_count_spin)
            self.params_layout.addLayout(topics_form)
            
            # Additional information
            info = QLabel("The interactive visualization will appear in the 'Interactive View' tab")
            info.setStyleSheet("color: blue; font-style: italic;")
            info.setWordWrap(True)
            self.params_layout.addWidget(info)
            
            # Return early as we've already added widgets directly
            return        
        # Add form to params layout for visualization types that use the form
        self.params_layout.addLayout(params_form)
        
    def update_topic_colors(self):
        """Update the colors for topics based on selected colormap"""
        # Only process if we have the topic list and colored topics
        if not hasattr(self, 'topic_list') or not hasattr(self, 'colored_topics'):
            return
        
        # Import for colormap
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        
        # Get current colormap
        cmap_name = self.colormap_combo.currentText()
        cmap = plt.get_cmap(cmap_name)
        
        # Get topic ids (excluding -1)
        topic_ids = [t[0] for t in self.colored_topics]
        
        # Update colors for each topic
        for i, topic_id in enumerate(topic_ids):
            # Generate new color
            color = cmap(i / max(1, len(topic_ids) - 1))
            color_hex = mcolors.rgb2hex(color)
            
            # Update stored color
            self.colored_topics[i] = (topic_id, color_hex)
            
            # Find the item in the list
            for j in range(self.topic_list.count()):
                item = self.topic_list.item(j)
                if item.data(Qt.UserRole) == topic_id:
                    # Get the widget
                    widget = self.topic_list.itemWidget(item)
                    if widget:
                        # Update the color chip
                        color_label = widget.layout().itemAt(0).widget()
                        color_label.setStyleSheet(f"background-color: {color_hex}; border: 1px solid #888;")
                    break    
    def set_documents(self, documents):
        """Set the documents for visualization"""
        if not documents:
            return
        
        # Store as both documents and original_documents initially
        self.documents = documents
        self.original_documents = documents.copy()  # Make a copy to preserve the original

    def set_chunked_documents(self, chunked_documents):
        """Set the chunked documents used for topic modeling"""
        if not chunked_documents:
            return
        
        # If original_documents is empty, store the current documents there first
        if not self.original_documents and self.documents:
            self.original_documents = self.documents.copy()
        
        # Now update documents to the chunked version
        self.documents = chunked_documents    
        
    def set_topics(self, topics, topics_words, probs, topic_info):
        """Set the topics data for visualization"""
        self.topics = topics
        self.topics_words = topics_words
        self.probs = probs
        self.topic_info = topic_info
        
        # Update topic list if topic highlighting is selected
        if self.viz_type_combo.currentData() == 'topic_highlighting':
            self.update_parameter_options()
    
    def generate_visualization(self):
        """Generate the selected visualization"""
        # Check if data is available
        if not self.documents:
            QMessageBox.warning(
                self, "No Data", "No documents are available for visualization."
            )
            return

        # Get selected visualization type
        viz_type = self.viz_type_combo.currentData()

        # Check if topic data is required
        if viz_type in ['topic_distribution', 'topic_keywords', 'topic_heatmap', 'topic_highlighting'] and not self.topics:
            QMessageBox.warning(
                self, "No Topics", "No topic data is available for visualization."
            )
            return

        # Special handling for topic highlighting
        if viz_type == 'topic_highlighting':
            self.generate_topic_highlighting()
            return

        # Special handling for pyLDAvis
        if viz_type == 'pyldavis':
            self.generate_pyldavis()
            return

        # Special handling for BERTopic interactive visualization
        if viz_type == 'bertopic_interactive':
            self.generate_bertopic_visualization()
            return

        # --- Show chunking info if applicable ---
        if hasattr(self, "topics") and hasattr(self, "original_documents"):
            if len(self.topics) > len(self.original_documents):
                chunk_msg = (
                    f"Your document was automatically divided into {len(self.topics)} chunks "
                    "for better topic analysis. Each chunk may be assigned different topics."
                    "Topic Heatmap may not work optimally only one original document is uploaded."
                )
                if hasattr(self, "chunk_info_label"):
                    self.chunk_info_label.setText(chunk_msg)
                    self.chunk_info_label.setVisible(True)
            else:
                if hasattr(self, "chunk_info_label"):
                    self.chunk_info_label.setVisible(False)

        # Disable UI elements during generation
        self.generate_button.setEnabled(False)

        # Show progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        # Prepare parameters based on visualization type
        kwargs = {}

        if viz_type == 'wordcloud':
            kwargs['language'] = self.language_combo.currentText()
            kwargs['colormap'] = self.colormap_combo.currentText()

        elif viz_type == 'word_freq':
            kwargs['language'] = self.language_combo.currentText()
            kwargs['top_n'] = self.top_n_spin.value()

        elif viz_type == 'ngrams':
            kwargs['language'] = self.language_combo.currentText()
            kwargs['n'] = self.n_spin.value()
            kwargs['top_n'] = self.top_n_spin.value()

        elif viz_type == 'topic_keywords':
            kwargs['top_n'] = self.top_n_spin.value()
            kwargs['colormap'] = self.colormap_combo.currentText()

        # Set the data based on visualization type
        if viz_type in ['wordcloud', 'word_freq', 'ngrams']:
            data = self.documents

        elif viz_type == 'topic_distribution':
            # Create a topic count dictionary
            topic_counts = {}
            for topic in self.topics:
                if topic not in topic_counts:
                    topic_counts[topic] = 0
                topic_counts[topic] += 1
            data = topic_counts

        elif viz_type == 'topic_keywords':
            data = self.topics_words

        elif viz_type == 'topic_heatmap':
            import numpy as np

            if not self.topics or len(self.topics) < 1:
                QMessageBox.warning(
                    self, "Insufficient Data",
                    "Need at least one document with topic assignments for heatmap visualization."
                )
                return

            num_items = min(len(self.topics), len(self.documents))
            if num_items < 1:
                QMessageBox.warning(
                    self, "No Data",
                    "No documents with topic assignments available."
                )
                return

            # Get unique topics and create mapping
            unique_topics = sorted(set(self.topics[:num_items]))
            topic_to_index = {t: i for i, t in enumerate(unique_topics)}

            # Create matrix
            doc_topic_matrix = np.zeros((num_items, len(unique_topics)))

            # Document labels
            doc_labels = []
            for i in range(num_items):
                doc_text = self.documents[i].replace('\n', ' ')
                preview = doc_text[:20] + "..." if len(doc_text) > 20 else doc_text
                doc_labels.append(f"Doc {i+1}: {preview}")

            for i in range(num_items):
                topic = self.topics[i]
                if topic in topic_to_index:
                    if isinstance(self.probs, list) and i < len(self.probs):
                        if isinstance(self.probs[i], (list, tuple)) and self.probs[i]:
                            doc_topic_matrix[i, topic_to_index[topic]] = max(self.probs[i])
                        else:
                            doc_topic_matrix[i, topic_to_index[topic]] = 1.0
                    else:
                        doc_topic_matrix[i, topic_to_index[topic]] = 1.0

            topic_labels = [f"Topic {t}" for t in unique_topics]
            data = doc_topic_matrix
            kwargs['topic_labels'] = topic_labels
            kwargs['document_labels'] = doc_labels

        # Create and configure worker
        worker = self.visualizer.generate_visualization(viz_type, data, **kwargs)

        # Connect worker signals
        worker.progress_updated.connect(self.update_progress)
        worker.visualization_completed.connect(self.on_visualization_completed)
        worker.error_occurred.connect(self.on_visualization_error)

        # Forward the progress signal to the main window
        worker.progress_updated.connect(self.progress_updated)

        # Update UI
        self.progress_updated.emit(5, f"Generating {self.viz_type_combo.currentText()} visualization...")

    def generate_pyldavis(self):
        """Generate pyLDAvis visualization for LDA topic model"""
        # Get the topic model from the main window
        from ..ui.main_window import MainWindow
        main_window = self.window()
        if not hasattr(main_window, 'topic_tab') or not hasattr(main_window.topic_tab, 'topic_modeler'):
            QMessageBox.warning(
                self, "No Topic Model", "No topic model available for visualization."
            )
            return
            
        topic_model = main_window.topic_tab.topic_modeler.get_model()
        if not topic_model:
            QMessageBox.warning(
                self, "No Topic Model", "No topic model available for visualization."
            )
            return
        
        # Check if it's an LDA model
        model_type = topic_model.__class__.__name__
        if not ("LDA" in model_type or "LatentDirichletAllocation" in model_type):
            # Ask for confirmation if not LDA
            confirmation = QMessageBox.question(
                self, "Non-LDA Model", 
                f"pyLDAvis is designed for LDA models, but your current model is {model_type}.\n\n"
                "This visualization may not work correctly or might produce misleading results.\n\n"
                "Do you want to continue anyway?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if confirmation == QMessageBox.No:
                return
        
        # Disable UI elements during generation
        self.generate_button.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        # Update status
        self.progress_updated.emit(10, "Preparing LDA visualization...")
        
        try:
            # For LDATopicModel wrapper
            if hasattr(topic_model, 'lda_model') and hasattr(topic_model, 'vectorizer'):
                lda_model = topic_model.lda_model
                vectorizer = topic_model.vectorizer
                
                # Get the document-term matrix
                dtm = vectorizer.transform(self.documents)
                
                # Prepare data for pyLDAvis
                data = {
                    'model': lda_model,
                    'dtm': dtm,
                    'vectorizer': vectorizer
                }
                
                # Get MDS algorithm
                kwargs = {'mds': self.mds_combo.currentText()}
                
                # Create and configure worker
                worker = self.visualizer.generate_visualization('pyldavis', data, **kwargs)
                
                # Connect worker signals
                worker.progress_updated.connect(self.update_progress)
                worker.visualization_completed.connect(self.on_pyldavis_completed)
                worker.error_occurred.connect(self.on_visualization_error)
                
                # Forward the progress signal to the main window
                worker.progress_updated.connect(self.progress_updated)
                
                # Update UI
                self.progress_updated.emit(15, "Generating interactive LDA visualization...")
                
            else:
                # For other models or if we can't access the LDA model directly
                QMessageBox.warning(
                    self, "Incompatible Model", 
                    f"Cannot access the LDA model or vectorizer directly from the {model_type} model. "
                    "pyLDAvis visualization requires direct access to these components."
                )
                self.generate_button.setEnabled(True)
                self.progress_bar.setVisible(False)
                
        except Exception as e:
            logger.error(f"Error preparing pyLDAvis visualization: {str(e)}", exc_info=True)
            QMessageBox.warning(
                self, "Visualization Error", f"Error preparing pyLDAvis visualization: {str(e)}"
            )
            self.generate_button.setEnabled(True)
            self.progress_bar.setVisible(False)   
            
    def generate_bertopic_visualization(self):
        """Generate BERTopic interactive visualization"""
        # Get the topic model from the main window
        from ..ui.main_window import MainWindow
        main_window = self.window()
        if not hasattr(main_window, 'topic_tab') or not hasattr(main_window.topic_tab, 'topic_modeler'):
            QMessageBox.warning(
                self, "No Topic Model", "No topic model available for visualization."
            )
            return
            
        topic_model = main_window.topic_tab.topic_modeler.get_model()
        if not topic_model:
            QMessageBox.warning(
                self, "No Topic Model", "No topic model available for visualization."
            )
            return
        
        # Check if it's a BERTopic model
        if not ("BERTopic" in topic_model.__class__.__name__ or hasattr(topic_model, 'visualize_topics')):
            # Ask for confirmation if not BERTopic
            confirmation = QMessageBox.question(
                self, "Non-BERTopic Model", 
                f"This visualization is designed for BERTopic models, but your current model is {topic_model.__class__.__name__}.\n\n"
                "This visualization may not work correctly or might produce an error.\n\n"
                "Do you want to continue anyway?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if confirmation == QMessageBox.No:
                return
        
        # Disable UI elements during generation
        self.generate_button.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        # Get parameters
        kwargs = {
            'topics': None,  # Use top N topics
            'width': 1000,
            'height': 800, 
            'seed': 42
        }
        
        # If we have topic count spinner
        if hasattr(self, 'topics_count_spin'):
            # Get top N topics
            try:
                topic_info = topic_model.get_topic_info()
                # Filter out -1 (outlier topic)
                filtered_info = topic_info[topic_info['Topic'] != -1]
                # Get top N topics by Count
                n_topics = self.topics_count_spin.value()
                top_topics = filtered_info.nlargest(n_topics, 'Count')['Topic'].tolist()
                kwargs['topics'] = top_topics
            except Exception as e:
                print(f"Error getting top topics: {str(e)}")
        
        # Create and configure worker
        worker = self.visualizer.generate_visualization('bertopic_interactive', topic_model, **kwargs)
        
        # Connect worker signals
        worker.progress_updated.connect(self.update_progress)
        worker.visualization_completed.connect(self.on_visualization_completed)
        worker.error_occurred.connect(self.on_visualization_error)
        
        # Forward the progress signal to the main window
        worker.progress_updated.connect(self.progress_updated)
        
        # Update UI
        self.progress_updated.emit(5, "Generating BERTopic visualization...")
                        
    def generate_topic_highlighting(self):
        """Generate topic highlighting visualization"""
        # Get the topic model from the main window
        from ..ui.main_window import MainWindow
        from ..ui.topic_tab import TopicTab
        main_window = self.window()
        if not hasattr(main_window, 'topic_tab') or not hasattr(main_window.topic_tab, 'topic_modeler'):
            QMessageBox.warning(
                self, "No Topic Model", "No topic model available for highlighting."
            )
            return
            
        topic_model = main_window.topic_tab.topic_modeler.get_model()
        if not topic_model:
            QMessageBox.warning(
                self, "No Topic Model", "No topic model available for highlighting."
            )
            return
        
        # Detect model type and warn if not BERTopic
        model_type = topic_model.__class__.__name__
        if "BERTopic" not in model_type and not (hasattr(topic_model, 'highlight_document') or hasattr(topic_model, 'transform')):
            QMessageBox.warning(
                self, "Unsupported Model Type", 
                f"Topic highlighting works best with BERTopic models. Current model ({model_type}) may produce limited results."
            )
        
        # Get selected topics
        selected_topics = []
        for i in range(self.topic_list.count()):
            item = self.topic_list.item(i)
            if item.isSelected():
                topic_id = item.data(Qt.UserRole)
                selected_topics.append(topic_id)
        
        if not selected_topics:
            QMessageBox.warning(
                self, "No Topics Selected", "Please select at least one topic to highlight."
            )
            return
        
        # Get color scheme
        colormap = self.colormap_combo.currentText()
        
        # Show progress
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        # Update status
        self.progress_updated.emit(10, "Highlighting topics in documents...")
        
        try:
            # Generate colors
            import matplotlib.pyplot as plt
            import matplotlib.colors as mcolors
            
            cmap = plt.get_cmap(colormap)
            colors = [mcolors.rgb2hex(cmap(i / len(selected_topics))) for i in range(len(selected_topics))]
            
            # Highlight topics in documents
            highlighted_docs = self.visualizer.highlight_topics_in_documents(
                self.documents, topic_model, selected_topics, colors
            )
            
            self.progress_updated.emit(50, "Creating document viewer...")
            
            # Create a new window to display the highlighted documents
            self.show_highlighted_documents(highlighted_docs)
            
            self.progress_updated.emit(100, "Topic highlighting complete")
            self.progress_bar.setVisible(False)
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            logger.error(f"Error highlighting topics: {str(e)}", exc_info=True)
            QMessageBox.warning(
                self, "Highlighting Error", f"Error highlighting topics: {str(e)}"
            )
    
    def show_highlighted_documents(self, highlighted_docs):
        """Show highlighted documents in a separate window with legend"""
        from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTextBrowser, 
                                QPushButton, QComboBox, QHBoxLayout, QFormLayout, QLabel, QGridLayout, QFrame)
        from PyQt5.QtGui import QColor
        
        # Import matplotlib modules
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Topic Highlighting")
        dialog.resize(800, 600)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Create document selector
        selector_form = QFormLayout()
        selector_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        doc_selector = QComboBox()
        doc_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Add "All Documents" option first
        doc_selector.addItem("All Documents")
        
        # Then add individual documents
        for i in range(len(highlighted_docs)):
            doc_selector.addItem(f"Document {i+1}")
        
        selector_form.addRow("Select Document:", doc_selector)
        layout.addLayout(selector_form)
        
        # Create legend section
        legend_layout = QVBoxLayout()
        
        # Get selected topic IDs and their colors
        selected_topics = []
        topic_colors = {}
        
        for i in range(self.topic_list.count()):
            item = self.topic_list.item(i)
            if item.isSelected():
                topic_id = item.data(Qt.UserRole)
                selected_topics.append(topic_id)
        
        # Get the colormap
        cmap = plt.get_cmap(self.colormap_combo.currentText())
        
        # Generate colors for each selected topic
        for i, topic_id in enumerate(selected_topics):
            color = cmap(i / max(1, len(selected_topics)))
            # Convert matplotlib color to hex
            hex_color = mcolors.rgb2hex(color)
            topic_colors[topic_id] = hex_color
        
        # Create legend title
        legend_title = QLabel("<b>Topic Legend:</b>")
        legend_layout.addWidget(legend_title)
        
        # Create legend grid layout
        legend_grid = QGridLayout()
        legend_grid.setSpacing(10)
        
        # Get words for each topic if available
        topic_labels = {}
        
        # Get topic model from the main window
        from ..ui.main_window import MainWindow
        main_window = self.window()
        topic_words = None
        
        if hasattr(main_window, 'topic_tab') and hasattr(main_window.topic_tab, 'topic_modeler'):
            topic_model = main_window.topic_tab.topic_modeler.get_model()
            if topic_model:
                try:
                    topic_words = topic_model.get_topics()
                except:
                    pass
        
        # Create color samples and labels for each topic
        col = 0
        for i, topic_id in enumerate(selected_topics):
            # Create color sample
            color_sample = QLabel()
            color_sample.setStyleSheet(f"background-color: {topic_colors[topic_id]}; border: 1px solid #888;")
            color_sample.setFixedSize(16, 16)
            
            # Create topic label with top words if available
            if topic_words and topic_id in topic_words:
                # Get top 3 words
                top_words = [word for word, _ in topic_words[topic_id][:3]]
                topic_text = f"Topic {topic_id}: {', '.join(top_words)}"
            else:
                topic_text = f"Topic {topic_id}"
                
            topic_label = QLabel(topic_text)
            
            # Add to grid - 2 topics per row
            row = i // 2
            col = (i % 2) * 2  # 0 or 2 for alternating columns
            
            legend_grid.addWidget(color_sample, row, col)
            legend_grid.addWidget(topic_label, row, col+1)
        
        # Add grid to legend layout
        legend_layout.addLayout(legend_grid)
        layout.addLayout(legend_layout)
        
        # Add horizontal separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Create text browser to display HTML
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(False)
        text_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Configure text browser for smoother scrolling
        text_browser.verticalScrollBar().setSingleStep(10)  # Smaller step size
        
        # Function to combine all documents as one continuous flow
        def combine_documents(docs):
            # Simple wrapper for the entire content
            combined_html = '<div style="font-family: Arial, sans-serif; line-height: 1.6;">'
            
            # Add each document with minimal separation
            for i, doc in enumerate(docs):
                # Add a subtle document separator
                if i > 0:
                    combined_html += '<hr style="border-top: 1px dotted #ccc; margin: 10px 0;">'
                
                # Add a small document indicator
                combined_html += f'<div style="color: #666; font-size: 0.9em; margin: 5px 0; padding: 2px 5px; border-left: 3px solid #ddd;">Document {i+1}</div>'
                
                # Extract the document content from the HTML
                if doc.strip().startswith('<div') and doc.strip().endswith('</div>'):
                    # If it has a div wrapper, extract the content
                    content = doc.strip()
                    # Remove the outer div wrapper if present to avoid nesting
                    if content.startswith('<div style="font-family: Arial, sans-serif; line-height: 1.6;">') and content.endswith('</div>'):
                        content = content[content.find('>')+1:content.rfind('</div>')]
                    combined_html += content
                else:
                    # Otherwise, add directly
                    combined_html += doc
            
            combined_html += '</div>'
            return combined_html
        
        # Prepare the combined document
        combined_doc = combine_documents(highlighted_docs)
        
        # Show the combined document by default
        text_browser.setHtml(combined_doc)
        
        layout.addWidget(text_browser)
        
        # Create close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        close_button.setMinimumHeight(BUTTON_HEIGHT)
        close_button.setMinimumWidth(BUTTON_MIN_WIDTH)
        layout.addWidget(close_button, 0, Qt.AlignRight)
        
        # Connect document selector
        def on_selection_changed(idx):
            text_browser.verticalScrollBar().setValue(0)  # Scroll to top
            
            if idx == 0:  # "All Documents" option
                text_browser.setHtml(combined_doc)
            else:
                doc_idx = idx - 1  # Adjust for the "All Documents" entry
                if 0 <= doc_idx < len(highlighted_docs):
                    text_browser.setHtml(highlighted_docs[doc_idx])
        
        doc_selector.currentIndexChanged.connect(on_selection_changed)
        
        # Show dialog
        dialog.exec_()   
          
    @pyqtSlot(int, str)
    def update_progress(self, progress, message):
        """Update the progress bar and message"""
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(f"{progress}% - {message}")
        
    @pyqtSlot(object)
    def on_pyldavis_completed(self, result):
        """Handle completed pyLDAvis visualization"""
        # Unpack the result
        fig, html_string = result
        
        # Store the HTML content for later saving
        self.current_html = html_string
        
        # Re-enable UI elements
        self.generate_button.setEnabled(True)
        self.save_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Store the current visualization
        self.current_viz = fig
        
        # Clear the existing visualization area
        while self.viz_area.count():
            item = self.viz_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create the canvas for the figure
        canvas = MatplotlibCanvas(fig)
        self.current_canvas = canvas
        
        # Create the toolbar for the canvas with smoother behavior
        toolbar = SmoothNavigationToolbar(canvas, self)
        
        # Add the toolbar and canvas to the layout
        self.viz_area.addWidget(toolbar)
        self.viz_area.addWidget(canvas)
        
        # If we have HTML for the interactive visualization
        if html_string:
            # Load the HTML into the web view
            self.web_view.setHtml(html_string)
            
            # Make the HTML tab visible
            self.viz_tab.setTabVisible(1, True)
            
            # Switch to the HTML tab
            self.viz_tab.setCurrentIndex(1)
        else:
            # Hide the HTML tab if no HTML content
            self.viz_tab.setTabVisible(1, False)
            
            # Show message
            QMessageBox.information(
                self, "Static Visualization Only", 
                "Only a static preview is available. The interactive visualization could not be generated."
            )  
                  
    @pyqtSlot(object)
    def on_visualization_completed(self, result):
        """Handle completed visualization"""
        # Check if we have a tuple result (for HTML content)
        if isinstance(result, tuple) and len(result) == 2:
            fig, html_string = result
            if html_string:
                # Use the pyLDAvis handler
                self.on_pyldavis_completed(result)
                return
        else:
            fig = result
        
        # Re-enable UI elements
        self.generate_button.setEnabled(True)
        self.save_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Store the current visualization
        self.current_viz = fig
        
        # Clear the existing visualization area
        while self.viz_area.count():
            item = self.viz_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create the canvas for the figure
        canvas = MatplotlibCanvas(fig)
        self.current_canvas = canvas
        
        # Create the toolbar for the canvas with smoother behavior
        toolbar = SmoothNavigationToolbar(canvas, self)
        
        # Add the toolbar and canvas to the layout
        self.viz_area.addWidget(toolbar)
        self.viz_area.addWidget(canvas)
        
        # Hide the HTML tab for regular visualizations
        self.viz_tab.setTabVisible(1, False)
        
        # Show the plot tab
        self.viz_tab.setCurrentIndex(0)   
     
    @pyqtSlot(str)
    def on_visualization_error(self, error_message):
        """Handle visualization errors"""
        # Re-enable UI elements
        self.generate_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Show error message
        QMessageBox.warning(
            self, "Visualization Error", f"Error generating visualization: {error_message}"
        )
        
        # Update progress in main window
        self.progress_updated.emit(0, "Visualization failed")
    
    def save_visualization(self):
        """Save the current visualization to a file"""
        if not self.current_viz:
            return
        
        # Check if we have an HTML visualization (pyLDAvis)
        is_html_viz = False
        if hasattr(self, 'web_view') and self.viz_tab.isTabVisible(1):
            is_html_viz = True
        
        # Use different file dialog options based on visualization type
        if is_html_viz:
            file_path, selected_filter = QFileDialog.getSaveFileName(
                self, "Save Interactive Visualization", "", 
                "HTML File (*.html);;All Files (*.*)"
            )
        else:
            file_path, selected_filter = QFileDialog.getSaveFileName(
                self, "Save Visualization", "", 
                "PNG Image (*.png);;JPEG Image (*.jpg);;PDF Document (*.pdf);;SVG Image (*.svg);;All Files (*.*)"
            )
        
        if not file_path:
            return
        
        try:
            # Save based on visualization type
            if is_html_viz:
                # For pyLDAvis visualizations, we should have the HTML content stored
                if hasattr(self, 'current_html') and self.current_html:
                    # Make sure file path has .html extension
                    if not file_path.lower().endswith('.html'):
                        file_path += '.html'
                    
                    # Save HTML content to file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(self.current_html)
                    
                    # Show success message
                    QMessageBox.information(
                        self, "Save Complete", f"Interactive visualization saved to {file_path}"
                    )
                else:
                    # Fallback method using the web view's current content
                    from PyQt5.QtCore import QUrl
                    
                    if file_path.lower().endswith('.html'):
                        self.progress_bar.setVisible(True)
                        self.progress_bar.setValue(10)
                        self.progress_updated.emit(10, "Saving HTML visualization...")
                        
                        # Use callback mechanism to save HTML
                        self.html_save_path = file_path  # Store the path for the callback
                        
                        # Get HTML content from page
                        self.web_view.page().toHtml(self._handle_html_for_save)
                    else:
                        QMessageBox.warning(
                            self, "Invalid Extension", "HTML visualizations should be saved with .html extension"
                        )
            else:
                # Save the matplotlib visualization with high quality
                self.current_viz.savefig(file_path, dpi=300, bbox_inches='tight')
                
                # Show success message
                QMessageBox.information(
                    self, "Save Complete", f"Visualization saved to {file_path}"
                )
        except Exception as e:
            logger.error(f"Error saving visualization: {str(e)}")
            QMessageBox.warning(
                self, "Save Error", f"Failed to save visualization: {str(e)}"
            )

    def _handle_html_for_save(self, html_content):
        """Callback handler for saving HTML from web view"""
        try:
            # Save HTML to file
            with open(self.html_save_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.progress_bar.setValue(100)
            self.progress_bar.setVisible(False)
            
            # Show success message
            QMessageBox.information(
                self, "Save Complete", f"Interactive visualization saved to {self.html_save_path}"
            )
        except Exception as e:
            self.progress_bar.setVisible(False)
            logger.error(f"Error saving HTML visualization: {str(e)}")
            QMessageBox.warning(
                self, "Save Error", f"Failed to save HTML visualization: {str(e)}"
            )
            
    def show_help_dialog(self):
        """Show help dialog with information about topic visualization"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QTextBrowser, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Topic Visualization Help")
        dialog.setMinimumSize(1000, 600)  # Larger dialog size for readability
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(WIDGET_SPACING)
        layout.setContentsMargins(LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN)
        
        # Create tab widget for different help sections
        tabs = QTabWidget()
        tabs.setDocumentMode(True)  # More modern tab appearance
        layout.addWidget(tabs)
        
        # Overview tab
        overview_tab = QTextBrowser()
        overview_tab.setOpenExternalLinks(True)
        overview_tab.setHtml("""
        <h2>Visualization Module Overview</h2>
        <p>This module allows you to create interactive visualizations for exploring your text data and topic models.</p>
        
        <h3>Basic Usage</h3>
        <ol>
            <li>Select a visualization type from the dropdown menu</li>
            <li>Configure the visualization parameters (if applicable)</li>
            <li>Click "Generate Visualization" to create the visualization</li>
            <li>Use the toolbar to zoom, pan, or save the visualization</li>
            <li>For interactive visualizations, use the "Interactive View" tab</li>
        </ol>
            
        <h3>Available Visualization Types</h3>
        <ul>
            <li><strong>Word Cloud</strong> - Visualize the most frequent words in your documents</li>
            <li><strong>Word Frequency</strong> - Bar chart of the most frequent words</li>
            <li><strong>N-grams</strong> - Bar chart of the most frequent phrases</li>
            <li><strong>Topic Distribution</strong> - Bar chart showing document counts per topic</li>
            <li><strong>Topic Keywords</strong> - Visualize the most important words for each topic</li>
            <li><strong>Topic Heatmap</strong> - Heat map showing topic distribution across documents</li>
            <li><strong>Topic Highlighting</strong> - View topics highlighted in the original texts</li>
            <li><strong>Interactive LDA</strong> - Interactive visualization of LDA topic models (pyLDAvis)</li>
        </ul>
        
        <p>These visualizations make it easier to understand your topic model results, identify patterns in your data, and 
        communicate your findings to others.</p>
        """)
        tabs.addTab(overview_tab, "Overview")
        
        # Word-based visualizations tab
        word_tab = QTextBrowser()
        word_tab.setHtml("""
        <h2>Text and Word Visualizations</h2>
        
        <h3>Word Cloud</h3>
        <p>A word cloud visualizes word frequency in your documents where the size of each word corresponds to its frequency.</p>
        
        <h4>Parameters</h4>
        <ul>
            <li><strong>Language</strong> - Select the language for better stopword removal</li>
            <li><strong>Color Scheme</strong> - Choose a color palette for the word cloud</li>
        </ul>
        
        <p>Word clouds are excellent for presentations and getting a quick visual overview of key terms in your corpus.</p>
        
        <h3>Word Frequency</h3>
        <p>A word frequency chart shows the most common words in your documents as a bar chart, making it easy to 
        compare exact frequencies.</p>
        
        <h4>Parameters</h4>
        <ul>
            <li><strong>Number of Words</strong> - How many top words to display</li>
            <li><strong>Language</strong> - Select the language for stopword removal</li>
        </ul>
        
        <p>Word frequency charts are more precise than word clouds and better for detailed analysis.</p>
        
        <h3>N-grams Analysis</h3>
        <p>An n-gram analysis shows the most common phrases (sequences of words) in your documents.</p>
        
        <h4>Parameters</h4>
        <ul>
            <li><strong>N-gram Size</strong> - How many words in each phrase (2=bigrams, 3=trigrams, etc.)</li>
            <li><strong>Number of N-grams</strong> - How many top phrases to display</li>
            <li><strong>Language</strong> - Select the language for appropriate preprocessing</li>
        </ul>
        
        <p>N-gram analysis helps identify common phrases and expressions that single-word analysis might miss.</p>
        
        <div style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <p><strong>Tip:</strong> When analyzing technical or domain-specific text, consider examining both 
            single words and multi-word phrases (n-grams) to capture important terminology that may consist 
            of multiple words.</p>
        </div>
        """)
        tabs.addTab(word_tab, "Word Visualizations")
        
        # Topic visualizations tab
        topic_tab = QTextBrowser()
        topic_tab.setHtml("""
        <h2>Topic Model Visualizations</h2>
        
        <h3>Topic Distribution</h3>
        <p>Shows how documents are distributed across topics, helping you understand which topics are most common in your corpus.</p>
        
        <p>This visualization doesn't require additional parameters. It creates a bar chart where:</p>
        <ul>
            <li>The x-axis shows topic IDs</li>
            <li>The y-axis shows the number of documents assigned to each topic</li>
        </ul>
        
        <h3>Topic Keywords</h3>
        <p>Visualizes the most representative words for each topic, helping you understand what each topic represents.</p>
        
        <h4>Parameters</h4>
        <ul>
            <li><strong>Words per Topic</strong> - How many top words to display for each topic</li>
            <li><strong>Color Scheme</strong> - Choose a color palette for the visualization</li>
        </ul>
        
        <p>This visualization creates a grid of word clouds or bar charts, with one panel per topic, making it easy to compare different topics.</p>
        
        <h3>Topic Heatmap</h3>
        <p>Creates a heatmap showing the distribution of topics across documents, where color intensity represents topic presence.</p>
        
        <p>This visualization doesn't require additional parameters. In the heatmap:</p>
        <ul>
            <li>Rows represent documents</li>
            <li>Columns represent topics</li>
            <li>Color intensity shows the strength of each topic in each document</li>
        </ul>
        
        <p>The heatmap helps identify patterns in topic distribution and documents with similar topic profiles.</p>
        
        <div style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <p><strong>Note:</strong> Topic visualizations require a trained topic model. You must first extract topics 
            using the Topic Tab before these visualizations become available.</p>
        </div>
        """)
        tabs.addTab(topic_tab, "Topic Visualizations")
        
        # Advanced visualizations tab
        advanced_tab = QTextBrowser()
        advanced_tab.setHtml("""
        <h2>Advanced Visualizations</h2>
        
        <h3>Topic Highlighting</h3>
        <p>This visualization highlights topics directly in your original text documents, making it easy to see where and how 
        topics appear in context.</p>
        
        <h4>Parameters</h4>
        <ul>
            <li><strong>Select topics to highlight</strong> - Choose which topics to include in the highlighting</li>
            <li><strong>Color Scheme</strong> - Choose a color palette for differentiating topics</li>
        </ul>
        
        <p>The visualization creates a separate window showing your documents with different topics highlighted in different colors. 
        You can navigate between documents using the dropdown menu.</p>
        
        <p>Topic highlighting is invaluable for validating your topic model and understanding how topics manifest in the actual text.</p>
        
        <h3>Interactive LDA Visualization (pyLDAvis)</h3>
        <p>Creates an interactive visualization of an LDA topic model, allowing deep exploration of topics and term relationships.</p>
        
        <h4>Parameters</h4>
        <ul>
            <li><strong>MDS Algorithm</strong> - Choose between t-SNE (better quality but slower) and PCoA (faster)</li>
        </ul>
        
        <p>The pyLDAvis visualization appears in the "Interactive View" tab and offers several interactive features:</p>
        <ul>
            <li>Topic bubbles positioned in a 2D space based on their similarity</li>
            <li>Term bars showing the most relevant terms for selected topics</li>
            <li>Interactive λ parameter to adjust term relevance calculation</li>
            <li>Topic selection to see topic-specific term distributions</li>
        </ul>
        
        <p>This visualization is specifically designed for LDA topic models and works best with models created using the 
        "LDA" method in the Topic Tab.</p>
        
        <div style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <p><strong>Important:</strong> The pyLDAvis visualization requires an LDA topic model. It may not work 
            correctly with other model types like BERTopic or NMF. You'll receive a warning if you try to use it with 
            an incompatible model.</p>
        </div>
        """)
        tabs.addTab(advanced_tab, "Advanced Visualizations")
        
        # Saving tab
        saving_tab = QTextBrowser()
        saving_tab.setHtml("""
        <h2>Saving and Exporting Visualizations</h2>
        
        <p>All visualizations can be saved for use in reports, presentations, or further analysis.</p>
        
        <h3>Saving Static Visualizations</h3>
        <p>For standard visualizations (word clouds, bar charts, heatmaps, etc.):</p>
        <ol>
            <li>Generate the visualization</li>
            <li>Click the "Save Visualization" button</li>
            <li>Choose a file format:
                <ul>
                    <li><strong>PNG</strong> - Good for presentations and web use</li>
                    <li><strong>JPEG</strong> - Alternative format, generally larger file size</li>
                    <li><strong>PDF</strong> - Vector format, good for printing and publications</li>
                    <li><strong>SVG</strong> - Vector format, excellent for further editing</li>
                </ul>
            </li>
            <li>Choose a save location and filename</li>
        </ol>
        
        <p>You can also use the toolbar below the visualization to adjust the view before saving:</p>
        <ul>
            <li>Pan and zoom to focus on specific areas</li>
            <li>Adjust the layout</li>
            <li>Save the current view directly from the toolbar</li>
        </ul>
        
        <h3>Saving Interactive Visualizations</h3>
        <p>For interactive visualizations (like pyLDAvis):</p>
        <ol>
            <li>Generate the visualization</li>
            <li>Switch to the "Interactive View" tab</li>
            <li>Click the "Save Visualization" button</li>
            <li>Choose HTML format</li>
            <li>Select a save location and filename</li>
        </ol>
        
        <p>The saved HTML file can be opened in any web browser and contains the complete interactive visualization. This is 
        ideal for sharing with others who don't have the application.</p>
        
        <div style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <p><strong>Tip:</strong> For academic publications, save visualizations as PDF or SVG. For web sharing 
            or presentations, use PNG format. For interactive visualizations that you want to share, save as HTML.</p>
        </div>
        """)
        tabs.addTab(saving_tab, "Saving & Exporting")
        
        # Tips tab
        tips_tab = QTextBrowser()
        tips_tab.setHtml("""
        <h2>Tips for Effective Visualization</h2>
        
        <h3>Choosing the Right Visualization</h3>
        <ul>
            <li><strong>For presenting key themes:</strong> Word clouds or topic keywords visualization</li>
            <li><strong>For analyzing topic distribution:</strong> Topic distribution bar chart or heatmap</li>
            <li><strong>For validating topic model quality:</strong> Topic highlighting in original documents</li>
            <li><strong>For in-depth LDA model exploration:</strong> Interactive LDA visualization</li>
            <li><strong>For linguistic analysis:</strong> N-grams visualization</li>
        </ul>
        
        <h3>Improving Visualization Quality</h3>
        <ul>
            <li><strong>Filter unnecessary topics:</strong> Consider excluding the outlier topic (-1) from visualizations</li>
            <li><strong>Choose appropriate color schemes:</strong> Use contrasting colors for better readability</li>
            <li><strong>Adjust parameters:</strong> Experiment with different parameter settings to highlight key patterns</li>
            <li><strong>Focus on meaningful data:</strong> Sometimes less is more - visualize fewer topics or words if it makes patterns clearer</li>
        </ul>
        
        <h3>Interpreting Visualizations</h3>
        <ul>
            <li><strong>Look for patterns:</strong> Identify clusters of related topics or terms</li>
            <li><strong>Check for balance:</strong> Is one topic dominating? This might indicate a need to adjust your topic model</li>
            <li><strong>Validate with original text:</strong> Use topic highlighting to confirm that topics make sense in context</li>
            <li><strong>Compare different views:</strong> Use multiple visualization types to get a comprehensive understanding</li>
        </ul>
        
        <h3>For Presentations</h3>
        <ul>
            <li><strong>Keep it simple:</strong> Word clouds and simple bar charts are more accessible to non-technical audiences</li>
            <li><strong>Tell a story:</strong> Organize visualizations to support a narrative about your data</li>
            <li><strong>Use consistent colors:</strong> Maintain the same color scheme across related visualizations</li>
            <li><strong>Include examples:</strong> Topic highlighting screenshots provide concrete examples of abstract topics</li>
        </ul>
        
        <div style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <p><strong>Remember:</strong> The goal of visualization is insight, not just pretty pictures. Choose visualizations 
            that best reveal the patterns and relationships in your data, and customize them to highlight your key findings.</p>
        </div>
        """)
        tabs.addTab(tips_tab, "Visualization Tips")
        
        # Add scrolling tip tab
        scrolling_tab = QTextBrowser()
        scrolling_tab.setHtml("""
        <h2>Navigation & Interaction Tips</h2>
        
        <h3>Smooth Scrolling</h3>
        <p>This visualization module has been optimized for smooth scrolling and navigation. Here are some tips:</p>
        
        <h4>Mouse Wheel Control</h4>
        <ul>
            <li><strong>Normal scrolling:</strong> Use the mouse wheel to scroll up and down smoothly</li>
            <li><strong>Zooming:</strong> Hold Ctrl while using the mouse wheel to zoom in and out of visualizations</li>
        </ul>
        
        <h4>Keyboard Navigation</h4>
        <ul>
            <li><strong>Arrow keys:</strong> Use arrow keys to pan around visualizations</li>
            <li><strong>+/- keys:</strong> Zoom in and out</li>
            <li><strong>Home:</strong> Reset to original view</li>
        </ul>
        
        <h4>Interactive Features</h4>
        <ul>
            <li><strong>Panning:</strong> Click and drag to move around larger visualizations</li>
            <li><strong>Selection:</strong> Some visualizations allow you to click on elements for more information</li>
            <li><strong>Toolbar:</strong> Use the toolbar below visualizations for additional controls:
                <ul>
                    <li>⬅️ Home: Reset to initial view</li>
                    <li>⬅️ Pan: Enter pan mode (click and drag to move)</li>
                    <li>⬅️ Zoom: Enter zoom mode (click or drag to zoom)</li>
                    <li>⬅️ Save: Save the current view</li>
                </ul>
            </li>
        </ul>
        
        <h4>For Large Visualizations</h4>
        <p>When working with large visualizations:</p>
        <ul>
            <li>Use the magnifying glass icon to temporarily zoom into an area</li>
            <li>Try different zoom levels to find the best view</li>
            <li>Pan around using click and drag when zoomed in</li>
            <li>Use the Home button to return to the default view</li>
        </ul>
        
        <h4>Web View Navigation</h4>
        <p>For interactive visualizations in the "Interactive View" tab:</p>
        <ul>
            <li>Scroll smoothly to explore content</li>
            <li>Click on interactive elements</li>
            <li>Adjust parameters if available (such as relevance sliders in pyLDAvis)</li>
        </ul>
        
        <div style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <p><strong>Tip:</strong> If scrolling ever feels too fast or jumpy, try using smaller mouse wheel movements 
            or use the scrollbar instead for more precise control.</p>
        </div>
        """)
        tabs.addTab(scrolling_tab, "Navigation Tips")
        
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