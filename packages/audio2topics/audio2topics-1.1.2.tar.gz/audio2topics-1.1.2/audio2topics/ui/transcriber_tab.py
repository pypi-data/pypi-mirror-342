#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcriber Tab module for the Audio to Topics application.
Provides UI for audio file transcription using Whisper.
"""

import os
import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QFileDialog, QListWidget, QGroupBox,
                           QTextEdit, QComboBox, QCheckBox, QProgressBar,
                           QSplitter, QListWidgetItem, QMessageBox, QStyle)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QCoreApplication
from PyQt5.QtGui import QIcon

from ..core.transcriber import Transcriber

# Configure logging
logger = logging.getLogger(__name__)

class TranscriberTab(QWidget):
    """Tab for audio transcription functionality"""
    
    # Define signals
    transcription_completed = pyqtSignal(dict)  # Emits transcriptions dictionary
    progress_updated = pyqtSignal(int, str)  # Emits progress percentage and message
    
    def __init__(self):
        super().__init__()
        
        # Initialize instance variables
        self.audio_files = {}  # Dictionary to store file paths and content
        self.transcriptions = {}  # Dictionary to store transcriptions
        self.transcriber = Transcriber()  # Transcriber instance
        
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
            "Click on Help button to learn about audio transcription module."
        )
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        help_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        # Add to the header layout, allowing it to expand
        header_layout.addWidget(help_label, 1)
        
        # Help button in the top right
        self.help_button = QPushButton()
        self.help_button.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.help_button.setToolTip("Learn about audio transcription and Whisper")
        self.help_button.setFixedSize(32, 32)  # Make it a square button
        self.help_button.clicked.connect(self.show_help_dialog)
        
        # Add to header layout with no stretching
        header_layout.addWidget(self.help_button, 0, Qt.AlignTop | Qt.AlignRight)
        
        # Add header layout to main layout
        main_layout.addLayout(header_layout)

        main_layout.addWidget(help_label)
        
        # Create a splitter for file list and transcription view
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter, 1)
        
        # Left panel - File selection and controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # File selection group
        file_group = QGroupBox("Audio Files")
        file_layout = QVBoxLayout(file_group)
        
        # File list widget
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_selected)
        file_layout.addWidget(self.file_list)
        
        # File selection buttons
        file_buttons_layout = QHBoxLayout()
        
        self.load_button = QPushButton("Load Audio Files")
        self.load_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.load_button.clicked.connect(self.load_audio_files)
        file_buttons_layout.addWidget(self.load_button)
        
        self.clear_button = QPushButton("Clear List")
        self.clear_button.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        self.clear_button.clicked.connect(self.clear_file_list)
        file_buttons_layout.addWidget(self.clear_button)
        
        file_layout.addLayout(file_buttons_layout)
        left_layout.addWidget(file_group)
        
        # Transcription controls group
        controls_group = QGroupBox("Transcription Controls")
        controls_layout = QVBoxLayout(controls_group)
        
        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Whisper Model:"))
        
        self.model_combo = QComboBox()
        for model_name in self.transcriber.get_available_models():
            self.model_combo.addItem(model_name)
        self.model_combo.setCurrentText("medium")  # Default to medium model
        model_layout.addWidget(self.model_combo)
        
        controls_layout.addLayout(model_layout)
        
        # Device selection
        device_layout = QHBoxLayout()
        device_layout.addWidget(QLabel("Device:"))
        # Language selection
        language_layout = QVBoxLayout()
        
        # Checkbox for auto-detection
        self.auto_detect_checkbox = QCheckBox("Auto-detect language")
        self.auto_detect_checkbox.setChecked(True)  # Enabled by default
        self.auto_detect_checkbox.stateChanged.connect(self.toggle_language_selection)
        language_layout.addWidget(self.auto_detect_checkbox)
        
        # Language dropdown
        language_selector_layout = QHBoxLayout()
        language_selector_layout.addWidget(QLabel("Language:"))
        
        self.language_combo = QComboBox()
        self.language_combo.addItem("English")
        self.language_combo.addItem("Norwegian")
        self.language_combo.setEnabled(False)  # Disabled initially because auto-detect is on
        language_selector_layout.addWidget(self.language_combo)
        
        language_layout.addLayout(language_selector_layout)
        controls_layout.addLayout(language_layout)
              
        self.device_combo = QComboBox()
        for device_name in self.transcriber.get_available_devices():
            self.device_combo.addItem(device_name)
        device_layout.addWidget(self.device_combo)
        
        controls_layout.addLayout(device_layout)
        
        
        # Transcribe button
        self.transcribe_button = QPushButton("Transcribe")
        self.transcribe_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.transcribe_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.transcribe_button.clicked.connect(self.start_transcription)
        self.transcribe_button.setEnabled(False)  # Disabled until files are loaded
        controls_layout.addWidget(self.transcribe_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setVisible(False)  # Hide initially
        controls_layout.addWidget(self.progress_bar)
        
        left_layout.addWidget(controls_group)
        splitter.addWidget(left_panel)
        
        # Right panel - Transcription view
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Transcription view group
        transcription_group = QGroupBox("Transcription")
        transcription_layout = QVBoxLayout(transcription_group)
        
        # Transcription text view
        self.transcription_text = QTextEdit()
        self.transcription_text.setReadOnly(True)
        self.transcription_text.setPlaceholderText("Transcribed text will appear here")
        transcription_layout.addWidget(self.transcription_text)
        
        # Save button
        self.save_button = QPushButton("Save Transcription")
        self.save_button.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.save_button.clicked.connect(self.save_transcription)
        self.save_button.setEnabled(False)  # Disabled until transcription is available
        transcription_layout.addWidget(self.save_button)
        
        right_layout.addWidget(transcription_group)
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes
        splitter.setSizes([300, 500])
        
        # Connect signals and slots
        self.connect_signals()
    
    def connect_signals(self):
        """Connect signals and slots"""
        # No need to change this method - the existing connection will work
        # as long as the worker emits the progress_updated signal
        pass
    
    def toggle_language_selection(self, state):
        """Enable or disable language selection based on auto-detect checkbox"""
        self.language_combo.setEnabled(not state)

    def load_audio_files(self):
        """Open file dialog to select audio files"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Audio Files", "", "Audio Files (*.mp3 *.wav *.m4a *.flac);;All Files (*)"
        )
        
        if not file_paths:
            return
        
        # Add files to the list and dictionary
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            
            # Check if file is already in the list
            if file_name in self.audio_files:
                continue
            
            try:
                # Read the file content
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                
                # Store the file content
                self.audio_files[file_name] = file_content
                
                # Add to the list widget
                item = QListWidgetItem(file_name)
                self.file_list.addItem(item)
            except Exception as e:
                logger.error(f"Error loading audio file {file_path}: {str(e)}")
                QMessageBox.warning(
                    self, "Load Error", f"Failed to load {file_path}: {str(e)}"
                )
        
        # Enable the transcribe button if files are loaded
        self.transcribe_button.setEnabled(len(self.audio_files) > 0)
    
    def clear_file_list(self):
        """Clear the file list and dictionary"""
        self.file_list.clear()
        self.audio_files.clear()
        self.transcriptions.clear()
        self.transcription_text.clear()
        self.transcribe_button.setEnabled(False)
        self.save_button.setEnabled(False)
    
    @pyqtSlot(QListWidgetItem)
    def on_file_selected(self, item):
        """Display the transcription for the selected file"""
        file_name = item.text()
        
        if file_name in self.transcriptions:
            self.transcription_text.setText(self.transcriptions[file_name])
            self.save_button.setEnabled(True)
        else:
            self.transcription_text.setText("No transcription available for this file.")
            self.save_button.setEnabled(False)
    
    def start_transcription(self):
        """Start the transcription process"""
        if not self.audio_files:
            QMessageBox.warning(
                self, "No Files", "Please load audio files first."
            )
            return
        
        # Disable UI elements during transcription
        self.transcribe_button.setEnabled(False)
        self.load_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        # Get selected model and device
        model_name = self.model_combo.currentText()
        device = self.device_combo.currentText()
        
        # Get language settings
        auto_detect = self.auto_detect_checkbox.isChecked()
        language = None if auto_detect else self.language_combo.currentText()
        
        # Create and configure worker
        worker = self.transcriber.transcribe_files(
            self.audio_files, 
            model_name=model_name,
            device=device,
            auto_detect_language=auto_detect,
            language=language
        )
        
        # Connect worker signals
        worker.progress_updated.connect(self.update_progress)
        worker.transcription_completed.connect(self.on_transcription_completed)
        worker.error_occurred.connect(self.on_transcription_error)
        
        # Forward the progress signal to the main window
        worker.progress_updated.connect(self.progress_updated)
        
        # Update UI
        self.progress_updated.emit(5, "Starting transcription...") 
           
    @pyqtSlot(int, str)
    def update_progress(self, progress, message):
        """Update the progress bar and message"""
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(f"{progress}% - {message}")
        
        # Update the UI more frequently to show smooth progress
        QCoreApplication.processEvents()
    
    @pyqtSlot(dict)
    def on_transcription_completed(self, transcriptions):
        """Handle completed transcriptions"""
        # Store the transcriptions
        self.transcriptions = transcriptions
        
        # Re-enable UI elements
        self.transcribe_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Update UI with the first transcription
        if self.file_list.count() > 0 and transcriptions:
            self.file_list.setCurrentRow(0)
            first_file = self.file_list.item(0).text()
            if first_file in transcriptions:
                self.transcription_text.setText(transcriptions[first_file])
                self.save_button.setEnabled(True)
        
        # Emit signal to notify main window
        self.transcription_completed.emit(transcriptions)
        
        # Show success message
        QMessageBox.information(
            self, "Transcription Complete", 
            f"Successfully transcribed {len(transcriptions)} audio files."
        )
    
    @pyqtSlot(str)
    def on_transcription_error(self, error_message):
        """Handle transcription errors"""
        # Re-enable UI elements
        self.transcribe_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Show error message
        QMessageBox.warning(
            self, "Transcription Error", f"Error during transcription: {error_message}"
        )
        
        # Update progress in main window
        self.progress_updated.emit(0, "Transcription failed")
    
    def save_transcription(self):
        """Save the current transcription to a file"""
        # Get the selected file
        current_item = self.file_list.currentItem()
        if not current_item:
            return
        
        file_name = current_item.text()
        if file_name not in self.transcriptions:
            return
        
        # Open save dialog
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Transcription", 
            f"{os.path.splitext(file_name)[0]}_transcription.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not save_path:
            return
        
        try:
            # Save the transcription
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(self.transcriptions[file_name])
            
            # Show success message
            QMessageBox.information(
                self, "Save Complete", f"Transcription saved to {save_path}"
            )
        except Exception as e:
            logger.error(f"Error saving transcription: {str(e)}")
            QMessageBox.warning(
                self, "Save Error", f"Failed to save transcription: {str(e)}"
            )

    def show_help_dialog(self):
        """Show help dialog with information about audio transcription and Whisper"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QTextBrowser, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Audio Transcription Help")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Create tab widget for different help sections
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Overview tab
        overview_tab = QTextBrowser()
        overview_tab.setOpenExternalLinks(True)
        overview_tab.setHtml("""
        <h2>Whisper Transcription Overview</h2>
        <p>Whisper is an automatic speech recognition (ASR) system developed by OpenAI. It's designed to convert 
        spoken language into written text with high accuracy across multiple languages.</p>
            <li>This tab allows you to transcribe audio files to text using the Whisper model.</li>
            <li>1. Select audio files using the 'Load Audio Files' button.</li>
            <li>2. Choose the Whisper model size (larger models are more accurate but slower).</li>
            <li>3. Click 'Transcribe' to start the transcription process.</li>
            <li>4. Once complete, you can view and save the transcribed text.</li>

        <p>Key features of Whisper:</p>
        <ul>
            <li>Trained on a diverse dataset of 680,000 hours of multilingual speech</li>
            <li>Support for transcription in multiple languages</li>
            <li>Automatic language detection for multilingual content</li>
            <li>Robust to background noise, accents, and technical language</li>
        </ul>
        
        <p>This application uses Whisper to transcribe your audio files, making it easy to convert spoken content 
        into text that can be analyzed, searched, and processed.</p>
        """)
        tabs.addTab(overview_tab, "Overview")
        
        # Models explanation tab
        models_tab = QTextBrowser()
        models_tab.setHtml("""
        <h2>Whisper Models</h2>
        
        <p>Whisper offers several model sizes, each with different accuracy and speed tradeoffs:</p>
        <p><i>The "large" model is the most accurate model, but it is slow.</i></p> 
        <p><i>For faster transcribing which balances between speed and accuracy, use the "turbo" model.</i></p>        
        <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f0f0f0;">
                <th>Model</th>
                <th>Parameters</th>
                <th>Disk Size</th>
                <th>Relative Speed</th>
                <th>Best For</th>
            </tr>
            <tr>
                <td><b>tiny</b></td>
                <td>39 M</td>
                <td>~75 MB</td>
                <td>~32x</td>
                <td>Quick transcriptions where accuracy is less critical</td>
            </tr>
            <tr>
                <td><b>base</b></td>
                <td>74 M</td>
                <td>~142 MB</td>
                <td>~16x</td>
                <td>Fast transcriptions with improved accuracy</td>
            </tr>
            <tr>
                <td><b>small</b></td>
                <td>244 M</td>
                <td>~466 MB</td>
                <td>~6x</td>
                <td>Good balance between speed and accuracy</td>
            </tr>
            <tr>
                <td><b>medium</b></td>
                <td>769 M</td>
                <td>~1.5 GB</td>
                <td>~2x</td>
                <td>High-quality transcriptions for most use cases</td>
            </tr>
            <tr>
                <td><b>large</b></td>
                <td>1550 M</td>
                <td>~3 GB</td>
                <td>1x</td>
                <td>Maximum accuracy for challenging audio</td>
            </tr>
            <tr>
                <td><b>turbo</b></td>
                <td>809 M</td>
                <td>~1.5 GB</td>
                <td>~8x</td>
                <td>Balances between speed and accuracy</td>
            </tr>
        </table>
        
        <p><b>Tips for choosing a model:</b></p>
        <ul>
            <li>Start with <b>medium</b> for a good balance of accuracy and speed</li>
            <li>Use <b>large</b> when accuracy is critical or for difficult audio (heavy accents, background noise)</li>
            <li>Use <b>small</b> or <b>base</b> for faster processing when transcribing many files</li>
            <li>Use <b>tiny</b> for quick previews or when working on battery power</li>
            <li>Use <b>turbo</b> to balance between speed and transcribing accuracy</li>
        </ul>
        
        <p>The chosen model will be downloaded automatically the first time you use it.</p>
        """)
        tabs.addTab(models_tab, "Models")
        
        multilingual_tab = QTextBrowser()
        multilingual_tab.setHtml("""
        <h2>Language Settings</h2>
        
        <p>Whisper can either automatically detect languages or use a specified language for transcription.</p>
        
        <h3>Automatic Language Detection</h3>
        <ul>
            <li>When enabled, Whisper analyzes each segment of audio to identify the language being spoken</li>
            <li>It transcribes each segment in its original language</li>
            <li>The result is a transcription that preserves all languages in the audio</li>
            <li>This is recommended for audio with multiple languages or when you're unsure of the language</li>
        </ul>
        
        <h3>Language Selection</h3>
        <p>You can disable automatic detection and select a specific language:</p>
        <ul>
            <li><b>English</b>: For audio in English</li>
            <li><b>Norwegian Bokmål</b>: For audio in Norwegian Bokmål (most common written form)</li>
            <li><b>Norwegian Nynorsk</b>: For audio in Norwegian Nynorsk</li>
        </ul>
        
        <p><b>Note:</b> Specifying a language can improve accuracy when you know the audio is entirely in one language.</p>
        
        <h3>Tips for Better Language Recognition</h3>
        <ul>
            <li><b>Use the large model</b>: The large model handles language detection much better than smaller models</li>
            <li><b>High-quality audio</b>: Clearer audio leads to better language detection</li>
            <li><b>Clear transitions</b>: Distinct pauses between language switches improves accuracy</li>
            <li><b>When in doubt, use auto-detection</b>: Whisper's language detection is generally very good</li>
        </ul>
        
        <h3>Supported Languages</h3>
        <p>Whisper works best with these languages:</p>
        <ul>
            <li>English, German, Spanish, French, Italian, Portuguese, Dutch</li>
            <li>Russian, Chinese (Mandarin), Japanese, Korean</li>
            <li>Arabic, Turkish, Polish, Ukrainian, Hindi</li>
            <li>Norwegian and other Nordic languages</li>
            <li>And many others with varying levels of support</li>
        </ul>
        
        <p>For multilingual audio containing less common languages, the larger models provide better results.</p>
        """)
        tabs.addTab(multilingual_tab, "Language Settings")  
              
        # Tips tab
        tips_tab = QTextBrowser()
        tips_tab.setHtml("""
        <h2>Tips for Better Transcriptions</h2>
        
        <h3>Audio Quality</h3>
        <ul>
            <li><b>Use clear recordings</b>: Higher audio quality leads to better transcriptions</li>
            <li><b>Minimize background noise</b>: While Whisper is relatively robust to noise, cleaner audio works better</li>
            <li><b>Ensure good microphone placement</b>: For recordings you control, position microphones properly</li>
            <li><b>Higher bitrates help</b>: When possible, use higher quality audio files</li>
        </ul>
        
        <h3>Processing Strategy</h3>
        <ul>
            <li><b>Split long recordings</b>: For very long files, consider splitting into 10-30 minute segments</li>
            <li><b>Test with samples</b>: Try transcribing a short segment with different models to determine best approach</li>
            <li><b>Batch similar files</b>: Process files with similar characteristics (same speaker, language, etc.) together</li>
            <li><b>Check CPU/GPU utilization</b>: Using a GPU significantly speeds up transcription</li>
        </ul>
        
        <h3>Handling Difficult Audio</h3>
        <ul>
            <li><b>Use larger models</b>: For audio with heavy accents, background noise, or multiple speakers</li>
            <li><b>Pre-process audio if needed</b>: Consider noise reduction or audio enhancement before transcription</li>
            <li><b>Technical content</b>: For specialized terminology, the large model typically performs best</li>
        </ul>
        """)
        tabs.addTab(tips_tab, "Tips")
        
        # Troubleshooting tab
        troubleshooting_tab = QTextBrowser()
        troubleshooting_tab.setHtml("""
        <h2>Troubleshooting</h2>
        
        <h3>Common Issues</h3>
        
        <div style="margin-bottom: 15px;">
            <p><b>Issue: Transcription fails to start</b></p>
            <p><b>Solutions:</b></p>
            <ul>
                <li>Check that you have an active internet connection (required for model download)</li>
                <li>Try a smaller model if you're experiencing memory issues</li>
                <li>Ensure you have sufficient disk space for model download</li>
                <li>Restart the application and try again</li>
            </ul>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Issue: Transcription quality is poor</b></p>
            <p><b>Solutions:</b></p>
            <ul>
                <li>Try a larger model (medium or large)</li>
                <li>Check audio quality and consider pre-processing to reduce noise</li>
                <li>Split complex audio with multiple speakers into smaller segments</li>
            </ul>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Issue: Transcription is very slow</b></p>
            <p><b>Solutions:</b></p>
            <ul>
                <li>Use a CPU with more cores or enable GPU acceleration if available</li>
                <li>Try a smaller model (base or small)</li>
                <li>Close other resource-intensive applications while transcribing</li>
                <li>For long files, consider splitting them into smaller chunks</li>
            </ul>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p><b>Issue: Languages not correctly identified in multilingual audio</b></p>
            <p><b>Solutions:</b></p>
            <ul>
                <li>Use the "large" model which has better language detection</li>
                <li>Ensure audio quality is high with clear pronunciation</li>
                <li>For critical content, consider splitting audio by language</li>
            </ul>
        </div>
        """)
        tabs.addTab(troubleshooting_tab, "Troubleshooting")
        
        # Add OK button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        # Show the dialog
        dialog.exec_()