import json
import os
import importlib.util
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

class MCPTool:
    """
    Represents a loaded MCP tool that can be run as an isolated FastMCP server.
    """
    def __init__(self, tool_id: str, module_path: str, port: Optional[int] = None):
        self.tool_id = tool_id
        self.module_path = module_path
        self.port = port or self._find_available_port()
        self._server_process = None
        
    def _find_available_port(self) -> int:
        """Find an available port to run the FastMCP server on."""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Start the FastMCP server for this tool and return the server info.
        """
        if self._server_process is None:
            # Start FastMCP server for this tool
            cmd = [
                sys.executable, "-m", "fastmcp", "serve",
                "--module", self.module_path,
                "--port", str(self.port)
            ]
            
            self._server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            time.sleep(1)
            
            if self._server_process.poll() is not None:
                # Server failed to start
                stdout, stderr = self._server_process.communicate()
                raise RuntimeError(f"Failed to start FastMCP server: {stderr}")
        
        return {
            "tool_id": self.tool_id,
            "server_url": f"http://localhost:{self.port}",
            "port": self.port,
            "process_id": self._server_process.pid
        }
    
    def stop(self):
        """Stop the FastMCP server if it's running."""
        if self._server_process is not None:
            self._server_process.terminate()
            self._server_process = None
    
    def __del__(self):
        """Ensure server is stopped when object is garbage collected."""
        self.stop()


class ToolRegistry:
    """
    Manages the registry of available MCP tools.
    """
    def __init__(self, registry_path: Optional[str] = None):
        self.registry_path = registry_path or self._get_default_registry_path()
        self.registry = self._load_registry()
        
    def _get_default_registry_path(self) -> str:
        """Get the default path to the tool registry JSON file."""
        return os.path.join(os.path.dirname(__file__), "tool_registry.json")
    
    def _load_registry(self) -> Dict[str, str]:
        """Load the tool registry from the JSON file."""
        if not os.path.exists(self.registry_path):
            return {}
        
        with open(self.registry_path, 'r') as f:
            return json.load(f)
    
    def get_tool_path(self, tool_id: str) -> Optional[str]:
        """Get the path to the tool module for the given tool ID."""
        return self.registry.get(tool_id)
    
    def list_tools(self) -> List[str]:
        """List all available tool IDs."""
        return list(self.registry.keys())
        
    def add_tool(self, tool_id: str, module_path: str) -> None:
        """
        Add a new tool to the registry.
        
        Args:
            tool_id: The ID of the tool (e.g., "notion.query_tasks")
            module_path: The path to the tool module
        """
        self.registry[tool_id] = module_path
        self._save_registry()
        
    def remove_tool(self, tool_id: str) -> bool:
        """
        Remove a tool from the registry.
        
        Args:
            tool_id: The ID of the tool to remove
            
        Returns:
            True if the tool was removed, False if it wasn't in the registry
        """
        if tool_id in self.registry:
            del self.registry[tool_id]
            self._save_registry()
            return True
        return False
        
    def _save_registry(self) -> None:
        """Save the tool registry to the JSON file."""
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)


def load_tool(tool_id: str) -> MCPTool:
    """
    Load and return an MCPTool instance for the given tool ID.
    """
    registry = ToolRegistry()
    module_path = registry.get_tool_path(tool_id)
    
    if not module_path:
        raise ValueError(f"Tool '{tool_id}' not found in registry")
    
    # Check if the module exists
    full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), module_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Tool module not found at {full_path}")
    
    return MCPTool(tool_id, module_path)
