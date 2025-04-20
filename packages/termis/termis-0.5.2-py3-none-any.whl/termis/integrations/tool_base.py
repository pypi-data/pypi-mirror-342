"""Base class for tool integrations."""

import shutil
from typing import Dict, Any, List, Optional

class ToolIntegration:
    """Base class for tool integrations."""
    
    @staticmethod
    def is_available(tool_name: str) -> bool:
        """Check if a tool is available in the system."""
        return shutil.which(tool_name) is not None
    
    @staticmethod
    def generate_commands(tool_config: Dict[str, Any], working_dir: Optional[str] = None) -> List[str]:
        """Generate commands for the tool based on configuration.
        
        Args:
            tool_config: Tool-specific configuration
            working_dir: Working directory for command execution
            
        Returns:
            List of commands to execute
        """
        return []