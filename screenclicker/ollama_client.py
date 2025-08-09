"""
Ollama client module for local LLM interactions.
"""

import ollama
import base64
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
             stream: bool = False, system_prompt: Optional[str] = None, 
             images: Optional[List[bytes]] = None, **kwargs) -> Union[Dict[str, Any], Any]:
        """Send chat completion request to Ollama.
        
        Args:
            model: Model name (e.g., 'llama2', 'mistral')
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream response
            system_prompt: System prompt to use (overrides global config)
            images: List of image bytes to send (for vision models)
            **kwargs: Additional parameters (options, tools, etc.)
            
        Returns:
            Response dict from Ollama or iterator if stream=True
        """
        config = get_config()
        actual_system_prompt = system_prompt if system_prompt is not None else config.system_prompt
        
        # Prepare messages with system prompt
        actual_messages = messages.copy()
        if actual_system_prompt:
            # Check if first message is already a system message
            if not actual_messages or actual_messages[0].get('role') != 'system':
                actual_messages.insert(0, {'role': 'system', 'content': actual_system_prompt})
            else:
                # Replace existing system message
                actual_messages[0] = {'role': 'system', 'content': actual_system_prompt}
        
        # Handle images - encode as base64 and add to the last user message
        if images:
            encoded_images = []
            for image_bytes in images:
                if isinstance(image_bytes, bytes):
                    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                    encoded_images.append(encoded_image)
                else:
                    # Assume it's already base64 encoded
                    encoded_images.append(image_bytes)
            
            # Find the last user message and add images to it
            for i in reversed(range(len(actual_messages))):
                if actual_messages[i].get('role') == 'user':
                    actual_messages[i]['images'] = encoded_images
                    break
            else:
                # No user message found, create one
                actual_messages.append({
                    'role': 'user',
                    'content': 'Please analyze this image.',
                    'images': encoded_images
                })
        
        return self.client.chat(
            model=model,
            messages=actual_messages,
            stream=stream,
            **kwargs
        )
    
    def generate(self, model: str, prompt: str, 
                 stream: bool = False, system_prompt: Optional[str] = None,
                 images: Optional[List[bytes]] = None, **kwargs) -> Union[Dict[str, Any], Any]:
        """Generate text completion.
        
        Args:
            model: Model name
            prompt: Input prompt
            stream: Whether to stream response
            system_prompt: System prompt to use (overrides global config)
            images: List of image bytes to send (for vision models)
            **kwargs: Additional parameters (options, context, etc.)
            
        Returns:
            Response dict from Ollama or iterator if stream=True
        """
        config = get_config()
        actual_system_prompt = system_prompt if system_prompt is not None else config.system_prompt
        
        # Prepare prompt with system prompt
        actual_prompt = prompt
        if actual_system_prompt:
            actual_prompt = f"{actual_system_prompt}\n\n{prompt}"
        
        # Handle images - encode as base64
        request_kwargs = kwargs.copy()
        if images:
            encoded_images = []
            for image_bytes in images:
                if isinstance(image_bytes, bytes):
                    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                    encoded_images.append(encoded_image)
                else:
                    # Assume it's already base64 encoded
                    encoded_images.append(image_bytes)
            request_kwargs['images'] = encoded_images
        
        return self.client.generate(
            model=model,
            prompt=actual_prompt,
            stream=stream,
            **request_kwargs
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
def quick_chat(model: Optional[str] = None, prompt: str = "", host: Optional[str] = None, system_prompt: Optional[str] = None, images: Optional[List[bytes]] = None) -> str:
    """Quick chat completion.
    
    Args:
        model: Model name (uses global config default if None)
        prompt: User prompt
        host: Ollama server host (uses global config if None)
        system_prompt: System prompt (overrides global config)
        images: List of image bytes to send (for vision models)
        
    Returns:
        Generated response text
    """
    config = get_config()
    actual_model = model if model is not None else config.model
    
    if host is not None:
        # Use custom host
        client = OllamaClient(host=host)
        response = client.chat(actual_model, [{"role": "user", "content": prompt}], system_prompt=system_prompt, images=images)
    else:
        # Use global config and system prompt
        config = get_config()
        actual_system_prompt = system_prompt if system_prompt is not None else config.system_prompt
        messages = [{"role": "user", "content": prompt}]
        
        # Add system message if system prompt provided
        if actual_system_prompt:
            messages.insert(0, {"role": "system", "content": actual_system_prompt})
        
        # Handle images for direct ollama.chat call
        if images:
            encoded_images = []
            for image_bytes in images:
                if isinstance(image_bytes, bytes):
                    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                    encoded_images.append(encoded_image)
                else:
                    encoded_images.append(image_bytes)
            # Add images to the user message
            messages[-1]['images'] = encoded_images
            
        response = ollama.chat(
            model=actual_model,
            messages=messages
        )
    return response['message']['content']


def quick_generate(model: Optional[str] = None, prompt: str = "", host: Optional[str] = None, system_prompt: Optional[str] = None, images: Optional[List[bytes]] = None) -> str:
    """Quick text generation.
    
    Args:
        model: Model name (uses global config default if None)
        prompt: Input prompt
        host: Ollama server host (uses global config if None)
        system_prompt: System prompt (overrides global config)
        images: List of image bytes to send (for vision models)
        
    Returns:
        Generated text
    """
    config = get_config()
    actual_model = model if model is not None else config.model
    
    if host is not None:
        # Use custom host
        client = OllamaClient(host=host)
        response = client.generate(actual_model, prompt, system_prompt=system_prompt, images=images)
    else:
        # Use global config and system prompt
        config = get_config()
        actual_system_prompt = system_prompt if system_prompt is not None else config.system_prompt
        actual_prompt = prompt
        
        # Prepend system prompt if provided
        if actual_system_prompt:
            actual_prompt = f"{actual_system_prompt}\n\n{prompt}"
        
        # Handle images for direct ollama.generate call
        generate_kwargs = {}
        if images:
            encoded_images = []
            for image_bytes in images:
                if isinstance(image_bytes, bytes):
                    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                    encoded_images.append(encoded_image)
                else:
                    encoded_images.append(image_bytes)
            generate_kwargs['images'] = encoded_images
            
        response = ollama.generate(model=actual_model, prompt=actual_prompt, **generate_kwargs)
    return response['response']


def data_from_path(file_path: str) -> bytes:
    """Load image data from a file path.
    
    Args:
        file_path: Path to the image file
        
    Returns:
        Raw image data as bytes
        
    Raises:
        RuntimeError: If the file cannot be read
    """
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read image from {file_path}: {e}")


def describe_image(image_bytes: bytes, prompt: str = "What do you see in this image?", 
                   model: Optional[str] = None, system_prompt: Optional[str] = None) -> str:
    """Describe an image using a vision language model.
    
    Uses gemma3:27b by default, which supports multimodal input (images + text).
    
    Args:
        image_bytes: Raw image data as bytes
        prompt: Question/prompt about the image (default: "What do you see in this image?")
        model: Model to use (uses global config default gemma3:27b if None)
        system_prompt: System prompt for the model
        
    Returns:
        Text description from the vision model
        
    Raises:
        RuntimeError: If the request fails
    """
    config = get_config()
    
    # Use provided model, or use the configured default (gemma3:27b supports images!)
    if model is None:
        # Use the default model from config - gemma3:27b supports multimodal input
        actual_model = config.model
    else:
        actual_model = model
    
    try:
        return quick_chat(
            model=actual_model,
            prompt=prompt,
            system_prompt=system_prompt,
            images=[image_bytes]
        )
    except Exception as e:
        raise RuntimeError(f"Failed to describe image with model {actual_model}: {e}")


def screenshot_and_describe(prompt: str = "What do you see in this screenshot?", 
                           monitor: int = 0, model: Optional[str] = None, 
                           system_prompt: Optional[str] = None) -> str:
    """Take a screenshot and describe it using a vision language model.
    
    Uses gemma3:27b by default, which supports multimodal input (images + text).
    
    Args:
        prompt: Question/prompt about the screenshot
        monitor: Monitor index to capture (default: 0 for primary monitor)
        model: Model to use (uses global config default gemma3:27b if None)
        system_prompt: System prompt for the model
        
    Returns:
        Text description of the screenshot
        
    Raises:
        RuntimeError: If screenshot fails or model request fails
    """
    from .screen import screenshot_monitor
    
    try:
        # Take screenshot
        image_bytes = screenshot_monitor(monitor)
        
        # Describe it
        return describe_image(image_bytes, prompt, model, system_prompt)
        
    except Exception as e:
        raise RuntimeError(f"Failed to screenshot and describe: {e}")


def describe_image_from_path(file_path: str, prompt: str = "What do you see in this image?", 
                            model: Optional[str] = None, system_prompt: Optional[str] = None) -> str:
    """Load an image from a file path and describe it using a vision language model.
    
    Convenience function that combines data_from_path() and describe_image().
    
    Args:
        file_path: Path to the image file
        prompt: Question/prompt about the image (default: "What do you see in this image?")
        model: Model to use (uses global config default gemma3:27b if None)
        system_prompt: System prompt for the model
        
    Returns:
        Text description from the vision model
        
    Raises:
        RuntimeError: If the file cannot be read or the request fails
    """
    try:
        image_bytes = data_from_path(file_path)
        return describe_image(image_bytes, prompt, model, system_prompt)
    except Exception as e:
        raise RuntimeError(f"Failed to describe image from {file_path}: {e}")