
"""Basic tests for the ai-ensemble-suite library."""

import pytest
import os
import yaml
from unittest.mock import AsyncMock, patch, MagicMock
from pathlib import Path

from ai_ensemble_suite import Ensemble
from ai_ensemble_suite.config import ConfigManager
from ai_ensemble_suite.exceptions import ModelError, ConfigurationError


# Test configuration
TEST_CONFIG = {
    "models": {
        "test_model": {
            "path": "models/test-model.gguf",
            "role": "primary",
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 100
            }
        }
    },
    "collaboration": {
        "mode": "simple",
        "phases": [
            {
                "name": "initial_response",
                "type": "async_thinking",
                "models": ["test_model"],
                "prompt_template": "single_query"
            }
        ]
    },
    "aggregation": {
        "strategy": "sequential_refinement",
        "final_phase": "initial_response"
    }
}


class TestEnsemble:
    """Tests for the Ensemble class."""
    
    @pytest.fixture
    def mock_model_manager(self):
        """Create a mock model manager."""
        mock = AsyncMock()
        mock.initialize = AsyncMock()
        mock.shutdown = AsyncMock()
        mock.run_inference = AsyncMock(return_value={"text": "Test response", "generation_time": 0.1})
        mock.run_all_models = AsyncMock(return_value={"test_model": {"text": "Test response", "generation_time": 0.1}})
        return mock
    
    @pytest.fixture
    def mock_config_manager(self):
        """Create a mock configuration manager."""
        mock = MagicMock()
        mock.get_collaboration_mode = MagicMock(return_value="simple")
        mock.get_collaboration_config = MagicMock(return_value={
            "mode": "simple",
            "phases": [
                {
                    "name": "initial_response",
                    "type": "async_thinking",
                    "models": ["test_model"]
                }
            ]
        })
        mock.get_aggregation_strategy = MagicMock(return_value="sequential_refinement")
        mock.get_aggregation_config = MagicMock(return_value={
            "strategy": "sequential_refinement",
            "final_phase": "initial_response"
        })
        return mock
    
    @pytest.mark.asyncio
    @patch('ai_ensemble_suite.ensemble.ModelManager')
    @patch('ai_ensemble_suite.ensemble.ConfigManager')
    async def test_ensemble_initialization(self, mock_config_manager_class, mock_model_manager_class, mock_model_manager):
        """Test ensemble initialization."""
        # Setup mocks
        mock_config_manager_class.return_value = MagicMock()
        mock_model_manager_class.return_value = mock_model_manager
        
        # Create ensemble
        ensemble = Ensemble(config_dict=TEST_CONFIG)
        
        # Check that ConfigManager was called with the correct arguments
        mock_config_manager_class.assert_called_once_with(None, TEST_CONFIG)
        
        # Initialize the ensemble
        await ensemble.initialize()
        
        # Check that ModelManager.initialize was called
        mock_model_manager.initialize.assert_called_once()
        
        # Check initialization status
        assert ensemble._initialized == True
        
        # Shutdown the ensemble
        await ensemble.shutdown()
        
        # Check that ModelManager.shutdown was called
        mock_model_manager.shutdown.assert_called_once()
        
        # Check initialization status after shutdown
        assert ensemble._initialized == False
    
    @pytest.mark.asyncio
    @patch('ai_ensemble_suite.ensemble.AsyncThinking')
    async def test_ensemble_ask(self, mock_async_thinking_class, mock_model_manager, mock_config_manager):
        """Test the ask method."""
        # Setup mocks
        mock_async_thinking = AsyncMock()
        mock_async_thinking.execute = AsyncMock(return_value={
            "output": "Test response",
            "confidence": 0.9
        })
        mock_async_thinking_class.return_value = mock_async_thinking
        
        # Create ensemble with mocked dependencies
        ensemble = Ensemble()
        ensemble.model_manager = mock_model_manager
        ensemble.config_manager = mock_config_manager
        ensemble._initialized = True
        
        # Mock the aggregation
        ensemble._aggregate_results = AsyncMock(return_value={
            "response": "Aggregated test response",
            "confidence": 0.95
        })
        
        # Test the ask method
        query = "Test query"
        response = await ensemble.ask(query)
        
        # Check the result
        assert response == "Aggregated test response"
        
        # Test with trace=True
        response_with_trace = await ensemble.ask(query, trace=True)
        
        # Check the result structure
        assert "response" in response_with_trace
        assert "trace" in response_with_trace
        assert "execution_time" in response_with_trace
        assert response_with_trace["response"] == "Aggregated test response"
    
    @pytest.mark.asyncio
    async def test_ensemble_context_manager(self, mock_model_manager, mock_config_manager):
        """Test using the ensemble as an async context manager."""
        # Setup
        with patch('ai_ensemble_suite.ensemble.ModelManager', return_value=mock_model_manager), \
             patch('ai_ensemble_suite.ensemble.ConfigManager', return_value=mock_config_manager):
            
            # Use context manager
            async with Ensemble(config_dict=TEST_CONFIG) as ensemble:
                # Check that ModelManager.initialize was called
                mock_model_manager.initialize.assert_called_once()
                
                # Mock the aggregation for ask method
                ensemble._aggregate_results = AsyncMock(return_value={
                    "response": "Aggregated test response",
                    "confidence": 0.95
                })
                
                # Test the ask method
                response = await ensemble.ask("Test query")
                assert response == "Aggregated test response"
            
            # Check that ModelManager.shutdown was called after context exit
            mock_model_manager.shutdown.assert_called_once()


class TestConfig:
    """Tests for configuration handling."""
    
    def test_config_manager_initialization(self):
        """Test ConfigManager initialization with dictionary."""
        config_manager = ConfigManager(config_dict=TEST_CONFIG)
        
        # Test that model_ids includes our test model
        assert "test_model" in config_manager.get_model_ids()
        
        # Test getting collaboration mode
        assert config_manager.get_collaboration_mode() == "simple"
        
        # Test getting aggregation strategy
        assert config_manager.get_aggregation_strategy() == "sequential_refinement"
    
    def test_config_manager_validation(self):
        """Test validation of invalid configuration."""
        # Invalid config with missing required fields
        invalid_config = {
            "models": {
                "test_model": {
                    # Missing path
                    "role": "primary"
                }
            }
        }
        
        # Check that ValidationError is raised
        with pytest.raises(ConfigurationError):
            ConfigManager(config_dict=invalid_config)
    
    def test_config_update(self):
        """Test updating configuration."""
        config_manager = ConfigManager(config_dict=TEST_CONFIG)
        
        # Update with new configuration
        update_config = {
            "models": {
                "new_model": {
                    "path": "models/new-model.gguf",
                    "role": "assistant"
                }
            }
        }
        
        config_manager.update(update_config)
        
        # Check that new model was added
        assert "new_model" in config_manager.get_model_ids()
        
        # Original model should still be there
        assert "test_model" in config_manager.get_model_ids()


if __name__ == "__main__":
    pytest.main(["-v", "test_basic.py"])
