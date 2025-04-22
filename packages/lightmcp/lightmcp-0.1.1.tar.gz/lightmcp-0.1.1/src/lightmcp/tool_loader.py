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
        self._module = None
        
    def _find_available_port(self) -> int:
        """Find an available port to run the FastMCP server on."""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    def _load_module(self):
        """Load the module from the module path."""
        if self._module is None:
            # Get the absolute path to the module
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            abs_path = os.path.join(base_dir, self.module_path)
            
            # Get the module name from the file path
            module_name = os.path.splitext(os.path.basename(abs_path))[0]
            
            # Load the module
            spec = importlib.util.spec_from_file_location(module_name, abs_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load module from {abs_path}")
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            self._module = module
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Start the tool and return the server info.
        
        Since FastMCP might not be properly installed as a command-line tool,
        we'll directly load and run the module instead.
        """
        try:
            # Try to start FastMCP server (original approach)
            if self._server_process is None:
                try:
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
                        # Server failed to start, fallback to direct module loading
                        stdout, stderr = self._server_process.communicate()
                        print(f"Warning: FastMCP server failed to start: {stderr}")
                        print("Falling back to direct module loading...")
                        self._server_process = None
                        raise RuntimeError("FastMCP server failed to start")
                
                except Exception as e:
                    # Fallback to direct module loading
                    self._load_module()
                    print(f"Tool '{self.tool_id}' loaded directly (not as a server)")
                    
                    return {
                        "tool_id": self.tool_id,
                        "module_path": self.module_path,
                        "direct_load": True,
                        "message": "Tool loaded directly (not as a server)"
                    }
            
            return {
                "tool_id": self.tool_id,
                "server_url": f"http://localhost:{self.port}",
                "port": self.port,
                "process_id": self._server_process.pid
            }
        
        except Exception as e:
            # If all else fails, just load the module directly
            self._load_module()
            print(f"Tool '{self.tool_id}' loaded directly (not as a server)")
            
            return {
                "tool_id": self.tool_id,
                "module_path": self.module_path,
                "direct_load": True,
                "message": f"Tool loaded directly (not as a server). Error: {str(e)}"
            }
    
    def call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the tool with the given parameters.
        
        This is used when the tool is loaded directly (not as a server).
        """
        if self._module is None:
            self._load_module()
        
        if hasattr(self._module, "run"):
            return self._module.run(params)
        else:
            raise ValueError(f"Module {self.module_path} does not have a 'run' function")
    
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
