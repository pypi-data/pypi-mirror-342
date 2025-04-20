"""Tools integration coordinator module."""

import logging
from typing import Dict, Any, List, Optional, Type
from .tool_base import ToolIntegration
from .vscode import VSCodeIntegration
from .git import GitIntegration
from .docker import DockerIntegration

logger = logging.getLogger('termis.tools')

class ToolsCoordinator:
    """Coordinates different tool integrations."""
    
    # Map of tool names to their integration classes
    TOOLS_MAP: Dict[str, Type[ToolIntegration]] = {
        'vscode': VSCodeIntegration,
        'docker': DockerIntegration,
        'git': GitIntegration,
    }
    
    @staticmethod
    def get_tool_integration(tool_name: str) -> Type[ToolIntegration]:
        """Get the appropriate tool integration class.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool integration class
        """
        return ToolsCoordinator.TOOLS_MAP.get(tool_name, ToolIntegration)
    
    @staticmethod
    def process_tool_hooks(pane_config: Dict[str, Any], working_dir: Optional[str] = None) -> List[str]:
        """Process tool hooks in pane configuration and return generated commands.
        
        Args:
            pane_config: Configuration for the pane
            working_dir: Working directory for command execution
            
        Returns:
            List of commands to execute
        """
        commands = []
        
        # Get tool hooks from pane configuration
        tools = pane_config.get('tools', {})
        
        # Ensure tools is a dictionary
        if not isinstance(tools, dict):
            logger.warning(f"Tools configuration must be a dictionary, got {type(tools)}")
            return commands
        
        # Process each tool
        for tool_name, tool_config in tools.items():
            try:
                # Get the integration class for this tool
                integration_class = ToolsCoordinator.get_tool_integration(tool_name)
                
                # Check if the tool is available
                if integration_class.is_available():
                    # Generate commands for this tool
                    tool_commands = integration_class.generate_commands(tool_config, working_dir)
                    logger.info(f"TOOLS: {tool_commands}")
                    if tool_commands:
                        commands.extend(tool_commands)
                else:
                    logger.warning(f"Tool '{tool_name}' is not available on this system")
            except Exception as e:
                logger.error(f"Error processing tool '{tool_name}': {e}")
                continue
        
        return commands