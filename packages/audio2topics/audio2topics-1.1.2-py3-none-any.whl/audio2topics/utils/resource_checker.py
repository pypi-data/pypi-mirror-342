#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resource Checker module for the Audio to Topics application.
Checks and downloads required resources for the application.
"""

import os
import sys
import logging
import subprocess
import importlib.util
import threading
import time
from typing import List, Dict, Tuple

from PyQt5.QtWidgets import (QProgressDialog, QMessageBox, QApplication)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Configure logging
logger = logging.getLogger(__name__)

class ResourceCheckWorker(QThread):
    """Worker thread for checking and downloading resources"""
    progress_updated = pyqtSignal(int, str)
    resource_checked = pyqtSignal(str, bool, str)
    all_checked = pyqtSignal(bool, dict)
    
    def __init__(self, resources_to_check: List[Dict]):
        super().__init__()
        self.resources = resources_to_check
        self.results = {}
    
    def run(self):
        """Run the resource check"""
        all_success = True
        total_resources = len(self.resources)
        
        for i, resource in enumerate(self.resources):
            resource_name = resource.get('name', 'Resource')
            progress = int((i / total_resources) * 100)
            
            self.progress_updated.emit(progress, f"Checking {resource_name}...")
            
            try:
                check_func = resource.get('check_func')
                install_func = resource.get('install_func')
                
                if not check_func:
                    raise ValueError(f"No check function for {resource_name}")
                    
                # Check if the resource is available
                is_available, message = check_func()
                
                if not is_available and install_func:
                    # Resource is not available, try to install it
                    self.progress_updated.emit(progress, f"Installing {resource_name}...")
                    install_success, install_message = install_func()
                    
                    if install_success:
                        # Recheck after installation
                        is_available, message = check_func()
                    else:
                        message = f"Installation failed: {install_message}"
                
                self.results[resource_name] = {
                    'available': is_available,
                    'message': message
                }
                
                self.resource_checked.emit(resource_name, is_available, message)
                
                if not is_available:
                    all_success = False
                    
            except Exception as e:
                logger.error(f"Error checking resource {resource_name}: {str(e)}", exc_info=True)
                self.results[resource_name] = {
                    'available': False,
                    'message': f"Error: {str(e)}"
                }
                self.resource_checked.emit(resource_name, False, f"Error: {str(e)}")
                all_success = False
        
        # Emit final signal
        self.progress_updated.emit(100, "Resource check completed")
        self.all_checked.emit(all_success, self.results)


def check_and_install_resources(parent=None):
    """
    Check and install required resources for the application.
    
    Args:
        parent: Parent widget for the progress dialog
        
    Returns:
        bool: True if all resources are available, False otherwise
    """
    # Define the resources to check
    resources = [
        {
            'name': 'PyTorch',
            'check_func': check_pytorch,
            'install_func': install_pytorch
        },
        {
            'name': 'Whisper',
            'check_func': check_whisper,
            'install_func': install_whisper
        },
        {
            'name': 'NLTK Data',
            'check_func': check_nltk_data,
            'install_func': install_nltk_data
        },
        {
            'name': 'SpaCy English Model',
            'check_func': lambda: check_spacy_model('en_core_web_sm'),
            'install_func': lambda: install_spacy_model('en_core_web_sm')
        },
        {
            'name': 'SpaCy Norwegian Model',
            'check_func': lambda: check_spacy_model('nb_core_news_sm'),
            'install_func': lambda: install_spacy_model('nb_core_news_sm')
        },
        {
            'name': 'BERTopic',
            'check_func': check_bertopic,
            'install_func': install_bertopic
        }
    ]
    
    # Create a progress dialog
    if parent is not None and QApplication.instance():
        progress_dialog = QProgressDialog("Checking required resources...", "Cancel", 0, 100, parent)
        progress_dialog.setWindowTitle("Resource Check")
        progress_dialog.setMinimumWidth(400)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setAutoClose(False)
        progress_dialog.setAutoReset(False)
        progress_dialog.setValue(0)
        progress_dialog.show()
        QApplication.processEvents()
        
        # Create and start worker thread
        worker = ResourceCheckWorker(resources)
        
        # Connect signals to update the progress dialog
        worker.progress_updated.connect(
            lambda progress, message: update_progress_dialog(progress_dialog, progress, message)
        )
        
        worker.all_checked.connect(
            lambda success, results: on_all_resources_checked(progress_dialog, success, results)
        )
        
        # Start the worker
        worker.start()
        
        # Wait for completion
        while worker.isRunning():
            QApplication.processEvents()
            
        # Get results
        all_available = all(result['available'] for result in worker.results.values())
        
        return all_available
    else:
        # No GUI available, run synchronously
        all_available = True
        
        for resource in resources:
            resource_name = resource.get('name', 'Resource')
            check_func = resource.get('check_func')
            install_func = resource.get('install_func')
            
            if not check_func:
                logger.error(f"No check function for {resource_name}")
                all_available = False
                continue
                
            # Check if the resource is available
            is_available, message = check_func()
            
            if not is_available and install_func:
                # Resource is not available, try to install it
                logger.info(f"Installing {resource_name}...")
                install_success, install_message = install_func()
                
                if install_success:
                    # Recheck after installation
                    is_available, message = check_func()
                else:
                    logger.error(f"Failed to install {resource_name}: {install_message}")
            
            if not is_available:
                logger.error(f"Resource {resource_name} is not available: {message}")
                all_available = False
        
        return all_available


def update_progress_dialog(dialog, progress, message):
    """Update the progress dialog"""
    if dialog and not dialog.wasCanceled():
        dialog.setValue(progress)
        dialog.setLabelText(message)
        QApplication.processEvents()


def on_all_resources_checked(dialog, success, results):
    """Handle completion of resource check"""
    if dialog:
        dialog.setValue(100)
        
        if success:
            dialog.setLabelText("All resources are available")
        else:
            missing_resources = [name for name, result in results.items() if not result['available']]
            dialog.setLabelText(f"Missing resources: {', '.join(missing_resources)}")
        
        # Close the dialog after a short delay
        QApplication.processEvents()
        time.sleep(1)
        dialog.close()
        
        # Show a message if there are missing resources
        if not success:
            missing_resource_messages = []
            for name, result in results.items():
                if not result['available']:
                    missing_resource_messages.append(f"{name}: {result['message']}")
            
            message = "Some required resources are missing:\n\n" + "\n".join(missing_resource_messages)
            
            QMessageBox.warning(
                dialog.parent(), 
                "Missing Resources",
                message + "\n\nThe application may not function correctly without these resources."
            )


# Resource check functions

def check_pytorch() -> Tuple[bool, str]:
    """Check if PyTorch is available"""
    try:
        import torch
        return True, f"PyTorch {torch.__version__} is available"
    except ImportError:
        return False, "PyTorch is not installed"


def install_pytorch() -> Tuple[bool, str]:
    """Install PyTorch"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio"])
        return True, "PyTorch installed successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to install PyTorch: {str(e)}"


def check_whisper() -> Tuple[bool, str]:
    """Check if Whisper is available"""
    try:
        import whisper
        return True, "Whisper is available"
    except ImportError:
        return False, "Whisper is not installed"


def install_whisper() -> Tuple[bool, str]:
    """Install Whisper"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai-whisper"])
        return True, "Whisper installed successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to install Whisper: {str(e)}"


def check_nltk_data() -> Tuple[bool, str]:
    """Check if NLTK data is available"""
    try:
        import nltk
        from nltk.data import find
        
        # Check for punkt
        try:
            find('tokenizers/punkt')
            punkt_available = True
        except LookupError:
            punkt_available = False
        
        # Check for stopwords
        try:
            from nltk.corpus import stopwords
            stopwords.words('english')
            stopwords_available = True
        except (LookupError, ImportError):
            stopwords_available = False
        
        if punkt_available and stopwords_available:
            return True, "NLTK data is available"
        else:
            missing = []
            if not punkt_available:
                missing.append("punkt")
            if not stopwords_available:
                missing.append("stopwords")
            return False, f"Missing NLTK data: {', '.join(missing)}"
    except ImportError:
        return False, "NLTK is not installed"


def install_nltk_data() -> Tuple[bool, str]:
    """Install NLTK data"""
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        return True, "NLTK data installed successfully"
    except Exception as e:
        return False, f"Failed to install NLTK data: {str(e)}"


def check_spacy_model(model_name: str) -> Tuple[bool, str]:
    """Check if a SpaCy model is available"""
    try:
        import spacy
        try:
            spacy.load(model_name)
            return True, f"SpaCy model {model_name} is available"
        except (OSError, IOError):
            return False, f"SpaCy model {model_name} is not installed"
    except ImportError:
        return False, "SpaCy is not installed"


def install_spacy_model(model_name: str) -> Tuple[bool, str]:
    """Install a SpaCy model"""
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
        return True, f"SpaCy model {model_name} installed successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to install SpaCy model {model_name}: {str(e)}"


def check_bertopic() -> Tuple[bool, str]:
    """Check if BERTopic is available"""
    try:
        import bertopic
        return True, "BERTopic is available"
    except ImportError:
        return False, "BERTopic is not installed"


def install_bertopic() -> Tuple[bool, str]:
    """Install BERTopic"""
    try:
        # Install required dependencies first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sentence-transformers", "hdbscan", "umap-learn"])
        
        # Install BERTopic
        subprocess.check_call([sys.executable, "-m", "pip", "install", "bertopic"])
        return True, "BERTopic installed successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to install BERTopic: {str(e)}"