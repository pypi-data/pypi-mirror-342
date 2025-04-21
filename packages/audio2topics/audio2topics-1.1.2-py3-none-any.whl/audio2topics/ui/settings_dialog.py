#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Dialog module for the Audio to Topics application.
Provides a dialog for configuring API keys and other settings.
"""

import logging
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                           QLabel, QLineEdit, QGroupBox, QPushButton, 
                           QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox,
                           QMessageBox, QStyle)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon

from ..core.llm_service import LLMService

# Configure logging
logger = logging.getLogger(__name__)

class SettingsDialog(QDialog):
    """Dialog for configuring application settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize LLM service
        self.llm_service = LLMService()
        
        # Set up the dialog
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 400)
        
        # Create the UI
        self.init_ui()
        
        # Load current settings
        self.load_settings()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create the tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # API keys tab
        api_tab = self.create_api_tab()
        self.tabs.addTab(api_tab, "API Keys")
        
        # Advanced settings tab
        advanced_tab = self.create_advanced_tab()
        self.tabs.addTab(advanced_tab, "Advanced Settings")
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        # Test connection button
        self.test_button = QPushButton("Test Connection") 	
        self.test_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.test_button.clicked.connect(self.test_connection)
        button_layout.addWidget(self.test_button)
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.save_button.setDefault(True)
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)
        
        main_layout.addLayout(button_layout)
    
    def create_api_tab(self):
        """Create the API keys tab"""
        api_tab = QGroupBox("API Keys Configuration")
        layout = QVBoxLayout(api_tab)
        
        # Provider selection
        provider_group = QGroupBox("LLM Provider")
        provider_layout = QVBoxLayout(provider_group)
        
        # Default provider
        provider_selection = QHBoxLayout()
        provider_selection.addWidget(QLabel("Default Provider:"))
        
        self.provider_combo = QComboBox()
        self.provider_combo.addItem("Anthropic Claude", "anthropic")
        self.provider_combo.addItem("OpenAI GPT", "openai")
        provider_selection.addWidget(self.provider_combo)
        
        provider_layout.addLayout(provider_selection)
        layout.addWidget(provider_group)
        
        # Anthropic API key
        anthropic_group = QGroupBox("Anthropic API")
        anthropic_layout = QVBoxLayout(anthropic_group)
        
        anthropic_key_layout = QHBoxLayout()
        anthropic_key_layout.addWidget(QLabel("API Key:"))
        
        self.anthropic_key_edit = QLineEdit()
        self.anthropic_key_edit.setEchoMode(QLineEdit.Password)
        self.anthropic_key_edit.setPlaceholderText("Enter your Anthropic API key")
        anthropic_key_layout.addWidget(self.anthropic_key_edit)
        
        # Show/hide password button
        self.anthropic_show_button = QPushButton()
        self.anthropic_show_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
        self.anthropic_show_button.setCheckable(True)
        self.anthropic_show_button.toggled.connect(lambda checked: self.toggle_password_visibility(self.anthropic_key_edit, checked))
        anthropic_key_layout.addWidget(self.anthropic_show_button)
        
        anthropic_layout.addLayout(anthropic_key_layout)
        
        # Anthropic model selection
        anthropic_model_layout = QHBoxLayout()
        anthropic_model_layout.addWidget(QLabel("Model:"))
        
        self.anthropic_model_combo = QComboBox()
        for model in ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]:
            self.anthropic_model_combo.addItem(model)
        anthropic_model_layout.addWidget(self.anthropic_model_combo)
        
        anthropic_layout.addLayout(anthropic_model_layout)
        layout.addWidget(anthropic_group)
        
        # OpenAI API key
        openai_group = QGroupBox("OpenAI API")
        openai_layout = QVBoxLayout(openai_group)
        
        openai_key_layout = QHBoxLayout()
        openai_key_layout.addWidget(QLabel("API Key:"))
        
        self.openai_key_edit = QLineEdit()
        self.openai_key_edit.setEchoMode(QLineEdit.Password)
        self.openai_key_edit.setPlaceholderText("Enter your OpenAI API key")
        openai_key_layout.addWidget(self.openai_key_edit)
        
        # Show/hide password button
        self.openai_show_button = QPushButton()
        self.openai_show_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
        self.openai_show_button.setCheckable(True)
        self.openai_show_button.toggled.connect(lambda checked: self.toggle_password_visibility(self.openai_key_edit, checked))
        openai_key_layout.addWidget(self.openai_show_button)
        
        openai_layout.addLayout(openai_key_layout)
        
        # OpenAI model selection
        openai_model_layout = QHBoxLayout()
        openai_model_layout.addWidget(QLabel("Model:"))
        
        self.openai_model_combo = QComboBox()
        for model in ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]:
            self.openai_model_combo.addItem(model)
        openai_model_layout.addWidget(self.openai_model_combo)
        
        openai_layout.addLayout(openai_model_layout)
        layout.addWidget(openai_group)
        
        return api_tab
    
    def create_advanced_tab(self):
        """Create the advanced settings tab"""
        advanced_tab = QGroupBox("Advanced Settings")
        layout = QVBoxLayout(advanced_tab)
        
        # LLM request settings
        llm_group = QGroupBox("LLM Request Parameters")
        llm_layout = QVBoxLayout(llm_group)
        
        # Temperature
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel("Temperature:"))
        
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 1.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(0.7)
        self.temperature_spin.setToolTip("Controls randomness: 0.0 is deterministic, 1.0 is more creative")
        temp_layout.addWidget(self.temperature_spin)
        
        llm_layout.addLayout(temp_layout)
        
        # Max tokens
        tokens_layout = QHBoxLayout()
        tokens_layout.addWidget(QLabel("Max Tokens:"))
        
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(10, 4000)
        self.max_tokens_spin.setSingleStep(10)
        self.max_tokens_spin.setValue(1000)
        self.max_tokens_spin.setToolTip("Maximum number of tokens in the response")
        tokens_layout.addWidget(self.max_tokens_spin)
        
        llm_layout.addLayout(tokens_layout)
        layout.addWidget(llm_group)
        
        # Reset to defaults button
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        self.reset_button.clicked.connect(self.reset_to_defaults)
        layout.addWidget(self.reset_button)
        
        return advanced_tab
    
    def toggle_password_visibility(self, edit, checked):
        """Toggle the visibility of a password field"""
        icon = QIcon.fromTheme("view-visible" if checked else "view-hidden")
        sender = self.sender()
        sender.setIcon(icon)
        
        edit.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)
    
    def load_settings(self):
        """Load settings from the LLM service"""
        # Provider
        self.provider_combo.setCurrentIndex(
            self.provider_combo.findData(self.llm_service.provider)
        )
        
        # API keys
        self.anthropic_key_edit.setText(self.llm_service.anthropic_key)
        self.openai_key_edit.setText(self.llm_service.openai_key)
        
        # Advanced settings
        self.temperature_spin.setValue(self.llm_service.temperature)
        self.max_tokens_spin.setValue(self.llm_service.max_tokens)
    
    def save_settings(self):
        """Save settings to the LLM service"""
        # Get values from UI
        provider = self.provider_combo.currentData()
        anthropic_key = self.anthropic_key_edit.text()
        openai_key = self.openai_key_edit.text()
        temperature = self.temperature_spin.value()
        max_tokens = self.max_tokens_spin.value()
        
        # Save to service
        success = self.llm_service.save_config(
            anthropic_key=anthropic_key,
            openai_key=openai_key,
            provider=provider,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        if success:
            QMessageBox.information(
                self, "Settings Saved", "Settings have been saved successfully."
            )
            self.accept()
        else:
            QMessageBox.warning(
                self, "Save Error", "Failed to save settings."
            )
    
    def reset_to_defaults(self):
        """Reset advanced settings to default values"""
        self.temperature_spin.setValue(0.7)
        self.max_tokens_spin.setValue(1000)
    
    def test_connection(self):
        """Test the API connection"""
        # Get the currently selected provider
        provider = self.provider_combo.currentData()
        
        # Get the API key for the selected provider
        api_key = (self.anthropic_key_edit.text() if provider == "anthropic" 
                  else self.openai_key_edit.text())
        
        if not api_key:
            QMessageBox.warning(
                self, "Missing API Key", f"Please enter an API key for {provider.capitalize()}."
            )
            return
        
        # Create a temporary service for testing
        temp_service = LLMService()
        
        # Set the provider and API key
        if provider == "anthropic":
            temp_service.anthropic_key = api_key
            temp_service.provider = "anthropic"
        else:
            temp_service.openai_key = api_key
            temp_service.provider = "openai"
        
        # Create a simple test message
        test_topics_words = {
            0: [("test", 1.0), ("connection", 0.8)]
        }
        
        # Disable buttons during test
        self.test_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        
        # Create worker for LLM request
        self.test_worker = temp_service.create_worker(test_topics_words)
        
        # Connect signals
        self.test_worker.response_received.connect(self.on_test_response)
        
        # Start the worker
        self.test_worker.start()
        
        # Show testing message
        QMessageBox.information(
            self, "Testing Connection", 
            f"Testing connection to {provider.capitalize()}.\n\nThis may take a few seconds."
        )
    
    @pyqtSlot(object)
    def on_test_response(self, response):
        """Handle test response"""
        # Re-enable buttons
        self.test_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
        
        # Check for errors
        if response.error:
            QMessageBox.critical(
                self, "Connection Failed", 
                f"Failed to connect: {response.error}"
            )
        else:
            QMessageBox.information(
                self, "Connection Successful", 
                "Successfully connected to the API."
            )