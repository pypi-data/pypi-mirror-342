#!/usr/bin/env python3
"""Test the main module."""

import unittest
import unittest.mock as mock
import sys
import os
import asyncio

# Add the parent directory to the path to allow importing from main
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from main import just_get_version, list_namespaces, get_config, publish_config, remove_config


class TestMain(unittest.TestCase):
    """Test cases for the main module."""

    def test_version(self):
        """Test that just_get_version returns a version string."""
        # Run the coroutine in an event loop
        result = asyncio.run(just_get_version())
        self.assertIsInstance(result, str)

    @mock.patch('requests.get')
    def test_list_namespaces(self, mock_get):
        """Test the list_namespaces function."""
        # Mock response
        mock_response = mock.Mock()
        mock_response.json.return_value = {"namespaces": [{"namespace": "test"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Run the coroutine in an event loop
        result = asyncio.run(list_namespaces("http://localhost:8848"))
        
        # Verify
        self.assertEqual(result, {"namespaces": [{"namespace": "test"}]})
        mock_get.assert_called_once_with("http://localhost:8848/nacos/v1/console/namespaces")

    @mock.patch('requests.get')
    def test_get_config(self, mock_get):
        """Test the get_config function."""
        # Mock response
        mock_response = mock.Mock()
        mock_response.text = "test_config_content"
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Run the coroutine in an event loop
        result = asyncio.run(get_config("http://localhost:8848", "test-data-id", "DEFAULT_GROUP"))
        
        # Verify
        self.assertEqual(result, {"content": "test_config_content", "status": 200})
        mock_get.assert_called_once()

    @mock.patch('requests.post')
    def test_publish_config(self, mock_post):
        """Test the publish_config function."""
        # Mock response
        mock_response = mock.Mock()
        mock_response.text = "true"
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Run the coroutine in an event loop
        result = asyncio.run(publish_config(
            "http://localhost:8848", 
            "test-data-id", 
            "DEFAULT_GROUP", 
            "test_content"
        ))
        
        # Verify
        self.assertEqual(result, {"success": True, "message": "Configuration published successfully"})
        mock_post.assert_called_once()

    @mock.patch('requests.delete')
    def test_remove_config(self, mock_delete):
        """Test the remove_config function."""
        # Mock response
        mock_response = mock.Mock()
        mock_response.text = "true"
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response

        # Run the coroutine in an event loop
        result = asyncio.run(remove_config(
            "http://localhost:8848", 
            "test-data-id", 
            "DEFAULT_GROUP"
        ))
        
        # Verify
        self.assertEqual(result, {"success": True, "message": "Configuration removed successfully"})
        mock_delete.assert_called_once()


if __name__ == "__main__":
    unittest.main() 