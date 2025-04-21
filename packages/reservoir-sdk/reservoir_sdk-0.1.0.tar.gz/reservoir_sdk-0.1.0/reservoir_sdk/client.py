import json
import requests
import os
from typing import List, Dict, Any, Optional, Union


class ReservoirClient:
    """Client for interacting with the Reservoir backend API.
    
    This client provides a simple interface to submit queries to the Reservoir
    backend and check on the status of those queries.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "http://localhost:8000"):
        """Initialize the Reservoir client.
        
        Args:
            api_key: API key for authentication. If not provided, will check RESERVOIR_API_KEY env var.
            base_url: The base URL of the Reservoir API. Defaults to localhost.
        """
        self.api_key = api_key or os.environ.get("RESERVOIR_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either directly or via RESERVOIR_API_KEY environment variable")
            
        self.base_url = base_url
        self.models = {
            "active_speaker": "Active Speaker Detection",
            "conversation_confidence": "Conversation Confidence Analysis",
            "speech_transcription": "Speech Transcription"
        }
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests including authentication."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def query(self, 
              query_text: str,
              max_duration_minutes: float = 10.0,
              max_chunks: int = 20,
              min_confidence: float = 0.5,
              models: Optional[List[str]] = None,
              creators_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Submit a query to search for video segments.
        
        Args:
            query_text: The search query text
            max_duration_minutes: Maximum total duration of results in minutes
            max_chunks: Maximum number of video chunks to return
            min_confidence: Minimum conversation confidence score (0.0-1.0)
            models: List of models to use (defaults to all available models)
            creators_ids: List of creator IDs to filter by
            
        Returns:
            Dictionary containing job_id, result_url, and other metadata
        """
        if models is None:
            models = list(self.models.keys())
        
        if creators_ids is None:
            creators_ids = []
            
        url = f"{self.base_url}/api/query-videos"
        
        payload = {
            "query": query_text,
            "maxDurationMinutes": max_duration_minutes,
            "maxChunks": max_chunks,
            "minConfidence": min_confidence,
            "models": models,
            "creators_id": creators_ids
        }
        
        response = requests.post(url, json=payload, headers=self._get_headers())
        response.raise_for_status()
        
        return response.json()
    
    def get_query_status(self, job_id: str) -> Dict[str, Any]:
        """Check the status of a submitted query.
        
        Args:
            job_id: The job ID returned from the query method
            
        Returns:
            Dictionary containing status information
        """
        url = f"{self.base_url}/api/query-status/{job_id}"
        
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        return response.json()
    
    def list_creators(self) -> List[Dict[str, Any]]:
        """Get a list of all available creators.
        
        Returns:
            List of creator objects with id, name, and avatar URL
        """
        url = f"{self.base_url}/api/get-creators"
        
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        return response.json().get("creators", [])
    
    def get_available_models(self) -> Dict[str, str]:
        """Get a dictionary of available models.
        
        Returns:
            Dictionary mapping model IDs to human-readable names
        """
        return self.models.copy() 