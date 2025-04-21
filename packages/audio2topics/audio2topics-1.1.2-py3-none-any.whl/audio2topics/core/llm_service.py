#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Service module for the Audio to Topics application.
Provides functionality for interacting with OpenAI and Anthropic APIs.
"""

import os
import json
import logging
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import requests
from .secure_config import SecureLLMConfig

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    """Container for LLM responses"""
    text: str
    error: Optional[str] = None

class LLMWorker(QThread):
    """Worker thread for LLM requests"""
    response_received = pyqtSignal(LLMResponse)
    progress_updated = pyqtSignal(int, str)
    
    def __init__(self, service, topics_words: Dict, prompt_type: str = "refine_topics"):
        super().__init__()
        self.service = service
        self.topics_words = topics_words
        self.prompt_type = prompt_type
        self.is_running = True

    def run(self):
        """Execute the LLM request"""
        try:
            self.progress_updated.emit(10, f"Preparing topic data for {self.service.provider.capitalize()}...")
            
            # Filter out outlier topic if present
            topics_to_process = {k: v for k, v in self.topics_words.items() if k != -1}
            total_topics = len(topics_to_process)
            
            # Process topics in batches if there are many
            MAX_TOPICS_PER_BATCH = 5
            topic_batches = []
            current_batch = {}
            
            for i, (topic_id, words) in enumerate(topics_to_process.items()):
                current_batch[topic_id] = words
                if len(current_batch) >= MAX_TOPICS_PER_BATCH or i == len(topics_to_process) - 1:
                    topic_batches.append(current_batch)
                    current_batch = {}
            
            # Process each batch and combine results
            refined_topics = {}
            
            for i, batch in enumerate(topic_batches):
                progress = 10 + (i / len(topic_batches) * 80)
                self.progress_updated.emit(int(progress), f"Processing topics batch {i+1}/{len(topic_batches)}...")
                
                # Get response for this batch
                if self.service.provider == "anthropic":
                    response = self.service.get_anthropic_response(batch)
                else:  # openai
                    response = self.service.get_openai_response(batch)
                
                if response.error:
                    raise Exception(response.error)
                
                # Parse response to extract refined topics
                batch_topics = self._parse_refined_topics(response.text, batch.keys())
                refined_topics.update(batch_topics)
            
            self.progress_updated.emit(90, "Processing complete, finalizing results...")
            
            if self.is_running:  # Check if we should still emit the response
                self.response_received.emit(LLMResponse(text=json.dumps(refined_topics)))
                
        except Exception as e:
            logger.error(f"Error in LLM worker: {str(e)}", exc_info=True)
            self.response_received.emit(LLMResponse(text="", error=str(e)))
    
    def _parse_refined_topics(self, text: str, topic_ids: List[int]) -> Dict[int, str]:
        """Parse the LLM response to extract refined topics"""
        refined_topics = {}
        
        try:
            # First try to parse as JSON
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict):
                    # Convert string keys to integers
                    for key, value in parsed.items():
                        try:
                            topic_id = int(key)
                            if topic_id in topic_ids:
                                refined_topics[topic_id] = value
                        except ValueError:
                            continue
                    return refined_topics
            except json.JSONDecodeError:
                pass
            
            # If not JSON, try to parse from text format like "Topic X: Description"
            lines = text.split('\n')
            current_topic = None
            current_description = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check for topic header pattern
                import re
                topic_match = re.match(r"^(?:Topic\s*)?(\d+)[:\.\)-]", line)
                
                if topic_match:
                    # Save previous topic if exists
                    if current_topic is not None and current_description:
                        refined_topics[current_topic] = '\n'.join(current_description).strip()
                        current_description = []
                    
                    # Extract topic ID
                    try:
                        topic_id = int(topic_match.group(1))
                        if topic_id in topic_ids:
                            current_topic = topic_id
                            # Extract description from the rest of this line
                            desc = line[topic_match.end():].strip()
                            if desc:
                                current_description.append(desc)
                    except ValueError:
                        current_topic = None
                elif current_topic is not None:
                    current_description.append(line)
            
            # Save last topic
            if current_topic is not None and current_description:
                refined_topics[current_topic] = '\n'.join(current_description).strip()
        
        except Exception as e:
            logger.error(f"Error parsing refined topics: {str(e)}", exc_info=True)
        
        # If we couldn't parse anything, create default descriptions
        if not refined_topics:
            for topic_id in topic_ids:
                refined_topics[topic_id] = f"Topic {topic_id}"
        
        return refined_topics

    def stop(self):
        """Stop the worker thread"""
        self.is_running = False


class LLMService(QObject):
    """Service for managing LLM interactions with OpenAI and Anthropic"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize secure config handler
        self.config = SecureLLMConfig()
        self.config.load()  # Load the configuration
        
        # Properties come from the secure config
        self.anthropic_key = self.config.anthropic_key
        self.openai_key = self.config.openai_key
        self.provider = self.config.provider
        self.temperature = self.config.temperature
        self.max_tokens = self.config.max_tokens

    def save_config(self, anthropic_key: str, openai_key: str, provider: str,
                   temperature: float = None, max_tokens: int = None):
        """Save API keys securely"""
        success = self.config.save(
            anthropic_key=anthropic_key,
            openai_key=openai_key,
            provider=provider,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        if success:
            # Update current instance values
            self.anthropic_key = anthropic_key
            self.openai_key = openai_key
            self.provider = provider
            if temperature is not None:
                self.temperature = temperature
            if max_tokens is not None:
                self.max_tokens = max_tokens
                
        return success

    def get_anthropic_response(self, topics_words: Dict[int, List]) -> LLMResponse:
        """Get response from Anthropic's Claude for topic refinement"""
        if not self.anthropic_key:
            return LLMResponse(text="", error="Anthropic API key not configured")

        headers = {
            "x-api-key": self.anthropic_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        # Create a formatted prompt for topic refinement
        system_message = (
            "You are an expert at analyzing topics and creating clear, concise descriptions. "
            "You will be given a set of automatically extracted topics, each represented by keywords. "
            "Your task is to identify what each topic represents and provide a short descriptive name and explanation."
        )
        
        prompt = "Here are the topics extracted from a set of documents:\n\n"
        
        for topic_id, words in topics_words.items():
            # Format keywords with their importance scores
            keywords = ", ".join([f"{word} ({score:.3f})" for word, score in words[:20]])
            prompt += f"Topic {topic_id}: {keywords}\n\n"
        
        prompt += (
            "For each topic, provide a concise description that captures its essence. "
            "Return your answers in this format:\n"
            "Topic 0: [Short descriptive name] - [Brief explanation]\n"
            "Topic 1: [Short descriptive name] - [Brief explanation]\n"
            "And so on for each topic.\n\n"
            "Be specific and precise in your descriptions, focusing on the subject matter represented by the keywords."
            "If you see that some of these topics are related or overlap, feel free to mention that at the end of your answer."
            "On the conterary if you see that some topics can possibly split into smaller once, feel free to mention that as well and why." 
        )

        # Claude 3 requires system message to be part of the first user message
        full_prompt = f"{system_message}\n\n{prompt}"
        messages = [{"role": "user", "content": full_prompt}]

        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json={
                    "messages": messages,
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature
                }
            )

            if response.status_code == 200:
                result = response.json()
                if "content" in result and isinstance(result["content"], list):
                    return LLMResponse(text=result["content"][0]["text"])
            
            return LLMResponse(text="", error=f"Anthropic API Error: {response.text}")

        except Exception as e:
            logger.error(f"Error calling Anthropic API: {str(e)}", exc_info=True)
            return LLMResponse(text="", error=f"Anthropic API Error: {str(e)}")

    def get_openai_response(self, topics_words: Dict[int, List]) -> LLMResponse:
        """Get response from OpenAI's GPT-4 for topic refinement"""
        if not self.openai_key:
            return LLMResponse(text="", error="OpenAI API key not configured")

        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }

        system_message = (
            "You are an expert at analyzing topics and creating clear, concise descriptions. "
            "You will be given a set of automatically extracted topics, each represented by keywords. "
            "Your task is to identify what each topic represents and provide a short descriptive name and explanation."
        )
        
        prompt = "Here are the topics extracted from a set of documents:\n\n"
        
        for topic_id, words in topics_words.items():
            # Format keywords with their importance scores
            keywords = ", ".join([f"{word} ({score:.3f})" for word, score in words[:20]])
            prompt += f"Topic {topic_id}: {keywords}\n\n"
        
        prompt += (
            "For each topic, provide a concise description that captures its essence. "
            "Return your answers in this format:\n"
            "Topic 0: [Short descriptive name] - [Brief explanation]\n"
            "Topic 1: [Short descriptive name] - [Brief explanation]\n"
            "And so on for each topic.\n\n"
            "Be specific and precise in your descriptions, focusing on the subject matter represented by the keywords."
            "If you see that some of these topics are related or overlap, feel free to mention that at the end of your answer."
            "On the conterary if you see that some topics can possibly split into smaller once, feel free to mention that as well and why." 
        )

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json={
                    "model": "gpt-4-turbo",
                    "messages": messages,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                }
            )

            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return LLMResponse(text=result["choices"][0]["message"]["content"])
            
            return LLMResponse(text="", error=f"OpenAI API Error: {response.text}")

        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}", exc_info=True)
            return LLMResponse(text="", error=f"OpenAI API Error: {str(e)}")

    def create_worker(self, topics_words: Dict[int, List], prompt_type: str = "refine_topics") -> LLMWorker:
        """Create a worker thread for handling LLM requests"""
        return LLMWorker(self, topics_words, prompt_type)
    
    def is_configured(self) -> bool:
        """Check if the service is configured with API keys"""
        return self.config.is_configured()
        
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get available models for each provider"""
        return {
            "anthropic": ["claude-3-5-sonnet-20241022"],
            "openai": ["gpt-4"]
        }
        
    def clear_keys(self) -> bool:
        """Clear API keys from storage - useful for security or when user wants to reset"""
        success = self.config.clear()
        if success:
            self.anthropic_key = ""
            self.openai_key = ""
        return success