"""
MERIT Kafka Collector

This module provides a collector for monitoring LLM interactions via Kafka.
"""

import json
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from confluent_kafka import Consumer, KafkaError, KafkaException

from .base_collector import BaseAPIInstrumentationCollector, CollectionResult, CollectionStatus
from ..models import LLMInteraction, LLMRequest, LLMResponse, TokenInfo
from ...core.logging import get_logger

logger = get_logger(__name__)

class KafkaCollector(BaseAPIInstrumentationCollector):
    """
    Collector that extracts LLM interaction data from Kafka topics.
    
    This collector can subscribe to Kafka topics that contain LLM interaction
    data and process them in real-time.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize with Kafka configuration.
        
        Args:
            config: Configuration for the Kafka consumer
                - bootstrap_servers: Kafka bootstrap servers (default: localhost:9092)
                - topics: List of topics to subscribe to (default: ["llm-interactions"])
                - group_id: Consumer group ID (default: "merit-monitor")
                - poll_interval: How often to poll for messages in seconds (default: 1.0)
                - auto_offset_reset: Where to start consuming from (default: "latest")
                - session_timeout_ms: Consumer session timeout (default: 30000)
                - message_format: Format of messages (json, avro, custom, default: "json")
                - transform_fn: Function to transform raw messages into LLMInteraction objects
                - field_mapping: Dictionary mapping source fields to target fields
                - parser_options: Additional options for message parsing
                - auto_detect_format: Whether to try to auto-detect message format (default: True)
        """
        super().__init__(config or {})
        self.bootstrap_servers = self.config.get("bootstrap_servers", "localhost:9092")
        self.topics = self.config.get("topics", ["llm-interactions"])
        self.group_id = self.config.get("group_id", "merit-monitor")
        self.poll_interval = float(self.config.get("poll_interval", 1.0))
        self.auto_offset_reset = self.config.get("auto_offset_reset", "latest")
        self.session_timeout_ms = int(self.config.get("session_timeout_ms", 30000))
        self.message_format = self.config.get("message_format", "json")
        self.transform_fn = self.config.get("transform_fn", self._default_transform)
        self.field_mapping = self.config.get("field_mapping", {})
        self.parser_options = self.config.get("parser_options", {})
        self.auto_detect_format = self.config.get("auto_detect_format", True)
        
        # Internal state
        self._consumer = None
        self._running = False
        self._thread = None
        self._messages = []
        self._lock = threading.Lock()
        
    def start(self):
        """Start consuming from Kafka topics."""
        if self._running:
            logger.warning("Kafka collector already running")
            return
        
        # Create consumer
        consumer_config = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': self.auto_offset_reset,
            'session.timeout.ms': self.session_timeout_ms,
            'enable.auto.commit': True,
            'client.id': f'merit-kafka-collector-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'broker.address.family': 'v4'  # Force IPv4
        }
        
        try:
            self._consumer = Consumer(consumer_config)
            self._consumer.subscribe(self.topics)
            logger.info(f"Subscribed to topics: {self.topics}")
            
            # Start background thread
            self._running = True
            self._thread = threading.Thread(target=self._consume_loop, daemon=True)
            self._thread.start()
            logger.info("Kafka collector started")
            
        except KafkaException as e:
            logger.error(f"Failed to start Kafka collector: {str(e)}")
            self._running = False
            raise
    
    def stop(self):
        """Stop consuming from Kafka topics."""
        if not self._running:
            logger.warning("Kafka collector not running")
            return
        
        self._running = False
        if self._thread:
            self._thread.join(timeout=5.0)
        
        if self._consumer:
            self._consumer.close()
            self._consumer = None
        
        logger.info("Kafka collector stopped")
    
    def collect(self) -> CollectionResult:
        """
        Process collected messages.
        
        Returns:
            CollectionResult: The collected messages since last call
        """
        with self._lock:
            messages = self._messages
            self._messages = []
        
        result = CollectionResult(
            status=CollectionStatus.SUCCESS,
            data=[],
            items_processed=0,
            items_collected=0
        )
        
        for msg in messages:
            result.items_processed += 1
            try:
                interaction = self._process_message(msg)
                if interaction:
                    # Convert to dictionary for storage if needed
                    if isinstance(interaction, LLMInteraction):
                        interaction_dict = interaction.to_dict()
                    else:
                        interaction_dict = interaction
                    
                    result.data.append(interaction_dict)
                    result.items_collected += 1
                    
                    # Notify callbacks
                    self._notify_callbacks(interaction)
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
        
        # Add metadata
        result.metadata = {
            "source": "kafka",
            "topics": self.topics,
            "count": result.items_collected
        }
        
        return result
    
    def _consume_loop(self):
        """Background thread for consuming messages."""
        while self._running:
            try:
                msg = self._consumer.poll(self.poll_interval)
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        logger.debug(f"Reached end of partition {msg.partition()}")
                    else:
                        logger.error(f"Error consuming message: {msg.error()}")
                else:
                    # Process message
                    with self._lock:
                        self._messages.append(msg)
                    
            except Exception as e:
                logger.error(f"Error in Kafka consumer loop: {str(e)}")
                time.sleep(1)  # Avoid busy loop on error
    
    def _process_message(self, msg):
        """
        Process a Kafka message.
        
        Args:
            msg: Kafka message
            
        Returns:
            LLMInteraction: The processed interaction
        """
        try:
            # Extract message value
            value = msg.value()
            
            # Try to parse the message based on format
            data = self._parse_message(value)
            if data is None:
                return None
                
            # Apply field mapping if provided
            if self.field_mapping:
                data = self._apply_field_mapping(data)
                
            # Transform data to LLMInteraction
            return self.transform_fn(data)
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return None
    
    def _parse_message(self, value):
        """
        Parse a message based on its format.
        
        Args:
            value: Raw message value
            
        Returns:
            Parsed data or None if parsing failed
        """
        # Try JSON format first if auto-detect is enabled or format is json
        if self.auto_detect_format or self.message_format == "json":
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                if self.message_format == "json":
                    logger.error("Failed to parse JSON message")
                    return None
                # If auto-detect is enabled, continue to other formats
        
        # Try Avro format if specified
        if self.message_format == "avro":
            # TODO: Implement Avro support
            logger.warning("Avro format not yet supported")
            return None
            
        # For custom formats, return the raw value for the transform function to handle
        if self.message_format == "custom":
            return value
            
        # If we get here with auto-detect enabled, return the raw value as a last resort
        if self.auto_detect_format:
            return value
            
        # If format is not recognized and auto-detect is disabled, return None
        logger.warning(f"Unsupported message format: {self.message_format}")
        return None
    
    def _apply_field_mapping(self, data):
        """
        Apply field mapping to data.
        
        Args:
            data: Data to map
            
        Returns:
            Mapped data
        """
        if isinstance(data, bytes) or isinstance(data, str):
            # Can't apply field mapping to raw data
            return data
            
        result = {}
        
        # Process each mapping
        for target_field, source_field in self.field_mapping.items():
            # Handle nested fields with dot notation
            if isinstance(source_field, str) and '.' in source_field:
                # Extract value from nested source field
                parts = source_field.split('.')
                value = data
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        value = None
                        break
                
                if value is not None:
                    # Set value in nested target field
                    if '.' in target_field:
                        target_parts = target_field.split('.')
                        target = result
                        for i, part in enumerate(target_parts[:-1]):
                            if part not in target:
                                target[part] = {}
                            target = target[part]
                        target[target_parts[-1]] = value
                    else:
                        result[target_field] = value
            
            # Handle direct field mapping
            elif isinstance(source_field, str) and source_field in data:
                if '.' in target_field:
                    # Set value in nested target field
                    target_parts = target_field.split('.')
                    target = result
                    for i, part in enumerate(target_parts[:-1]):
                        if part not in target:
                            target[part] = {}
                        target = target[part]
                    target[target_parts[-1]] = data[source_field]
                else:
                    result[target_field] = data[source_field]
            
            # Handle function mapping
            elif callable(source_field):
                result[target_field] = source_field(data)
        
        # Include unmapped fields if no mappings were applied or if specified in options
        if not result or self.parser_options.get("include_unmapped_fields", True):
            # Start with the original data
            if not isinstance(data, dict):
                return result or data
                
            # Merge with mapped fields, giving precedence to mapped fields
            merged = dict(data)
            merged.update(result)
            return merged
            
        return result
    
    def _default_transform(self, data) -> LLMInteraction:
        """
        Default transformation function for Kafka messages.
        
        Args:
            data: Raw message data
            
        Returns:
            LLMInteraction: The transformed interaction
        """
        # Handle raw bytes or strings (custom formats)
        if isinstance(data, bytes) or isinstance(data, str):
            try:
                # Try to parse as JSON first
                if isinstance(data, bytes):
                    data = data.decode('utf-8')
                    
                if data.startswith('{') and data.endswith('}'):
                    try:
                        data = json.loads(data)
                    except json.JSONDecodeError:
                        # Not valid JSON, try custom format parsing
                        pass
                
                # Try custom format parsing if still a string
                if isinstance(data, str):
                    # Example: parse pipe-delimited format
                    if '|' in data:
                        parts = data.split('|')
                        if len(parts) >= 4:  # Minimum fields needed
                            data = {
                                "request": {
                                    "id": parts[1] if len(parts) > 1 else "",
                                    "prompt": parts[2] if len(parts) > 2 else ""
                                },
                                "model": parts[3] if len(parts) > 3 else "",
                                "response": {
                                    "status": parts[4] if len(parts) > 4 else "unknown"
                                }
                            }
                            
                            # Add token info if available
                            if len(parts) > 7:
                                try:
                                    data["tokens"] = {
                                        "input_tokens": int(parts[5]),
                                        "output_tokens": int(parts[6]),
                                        "total_tokens": int(parts[7])
                                    }
                                except (ValueError, IndexError):
                                    pass
            except Exception as e:
                logger.error(f"Error parsing custom format: {str(e)}")
                return None
        
        # If still not a dict, we can't process it
        if not isinstance(data, dict):
            logger.error(f"Unsupported data format: {type(data)}")
            return None
        
        # Extract token information with flexible field access
        tokens = None
        tokens_data = data.get("tokens") or data.get("usage") or data.get("token_usage")
        if tokens_data:
            # Handle different field names for token counts
            input_tokens = (
                tokens_data.get("input_tokens") or 
                tokens_data.get("prompt_tokens") or 
                tokens_data.get("input") or 
                0
            )
            output_tokens = (
                tokens_data.get("output_tokens") or 
                tokens_data.get("completion_tokens") or 
                tokens_data.get("output") or 
                0
            )
            total_tokens = (
                tokens_data.get("total_tokens") or 
                tokens_data.get("total") or 
                (input_tokens + output_tokens)
            )
            
            tokens = TokenInfo(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens
            )
        
        # Extract request data with flexible field access
        request_data = data.get("request") or data.get("input") or {}
        prompt = (
            request_data.get("prompt") or 
            request_data.get("query") or 
            request_data.get("text") or 
            data.get("prompt") or 
            ""
        )
        
        # Extract response data with flexible field access
        response_data = data.get("response") or data.get("output") or {}
        completion = (
            response_data.get("completion") or 
            response_data.get("text") or 
            response_data.get("content") or 
            data.get("completion") or 
            ""
        )
        
        # Extract status and error with flexible field access
        status = (
            response_data.get("status") or 
            response_data.get("result") or 
            "success"  # Default to success if not specified
        )
        
        error = (
            response_data.get("error") or 
            response_data.get("error_message") or 
            None
        )
        
        # Extract model with flexible field access
        model = (
            data.get("model") or 
            request_data.get("model") or 
            response_data.get("model") or 
            ""
        )
        
        # Extract latency with flexible field access
        latency = (
            response_data.get("latency") or 
            response_data.get("latency_ms", 0) / 1000 if "latency_ms" in response_data else None
        )
        
        # Extract timestamp with flexible field access
        timestamp_str = data.get("timestamp") or data.get("created_at")
        timestamp = None
        if timestamp_str:
            if isinstance(timestamp_str, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                except ValueError:
                    # If parsing fails, use current time
                    timestamp = datetime.now()
            else:
                timestamp = timestamp_str
        
        # Extract metadata
        metadata = data.get("metadata") or {}
        
        # Create request and response objects
        request = LLMRequest(
            prompt=prompt,
            model=model,
            timestamp=timestamp,
            metadata=metadata
        )
        
        response = LLMResponse(
            request_id=request.id,
            completion=completion,
            model=model,
            tokens=tokens,
            latency=latency,
            status=status,
            timestamp=timestamp
        )
        
        # Set error if present
        if error:
            response.metadata = response.metadata or {}
            response.metadata["error"] = error
        
        # Create LLMInteraction
        return LLMInteraction(
            request=request,
            response=response
        )
