"""Git integration module."""

from typing import Dict, Any, List, Optional
from .tool_base import ToolIntegration

class GitIntegration(ToolIntegration):
    """Handles Git specific integrations."""
    
    @staticmethod
    def is_available() -> bool:
        """Check if Git is available."""
        return ToolIntegration.is_available('git')
    
    @staticmethod
    def generate_commands(git_config: Dict[str, Any], working_dir: Optional[str] = None) -> List[str]:
        """Generate Git specific commands.
        
        Args:
            git_config: Git specific configuration
            working_dir: Working directory for git operations
            
        Returns:
            List of commands to execute
        """
        commands = []
        
        # Clone repository if specified
        if git_config.get('clone'):
            repo_url = git_config['clone']
            target_dir = git_config.get('target_dir', '')
            clone_cmd = f"git clone {repo_url}"
            if target_dir:
                clone_cmd += f" {target_dir}"
            commands.append(clone_cmd)
            
        # Checkout branch if specified
        if git_config.get('checkout'):
            commands.append(f"git checkout {git_config['checkout']}")
            
        # Pull updates if specified
        if git_config.get('pull'):
            commands.append("git pull")
            
        # Set up git config if specified
        if git_config.get('config'):
            for key, value in git_config['config'].items():
                commands.append(f"git config {key} '{value}'")
                
        return commands