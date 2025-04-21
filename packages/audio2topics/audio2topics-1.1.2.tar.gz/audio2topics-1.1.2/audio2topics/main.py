#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio2Topics - PyQt application for topic modeling on audio files and text.

This application allows users to:
1. Transcribe audio files using Whisper
2. Process and clean text
3. Extract topics using BERTopic
4. Refine topics using LLM APIs (OpenAI or Anthropic)
5. Validate and visualize topics
"""

import sys
import os
import logging
import argparse
from PyQt5.QtWidgets import QApplication, QStyleFactory, QSplashScreen, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication, QTimer, QRect, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Import this to ensure it's available

from .ui.main_window import MainWindow
from .utils.resource_checker import check_and_install_resources 

# Define application version to display in the splach window
__version__ = "1.1.2"  

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        # Get the directory where this script is located
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error finding resource: {e}")
        # Fallback to looking in the current directory
        return relative_path

# Configure logging
def setup_logging(log_level=logging.INFO):
    """Set up logging configuration"""
    log_format = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    logging.basicConfig(level=log_level, format=log_format)
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.expanduser("~"), ".audio_to_topics", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Create file handler
    log_file = os.path.join(log_dir, "audio2topics.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Add file handler to root logger
    logging.getLogger().addHandler(file_handler)
    
    return logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Audio2Topics - Topic modeling on audio and text")
    
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging"
    )
    parser.add_argument(
        "--style", choices=QStyleFactory.keys(), help="Set application style"
    )
    parser.add_argument(
        "--skip-resource-check", action="store_true", help="Skip resource checking"
    )
    parser.add_argument(
        "--normal-scale", action="store_true", help="Use normal UI scaling instead of compact"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the application"""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logger = setup_logging(log_level)
    
    # Log application version
    logger.info(f"Starting Audio2Topics version {__version__}")
    
    # Set required attributes BEFORE creating QApplication
    if not args.normal_scale:
        # Use compact UI scaling (smaller UI elements)
        QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_Use96Dpi)
    else:
        # Use default scaling
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    
    # Create Qt application ONCE
    app = QApplication(sys.argv)
    app.setApplicationName("Audio2Topics")
    app.setOrganizationName("Audio2Topics")
    
    # Window icon with fallback
    icon_path = get_resource_path('resources/icons/app_icon.png')
    if os.path.exists(icon_path):
        app_icon = QPixmap(icon_path)
        app.setWindowIcon(QIcon(app_icon))
    else:
        # Create a fallback icon for the application window
        fallback_icon = QPixmap(64, 64)
        fallback_icon.fill(Qt.blue)
        app.setWindowIcon(QIcon(fallback_icon))
        logger.warning(f"Using fallback window icon because icon not found at: {icon_path}")
    
    # Apply global UI scaling for more compact interface components
    if not args.normal_scale:
        # Set a moderately sized application font (increase from 8 to 10)
        font = QFont("Arial", 12)
        app.setFont(font)
        
        # Use Fusion style for a more compact UI if no style is specified
        if not args.style:
            app.setStyle("Fusion")
            
        # Apply stylesheet for slightly compact UI elements
        app.setStyleSheet("""
            * { 
                font-size: 14px;
                padding: 2px; 
                margin: 2px; 
            }
            QToolBar { 
                icon-size: 24px; 
            }
            QProgressBar {
                text-align: center;
                padding-top: 4px;   /* Adjust this value until the text is centered */
                padding-bottom: 4px;
            }
            QPushButton { 
                min-height: 28px;
                max-height: 28px;
                padding: 3px 10px;
            }
            QGroupBox {
                /* Increase the margin so the title doesn't collide with the border */
                margin-top: 24px; /* Adjust as needed */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left; /* or 'top left' if you prefer */
                padding: 3px;  /* Extra space around the title text */
            }
            QComboBox {
                min-height: 24px;
                max-height: 28px;
            }
            QSpinBox, QDoubleSpinBox {
                min-height: 24px;
                max-height: 28px;
            }
            QTabBar::tab {
                padding: 6px 12px;
            }
            QHeaderView::section {
                padding: 3px;
            }
            QTableView::indicator, QTreeView::indicator {
                width: 30px;
            }
        """)
    
    # Set application style if specified (overrides the Fusion style set above)
    if args.style:
        app.setStyle(QStyleFactory.create(args.style))
    
    # Log available styles
    logger.debug(f"Available styles: {', '.join(QStyleFactory.keys())}")
    logger.debug(f"Using style: {app.style().objectName()}")
    
    # Create custom splash screen
    splash_pixmap = QPixmap(500, 350)
    splash_pixmap.fill(Qt.white)
    
    # Paint on the pixmap
    painter = QPainter(splash_pixmap)
    
    # Initialize icon position variables
    icon_y = 50  # Default margin from top
    icon_x = 250  # Default x position (center of 500px width)
    
    # Draw app icon for splash screen
    icon_path = get_resource_path('resources/icons/app_icon.png')
    if os.path.exists(icon_path):
        app_icon = QPixmap(icon_path)
        # Scale icon if needed
        if app_icon.width() > 200 or app_icon.height() > 200:
            app_icon = app_icon.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Position the icon in the center top area
        icon_x = (splash_pixmap.width() - app_icon.width()) // 2
        painter.drawPixmap(icon_x, icon_y, app_icon)
    else:
        # Create a simple fallback icon
        fallback_icon = QPixmap(64, 64)
        fallback_icon.fill(Qt.blue)
        painter.drawPixmap(icon_x, icon_y, fallback_icon)
        logger.warning(f"Using fallback splash icon because icon not found at: {icon_path}")
    
    # Draw application title
    title_font = QFont("Arial", 18, QFont.Bold)
    painter.setFont(title_font)
    painter.drawText(splash_pixmap.rect(), Qt.AlignHCenter | Qt.AlignTop, "Audio2Topics")
    
    # Draw developer credit
    credit_font = QFont("Arial", 8)
    painter.setFont(credit_font)
    credit_rect = splash_pixmap.rect()
    credit_rect.setTop(icon_y + 200)  # Position below icon
    painter.drawText(credit_rect, Qt.AlignHCenter | Qt.AlignTop, "Developed by: Mohsen Askar")
    
    # Draw version information
    version_font = QFont("Arial", 8)
    painter.setFont(version_font)
    version_rect = splash_pixmap.rect()
    version_rect.setTop(icon_y + 220)  # Position below developer credit
    painter.drawText(version_rect, Qt.AlignHCenter | Qt.AlignTop, f"Version {__version__}")
    
    # Finish painting
    painter.end()
    
    # Create splash screen with the custom pixmap
    splash = QSplashScreen(splash_pixmap)
    splash.show()
    app.processEvents()
    
    # Update splash screen message
    splash.showMessage("Starting Audio2Topics...", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
    app.processEvents()
    
    # Check for required resources if not skipped
    if not args.skip_resource_check:
        splash.showMessage("Checking required resources...", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
        app.processEvents()
        
        resources_available = check_and_install_resources()
        
        if not resources_available:
            logger.warning("Some required resources are missing. The application may not function correctly.")
            
            # Show warning after splash screen closes
            def show_resource_warning():
                QMessageBox.warning(
                    None, 
                    "Missing Resources",
                    "Some required resources could not be installed automatically.\n\n"
                    "The application will continue to run, but some features may not work correctly.\n\n"
                    "Please check the logs for more information."
                )
            
            QTimer.singleShot(0, show_resource_warning)
            
    # Create and show the main window
    splash.showMessage("Loading main window...", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
    app.processEvents()
    
    main_window = MainWindow()
    # Set icon directly on the main window
    icon_path = get_resource_path('resources/icons/app_icon.png')
    if os.path.exists(icon_path):
        main_window.setWindowIcon(QIcon(QPixmap(icon_path)))
    else:
        # Create a fallback icon
        fallback_icon = QPixmap(64, 64)
        fallback_icon.fill(Qt.blue)
        main_window.setWindowIcon(QIcon(fallback_icon))
        logger.warning(f"Using fallback window icon on main window because icon not found at: {icon_path}")
    
    # Add version to window title
    main_window.setWindowTitle(f"Audio2Topics v{__version__}")
        
    # Close splash screen and show main window
    splash.finish(main_window)
    main_window.setMinimumSize(800, 600)
    main_window.show()
    
    # Enter the application event loop
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()