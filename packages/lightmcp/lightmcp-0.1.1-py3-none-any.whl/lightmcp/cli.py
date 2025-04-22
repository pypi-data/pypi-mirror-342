"""
Command-line interface for LightMCP.
"""
import argparse
import os
import sys
from typing import List, Optional

from .tool_loader import ToolRegistry


def add_tool_command(args):
    """Add a tool to the registry."""
    registry = ToolRegistry()
    registry.add_tool(args.tool_id, args.module_path)
    print(f"Tool '{args.tool_id}' added to registry.")


def remove_tool_command(args):
    """Remove a tool from the registry."""
    registry = ToolRegistry()
    if registry.remove_tool(args.tool_id):
        print(f"Tool '{args.tool_id}' removed from registry.")
    else:
        print(f"Tool '{args.tool_id}' not found in registry.")


def list_tools_command(args):
    """List all tools in the registry."""
    registry = ToolRegistry()
    tools = registry.list_tools()
    
    if not tools:
        print("No tools found in registry.")
        return
    
    print("Available tools:")
    for tool_id in tools:
        print(f"  - {tool_id}")


def main(argv: Optional[List[str]] = None):
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="LightMCP - A lightweight MCP tool layer for LLM agent frameworks."
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Add tool command
    add_parser = subparsers.add_parser("add-tool", help="Add a tool to the registry")
    add_parser.add_argument("tool_id", help="ID of the tool (e.g., 'notion.query_tasks')")
    add_parser.add_argument("module_path", help="Path to the tool module")
    add_parser.set_defaults(func=add_tool_command)
    
    # Remove tool command
    remove_parser = subparsers.add_parser("remove-tool", help="Remove a tool from the registry")
    remove_parser.add_argument("tool_id", help="ID of the tool to remove")
    remove_parser.set_defaults(func=remove_tool_command)
    
    # List tools command
    list_parser = subparsers.add_parser("list-tools", help="List all tools in the registry")
    list_parser.set_defaults(func=list_tools_command)
    
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
