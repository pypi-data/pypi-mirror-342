"""
Explore the FastMCP structure to understand how tools are stored.
"""

from mcp.server import FastMCP

def simple_tool(text: str) -> str:
    """A simple tool that returns the input text."""
    return f"Processed: {text}"

def explore_fastmcp():
    # Create a server instance
    server = FastMCP()
    
    # Add a tool
    server.add_tool(simple_tool)
    
    # List all available tools
    print("Available tools:")
    tools = server.list_tools()
    print(tools)
    
    # Print some attributes of the tool manager if available
    if hasattr(server, '_tool_manager'):
        print("\nTool manager attributes:")
        tool_manager = server._tool_manager
        for attr_name in dir(tool_manager):
            if not attr_name.startswith('__'):
                try:
                    attr = getattr(tool_manager, attr_name)
                    print(f"  {attr_name}: {type(attr)}")
                except Exception as e:
                    print(f"  {attr_name}: Error accessing - {e}")
        
        # Check if tool manager has tools stored
        print("\nChecking tool manager for tools:")
        if hasattr(tool_manager, 'tools'):
            print("  Tools in tool_manager.tools:", tool_manager.tools)
        if hasattr(tool_manager, '_tools'):
            print("  Tools in tool_manager._tools:", tool_manager._tools)

if __name__ == "__main__":
    explore_fastmcp() 