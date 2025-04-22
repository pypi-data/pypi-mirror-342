"""
Gemini API Client for MERIT.

This module provides a client for the Google Gemini API that implements
the AIAPIClient interface.
"""
from typing import List, Dict, Any, Optional, Union

from google import genai
from google.genai import types

from .client import AIAPIClient

class GeminiClient(AIAPIClient):
    """
    A client for the Google Gemini API.
    
    This client implements the AIAPIClient interface and uses the
    Google Generative AI (genai) library to interact with the Gemini models.
    """
    
    def __init__(
        self,
        api_key: str,
        **kwargs
    ):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: The API key for the Gemini API.
            **kwargs: Additional parameters:
                - model: The model to use for text generation (alias for generation_model).
                - generation_model: The model to use for text generation.
                - embedding_model: The model to use for embeddings.
                - max_output_tokens: The maximum number of tokens to generate.
                - temperature: The temperature for text generation.
                - top_p: The top-p value for text generation.
                - top_k: The top-k value for text generation.
        """
        self.client = genai.Client(api_key=api_key)
        
        # Support both 'model' and 'generation_model' parameters
        self.generation_model = kwargs.get('model', kwargs.get('generation_model', 'gemini-1.5-pro'))
        self.embedding_model = kwargs.get('embedding_model', 'embedding-001')
        self.max_output_tokens = kwargs.get('max_output_tokens', 1024)
        self.temperature = kwargs.get('temperature', 0.1)
        self.top_p = kwargs.get('top_p', 0.95)
        self.top_k = kwargs.get('top_k', 40)
    
    def generate_text(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Generate text based on a prompt.
        
        Args:
            prompt: The prompt to generate text from.
            max_tokens: The maximum number of tokens to generate.
            temperature: The temperature for text generation.
            system_prompt: A system prompt to use.
            
        Returns:
            str: The generated text.
            
        Raises:
            TypeError: If prompt is not a string.
            ValueError: If temperature is not in the valid range (0.0-1.0).
        """
        # Type checking and validation
        if not isinstance(prompt, str):
            raise TypeError(f"Expected prompt to be a string, got {type(prompt)}")
        
        if temperature is not None and (temperature < 0.0 or temperature > 1.0):
            raise ValueError(f"Temperature must be between 0.0 and 1.0, got {temperature}")
            
        if max_tokens is not None and not isinstance(max_tokens, int):
            raise TypeError(f"Expected max_tokens to be an integer, got {type(max_tokens)}")
            
        if system_prompt is not None and not isinstance(system_prompt, str):
            raise TypeError(f"Expected system_prompt to be a string, got {type(system_prompt)}")
        
        # Set up the generation config
        config = types.GenerateContentConfig(
            max_output_tokens=max_tokens or self.max_output_tokens,
            temperature=temperature or self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
        )
        
        # Add system prompt if provided
        if system_prompt:
            config.system_instruction = system_prompt
        
        # Generate the content
        response = self.client.models.generate_content(
            model=self.generation_model,
            contents=prompt,
            config=config
        )
        
        # Return the generated text
        return response.text
    
    def get_embeddings(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Get embeddings for the given texts.
        
        Args:
            texts: A string or list of strings to get embeddings for.
            
        Returns:
            List[List[float]]: A list of embeddings, where each embedding is a list of floats.
            For a single input text, still returns a list containing one embedding.
        """
        # Ensure texts is a list
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = []
        
        for text in texts:
            result = self.client.models.embed_content(
                model=self.embedding_model,
                contents=text
            )
            
            # Convert ContentEmbedding to a list of floats
            if hasattr(result.embeddings, 'values'):
                # If it's a ContentEmbedding object with a 'values' attribute
                if hasattr(result.embeddings.values, 'tolist'):
                    embedding_values = result.embeddings.values.tolist()
                else:
                    embedding_values = result.embeddings.values
            elif isinstance(result.embeddings, list) and len(result.embeddings) == 1:
                # If it's a list containing a single embedding
                if hasattr(result.embeddings[0], 'values'):
                    # If the embedding has a 'values' attribute
                    if hasattr(result.embeddings[0].values, 'tolist'):
                        embedding_values = result.embeddings[0].values.tolist()
                    else:
                        embedding_values = result.embeddings[0].values
                else:
                    # If the embedding is already a list
                    embedding_values = result.embeddings[0]
            else:
                # Fallback to using the embeddings as is
                embedding_values = result.embeddings
            
            embeddings.append(embedding_values)
        
        return embeddings
