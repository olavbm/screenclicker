"""
Configuration management for ScreenClicker Ollama integration.
"""

import os
from typing import Optional, Dict, Any


class OllamaConfig:
    """Global configuration for Ollama integration."""
    
    # Default values
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 11434
    DEFAULT_MODEL = "qwen3-vl:4b"
    DEFAULT_SYSTEM_PROMPT = None
    
    def __init__(self):
        """Initialize configuration with defaults and environment variables."""
        self._host = None
        self._port = None
        self._model = None
        self._system_prompt = None
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Load from environment variables if available
        if 'OLLAMA_HOST' in os.environ:
            self._host = os.environ['OLLAMA_HOST']
        if 'OLLAMA_PORT' in os.environ:
            try:
                self._port = int(os.environ['OLLAMA_PORT'])
            except ValueError:
                pass  # Keep default if invalid
        if 'OLLAMA_MODEL' in os.environ:
            self._model = os.environ['OLLAMA_MODEL']
        if 'OLLAMA_SYSTEM_PROMPT' in os.environ:
            self._system_prompt = os.environ['OLLAMA_SYSTEM_PROMPT']
    
    @property
    def host(self) -> str:
        """Get Ollama server hostname."""
        return self._host if self._host is not None else self.DEFAULT_HOST
    
    @host.setter
    def host(self, value: str):
        """Set Ollama server hostname."""
        self._host = value
    
    @property
    def port(self) -> int:
        """Get Ollama server port."""
        return self._port if self._port is not None else self.DEFAULT_PORT
    
    @port.setter
    def port(self, value: int):
        """Set Ollama server port."""
        if not isinstance(value, int) or value <= 0 or value > 65535:
            raise ValueError(f"Port must be a valid integer between 1-65535, got: {value}")
        self._port = value
    
    @property
    def model(self) -> str:
        """Get default Ollama model."""
        return self._model if self._model is not None else self.DEFAULT_MODEL
    
    @model.setter
    def model(self, value: str):
        """Set default Ollama model."""
        if not value or not isinstance(value, str):
            raise ValueError(f"Model must be a non-empty string, got: {value}")
        self._model = value
    
    @property
    def system_prompt(self) -> Optional[str]:
        """Get default system prompt."""
        return self._system_prompt if self._system_prompt is not None else self.DEFAULT_SYSTEM_PROMPT
    
    @system_prompt.setter
    def system_prompt(self, value: Optional[str]):
        """Set default system prompt."""
        if value is not None and not isinstance(value, str):
            raise ValueError(f"System prompt must be a string or None, got: {type(value)}")
        self._system_prompt = value
    
    @property
    def url(self) -> str:
        """Get full Ollama server URL."""
        return f"http://{self.host}:{self.port}"
    
    def reset(self):
        """Reset all configuration to defaults."""
        self._host = None
        self._port = None
        self._model = None
        self._system_prompt = None
        self._load_from_env()  # Reload from environment
    
    def update(self, **kwargs):
        """Update multiple configuration values at once.
        
        Args:
            host: Ollama server hostname
            port: Ollama server port
            model: Default model name
            system_prompt: Default system prompt
        """
        if 'host' in kwargs:
            self.host = kwargs['host']
        if 'port' in kwargs:
            self.port = kwargs['port']
        if 'model' in kwargs:
            self.model = kwargs['model']
        if 'system_prompt' in kwargs:
            self.system_prompt = kwargs['system_prompt']
    
    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return {
            'host': self.host,
            'port': self.port,
            'model': self.model,
            'system_prompt': self.system_prompt,
            'url': self.url
        }
    
    def __repr__(self) -> str:
        """String representation of configuration."""
        prompt_str = f", system_prompt='{self.system_prompt[:50]}...'" if self.system_prompt and len(self.system_prompt) > 50 else f", system_prompt='{self.system_prompt}'"
        return f"OllamaConfig(host='{self.host}', port={self.port}, model='{self.model}'{prompt_str})"


# Global configuration instance
ollama_config = OllamaConfig()


# Convenience functions for easy access
def get_config() -> OllamaConfig:
    """Get the global Ollama configuration instance."""
    return ollama_config


def set_host(host: str):
    """Set the Ollama server hostname."""
    ollama_config.host = host


def set_port(port: int):
    """Set the Ollama server port."""
    ollama_config.port = port


def set_model(model: str):
    """Set the default Ollama model."""
    ollama_config.model = model


def set_system_prompt(system_prompt: Optional[str]):
    """Set the default system prompt."""
    ollama_config.system_prompt = system_prompt


def set_config(host: Optional[str] = None, port: Optional[int] = None, model: Optional[str] = None, system_prompt: Optional[str] = None):
    """Set multiple configuration values at once."""
    if host is not None:
        ollama_config.host = host
    if port is not None:
        ollama_config.port = port
    if model is not None:
        ollama_config.model = model
    if system_prompt is not None:
        ollama_config.system_prompt = system_prompt


def get_url() -> str:
    """Get the full Ollama server URL."""
    return ollama_config.url


def get_model() -> str:
    """Get the default Ollama model."""
    return ollama_config.model


def get_system_prompt() -> Optional[str]:
    """Get the default system prompt."""
    return ollama_config.system_prompt


def reset_config():
    """Reset configuration to defaults."""
    ollama_config.reset()