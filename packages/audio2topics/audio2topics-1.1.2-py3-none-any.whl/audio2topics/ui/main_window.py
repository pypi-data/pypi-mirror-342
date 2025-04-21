#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window for the Audio to Topics application.
Provides the main application window with tabs for different functions.
"""

import os
import logging
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QAction, QFileDialog, 
                            QMessageBox, QLabel, QStatusBar, QVBoxLayout, 
                            QHBoxLayout, QWidget, QProgressBar, QMenu, QStyle)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QSize

from .transcriber_tab import TranscriberTab
from .processor_tab import ProcessorTab
from .topic_tab import TopicTab
from .validator_tab import ValidatorTab
from .visualizer_tab import VisualizerTab
from .settings_dialog import SettingsDialog
from .comparison_tab import ComparisonTab

# Configure logging
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Main application window for the Audio to Topics application"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize instance variables
        self.documents = []  # For storing processed documents
        self.transcriptions = {}  # For storing audio transcriptions
        self.topic_model = None  # For storing the trained topic model
        self.topics = None  # For storing extracted topics
        self.topics_words = None  # For storing topic words
        
        # Set up the main window
        self.setWindowTitle("Audio2Topics")
        self.setMinimumSize(800, 600) # 900x700 or 1024x768 
        self.resize(1024, 768) 
        self.setWindowIcon(QIcon(r"resources/icons/app_icon.png"))
        
        # Create the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)  # Add margins
        self.layout.setSpacing(10)  # Add spacing
        
        # Create the tab widget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs, 1)
        
        # Create and add tabs with icons
        self.transcriber_tab = TranscriberTab()
        self.processor_tab = ProcessorTab()
        self.topic_tab = TopicTab()
        self.validator_tab = ValidatorTab()
        self.visualizer_tab = VisualizerTab()
        self.comparison_tab = ComparisonTab()


        # Add tabs with icons
        self.tabs.addTab(self.transcriber_tab, 
                        self.style().standardIcon(QStyle.SP_MediaVolume), 
                        "Transcribe Audio")
                        
        self.tabs.addTab(self.processor_tab, 
                        self.style().standardIcon(QStyle.SP_FileDialogDetailedView), 
                        "Process Text")
                        
        self.tabs.addTab(self.topic_tab, 
                        self.style().standardIcon(QStyle.SP_FileDialogContentsView), 
                        "Extract Topics")
                        
        self.tabs.addTab(self.validator_tab, 
                        self.style().standardIcon(QStyle.SP_DialogApplyButton), 
                        "Validate Topics")
                        
        self.tabs.addTab(self.visualizer_tab, 
                        self.style().standardIcon(QStyle.SP_ComputerIcon), 
                        "Visualize Results")
        self.tabs.addTab(self.comparison_tab, 
                self.style().standardIcon(QStyle.SP_BrowserReload), 
                "Compare Models")
        
        # Create the status bar with a progress bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add progress bar to status bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMaximumWidth(250)
        self.progress_bar.setVisible(False)  # Hide initially
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Create status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        # Create the menu bar
        self.create_menu_bar()
        
        # Connect signals and slots
        self.connect_signals()
        
    def create_menu_bar(self):
        """Create the application menu bar"""
        # Create the menu bar
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # Load transcriptions action
        load_trans_action = QAction(QIcon.fromTheme("document-open"), "Load Transcriptions", self)
        load_trans_action.setShortcut("Ctrl+O")
        load_trans_action.setStatusTip("Load saved transcriptions from text files")
        load_trans_action.triggered.connect(self.load_transcriptions)
        file_menu.addAction(load_trans_action)
        
        # Load documents action
        load_docs_action = QAction(QIcon.fromTheme("document-open"), "Load Text Documents", self)
        load_docs_action.setShortcut("Ctrl+D")
        load_docs_action.setStatusTip("Load text documents for processing")
        load_docs_action.triggered.connect(self.load_documents)
        file_menu.addAction(load_docs_action)
        
        # Save documents action
        save_docs_action = QAction(QIcon.fromTheme("document-save"), "Save Processed Documents", self)
        save_docs_action.setShortcut("Ctrl+S")
        save_docs_action.setStatusTip("Save processed documents to text files")
        save_docs_action.triggered.connect(self.save_documents)
        file_menu.addAction(save_docs_action)
        
        file_menu.addSeparator()
        
        # Save topic model action
        save_model_action = QAction(QIcon.fromTheme("document-save"), "Save Topic Model", self)
        save_model_action.setStatusTip("Save the trained topic model")
        save_model_action.triggered.connect(self.save_topic_model)
        file_menu.addAction(save_model_action)
        
        # Load topic model action
        load_model_action = QAction(QIcon.fromTheme("document-open"), "Load Topic Model", self)
        load_model_action.setStatusTip("Load a saved topic model")
        load_model_action.triggered.connect(self.load_topic_model)
        file_menu.addAction(load_model_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction(QIcon.fromTheme("application-exit"), "E&xit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu
        settings_menu = menu_bar.addMenu("&Settings")
        
        # API settings action
        api_settings_action = QAction(QIcon.fromTheme("preferences-system"), "API Keys", self)
        api_settings_action.setStatusTip("Configure API keys for LLM services")
        api_settings_action.triggered.connect(self.show_settings_dialog)
        settings_menu.addAction(api_settings_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        # About action
        about_action = QAction(QIcon.fromTheme("help-about"), "About", self)
        about_action.setStatusTip("Show information about the application")
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def connect_signals(self):
        """Connect signals and slots between tabs and components"""
        # Connect tab signals and slots
        
        # Transcriber tab signals
        self.transcriber_tab.transcription_completed.connect(self.on_transcription_completed)
        self.transcriber_tab.progress_updated.connect(self.update_progress)
        
        # Processor tab signals
        self.processor_tab.processing_completed.connect(self.on_processing_completed)
        self.processor_tab.progress_updated.connect(self.update_progress)
        
        # Topic tab signals
        self.topic_tab.topics_extracted.connect(self.on_topics_extracted)
        self.topic_tab.progress_updated.connect(self.update_progress)


        # Validator tab signals
        self.validator_tab.validation_completed.connect(self.on_validation_completed)
        self.validator_tab.progress_updated.connect(self.update_progress)
        
        # Visualizer tab signals
        self.visualizer_tab.progress_updated.connect(self.update_progress)
        self.comparison_tab.progress_updated.connect(self.update_progress)

    # Slot methods for received signals
    
    @pyqtSlot(dict)
    def on_transcription_completed(self, transcriptions):
        """Handle completed transcriptions"""
        self.transcriptions = transcriptions
        self.status_label.setText(f"Transcribed {len(transcriptions)} audio files")
        
        # Pass transcriptions to the processor tab
        documents = list(transcriptions.values())
        self.processor_tab.set_documents(documents)
        
        # Switch to the processor tab
        self.tabs.setCurrentWidget(self.processor_tab)
    
    @pyqtSlot(list)
    def on_processing_completed(self, documents):
        """Handle completed text processing"""
        self.documents = documents
        self.status_label.setText(f"Processed {len(documents)} documents")
        
        # Pass documents to the topic tab
        self.topic_tab.set_documents(documents)
        
        # Switch to the topic tab
        self.tabs.setCurrentWidget(self.topic_tab)
        
    def _on_topic_modeling_completed(self, topics, probs, topics_words, topic_info, model, documents):
        """
        Handle completion of topic modeling by passing results to other tabs.
        """
        # Update validator tab
        self.validator_tab.set_topic_model_data(model, topics, topics_words, documents)
        
        # Update visualizer tab
        self.visualizer_tab.set_topic_model_data(model, topics, topics_words, documents)
        
        # Update graph knowledge tab
        self.graph_knowledge_tab.set_topic_model_data(
            self.topic_tab.topic_modeler, documents, topics, topic_info, topics_words
        )
        
        # Enable the graph knowledge tab after topic modeling
        tab_index = self.tabs.indexOf(self.graph_knowledge_tab)
        if tab_index >= 0:
            self.tab_widget_status[tab_index] = True
            self.update_tab_status()  
              
    @pyqtSlot(object, object, object, object, object)
    def on_topics_extracted(self, topics, probs, topics_words, topic_info, chunked_docs):
        """Handle extracted topics"""
        self.topics = topics
        self.topics_words = topics_words
        self.status_label.setText(f"Extracted {len(set(topics))} topics")
        
        # Pass topics to the validator tab
        self.validator_tab.set_topics(topics, topics_words, topic_info)
        self.validator_tab.set_documents(self.documents)
        
        # Pass topics to the visualizer tab
        self.visualizer_tab.set_topics(topics, topics_words, probs, topic_info)
        # Pass chunked documents to visualization tab
        if chunked_docs is not None:
            self.visualizer_tab.set_documents(chunked_docs)  # Replace the original docs with chunks!
            
        self.visualizer_tab.set_documents(self.documents)
        
        # Pass topics to the comparison tab
        self.comparison_tab.set_documents(self.documents)
        # Switch to the validator tab
        self.tabs.setCurrentWidget(self.validator_tab)
    
    @pyqtSlot(dict, object)
    def on_validation_completed(self, metrics, summary_df):
        """Handle completed topic validation"""
        self.status_label.setText(f"Validated topics: {metrics['num_topics']} topics found")
        
        # Switch to the visualizer tab
        self.tabs.setCurrentWidget(self.visualizer_tab)
    
    @pyqtSlot(int, str)
    def update_progress(self, progress, message):
        """Update the progress bar and status message"""
        if progress > 0:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(progress)
            self.status_label.setText(message)
        else:
            self.progress_bar.setVisible(False)
            self.status_label.setText(message)
    
    # Menu action handlers
    
    def load_transcriptions(self):
        """Load transcriptions from text files"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Load Transcriptions", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if not file_paths:
            return
        
        transcriptions = {}
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    file_name = os.path.basename(file_path)
                    transcriptions[file_name] = content
            except Exception as e:
                logger.error(f"Error loading transcription {file_path}: {str(e)}")
                QMessageBox.warning(
                    self, "Load Error", f"Failed to load {file_path}: {str(e)}"
                )
        
        if transcriptions:
            self.on_transcription_completed(transcriptions)
    
    def load_documents(self):
        """Load text documents for processing"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Load Documents", "", "Text Files (*.txt);;Word Documents (*.docx);;All Files (*)"
        )
        
        if not file_paths:
            return
        
        documents = []
        
        for file_path in file_paths:
            try:
                if file_path.lower().endswith('.docx'):
                    # Handle Word documents
                    from docx import Document
                    doc = Document(file_path)
                    content = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
                else:
                    # Handle text files
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                
                documents.append(content)
            except Exception as e:
                logger.error(f"Error loading document {file_path}: {str(e)}")
                QMessageBox.warning(
                    self, "Load Error", f"Failed to load {file_path}: {str(e)}"
                )
        
        if documents:
            self.processor_tab.set_documents(documents)
            self.tabs.setCurrentWidget(self.processor_tab)
    
    def save_documents(self):
        """Save processed documents to text files"""
        if not self.documents:
            QMessageBox.information(
                self, "No Documents", "No processed documents available to save."
            )
            return
        
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory to Save Documents"
        )
        
        if not directory:
            return
        
        for i, doc in enumerate(self.documents):
            try:
                file_path = os.path.join(directory, f"document_{i+1}.txt")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(doc)
            except Exception as e:
                logger.error(f"Error saving document {i+1}: {str(e)}")
                QMessageBox.warning(
                    self, "Save Error", f"Failed to save document {i+1}: {str(e)}"
                )
        
        QMessageBox.information(
            self, "Save Complete", f"Saved {len(self.documents)} documents to {directory}"
        )
    
    def save_topic_model(self):
        """Save the trained topic model"""
        if not self.topic_tab.topic_modeler.get_model():
            QMessageBox.information(
                self, "No Model", "No topic model has been trained yet."
            )
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Topic Model", "", "BERTopic Model (*.bertopic);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            self.topic_tab.topic_modeler.save_model(file_path)
            QMessageBox.information(
                self, "Save Complete", f"Topic model saved to {file_path}"
            )
        except Exception as e:
            logger.error(f"Error saving topic model: {str(e)}")
            QMessageBox.warning(
                self, "Save Error", f"Failed to save topic model: {str(e)}"
            )
    
    def load_topic_model(self):
        """Load a saved topic model"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Topic Model", "", "BERTopic Model (*.bertopic);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            self.topic_tab.topic_modeler.load_model(file_path)
            
            # If we have documents, transform them with the loaded model
            if self.documents:
                model = self.topic_tab.topic_modeler.get_model()
                topics, probs = model.transform(self.documents)
                topics_words = model.get_topics()
                topic_info = model.get_topic_info()
                
                # Fix: Add chunked_docs parameter (use original documents)
                self.on_topics_extracted(topics, probs, topics_words, topic_info, self.documents)
            
            QMessageBox.information(
                self, "Load Complete", f"Topic model loaded from {file_path}"
            )
        except Exception as e:
            logger.error(f"Error loading topic model: {str(e)}")
            QMessageBox.warning(
                self, "Load Error", f"Failed to load topic model: {str(e)}"
            )    
    def show_settings_dialog(self):
        """Show the settings dialog for API configuration"""
        dialog = SettingsDialog(self)
        dialog.exec_()
    
    def show_about_dialog(self):
        """Show the about dialog with application information"""
        QMessageBox.about(
            self,
            "About Audio2Topics",
            "<h2>Audio2Topics</h2>"
            "<p>Version 1.0</p>"
            "<p>A PyQt application for transcribing audio files and extracting topics.</p>"
            "<p>Features:</p>"
            "<ul>"
            "<li>Audio transcription with Whisper</li>"
            "<li>Text processing and cleaning</li>"
            "<li>Topic extraction with BERTopic</li>"
            "<li>Topic refinement with LLM APIs</li>"
            "<li>Topic validation and visualization</li>"
            "</ul>"
        )
