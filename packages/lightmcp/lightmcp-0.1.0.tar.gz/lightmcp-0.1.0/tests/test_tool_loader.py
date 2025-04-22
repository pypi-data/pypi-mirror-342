"""
Tests for the LightMCP tool loader.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import lightmcp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from lightmcp import add
from lightmcp.tool_loader import ToolRegistry, MCPTool


class TestToolLoader(unittest.TestCase):
    """Test cases for the LightMCP tool loader."""
    
    @patch("lightmcp.tool_loader.ToolRegistry._load_registry")
    def test_add_function(self, mock_load_registry):
        """Test that the add function returns an MCPTool instance."""
        # Mock the registry to return a known path for a test tool
        mock_load_registry.return_value = {
            "test.tool": "toolz/test/tool.py"
        }
        
        # Mock os.path.exists to return True for our test tool
        with patch("os.path.exists", return_value=True):
            # Call the add function
            tool = add("test.tool")
            
            # Check that it returns an MCPTool instance
            self.assertIsInstance(tool, MCPTool)
            self.assertEqual(tool.tool_id, "test.tool")
            self.assertEqual(tool.module_path, "toolz/test/tool.py")
    
    @patch("lightmcp.tool_loader.ToolRegistry._load_registry")
    def test_tool_not_found(self, mock_load_registry):
        """Test that add raises ValueError when tool is not found."""
        # Mock an empty registry
        mock_load_registry.return_value = {}
        
        # Check that add raises ValueError for unknown tool
        with self.assertRaises(ValueError):
            add("unknown.tool")
    
    @patch("lightmcp.tool_loader.ToolRegistry._load_registry")
    def test_tool_file_not_found(self, mock_load_registry):
        """Test that add raises FileNotFoundError when tool file doesn't exist."""
        # Mock the registry to return a path for a non-existent tool
        mock_load_registry.return_value = {
            "missing.tool": "toolz/missing/tool.py"
        }
        
        # Mock os.path.exists to return False
        with patch("os.path.exists", return_value=False):
            # Check that add raises FileNotFoundError
            with self.assertRaises(FileNotFoundError):
                add("missing.tool")
    
    @patch("subprocess.Popen")
    @patch("lightmcp.tool_loader.ToolRegistry._load_registry")
    def test_tool_run(self, mock_load_registry, mock_popen):
        """Test that MCPTool.run starts a FastMCP server."""
        # Mock the registry
        mock_load_registry.return_value = {
            "test.tool": "toolz/test/tool.py"
        }
        
        # Mock the subprocess.Popen
        mock_process = MagicMock()
        mock_process.poll.return_value = None  # Process is running
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        # Mock os.path.exists
        with patch("os.path.exists", return_value=True):
            # Add and run the tool
            tool = add("test.tool")
            info = tool.run()
            
            # Check that Popen was called with the right arguments
            mock_popen.assert_called_once()
            args = mock_popen.call_args[0][0]
            self.assertIn("fastmcp", args)
            self.assertIn("serve", args)
            self.assertIn("--module", args)
            self.assertIn("toolz/test/tool.py", args)
            
            # Check the returned info
            self.assertEqual(info["tool_id"], "test.tool")
            self.assertTrue(info["server_url"].startswith("http://localhost:"))
            self.assertEqual(info["process_id"], 12345)


if __name__ == "__main__":
    unittest.main()
