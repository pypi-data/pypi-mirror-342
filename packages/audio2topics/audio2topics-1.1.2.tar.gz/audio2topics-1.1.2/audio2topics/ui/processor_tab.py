#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processor Tab module for the Audio to Topics application.
Provides UI for text processing and cleaning.
"""

import os
import logging
import pandas as pd
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QFileDialog, QTextEdit, QGroupBox,
                           QComboBox, QCheckBox, QProgressBar, QSplitter,
                           QTabWidget, QTableWidget, QTableWidgetItem, QMessageBox, QStyle, QDialog,
                           QGridLayout, QListWidget, QTableWidget, QTableWidgetItem, QDialogButtonBox, QLineEdit, QListWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon

from ..core.text_processor import TextProcessor

# Configure logging
logger = logging.getLogger(__name__)

class CSVImportDialog(QDialog):
    """Dialog for configuring CSV import options"""
    
    def __init__(self, csv_path, parent=None):
        super().__init__(parent)
        self.csv_path = csv_path
        self.preview_data = None
        self.selected_columns = []
        
        self.setWindowTitle("CSV Import Options")
        self.setMinimumSize(700, 500)
        
        self.init_ui()
        self.load_preview()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Options group
        options_group = QGroupBox("Import Options")
        options_layout = QGridLayout(options_group)
        
        # Delimiter option
        options_layout.addWidget(QLabel("Delimiter:"), 0, 0)
        self.delimiter_combo = QComboBox()
        self.delimiter_combo.addItems([
            "Comma (,)", "Semicolon (;)", "Tab (\\t)", "Pipe (|)", "Custom"
        ])
        options_layout.addWidget(self.delimiter_combo, 0, 1)
        
        # Custom delimiter field
        self.custom_delimiter = QLineEdit()
        self.custom_delimiter.setPlaceholderText("Enter custom delimiter")
        self.custom_delimiter.setEnabled(False)
        options_layout.addWidget(self.custom_delimiter, 0, 2)
        
        # Connect delimiter change event
        self.delimiter_combo.currentIndexChanged.connect(self.on_delimiter_changed)
        
        # Encoding option
        options_layout.addWidget(QLabel("Encoding:"), 1, 0)
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems([
            "UTF-8", "ASCII", "ISO-8859-1", "Windows-1252", "UTF-16"
        ])
        options_layout.addWidget(self.encoding_combo, 1, 1, 1, 2)
        
        # Header row option
        self.header_checkbox = QCheckBox("First row contains headers")
        self.header_checkbox.setChecked(True)
        options_layout.addWidget(self.header_checkbox, 2, 0, 1, 3)
        
        # Reload preview button
        self.reload_button = QPushButton("Reload Preview")
        self.reload_button.clicked.connect(self.load_preview)
        options_layout.addWidget(self.reload_button, 3, 0, 1, 3)
        
        layout.addWidget(options_group)
        
        # Column selection
        columns_group = QGroupBox("Column Selection")
        columns_layout = QVBoxLayout(columns_group)
        
        columns_label = QLabel("Select columns to import as text (multiple selection allowed):")
        columns_layout.addWidget(columns_label)
        
        self.columns_list = QListWidget()
        self.columns_list.setSelectionMode(QListWidget.MultiSelection)
        columns_layout.addWidget(self.columns_list)
        
        layout.addWidget(columns_group)
        
        # Preview group
        preview_group = QGroupBox("Data Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_table = QTableWidget()
        self.preview_table.verticalHeader().setMinimumWidth(30)  
        preview_layout.addWidget(self.preview_table)
        
        layout.addWidget(preview_group)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def on_delimiter_changed(self, index):
        """Handle delimiter selection change"""
        self.custom_delimiter.setEnabled(index == 4)  # Enable for "Custom" option
        if index < 4:
            self.load_preview()
    
    def get_delimiter(self):
        """Get the selected delimiter"""
        delimiter_map = {
            0: ",",  # Comma
            1: ";",  # Semicolon
            2: "\t", # Tab
            3: "|",  # Pipe
            4: self.custom_delimiter.text()  # Custom
        }
        return delimiter_map[self.delimiter_combo.currentIndex()]
    
    def load_preview(self):
        """Load preview data from CSV"""
        try:
            import csv
            
            delimiter = self.get_delimiter()
            encoding = self.encoding_combo.currentText()
            has_header = self.header_checkbox.isChecked()
            
            with open(self.csv_path, 'r', encoding=encoding, newline='') as csvfile:
                # Read the first few rows for preview
                reader = csv.reader(csvfile, delimiter=delimiter)
                preview_data = []
                for i, row in enumerate(reader):
                    preview_data.append(row)
                    if i >= 5:  # Limit to first 6 rows (including header)
                        break
            
            if not preview_data:
                raise ValueError("CSV file appears to be empty")
            
            # Update columns list
            self.columns_list.clear()
            headers = preview_data[0] if has_header else [f"Column {i+1}" for i in range(len(preview_data[0]))]
            
            for header in headers:
                item = QListWidgetItem(header)
                self.columns_list.addItem(item)
                item.setSelected(True)  # Select all columns by default
            
            # Update preview table
            self.update_preview_table(preview_data, headers, has_header)
            
            # Store preview data
            self.preview_data = preview_data
            
        except Exception as e:
            QMessageBox.warning(
                self, "Preview Error", f"Failed to load CSV preview: {str(e)}"
            )
    
    def update_preview_table(self, data, headers, has_header):
        """Update the preview table with data"""
        self.preview_table.clear()
        
        if not data:
            return
        
        # Set column and row count
        col_count = len(data[0])
        row_count = len(data) - 1 if has_header else len(data)
        
        self.preview_table.setColumnCount(col_count)
        self.preview_table.setRowCount(row_count)
        
        # Set headers
        self.preview_table.setHorizontalHeaderLabels(headers)
        
        # Fill data
        start_row = 1 if has_header else 0
        for row_idx, row in enumerate(data[start_row:]):
            for col_idx, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))
                self.preview_table.setItem(row_idx, col_idx, item)
        
        # Resize columns to content
        self.preview_table.resizeColumnsToContents()
    
    def get_selected_columns(self):
        """Get indices of selected columns"""
        return [self.columns_list.row(item) for item in self.columns_list.selectedItems()]
    
    def get_import_options(self):
        """Get all import options as a dictionary"""
        return {
            'delimiter': self.get_delimiter(),
            'encoding': self.encoding_combo.currentText(),
            'has_header': self.header_checkbox.isChecked(),
            'selected_columns': self.get_selected_columns()
        }

class ProcessorTab(QWidget):
    """Tab for text processing functionality"""
    
    # Define signals
    processing_completed = pyqtSignal(list)  # Emits processed documents
    progress_updated = pyqtSignal(int, str)  # Emits progress percentage and message
    
    def __init__(self):
        super().__init__()
        
        # Initialize instance variables
        self.raw_documents = []  # Original documents
        self.processed_documents = []  # Processed documents
        self.text_processor = TextProcessor()  # Text processor instance
        
        # Set up the UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        header_layout = QHBoxLayout()        
       
        # Add introduction/help text
        help_text = (
            "Click on the Help button to learn about text processing module."
        )
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        help_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        header_layout.addWidget(help_label, 1)
        
        # Help button in the top right
        self.help_button = QPushButton()
        self.help_button.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.help_button.setToolTip("Learn about text processing and cleaning")
        self.help_button.setFixedSize(32, 32)  # Make it a square button
        self.help_button.clicked.connect(self.show_help_dialog)
        
        # Add to header layout with no stretching
        header_layout.addWidget(self.help_button, 0, Qt.AlignTop | Qt.AlignRight)
        
        # Add header layout to main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(help_label)
        
        # Controls section
        controls_layout = QHBoxLayout()
        
        # Language selection
        language_layout = QHBoxLayout()
        language_layout.addWidget(QLabel("Language:"))
        
        self.language_combo = QComboBox()
        for language in self.text_processor.get_available_languages():
            self.language_combo.addItem(language)
        language_layout.addWidget(self.language_combo)
        
        controls_layout.addLayout(language_layout)
        
        # Process button
        self.process_button = QPushButton("Process Text")
        self.process_button.setIcon(self.style().standardIcon(QStyle.SP_CommandLink))
        self.process_button.clicked.connect(self.start_processing)
        controls_layout.addWidget(self.process_button)
        
        # Load text button
        self.load_button = QPushButton("Load Text Files")
        self.load_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.load_button.clicked.connect(self.load_text_files)
        controls_layout.addWidget(self.load_button)
        
        # Clear text button
        self.clear_button = QPushButton("Clear All")
        self.clear_button.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        self.clear_button.clicked.connect(self.clear_all)
        controls_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(controls_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setVisible(False)  # Hide initially
        main_layout.addWidget(self.progress_bar)
        
        # Create a splitter for text editing and viewing
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter, 1)
        
        # Left panel - Raw text input
        left_panel = QGroupBox("Original Text")
        left_layout = QVBoxLayout(left_panel)
        
        self.raw_text_edit = QTextEdit()
        self.raw_text_edit.setPlaceholderText("Enter or paste text here, or load from files.\n\n"
                                            "You can enter multiple documents separated by blank lines.")
        left_layout.addWidget(self.raw_text_edit)
        
        splitter.addWidget(left_panel)
        
        # Right panel - Processed text and analysis
        right_panel = QTabWidget()
        
        # Processed text tab
        processed_tab = QWidget()
        processed_layout = QVBoxLayout(processed_tab)
        
        self.processed_text_edit = QTextEdit()
        self.processed_text_edit.setReadOnly(True)
        self.processed_text_edit.setPlaceholderText("Processed text will appear here")
        processed_layout.addWidget(self.processed_text_edit)
        
        right_panel.addTab(processed_tab, "Processed Text")
        
        # Text statistics tab
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)
        
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.stats_table.horizontalHeader().setStretchLastSection(True)
        self.stats_table.verticalHeader().setMinimumWidth(30)  # Adjust width as needed
        stats_layout.addWidget(self.stats_table)
        
        right_panel.addTab(stats_tab, "Statistics")
        
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes
        splitter.setSizes([400, 400])
        
        # Connect signals and slots
        self.connect_signals()
    
    def connect_signals(self):
        """Connect signals and slots"""
        # Connect to progress updates from the text processor
        pass  # Will be implemented when the worker is created
    
    def set_documents(self, documents):
        """Set the documents to be processed"""
        if not documents:
            return
        
        self.raw_documents = documents
        
        # Update the text edit with the raw documents
        self.raw_text_edit.clear()
        for i, doc in enumerate(documents):
            if i > 0:
                self.raw_text_edit.append("\n\n")
            self.raw_text_edit.append(doc)
    
    def load_text_files(self):
        """Open file dialog to select text files"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Text Files", "", 
            "Text Files (*.txt);;CSV Files (*.csv);;Word Documents (*.docx);;All Files (*)"
        )
        
        if not file_paths:
            return
        
        # Clear existing text
        self.raw_text_edit.clear()
        self.raw_documents = []
        
        # Load and display each file
        for file_path in file_paths:
            try:
                if file_path.lower().endswith('.docx'):
                    # Handle Word documents
                    from docx import Document
                    doc = Document(file_path)
                    content = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
                elif file_path.lower().endswith('.csv'):
                    # Handle CSV files using the dialog
                    content = self.handle_csv_file(file_path)
                    if content is None:
                        continue  # User cancelled or error occurred
                else:
                    # Handle text files
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                
                # Add to documents list
                self.raw_documents.append(content)
                
                # Add to text edit
                if self.raw_text_edit.toPlainText():
                    self.raw_text_edit.append("\n\n")
                self.raw_text_edit.append(content)
            except Exception as e:
                logger.error(f"Error loading text file {file_path}: {str(e)}")
                QMessageBox.warning(
                    self, "Load Error", f"Failed to load {file_path}: {str(e)}"
                )      
    def handle_csv_file(self, file_path):
        """Handle CSV file import with options dialog"""
        try:
            # Check file size first
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
            
            # Warn if file is very large (over 5MB)
            if file_size > 5:
                confirm = QMessageBox.question(
                    self, 
                    "Large CSV File", 
                    f"The selected CSV file is {file_size:.1f} MB in size and may take a while to process. "
                    f"Very large files might cause the application to become less responsive.\n\n"
                    f"Would you like to continue importing this file?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirm == QMessageBox.No:
                    return None
            
            # Show import dialog
            dialog = CSVImportDialog(file_path, self)
            if dialog.exec_() != QDialog.Accepted:
                return None
            
            # Get import options
            options = dialog.get_import_options()
            delimiter = options['delimiter']
            encoding = options['encoding']
            has_header = options['has_header']
            selected_columns = options['selected_columns']
            
            # Import data
            import csv
            rows = []
            
            with open(file_path, 'r', encoding=encoding, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=delimiter)
                
                # Skip header if necessary
                if has_header:
                    headers = next(reader)
                
                # Process rows
                for row in reader:
                    if not row:  # Skip empty rows
                        continue
                        
                    # Extract selected columns only
                    if selected_columns:
                        selected_text = []
                        for idx in selected_columns:
                            if idx < len(row):
                                selected_text.append(str(row[idx]))
                        row_text = ' '.join(selected_text)
                    else:
                        row_text = ' '.join(str(field) for field in row)
                    
                    if row_text.strip():
                        rows.append(row_text)
            
            # Join all rows with newlines
            content = '\n'.join(rows)
            return content
            
        except Exception as e:
            logger.error(f"Error processing CSV file {file_path}: {str(e)}")
            QMessageBox.warning(
                self, "CSV Import Error", f"Failed to process {file_path}: {str(e)}"
            )
            return None                   
    def clear_all(self):
        """Clear all text inputs and results"""
        self.raw_text_edit.clear()
        self.processed_text_edit.clear()
        self.stats_table.setRowCount(0)
        self.raw_documents = []
        self.processed_documents = []
    
    def start_processing(self):
        """Start the text processing"""
        # Get text from the text edit
        text = self.raw_text_edit.toPlainText()
        
        if not text.strip():
            QMessageBox.warning(
                self, "No Text", "Please enter or load some text first."
            )
            return
        
        # ALWAYS update raw_documents with the current text, regardless of previous state
        import re
        # Split by double line breaks to separate documents
        docs = re.split(r'\n\s*\n', text)
        self.raw_documents = [doc.strip() for doc in docs if doc.strip()]
        
        # Disable UI elements during processing
        self.process_button.setEnabled(False)
        self.load_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.raw_text_edit.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        # Get selected language
        language = self.language_combo.currentText()
        
        # Create and configure worker
        worker = self.text_processor.process_text(self.raw_documents, language)
        
        # Connect worker signals
        worker.progress_updated.connect(self.update_progress)
        worker.processing_completed.connect(self.on_processing_completed)
        worker.error_occurred.connect(self.on_processing_error)
        
        # Forward the progress signal to the main window
        worker.progress_updated.connect(self.progress_updated)
        
        # Update UI
        self.progress_updated.emit(5, "Starting text processing...") 
       
    @pyqtSlot(int, str)
    def update_progress(self, progress, message):
        """Update the progress bar and message"""
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(f"{progress}% - {message}")
    
    @pyqtSlot(list)
    def on_processing_completed(self, processed_docs):
        """Handle completed text processing"""
        # Store the processed documents
        self.processed_documents = processed_docs
        
        # Re-enable UI elements
        self.process_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.raw_text_edit.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Update UI with processed text
        self.processed_text_edit.clear()
        for i, doc in enumerate(processed_docs):
            if i > 0:
                self.processed_text_edit.append("\n\n")
            self.processed_text_edit.append(doc)
        
        # Calculate and display text statistics
        self.update_statistics()
        
        # Emit signal to notify main window
        self.processing_completed.emit(processed_docs)
    
    @pyqtSlot(str)
    def on_processing_error(self, error_message):
        """Handle processing errors"""
        # Re-enable UI elements
        self.process_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.raw_text_edit.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Show error message
        QMessageBox.warning(
            self, "Processing Error", f"Error during text processing: {error_message}"
        )
        
        # Update progress in main window
        self.progress_updated.emit(0, "Text processing failed")
    
    def update_statistics(self):
        """Calculate and display text statistics"""
        if not self.processed_documents:
            return
        
        # Join all documents for statistics
        all_text = " ".join(self.processed_documents)
        
        # Get selected language
        language = self.language_combo.currentText()
        
        # Calculate statistics
        stats = self.text_processor.get_text_statistics(all_text, language)
        
        # Update the stats table
        self.stats_table.setRowCount(0)  # Clear existing rows
        
        for i, (metric, value) in enumerate(stats):
            # Handle special case for most common words
            if metric == "Most common words":
                self.stats_table.insertRow(i)
                metric_item = QTableWidgetItem(metric)
                self.stats_table.setItem(i, 0, metric_item)
                
                # Format most common words as a string
                words_str = ", ".join([f"{word} ({count})" for word, count in value])
                value_item = QTableWidgetItem(words_str)
                self.stats_table.setItem(i, 1, value_item)
            else:
                self.stats_table.insertRow(i)
                metric_item = QTableWidgetItem(metric)
                value_item = QTableWidgetItem(str(value))
                
                self.stats_table.setItem(i, 0, metric_item)
                self.stats_table.setItem(i, 1, value_item)
        
        # Resize the table to fit the content
        self.stats_table.resizeColumnsToContents()

    def show_help_dialog(self):
        """Show help dialog with information about text processing and cleaning"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QTextBrowser, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Text Processing Help")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Create tab widget for different help sections
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Overview tab
        overview_tab = QTextBrowser()
        overview_tab.setOpenExternalLinks(True)
        overview_tab.setHtml("""
        <h2>Text Processing Overview</h2>
        <p>Text processing prepares raw text for topic modeling and analysis by cleaning, normalizing, 
        and standardizing the content. This step is crucial for getting meaningful results from subsequent 
        topic modeling.</p>
            <li>This tab allows you to process and clean text documents.</li>
            <li>1. Enter text, paste from clipboard, or load from files.</li>
            <li>2. Choose the language and processing options.</li>
            <li>3. Click 'Process Text' to start cleaning.</li>
            <li>4. View the original and processed text side by side.</li>

        <p>The text processor performs several key operations:</p>
        <ul>
            <li><b>Cleaning</b>: Removes unwanted elements like special characters, numbers, and URLs</li>
            <li><b>Tokenization</b>: Breaks text into individual words or tokens</li>
            <li><b>Stopword removal</b>: Filters out common words (like "the", "and", "is") that don't contribute to meaning</li>
            <li><b>Lemmatization</b>: Reduces words to their base or dictionary form</li>
            <li><b>Optional stemming</b>: Reduces words to their root form by removing suffixes</li>
        </ul>
        
        <p>When uploaidn one document. Remeber that the algroithms can consider text as different documents if there are serveral lines between text.
        Remove these lines if you want the text to be considered as one document.</p>
        
        <p>Well-processed text leads to more coherent topics, clearer patterns, and better insights
        during the topic modeling stage.</p>
        """)
        tabs.addTab(overview_tab, "Overview")
        
        # Text Cleaning tab
        cleaning_tab = QTextBrowser()
        cleaning_tab.setHtml("""
        <h2>Text Cleaning Process</h2>
        
        <p>The text cleaning process transforms raw text into a standardized format that's optimal
        for topic modeling. Here's what happens during processing:</p>
        
        <div style="margin-bottom: 15px;">
            <p><b>1. Special Character Removal</b></p>
            <p>Removes punctuation, special characters, and symbols that don't contribute to meaning.</p>
            <p><i>Example:</i> "Hello, world!" → "Hello world"</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>2. Email and URL Removal</b></p>
            <p>Identifies and removes email addresses and web URLs.</p>
            <p><i>Example:</i> "Contact info@example.com or visit www.example.com" → "Contact or visit"</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>3. Number Removal</b></p>
            <p>Removes numeric digits that typically don't contribute to topic meaning.</p>
            <p><i>Example:</i> "There are 123 examples" → "There are examples"</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>4. Case Normalization</b></p>
            <p>Converts all text to lowercase for consistent processing.</p>
            <p><i>Example:</i> "Text Processing" → "text processing"</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>5. Stopword Removal</b></p>
            <p>Filters out common words (stopwords) that appear frequently but carry little meaning.</p>
            <p><i>Example:</i> "the cat is on the mat" → "cat mat"</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>6. Lemmatization</b></p>
            <p>Reduces words to their dictionary form to group similar words together.</p>
            <p><i>Example:</i> "running runs runner" → "run run runner"</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>7. Optional Stemming</b></p>
            <p>Reduces words to their root form by removing prefixes and suffixes.</p>
            <p><i>Example:</i> "historical histories history" → "histor histor histor"</p>
        </div>
        
        <p>The result is clean, standardized text that's ready for topic modeling and analysis.</p>
        """)
        tabs.addTab(cleaning_tab, "Text Cleaning")
        
        # Language Support tab
        language_tab = QTextBrowser()
        language_tab.setHtml("""
        <h2>Language Support</h2>
        
        <p>The text processor supports multiple languages. Each language has its own set of
        stopwords, stemming rules, and lemmatization capabilities.</p>
        
        <h3>Fully Supported Languages</h3>
        <p>These languages have complete support for all text processing features:</p>
        <ul>
            <li><b>English</b>: Full stopword, stemming, and lemmatization support</li>
            <li><b>Norwegian</b>: Complete language support including Nordic-specific processing</li>
        </ul>
        
        <h3>Language-Specific Processing</h3>
        <p>Different languages require different processing approaches:</p>
        <ul>
            <li><b>Stopwords</b>: Each language has its own list of common words to remove</li>
            <li><b>Stemming</b>: Language-specific stemming algorithms handle different word structures</li>
            <li><b>Lemmatization</b>: Relies on language-specific dictionaries for word reduction</li>
        </ul>
        
        <h3>Multilingual Documents</h3>
        <p>For documents containing multiple languages:</p>
        <ul>
            <li>Select the predominant language for processing</li>
            <li>Be aware that minority language content may not be processed optimally</li>
            <li>Consider splitting multilingual documents if possible</li>
        </ul>
        
        <p>For best results, process documents in their native language rather than translations.</p>
        """)
        tabs.addTab(language_tab, "Languages")
        
        # Text Statistics tab
        statistics_tab = QTextBrowser()
        statistics_tab.setHtml("""
        <h2>Understanding Text Statistics</h2>
        
        <p>The Statistics tab provides metrics about your text before and after processing.
        These metrics help you understand your data and evaluate the effects of text cleaning.</p>
        
        <h3>Available Statistics</h3>
        
        <div style="margin-bottom: 15px;">
            <p><b>Number of sentences</b></p>
            <p>The total count of sentences detected in the text. This helps gauge document complexity and structure.</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Number of tokens</b></p>
            <p>Total count of words and other elements (like punctuation) before filtering. This represents the raw
            size of the text.</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Number of unique words</b></p>
            <p>Count of distinct words, showing vocabulary richness and diversity.</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Number of words (excluding stopwords)</b></p>
            <p>Count of meaningful words after removing common stopwords. This represents the meaningful content.</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Number of stop words</b></p>
            <p>Count of common words that were filtered out. Helps understand how much "noise" was removed.</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Average sentence length</b></p>
            <p>Average number of words per sentence. Indicates writing style and complexity.</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Most common words</b></p>
            <p>List of the most frequently occurring words and their counts. Provides a quick glimpse of key terms.</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Number of characters</b></p>
            <p>Total character count in the text.</p>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Average word length</b></p>
            <p>Average number of characters per word. Another indicator of text complexity.</p>
        </div>
        
        <p>These statistics can help you evaluate whether your text is suitable for topic modeling
        and identify potential issues before proceeding.</p>
        """)
        tabs.addTab(statistics_tab, "Statistics")
        
        # Tips tab
        tips_tab = QTextBrowser()
        tips_tab.setHtml("""
        <h2>Text Processing Tips</h2>
        
        <h3>Best Practices</h3>
        <ul>
            <li><b>Check the statistics</b> before and after processing to understand the transformation</li>
            <li><b>Review the processed text</b> to ensure important content wasn't lost during cleaning</li>
            <li><b>Process related documents</b> using the same settings for consistency</li>
            <li><b>Select the correct language</b> for optimal stopword removal and lemmatization</li>
            <li><b>Split long documents</b> into meaningful chunks if they cover multiple distinct topics</li>
        </ul>
        
        <h3>For Better Topic Modeling</h3>
        <ul>
            <li><b>Remove custom stopwords</b> for your specific domain if needed</li>
            <li><b>Ensure adequate text volume</b> - aim for at least several thousand words total</li>
            <li><b>Balance document lengths</b> - very short and very long documents together can skew results</li>
            <li><b>Consider keeping key phrases</b> intact rather than splitting them into individual words</li>
            <li><b>Maintain document boundaries</b> - don't merge unrelated texts into single documents</li>
        </ul>
        
        <h3>Handling Special Content</h3>
        <ul>
            <li><b>Technical terminology</b>: Consider keeping field-specific terms even if uncommon</li>
            <li><b>Names and proper nouns</b>: May be important for your analysis despite being uncommon words</li>
            <li><b>Abbreviations and acronyms</b>: Consider standardizing these before processing</li>
            <li><b>Formatted text</b>: Remove formatting marks (like Markdown or HTML tags) if present</li>
        </ul>
        
        <h3>Common Issues</h3>
        <ul>
            <li><b>Over-processing</b>: Too aggressive cleaning can remove meaningful content</li>
            <li><b>Under-processing</b>: Insufficient cleaning leaves noise that can affect topic quality</li>
            <li><b>Language mismatch</b>: Using English processing on non-English text produces poor results</li>
            <li><b>Very short documents</b>: Documents with just a few words may not provide enough context</li>
        </ul>
        """)
        tabs.addTab(tips_tab, "Tips")
        
        # Add OK button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        # Show the dialog
        dialog.exec_()