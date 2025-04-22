"""Tests for the mcp-think package."""

import unittest
from unittest.mock import patch, MagicMock
import datetime
from mcp_think.server import think


class TestThinkTool(unittest.TestCase):
    """Test the think tool functionality."""

    @patch('mcp_think.server.datetime')
    async def test_think_tool(self, mock_datetime):
        """Test that the think tool correctly logs thoughts."""
        # Setup mock datetime
        mock_now = MagicMock()
        mock_now.isoformat.return_value = "2025-04-18T22:00:00"
        mock_datetime.datetime.now.return_value = mock_now

        # Call the think function
        thought = "This is a test thought"
        result = await think(thought)

        # Check the result
        self.assertEqual(result, thought)
        
        # Check that the thought was logged
        from mcp_think.server import thoughts_log
        self.assertEqual(len(thoughts_log), 1)
        self.assertEqual(thoughts_log[0]["timestamp"], "2025-04-18T22:00:00")
        self.assertEqual(thoughts_log[0]["thought"], thought)


if __name__ == "__main__":
    unittest.main()