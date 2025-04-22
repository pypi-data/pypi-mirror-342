"""Tests for the VisionFi client."""

import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visionfi import VisionFi
from visionfi.exceptions import VisionFiError


class TestVisionFiClient(unittest.TestCase):
    """Test cases for VisionFi client."""

    @patch("visionfi.client.ServiceAccountAuth", autospec=True)
    def setUp(self, mock_auth_class):
        """Set up test fixtures."""
        # Create a mock instance that will be returned when ServiceAccountAuth is instantiated
        self.mock_auth_instance = MagicMock()
        mock_auth_class.return_value = self.mock_auth_instance
        
        # Configure the mock's behavior
        self.mock_auth_instance.get_authorization_header.return_value = {
            "Authorization": "Bearer mock-token"
        }
        
        # Create the client with test credentials (doesn't matter what's in here as we're mocking)
        self.client = VisionFi(
            service_account_json={"type": "service_account", "project_id": "test"}
        )

    @patch("visionfi.client.requests.Session.request")
    def test_verify_auth(self, mock_request):
        """Test verify_auth method."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "success": True,
            "message": "Authentication successful",
            "data": {"authenticated": True}
        }
        mock_request.return_value = mock_response
        
        # Call method
        result = self.client.verify_auth()
        
        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Authentication successful")
        self.assertTrue(result.data["authenticated"])
        mock_request.assert_called_once()

    @patch("visionfi.client.requests.Session.request")
    def test_analyze_document(self, mock_request):
        """Test analyze_document method."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "uuid": "test-uuid",
                "status": "processing",
                "created_at": "2023-01-01T00:00:00Z",
                "client_id": "test-client"
            }
        }
        mock_request.return_value = mock_response
        
        # Call method with test data
        test_data = b"test file content"
        options = {
            "file_name": "test.pdf",
            "analysis_type": "test_analysis"
        }
        
        result = self.client.analyze_document(test_data, options)
        
        # Assert
        self.assertEqual(result.uuid, "test-uuid")
        self.assertEqual(result.status, "processing")
        mock_request.assert_called_once()

    def test_analyze_document_missing_options(self):
        """Test analyze_document with missing options."""
        test_data = b"test file content"
        
        # Missing file_name
        with self.assertRaises(VisionFiError):
            self.client.analyze_document(test_data, {"analysis_type": "test"})
        
        # Missing analysis_type
        with self.assertRaises(VisionFiError):
            self.client.analyze_document(test_data, {"file_name": "test.pdf"})


if __name__ == "__main__":
    unittest.main()