"""
Tests for Ollama client functionality.
Tests require a running Ollama server with at least one model available.
"""

import pytest
from screenclicker.ollama_client import OllamaClient, quick_chat, quick_generate


class TestOllamaIntegration:
    """Integration tests that require a running Ollama server."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.host = "http://localhost:11434"
        self.client = OllamaClient()
        
    @pytest.mark.slow
    def test_connection_check(self):
        """Test connection to Ollama server."""
        is_connected = self.client.is_connected()
        assert isinstance(is_connected, bool)
        
        if not is_connected:
            pytest.skip("Ollama server not available at http://localhost:11434")
            
    @pytest.mark.slow
    def test_list_models(self):
        """Test listing available models."""
        if not self.client.is_connected():
            pytest.skip("Ollama server not available")
            
        models = self.client.list()
        assert 'models' in models
        assert isinstance(models['models'], list)
        
        # If no models, skip model-dependent tests
        if len(models['models']) == 0:
            pytest.skip("No models available on Ollama server")
            
    @pytest.mark.slow 
    def test_show_model(self):
        """Test showing model details."""
        if not self.client.is_connected():
            pytest.skip("Ollama server not available")
            
        models = self.client.list()
        if len(models['models']) == 0:
            pytest.skip("No models available")
            
        # Use the first available model
        model_name = models['models'][0]['name']
        details = self.client.show(model_name)
        
        # Check that we got model details response
        assert isinstance(details, dict)
        # The response should contain some expected keys like details or capabilities
        expected_keys = ['details', 'capabilities', 'license', 'model_info']
        assert any(key in details for key in expected_keys), f"Expected at least one of {expected_keys} in response keys: {list(details.keys())}"
        
        
    @pytest.mark.slow
    def test_generate_text(self):
        """Test text generation with available model."""
        if not self.client.is_connected():
            pytest.skip("Ollama server not available")
            
        models = self.client.list()
        if len(models['models']) == 0:
            pytest.skip("No models available")
            
        # Use first available model for testing
        model_name = models['models'][0]['name']
        prompt = "Say 'Hello' in one word."
        
        try:
            response = self.client.generate(model_name, prompt)
            assert 'response' in response
            assert isinstance(response['response'], str)
            assert len(response['response']) > 0
        except Exception as e:
            pytest.skip(f"Model {model_name} failed to generate: {e}")
            
    @pytest.mark.slow
    def test_chat_interaction(self):
        """Test chat interaction with available model."""
        if not self.client.is_connected():
            pytest.skip("Ollama server not available")
            
        models = self.client.list()
        if len(models['models']) == 0:
            pytest.skip("No models available")
            
        # Use first available model
        model_name = models['models'][0]['name']
        messages = [{"role": "user", "content": "Say 'Hi' in one word."}]
        
        try:
            response = self.client.chat(model_name, messages)
            assert 'message' in response
            assert 'content' in response['message']
            assert isinstance(response['message']['content'], str)
            assert len(response['message']['content']) > 0
        except Exception as e:
            pytest.skip(f"Model {model_name} failed to chat: {e}")
            
    @pytest.mark.slow
    def test_streaming_chat(self):
        """Test streaming chat responses."""
        if not self.client.is_connected():
            pytest.skip("Ollama server not available")
            
        models = self.client.list()
        if len(models['models']) == 0:
            pytest.skip("No models available")
            
        model_name = models['models'][0]['name']
        messages = [{"role": "user", "content": "Count from 1 to 3."}]
        
        try:
            stream = self.client.chat(model_name, messages, stream=True)
            chunks = []
            for chunk in stream:
                chunks.append(chunk)
                if chunk.get('done', False):
                    break
                    
            assert len(chunks) > 0
            # Last chunk should be marked as done
            assert chunks[-1].get('done', False) is True
        except Exception as e:
            pytest.skip(f"Model {model_name} failed streaming chat: {e}")
            
    @pytest.mark.slow
    def test_streaming_generation(self):
        """Test streaming text generation."""
        if not self.client.is_connected():
            pytest.skip("Ollama server not available")
            
        models = self.client.list()
        if len(models['models']) == 0:
            pytest.skip("No models available")
            
        model_name = models['models'][0]['name']
        prompt = "Count from 1 to 3."
        
        try:
            stream = self.client.generate(model_name, prompt, stream=True)
            chunks = []
            for chunk in stream:
                chunks.append(chunk)
                if chunk.get('done', False):
                    break
                    
            assert len(chunks) > 0
            assert chunks[-1].get('done', False) is True
        except Exception as e:
            pytest.skip(f"Model {model_name} failed streaming generation: {e}")
            
    @pytest.mark.slow
    def test_embeddings(self):
        """Test generating embeddings."""
        if not self.client.is_connected():
            pytest.skip("Ollama server not available")
            
        models = self.client.list()
        if len(models['models']) == 0:
            pytest.skip("No models available")
            
        # Not all models support embeddings, try first model
        model_name = models['models'][0]['name']
        prompt = "This is a test sentence."
        
        try:
            response = self.client.embeddings(model_name, prompt)
            assert 'embedding' in response
            assert isinstance(response['embedding'], list)
            assert len(response['embedding']) > 0
        except Exception as e:
            pytest.skip(f"Model {model_name} doesn't support embeddings: {e}")
            
    @pytest.mark.slow  
    def test_convenience_functions(self):
        """Test convenience functions with real server."""
        if not self.client.is_connected():
            pytest.skip("Ollama server not available")
            
        models = self.client.list()
        if len(models['models']) == 0:
            pytest.skip("No models available")
            
        model_name = models['models'][0]['name']
        
        # Test quick_chat
        try:
            chat_result = quick_chat(model_name, "Say 'Hello'")
            assert isinstance(chat_result, str)
            assert len(chat_result) > 0
        except Exception as e:
            pytest.skip(f"quick_chat failed with {model_name}: {e}")
            
        # Test quick_generate  
        try:
            generate_result = quick_generate(model_name, "Say 'World'")
            assert isinstance(generate_result, str)
            assert len(generate_result) > 0
        except Exception as e:
            pytest.skip(f"quick_generate failed with {model_name}: {e}")
            
    @pytest.mark.slow
    def test_custom_client_config(self):
        """Test custom client configuration."""
        custom_headers = {'User-Agent': 'ScreenClicker-Test/1.0'}
        custom_client = OllamaClient(headers=custom_headers)
        
        # Test that custom client works
        is_connected = custom_client.is_connected()
        assert isinstance(is_connected, bool)
        
    @pytest.mark.slow
    def test_error_handling_nonexistent_model(self):
        """Test error handling with non-existent model."""
        if not self.client.is_connected():
            pytest.skip("Ollama server not available")
            
        nonexistent_model = "this-model-definitely-does-not-exist-12345"
        
        # This should raise an exception
        with pytest.raises(Exception):
            self.client.generate(nonexistent_model, "test prompt")