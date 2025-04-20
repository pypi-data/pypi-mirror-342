"""VS Code integration module."""

import shutil
from typing import Dict, Any, List, Optional
from .tool_base import ToolIntegration

class VSCodeIntegration(ToolIntegration):
    """Handles VS Code specific integrations."""
    
    @staticmethod
    def is_available() -> bool:
        """Check if VS Code is available."""
        return shutil.which("code") is not None or shutil.which("code-insiders") is not None
    
    @staticmethod
    def generate_commands(vscode_config: Dict[str, Any], working_dir: Optional[str] = None) -> List[str]:
        """Generate VS Code specific commands.
        
        Args:
            vscode_config: VS Code specific configuration
            working_dir: Working directory to open
            
        Returns:
            List of commands to execute
        """
        commands = []
        
        # Determine which VS Code command to use
        code_cmd = "code" if shutil.which("code") is not None else "code-insiders"
        
        # Build the command based on configuration
        base_cmd = code_cmd
        
        # Open folder if specified
        if working_dir:
            base_cmd += f" {working_dir}"
        
        # Add specified files
        if vscode_config.get('files'):
            files = " ".join(vscode_config['files'])
            base_cmd += f" {files}"
            
        # Open in new window if specified
        if vscode_config.get('new_window'):
            base_cmd += " --new-window"
            
        # Use specific extensions
        if vscode_config.get('extensions'):
            for ext in vscode_config['extensions']:
                commands.append(f"{code_cmd} --install-extension {ext}")
        
        commands.append(base_cmd)
        return commands