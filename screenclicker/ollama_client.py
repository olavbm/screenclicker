"""
Ollama client module for local LLM interactions.
"""

import ollama
from typing import Optional, Dict, Any, List, Union
from .config import get_config


class OllamaClient:
    """Client for interacting with locally hosted Ollama server."""
    
    def __init__(self, host: Optional[str] = None, **kwargs):
        """Initialize Ollama client.
        
        Args:
            host: Ollama server host URL (uses global config if None)
            **kwargs: Additional arguments passed to ollama.Client
        """
        config = get_config()
        self.host = host if host is not None else config.url
        self.client = ollama.Client(host=self.host, **kwargs)
    
    def chat(self, model: str, messages: List[Dict[str, str]], 
             stream: bool = False, **kwargs) -> Union[Dict[str, Any], Any]:
        """Send chat completion request to Ollama.
        
        Args:
            model: Model name (e.g., 'llama2', 'mistral')
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream response
            **kwargs: Additional parameters (options, tools, etc.)
            
        Returns:
            Response dict from Ollama or iterator if stream=True
        """
        return self.client.chat(
            model=model,
            messages=messages,
            stream=stream,
            **kwargs
        )
    
    def generate(self, model: str, prompt: str, 
                 stream: bool = False, **kwargs) -> Union[Dict[str, Any], Any]:
        """Generate text completion.
        
        Args:
            model: Model name
            prompt: Input prompt
            stream: Whether to stream response
            **kwargs: Additional parameters (options, context, etc.)
            
        Returns:
            Response dict from Ollama or iterator if stream=True
        """
        return self.client.generate(
            model=model,
            prompt=prompt,
            stream=stream,
            **kwargs
        )
    
    def list(self) -> Dict[str, List[Dict[str, Any]]]:
        """List available models.
        
        Returns:
            Dict with 'models' key containing list of model info
        """
        return self.client.list()
    
    def show(self, name: str) -> Dict[str, Any]:
        """Show model details.
        
        Args:
            name: Model name
            
        Returns:
            Model details dict
        """
        return self.client.show(name)
    
    def pull(self, name: str, stream: bool = False) -> Union[Dict[str, Any], Any]:
        """Pull a model from registry.
        
        Args:
            name: Model name to pull
            stream: Whether to stream progress
            
        Returns:
            Pull response or iterator if stream=True
        """
        return self.client.pull(name=name, stream=stream)
    
    def embeddings(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate embeddings for text.
        
        Args:
            model: Model name
            prompt: Input text
            **kwargs: Additional parameters
            
        Returns:
            Dict with 'embedding' array
        """
        return self.client.embeddings(model=model, prompt=prompt, **kwargs)
    
    
    def is_connected(self) -> bool:
        """Check if Ollama server is accessible.
        
        Returns:
            True if server is reachable, False otherwise
        """
        try:
            self.client.list()
            return True
        except Exception:
            return False


# Convenience functions for quick usage
def quick_chat(model: Optional[str] = None, prompt: str = "", host: Optional[str] = None) -> str:
    """Quick chat completion.
    
    Args:
        model: Model name (uses global config default if None)
        prompt: User prompt
        host: Ollama server host (uses global config if None)
        
    Returns:
        Generated response text
    """
    config = get_config()
    actual_model = model if model is not None else config.model
    
    if host is not None:
        # Use custom host
        client = OllamaClient(host=host)
        response = client.chat(actual_model, [{"role": "user", "content": prompt}])
    else:
        # Use global config
        response = ollama.chat(
            model=actual_model,
            messages=[{"role": "user", "content": prompt}]
        )
    return response['message']['content']


def quick_generate(model: Optional[str] = None, prompt: str = "", host: Optional[str] = None) -> str:
    """Quick text generation.
    
    Args:
        model: Model name (uses global config default if None)
        prompt: Input prompt
        host: Ollama server host (uses global config if None)
        
    Returns:
        Generated text
    """
    config = get_config()
    actual_model = model if model is not None else config.model
    
    if host is not None:
        # Use custom host
        client = OllamaClient(host=host)
        response = client.generate(actual_model, prompt)
    else:
        # Use global config
        response = ollama.generate(model=actual_model, prompt=prompt)
    return response['response']