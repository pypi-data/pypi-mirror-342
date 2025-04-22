"""
Log collectors for MERIT monitoring.

This module provides base functionality for collectors that extract data
from log files in various formats.

API instrumentation collectors for MERIT monitoring.

This module provides base functionality for collectors that use direct
API instrumentation to capture LLM interaction data.
Network traffic collectors for MERIT monitoring.

This module provides base functionality for collectors that monitor
network traffic such as API calls and HTTP requests/responses.
"""

import os
import time
import queue
from datetime import datetime
from typing import Dict, Any, List, Optional, Set, Pattern
import re
from pathlib import Path
import gzip
import threading

from .base import BaseDataCollector, CollectionResult, CollectionStatus
from ..models import LLMInteraction, LLMRequest, LLMResponse, TokenInfo

class BaseNetworkTrafficCollector(BaseDataCollector):
    """
    Base class for collectors that monitor network traffic.
    
    This collector type specializes in intercepting and analyzing
    network traffic, particularly API calls to LLM providers.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the network traffic collector.
        
        Args:
            config: Configuration dictionary with the following options:
                - buffer_size: Max number of interactions to store in memory (default: 1000)
                - include_model_patterns: List of model name patterns to include
                - exclude_model_patterns: List of model name patterns to exclude
                - enabled_providers: List of provider names to monitor (default: all)
        """
        super().__init__(config or {})
        self.buffer_size = self.config.get("buffer_size", 1000)
        self.include_model_patterns = self.config.get("include_model_patterns", [])
        self.exclude_model_patterns = self.config.get("exclude_model_patterns", [])
        self.enabled_providers = self.config.get("enabled_providers", ["openai", "anthropic", "google", "azure", "cohere"])
        
        # Compile model patterns
        self._include_patterns = [re.compile(pattern) for pattern in self.include_model_patterns]
        self._exclude_patterns = [re.compile(pattern) for pattern in self.exclude_model_patterns]
        
        # Internal state
        self._interaction_queue = queue.Queue(maxsize=self.buffer_size)
        self._active_requests: Dict[str, Dict[str, Any]] = {}  # request_id -> request_data
        self._processing_thread: Optional[threading.Thread] = None
        self._request_count = 0
        self._response_count = 0
    
    def start(self) -> None:
        """Start collecting network traffic data in the background."""
        super().start()
        
        # Start background thread for processing interactions
        if not self._processing_thread or not self._processing_thread.is_alive():
            self._processing_thread = threading.Thread(
                target=self._process_interactions,
                daemon=True
            )
            self._processing_thread.start()
    
    def stop(self) -> None:
        """Stop collecting network traffic data and clean up resources."""
        super().stop()
        
        # Stop processing thread
        if self._processing_thread and self._processing_thread.is_alive():
            # Add None to the queue to signal thread to exit
            try:
                self._interaction_queue.put(None, block=False)
            except queue.Full:
                pass
                
            # Wait for thread to finish
            self._processing_thread.join(timeout=5.0)
    
    def collect(self) -> CollectionResult:
        """
        Collect all available interactions from the buffer.
        
        Returns:
            CollectionResult with the data collected
        """
        result = CollectionResult(
            status=CollectionStatus.SUCCESS,
            start_time=datetime.now()
        )
        
        interactions = []
        try:
            # Get all items from the queue without waiting
            while not self._interaction_queue.empty() and result.items_processed < self.buffer_size:
                try:
                    item = self._interaction_queue.get_nowait()
                    if item is not None:  # None is a signal to stop
                        interactions.append(item)
                        result.items_processed += 1
                        result.items_collected += 1
                        self._interaction_queue.task_done()
                except queue.Empty:
                    break
            
            # Add interactions to result
            result.data = interactions
            
            # Determine final status
            if result.items_processed == 0:
                result.status = CollectionStatus.SUCCESS  # No data is still success
        
        except Exception as e:
            result.status = CollectionStatus.FAILURE
            result.error = str(e)
        
        finally:
            result.end_time = datetime.now()
            return result
    
    def record_request(self, provider: str, endpoint: str, 
                       request_data: Dict[str, Any], 
                       request_id: Optional[str] = None) -> str:
        """
        Record a network request.
        
        This should be called before sending a request to the service.
        
        Args:
            provider: Name of the service provider (e.g., "openai", "anthropic")
            endpoint: API endpoint (e.g., "/v1/chat/completions")
            request_data: Complete request data including parameters
            request_id: Optional ID for the request (will be generated if not provided)
            
        Returns:
            The request ID (useful for linking to the response)
        """
        if not self.is_running:
            return request_id or ""
            
        if provider.lower() not in [p.lower() for p in self.enabled_providers]:
            return request_id or ""
        
        try:
            # Generate request ID if not provided
            if not request_id:
                import uuid
                request_id = str(uuid.uuid4())
                
            # Create request object with metadata
            req_obj = {
                "id": request_id,
                "provider": provider,
                "endpoint": endpoint,
                "timestamp": datetime.now().isoformat(),
                "data": request_data
            }
            
            # Extract model info for filtering
            model = self._extract_model_from_request(provider, request_data)
            if model:
                req_obj["model"] = model
                
                # Skip if model doesn't match filters
                if not self._should_include_model(model):
                    return request_id
            
            # Store in active requests map
            self._active_requests[request_id] = req_obj
            self._request_count += 1
            
            return request_id
            
        except Exception as e:
            # Log error but don't fail
            print(f"Error recording network request: {str(e)}")
            return request_id or ""
    
    def record_response(self, request_id: str, response_data: Dict[str, Any], 
                        status_code: int = 200, error: Optional[str] = None) -> None:
        """
        Record a network response.
        
        This should be called after receiving a response from the service.
        
        Args:
            request_id: ID of the corresponding request
            response_data: Complete response data
            status_code: HTTP status code
            error: Error message if the request failed
        """
        if not self.is_running:
            return
            
        if not request_id or request_id not in self._active_requests:
            return
            
        try:
            # Get the request data
            request_obj = self._active_requests.pop(request_id)
            
            # Create response object
            resp_obj = {
                "request_id": request_id,
                "timestamp": datetime.now().isoformat(),
                "status_code": status_code,
                "data": response_data
            }
            
            if error:
                resp_obj["error"] = error
            
            # Calculate latency
            try:
                req_time = datetime.fromisoformat(request_obj["timestamp"])
                resp_time = datetime.fromisoformat(resp_obj["timestamp"])
                latency = (resp_time - req_time).total_seconds()
                resp_obj["latency"] = latency
            except (ValueError, KeyError):
                # If timestamp is missing or invalid, skip latency calculation
                pass
            
            # Create complete interaction
            interaction = {
                "request": request_obj,
                "response": resp_obj
            }
            
            # Add to queue for processing
            try:
                self._interaction_queue.put(interaction, block=False)
                self._response_count += 1
            except queue.Full:
                # Queue is full, discard oldest item and try again
                try:
                    self._interaction_queue.get_nowait()
                    self._interaction_queue.put(interaction, block=False)
                except (queue.Empty, queue.Full):
                    pass
        
        except Exception as e:
            # Log error but don't fail
            print(f"Error recording network response: {str(e)}")
    
    def _process_interactions(self) -> None:
        """
        Background thread method for processing interactions.
        
        This continuously processes interactions from the queue and
        notifies callbacks.
        """
        while self.is_running:
            try:
                # Get the next interaction from the queue
                interaction = self._interaction_queue.get(block=True, timeout=1.0)
                
                # None is the signal to stop
                if interaction is None:
                    break
                
                # Process the interaction
                self._process_interaction(interaction)
                
                # Mark as done
                self._interaction_queue.task_done()
                
            except queue.Empty:
                # Timeout, check if we're still running
                continue
                
            except Exception as e:
                # Log error but continue
                print(f"Error processing network interaction: {str(e)}")
    
    def _process_interaction(self, interaction: Dict[str, Any]) -> None:
        """
        Process a single interaction.
        
        This extracts relevant data, converts to LLM models if possible,
        and notifies callbacks.
        
        Args:
            interaction: Raw interaction data with request and response
        """
        try:
            # Notify raw data callbacks
            self._notify_callbacks(interaction)
            
            # Convert to LLM interaction if possible
            llm_interaction = self._create_interaction(interaction)
            if llm_interaction:
                self._notify_callbacks(llm_interaction)
                
        except Exception as e:
            # Log error but don't fail
            print(f"Error processing interaction: {str(e)}")
    
    def _create_interaction(self, data: Dict[str, Any]) -> Optional[LLMInteraction]:
        """
        Convert raw API data to an LLMInteraction object.
        
        Args:
            data: Raw interaction data with request and response
            
        Returns:
            LLMInteraction object or None if conversion not possible
        """
        try:
            request_obj = data.get("request", {})
            response_obj = data.get("response", {})
            
            if not request_obj or not response_obj:
                return None
                
            # Get provider and endpoint
            provider = request_obj.get("provider", "")
            endpoint = request_obj.get("endpoint", "")
            
            # Get request and response data
            request_data = request_obj.get("data", {})
            response_data = response_obj.get("data", {})
            
            # Extract information based on provider and endpoint
            prompt, completion, token_info = self._extract_provider_specific_data(
                provider, endpoint, request_data, response_data
            )
            
            if not prompt:  # No valid LLM data found
                return None
            
            # Create request object
            request_id = request_obj.get("id", "")
            model = request_obj.get("model") or self._extract_model_from_request(provider, request_data)
            temperature = request_data.get("temperature")
            max_tokens = request_data.get("max_tokens")
            
            request = LLMRequest(
                id=request_id,
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Create response object
            status = "success" if response_obj.get("status_code", 200) < 400 else "error"
            latency = response_obj.get("latency")
            
            response = LLMResponse(
                request_id=request_id,
                completion=completion,
                model=model,
                tokens=token_info,
                status=status,
                latency=latency
            )
            
            # Create complete interaction
            return LLMInteraction(request=request, response=response)
        
        except Exception as e:
            # Log error but don't fail
            print(f"Error creating LLM interaction: {str(e)}")
            return None
    
    def _extract_provider_specific_data(self, provider: str, endpoint: str,
                                        request_data: Dict[str, Any],
                                        response_data: Dict[str, Any]) -> tuple[str, str, Optional[TokenInfo]]:
        """
        Extract provider-specific data from request and response.
        
        Different providers use different request/response formats, so we need
        provider-specific logic to extract the relevant data.
        
        Args:
            provider: Provider name
            endpoint: API endpoint
            request_data: Request data
            response_data: Response data
            
        Returns:
            Tuple of (prompt, completion, token_info)
        """
        # This method should be implemented by subclasses
        return "", "", None
    
    def _extract_model_from_request(self, provider: str, request_data: Dict[str, Any]) -> Optional[str]:
        """
        Extract model name from request data.
        
        Args:
            provider: Provider name
            request_data: Request data
            
        Returns:
            Model name or None if not found
        """
        # This method should be implemented by subclasses
        return None
    
    def _should_include_model(self, model: str) -> bool:
        """
        Check if a model should be included based on patterns.
        
        Args:
            model: Model name to check
            
        Returns:
            Whether the model should be included
        """
        if not model:
            return True  # Include by default if no model info
            
        # If include patterns specified, model must match at least one
        if self._include_patterns:
            if not any(pattern.search(model) for pattern in self._include_patterns):
                return False
        
        # If exclude patterns specified, model must not match any
        if self._exclude_patterns:
            if any(pattern.search(model) for pattern in self._exclude_patterns):
                return False
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the collector.
        
        Returns:
            Dictionary with status information
        """
        status = super().get_status()
        status.update({
            "request_count": self._request_count,
            "response_count": self._response_count,
            "pending_requests": len(self._active_requests),
            "queued_interactions": self._interaction_queue.qsize(),
            "enabled_providers": self.enabled_providers
        })
        return status

class BaseAPIInstrumentationCollector(BaseDataCollector):
    """
    Base class for collectors that use direct API instrumentation.
    
    This collector type specializes in capturing data through direct
    instrumentation of APIs, message queues, or webhooks.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the API instrumentation collector.
        
        Args:
            config: Configuration dictionary with collector options
                - buffer_size: Max number of interactions to store in memory (default: 1000)
                - process_interval: How often to process data in seconds (default: 1.0)
        """
        super().__init__(config or {})
        self.buffer_size = self.config.get("buffer_size", 1000)
        self.process_interval = self.config.get("process_interval", 1.0)
        
        # Internal state
        self._interaction_queue = queue.Queue(maxsize=self.buffer_size)
        self._processing_thread: Optional[threading.Thread] = None
        self._items_processed = 0
        self._items_collected = 0
    
    def start(self) -> None:
        """Start collecting data through API instrumentation."""
        super().start()
        
        # Start background thread for processing interactions
        if not self._processing_thread or not self._processing_thread.is_alive():
            self._processing_thread = threading.Thread(
                target=self._process_queue,
                daemon=True
            )
            self._processing_thread.start()
    
    def stop(self) -> None:
        """Stop collecting data and clean up resources."""
        super().stop()
        
        # Stop processing thread
        if self._processing_thread and self._processing_thread.is_alive():
            # Add None to the queue to signal thread to exit
            try:
                self._interaction_queue.put(None, block=False)
            except queue.Full:
                pass
                
            # Wait for thread to finish
            self._processing_thread.join(timeout=5.0)
    
    def collect(self) -> CollectionResult:
        """
        Collect all available interactions from the buffer.
        
        Returns:
            CollectionResult with the data collected
        """
        result = CollectionResult(
            status=CollectionStatus.SUCCESS,
            start_time=datetime.now()
        )
        
        interactions = []
        try:
            # Get all items from the queue without waiting
            while not self._interaction_queue.empty() and result.items_processed < self.buffer_size:
                try:
                    item = self._interaction_queue.get_nowait()
                    if item is not None:  # None is a signal to stop
                        interactions.append(item)
                        result.items_processed += 1
                        result.items_collected += 1
                        self._interaction_queue.task_done()
                except queue.Empty:
                    break
            
            # Add interactions to result
            result.data = interactions
            
        except Exception as e:
            result.status = CollectionStatus.FAILURE
            result.error = str(e)
        
        finally:
            result.end_time = datetime.now()
            return result
    
    def add_interaction(self, interaction: Dict[str, Any]) -> bool:
        """
        Add an interaction to the processing queue.
        
        Args:
            interaction: The interaction data to add
            
        Returns:
            bool: Whether the interaction was successfully added
        """
        if not self.is_running:
            return False
            
        try:
            self._interaction_queue.put(interaction, block=False)
            return True
        except queue.Full:
            # Queue is full, discard oldest item and try again
            try:
                self._interaction_queue.get_nowait()
                self._interaction_queue.put(interaction, block=False)
                return True
            except (queue.Empty, queue.Full):
                return False
    
    def _process_queue(self) -> None:
        """
        Background thread method for processing the interaction queue.
        
        This continuously processes interactions from the queue and
        notifies callbacks.
        """
        while self.is_running:
            try:
                # Get the next interaction from the queue
                interaction = self._interaction_queue.get(block=True, timeout=self.process_interval)
                
                # None is the signal to stop
                if interaction is None:
                    break
                
                # Process the interaction
                self._process_interaction(interaction)
                self._items_processed += 1
                
                # Mark as done
                self._interaction_queue.task_done()
                
            except queue.Empty:
                # Timeout, check if we're still running
                continue
                
            except Exception as e:
                # Log error but continue
                print(f"Error processing interaction: {str(e)}")
    
    def _process_interaction(self, interaction: Dict[str, Any]) -> None:
        """
        Process a single interaction.
        
        This extracts relevant data, converts to LLM models if possible,
        and notifies callbacks.
        
        Args:
            interaction: Raw interaction data
        """
        try:
            # Notify raw data callbacks
            self._notify_callbacks(interaction)
            
            # Convert to LLM interaction if possible
            llm_interaction = self._create_interaction(interaction)
            if llm_interaction:
                self._notify_callbacks(llm_interaction)
                self._items_collected += 1
                
        except Exception as e:
            # Log error but don't fail
            print(f"Error processing interaction: {str(e)}")
    
    def _create_interaction(self, data: Dict[str, Any]) -> Optional[LLMInteraction]:
        """
        Convert raw data to an LLMInteraction object.
        
        Args:
            data: Raw interaction data
            
        Returns:
            LLMInteraction object or None if conversion not possible
        """
        # This method should be implemented by subclasses
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the collector.
        
        Returns:
            Dictionary with status information
        """
        status = super().get_status()
        status.update({
            "items_processed": self._items_processed,
            "items_collected": self._items_collected,
            "queued_interactions": self._interaction_queue.qsize()
        })
        return status

class BaseLogCollector(BaseDataCollector):
    """
    Base class for collectors that extract data from log files.
    
    This collector type specializes in reading and parsing log files
    to extract structured information about interactions. It provides
    common functionality for file operations, monitoring, and reading.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the log collector.
        
        Args:
            config: Configuration dictionary with the following options:
                - log_path: Path to log file or directory of log files
                - file_pattern: Glob pattern for log files (default: "*.log")
                - format: Format of log entries ("json" or "regex")
                - regex_pattern: Regex pattern for extracting data (if format="regex")
                - json_path: JSON path to data (if format="json")
                - tail: Whether to watch files for new data (default: False)
                - tail_interval: How often to check for new data in seconds (default: 1.0)
                - batch_size: Number of log entries to process at once (default: 100)
                - max_history: Max number of historical log entries to process (default: 1000)
        """
        super().__init__(config or {})
        self.log_path = self.config.get("log_path", "")
        self.file_pattern = self.config.get("file_pattern", "*.log")
        self.format = self.config.get("format", "json")
        self.regex_pattern = self.config.get("regex_pattern", "")
        self.json_path = self.config.get("json_path", "")
        self.tail = self.config.get("tail", False)
        self.tail_interval = self.config.get("tail_interval", 1.0)
        self.batch_size = self.config.get("batch_size", 100)
        self.max_history = self.config.get("max_history", 1000)
        
        # Compiled regex pattern if needed
        self._compiled_regex: Optional[Pattern] = None
        if self.format == "regex" and self.regex_pattern:
            self._compiled_regex = re.compile(self.regex_pattern)
        
        # State for file monitoring
        self._file_positions: Dict[str, int] = {}
        self._processed_files: Set[str] = set()
        self._monitor_thread: Optional[threading.Thread] = None
    
    def start(self) -> None:
        """
        Start collecting data from log files.
        
        If in tail mode, this starts a background thread to monitor log files
        for new data. Otherwise, it just prepares the collector for batch operations.
        """
        super().start()
        
        # Initialize file positions for monitoring
        if self.tail:
            # Start from end of files for tail mode
            for file_path in self._get_log_files():
                if os.path.isfile(file_path):
                    self._file_positions[file_path] = os.path.getsize(file_path)
            
            # Start monitoring thread
            if not self._monitor_thread or not self._monitor_thread.is_alive():
                self._monitor_thread = threading.Thread(
                    target=self._monitor_files, 
                    daemon=True
                )
                self._monitor_thread.start()
    
    def stop(self) -> None:
        """
        Stop collecting data from log files.
        
        This stops any background monitoring threads and cleans up resources.
        """
        super().stop()
        
        # Wait for monitor thread to finish if it's running
        if self._monitor_thread and self._monitor_thread.is_alive():
            # We can't directly stop the thread, but setting is_running to False
            # will cause it to exit on the next iteration
            self._monitor_thread.join(timeout=self.tail_interval * 2)
    
    def collect(self) -> CollectionResult:
        """
        Process log files and extract data.
        
        In batch mode, this processes all matching log files up to max_history.
        In tail mode with no background thread, this processes new entries since
        the last call.
        
        Returns:
            CollectionResult with the extracted data
        """
        start_time = datetime.now()
        result = CollectionResult(
            status=CollectionStatus.SUCCESS,
            start_time=start_time
        )
        
        try:
            # Get list of log files to process
            log_files = self._get_log_files()
            
            for file_path in log_files:
                if not os.path.isfile(file_path):
                    continue
                    
                # Skip already processed files in batch mode
                if not self.tail and file_path in self._processed_files:
                    continue
                
                # Get position to start reading from
                position = self._file_positions.get(file_path, 0)
                
                # Process the file
                new_position, file_result = self._process_file(
                    file_path, position, self.batch_size
                )
                
                # Update state
                self._file_positions[file_path] = new_position
                if new_position >= os.path.getsize(file_path):
                    self._processed_files.add(file_path)
                
                # Update result
                result.items_processed += file_result.items_processed
                result.items_collected += file_result.items_collected
                result.data.extend(file_result.data)
                
                if result.items_processed >= self.max_history:
                    break
            
            # Determine final status
            if result.items_processed == 0:
                result.status = CollectionStatus.SUCCESS  # No data is still success
            elif result.items_collected == 0:
                result.status = CollectionStatus.FAILURE
                result.error = "No valid data found in logs"
            elif result.items_collected < result.items_processed:
                result.status = CollectionStatus.PARTIAL
                result.error = f"Only processed {result.items_collected}/{result.items_processed} items"
        
        except Exception as e:
            result.status = CollectionStatus.FAILURE
            result.error = str(e)
        
        finally:
            result.end_time = datetime.now()
            return result
    
    def _get_log_files(self) -> List[str]:
        """
        Get list of log files to process based on configuration.
        
        Returns:
            List of file paths to process
        """
        if not self.log_path:
            return []
            
        log_path = Path(self.log_path)
        
        if log_path.is_file():
            return [str(log_path)]
            
        if log_path.is_dir():
            # Get files matching the pattern
            files = list(log_path.glob(self.file_pattern))
            # Sort by modification time (newest first)
            files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            return [str(f) for f in files]
            
        return []
    
    def _process_file(self, file_path: str, start_position: int, max_entries: int) -> tuple[int, CollectionResult]:
        """
        Process a single log file and extract data.
        
        Args:
            file_path: Path to the log file
            start_position: Position to start reading from
            max_entries: Maximum number of entries to process
            
        Returns:
            Tuple of (new position, CollectionResult)
        """
        result = CollectionResult(
            status=CollectionStatus.SUCCESS,
            start_time=datetime.now()
        )
        
        # Detect if the file is gzipped
        is_gzipped = file_path.endswith('.gz')
        
        try:
            if is_gzipped:
                # Can't easily seek in gzipped files, so we read the whole thing
                # and then skip to the position we want
                with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                    lines = f.readlines()
                    lines = lines[start_position:]
                    
                    for i, line in enumerate(lines):
                        if i >= max_entries:
                            break
                            
                        self._process_log_entry(line.strip(), result)
                        
                    new_position = start_position + min(len(lines), max_entries)
            else:
                # For regular files, we can seek to the start position
                with open(file_path, 'r', encoding='utf-8') as f:
                    f.seek(start_position)
                    
                    for _ in range(max_entries):
                        line = f.readline()
                        if not line:
                            break
                            
                        self._process_log_entry(line.strip(), result)
                    
                    new_position = f.tell()
                    
        except Exception as e:
            result.status = CollectionStatus.FAILURE
            result.error = f"Error processing file {file_path}: {str(e)}"
            new_position = start_position  # Don't advance if there was an error
        
        result.end_time = datetime.now()
        return new_position, result
    
    def _process_log_entry(self, line: str, result: CollectionResult) -> None:
        """
        Process a single log entry and extract data.
        
        Args:
            line: Log line to process
            result: CollectionResult to update with processing results
        """
        result.items_processed += 1
        
        try:
            data = self._extract_data(line)
                
            if data:
                result.items_collected += 1
                result.data.append(data)
                
                # Notify callbacks if registered
                self._notify_callbacks(data)
                
                # Try to convert to structured data if possible
                interaction = self._create_interaction(data)
                if interaction:
                    self._notify_callbacks(interaction)
        
        except Exception as e:
            # Log error but continue processing
            print(f"Error processing log entry: {str(e)}")
    
    def _extract_data(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Extract data from a log entry.
        
        Args:
            line: Log line to process
            
        Returns:
            Extracted data dictionary or None if no valid data
        """
        # This method should be implemented by subclasses
        return None
    
    def _create_interaction(self, data: Dict[str, Any]) -> Optional[Any]:
        """
        Convert raw data to a structured interaction object.
        
        Args:
            data: Raw data dictionary from logs
            
        Returns:
            Structured interaction object or None if conversion not possible
        """
        try:
            # Try to create an LLMInteraction from the data
            # This is a flexible implementation that tries to extract as much information as possible
            # from the log data, even if it doesn't have the exact structure we expect
            
            # Extract request information
            request_data = {}
            if "request" in data and isinstance(data["request"], dict):
                request_data = data["request"]
            
            # Get request ID
            request_id = None
            if "id" in request_data:
                request_id = request_data["id"]
            elif "request_id" in data:
                request_id = data["request_id"]
            elif "id" in data:
                request_id = data["id"]
            else:
                # Generate a request ID if none exists
                import uuid
                request_id = str(uuid.uuid4())
            
            # Get prompt
            prompt = None
            if "prompt" in request_data:
                prompt = request_data["prompt"]
            elif "prompt" in data:
                prompt = data["prompt"]
            elif "query" in data:
                prompt = data["query"]
            elif "input" in data:
                prompt = data["input"]
            
            # Get model
            model = None
            if "model" in request_data:
                model = request_data["model"]
            elif "model" in data:
                model = data["model"]
            
            # Create request object
            from ..models import LLMRequest
            request = LLMRequest(
                id=request_id,
                prompt=prompt or "",
                model=model
            )
            
            # Extract response information
            response_data = {}
            if "response" in data and isinstance(data["response"], dict):
                response_data = data["response"]
            
            # Get completion
            completion = None
            if "completion" in response_data:
                completion = response_data["completion"]
            elif "completion" in data:
                completion = data["completion"]
            elif "output" in data:
                completion = data["output"]
            elif "response" in data and isinstance(data["response"], str):
                completion = data["response"]
            
            # Get status
            status = "success"  # Default to success
            if "status" in response_data:
                status = response_data["status"]
            elif "status" in data:
                status = data["status"]
            elif "error" in data and data["error"]:
                status = "error"
            
            # Get token information
            token_info = None
            from ..models import TokenInfo
            
            if "tokens" in data and isinstance(data["tokens"], dict):
                tokens_data = data["tokens"]
                input_tokens = tokens_data.get("input_tokens", 0)
                output_tokens = tokens_data.get("output_tokens", 0)
                total_tokens = tokens_data.get("total_tokens", input_tokens + output_tokens)
                
                token_info = TokenInfo(
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=total_tokens
                )
            
            # Create response object
            from ..models import LLMResponse
            response = LLMResponse(
                request_id=request_id,
                completion=completion or "",
                model=model,
                tokens=token_info,
                status=status
            )
            
            # Create interaction object
            from ..models import LLMInteraction
            return LLMInteraction(
                request=request,
                response=response
            )
            
        except Exception as e:
            # Log error but don't fail
            print(f"Error creating LLM interaction: {str(e)}")
            return None
    
    def _monitor_files(self) -> None:
        """
        Background thread method to continuously monitor log files for new data.
        
        This runs until the collector is stopped.
        """
        while self.is_running:
            try:
                # Collect data from log files
                self.collect()
                
                # Check for new log files
                log_files = self._get_log_files()
                for file_path in log_files:
                    if file_path not in self._file_positions and os.path.isfile(file_path):
                        # Start from end for new files
                        self._file_positions[file_path] = os.path.getsize(file_path)
                
                # Wait for next interval
                time.sleep(self.tail_interval)
                
            except Exception as e:
                # Log error but continue
                print(f"Error in log file monitor: {str(e)}")
                time.sleep(self.tail_interval)
