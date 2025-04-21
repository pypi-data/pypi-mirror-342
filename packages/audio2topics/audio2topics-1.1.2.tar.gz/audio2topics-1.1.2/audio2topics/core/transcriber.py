#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcriber module for the Audio to Topics application.
Provides functionality for transcribing audio files using Whisper.
"""

import os
import tempfile
import torch
import whisper
import logging
from typing import Dict, List, Union, BinaryIO, Optional
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# Configure logging
logger = logging.getLogger(__name__)

class TranscriberWorker(QThread):
    """Worker thread for audio transcription with continuous progress tracking"""
    progress_updated = pyqtSignal(int, str)
    transcription_completed = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, audio_files, model_name="medium", device=None, auto_detect_language=True, language=None):
        # Fixed the parameters to match what's being passed
        super().__init__()
        self.audio_files = audio_files
        self.model_name = model_name
        self.device = device if device else "cuda" if torch.cuda.is_available() else "cpu"
        self.auto_detect_language = auto_detect_language
        self.language = language
        
        # Map language names to Whisper language codes
        self.language_codes = {
            "English": "en",
            "Norwegian Bokmål": "no",
            "Norwegian Nynorsk": "no"
        }
    
    def _get_segment_info(self, result):
        """
        Extract segment information from Whisper result.
        Returns tuple of (last_timestamp, has_timestamps)
        """
        try:
            # Check if we have segments in the result
            if hasattr(result, 'segments') and result.segments:
                segments = result.segments
                if isinstance(segments, list) and len(segments) > 0:
                    # Get the end time of the last segment
                    last_segment = segments[-1]
                    if isinstance(last_segment, dict) and 'end' in last_segment:
                        return last_segment['end'], True
            
            # For new versions of Whisper that might use a different structure
            if hasattr(result, 'json') and callable(result.json):
                json_data = result.json()
                if 'segments' in json_data and json_data['segments']:
                    segments = json_data['segments']
                    if len(segments) > 0 and 'end' in segments[-1]:
                        return segments[-1]['end'], True
                        
            # If we reached here, couldn't find timestamp info
            return 0, False
        except Exception as e:
            logger.warning(f"Error extracting segment info: {str(e)}")
            return 0, False
               
    def run(self):
        """Execute the transcription with enhanced progress tracking"""
        try:
            self.progress_updated.emit(5, f"Loading Whisper model ({self.model_name})...")
            
            # Load model
            model = whisper.load_model(self.model_name, device=self.device)
            
            self.progress_updated.emit(10, "Model loaded successfully")
            
            # Process each audio file
            transcriptions = {}
            total_files = len(self.audio_files)
            
            # Allocate progress percentage ranges
            # 10% - Model loading
            # 85% - File processing (divided among files)
            # 5% - Finalization
            progress_per_file = 85 / total_files
            
            for i, (filename, file_data) in enumerate(self.audio_files.items()):
                # Calculate starting progress for this file
                file_start_progress = 10 + (i * progress_per_file)
                self.progress_updated.emit(int(file_start_progress), f"Preparing {filename}...")
                
                # Process the audio file
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
                    temp_file.write(file_data)
                    temp_path = temp_file.name
                
                try:
                    # Load audio
                    self.progress_updated.emit(int(file_start_progress + progress_per_file * 0.1), 
                                             f"Loading audio: {filename}")
                    audio = whisper.load_audio(temp_path)
                    
                    # Get audio duration to estimate progress
                    audio_duration = len(audio) / whisper.audio.SAMPLE_RATE
                    
                    # Create custom callback for time-based progress tracking
                    def progress_callback(transcribed_time, total_time):
                        # Calculate progress as percentage of total audio duration
                        time_progress = min(0.95, transcribed_time / total_time) if total_time > 0 else 0
                        
                        # Calculate overall progress for the UI
                        current_progress = file_start_progress + (progress_per_file * time_progress)
                        
                        # Format times as minutes:seconds
                        transcribed_min, transcribed_sec = divmod(int(transcribed_time), 60)
                        total_min, total_sec = divmod(int(total_time), 60)
                        
                        # Update progress message with time information
                        self.progress_updated.emit(
                            int(current_progress),
                            f"Transcribing {filename}: " +
                            f"{int(time_progress * 100)}% " +
                            f"({transcribed_min}:{transcribed_sec:02d}/{total_min}:{total_sec:02d})"
                        )
                    
                    # Transcription options
                    options = {
                        "task": "transcribe",  # Always transcribe, never translate
                        "verbose": True,       # For better debugging
                        "fp16": False          # For better reliability
                    }
                    
                    # Add language settings if auto-detection is disabled
                    if not self.auto_detect_language and self.language:
                        lang_code = self.language_codes.get(self.language, "en")
                        options["language"] = lang_code
                        self.progress_updated.emit(
                            int(file_start_progress + progress_per_file * 0.15),
                            f"Starting transcription with language set to {self.language} ({lang_code}) for {filename}"
                        )
                    else:
                        self.progress_updated.emit(
                            int(file_start_progress + progress_per_file * 0.15),
                            f"Starting transcription with auto language detection for {filename}"
                        )
                    
                    # Create custom transcribe method that provides progress updates
                    result = self._transcribe_with_progress(model, audio, progress_callback, options)
                    transcriptions[filename] = result["text"]
                    
                    # Update progress for completed file
                    file_end_progress = 10 + ((i + 1) * progress_per_file)
                    self.progress_updated.emit(int(file_end_progress), 
                                             f"Completed {filename} ({i+1}/{total_files})")
                finally:
                    # Clean up temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            
            self.progress_updated.emit(95, "Finalizing transcriptions...")
            self.transcription_completed.emit(transcriptions)
            self.progress_updated.emit(100, "Transcription complete!")
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}", exc_info=True)
            self.error_occurred.emit(f"Error during transcription: {str(e)}")
    
    def _get_time_estimate(self, model_name):
        """Get estimated processing time per minute of audio based on model size"""
        # These are rough estimates and will vary based on hardware
        estimates = {
            "tiny": 0.5,    # 0.5x realtime on CPU
            "base": 0.6,    # 0.6x realtime on CPU
            "small": 1.5,   # 1.5x realtime on CPU
            "medium": 3,    # 3x realtime on CPU
            "large": 6,     # 6x realtime on CPU
            "turbo": 1.0    # Estimate for turbo model
        }
        return estimates.get(model_name, 3)  # Default to medium model estimate
    
    def _transcribe_with_progress(self, model, audio, progress_callback, options=None):
        """
        Custom wrapper around Whisper's transcribe method that provides progress updates
        based on audio duration rather than segment count.
        """
        if options is None:
            options = {}
            
        # Get the length of audio in seconds
        audio_len = len(audio) / whisper.audio.SAMPLE_RATE
        
        # For short audio (<30 sec), just use regular transcribe
        if audio_len < 30:
            progress_callback(0, audio_len)
            result = model.transcribe(audio, **options)
            progress_callback(audio_len, audio_len)
            return result
        
        # Store original functions we'll modify
        original_decode = model.decode
        
        # Track the current transcribed time
        transcribed_time = 0
        last_callback_time = 0  # Avoid sending too many updates
        
        # Create tracking wrapper around decode
        def decode_with_progress(*args, **kwargs):
            nonlocal transcribed_time, last_callback_time
            
            # Get the result from the original decode method
            result = original_decode(*args, **kwargs)
            
            # Try to extract segment timestamp information
            end_time, has_timestamps = self._get_segment_info(result)
            
            if has_timestamps:
                # Use the actual timestamp data
                transcribed_time = max(transcribed_time, end_time)
            else:
                # Fallback to incremental estimation
                transcribed_time += 10  # Assume roughly 10 seconds per decode call
            
            # Cap the time at audio_len
            transcribed_time = min(transcribed_time, audio_len)
            
            # Limit callback frequency (only send updates if time changed by at least 1 second)
            current_time = int(transcribed_time)
            if current_time > last_callback_time:
                progress_callback(transcribed_time, audio_len)
                last_callback_time = current_time
                
            return result
        
        try:
            # Replace decode method with our tracking version
            model.decode = decode_with_progress
            
            # Send initial progress
            progress_callback(0, audio_len)
            
            # Start transcription with our options
            result = model.transcribe(audio, **options)
            
            # Send final progress
            progress_callback(audio_len, audio_len)
            
            return result
        finally:
            # Restore original decode method
            model.decode = original_decode

class Transcriber(QObject):
    """
    Handles audio transcription using Whisper.
    
    This class manages the transcription of audio files to text using OpenAI's Whisper model.
    It uses a worker thread for processing to keep the UI responsive.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.transcriptions = {}
        
    def transcribe_files(self, 
                        audio_files: Dict[str, bytes], 
                        model_name: str = "medium", 
                        device: Optional[str] = None,
                        auto_detect_language: bool = True,
                        language: Optional[str] = None) -> TranscriberWorker:
        """
        Start transcribing audio files.
        
        Args:
            audio_files: Dictionary mapping filenames to file content as bytes
            model_name: Whisper model name to use
            device: Computation device to use (cuda, cpu, etc.)
            auto_detect_language: Whether to auto-detect language or use specified language
            language: Language to use for transcription if auto_detect_language is False
            
        Note:
            This method starts a worker thread. Results will be emitted via signals.
            
        Returns:
            The worker thread object that handles the transcription
        """
        # Create and configure worker
        device = device if device else "cuda" if torch.cuda.is_available() else "cpu"
        self.worker = TranscriberWorker(
            audio_files, 
            model_name, 
            device,
            auto_detect_language,
            language
        )
        
        # Clean up when done
        self.worker.finished.connect(self.worker.deleteLater)
        
        # Start the worker
        self.worker.start()
        
        return self.worker    
    def save_transcriptions(self, transcriptions: Dict[str, str], output_dir: str = None) -> List[str]:
        """
        Save transcriptions to text files.
        
        Args:
            transcriptions: Dictionary with filenames as keys and transcriptions as values
            output_dir: Directory to save files (default: current directory)
            
        Returns:
            List of paths to saved transcription files
        """
        saved_files = []
        
        if output_dir is None:
            output_dir = os.getcwd()
        
        os.makedirs(output_dir, exist_ok=True)
        
        for filename, text in transcriptions.items():
            # Create a filename for the transcription file
            base_name = os.path.splitext(os.path.basename(filename))[0]
            txt_filename = f"{base_name}_transcription.txt"
            file_path = os.path.join(output_dir, txt_filename)
            
            # Save text to a .txt file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            
            saved_files.append(file_path)
        
        return saved_files
        
    def get_available_devices(self):
        """
        Get available devices for transcription.
        
        Returns:
            List of available devices (CPU and GPUs if available)
        """
        devices = ["cpu"]
        
        if torch.cuda.is_available():
            devices = ["cuda"] + [f"cuda:{i}" for i in range(torch.cuda.device_count())]
            
        return devices
    
    def get_available_models(self):
        """
        Get available Whisper models.
        
        Returns:
            List of available model names
        """
        return ["tiny", "base", "small", "medium", "large", "turbo"]