"""Command execution handling for iTerm2 sessions."""

import asyncio
import logging
from typing import Dict, Any, List, Optional
import iterm2

from ..integrations.tools_coordinator import ToolsCoordinator

logger = logging.getLogger('termis.executor')

class CommandExecutor:
    """Handles command execution in iTerm2 sessions."""
    
    @staticmethod
    async def execute_commands(session: iterm2.Session, 
                             commands: List[str], 
                             delay: int = 0, 
                             working_dir: Optional[str] = None,
                             pane_config: Optional[Dict[str, Any]] = None) -> None:
        """Execute commands in a session with optional delay and working directory.
        
        Args:
            session: iTerm2 session to execute commands in
            commands: List of commands to execute
            delay: Delay between commands in seconds
            working_dir: Working directory for command execution
            pane_config: Additional pane configuration for tool integrations
        """
        try:
            commands_to_run = commands.copy()  # Create a copy to avoid modifying the original

            # Change to working directory if specified
            if working_dir:
                await session.async_send_text(f"cd {working_dir}\n")
            
            # Process tool integrations if configured
            if pane_config and pane_config.get('tools'):
                tool_commands = ToolsCoordinator.process_tool_hooks(pane_config, working_dir)
                # Only prepend tool commands if they exist and aren't empty
                logger.info(f"COM: {tool_commands}")
                if tool_commands and len(tool_commands) > 0:
                    commands_to_run = tool_commands + commands_to_run

            # Execute each command with optional delay
            for command in commands_to_run:
                if delay > 0:
                    await asyncio.sleep(delay)
                await session.async_send_text(f"{command}")
                
        except Exception as e:
            logger.error(f"Error executing commands: {e}")
            raise
    
    @staticmethod
    async def format_commands(commands: List[str], prompt: Optional[str] = None) -> List[str]:
        """Format commands for execution.
        
        Args:
            commands: List of commands to format
            prompt: Optional prompt to add after commands
            
        Returns:
            Formatted list of commands
        """
        # Add newlines to commands
        formatted = [f"{command}\n" for command in commands]
        
        # Add prompt if specified
        if prompt:
            formatted.append(prompt)
            
        return formatted