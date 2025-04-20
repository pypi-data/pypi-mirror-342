"""Interactive configuration wizard module."""

import yaml
from typing import Dict, Any, List, Tuple
from ..utils.constants import BADGE_THEMES

class ConfigWizard:
    """Handles interactive configuration setup."""
    
    @staticmethod
    def run_wizard() -> Tuple[str, Dict[str, Any]]:
        """Run the interactive configuration wizard.
        
        Returns:
            Tuple of (config_path, config_dict)
        """
        print("Termis Configuration Wizard")
        print("===========================")
        
        config = {
            'profile': 'Default',
            'tabs': {}
        }
        
        # Get basic configuration
        config['profile'] = input("Default iTerm profile to use [Default]: ") or 'Default'
        
        tab_count = int(input("Number of tabs to configure: "))
        
        for i in range(tab_count):
            tab_id = input(f"Tab {i+1} ID: ")
            tab_config = ConfigWizard._configure_tab(tab_id)
            config['tabs'][tab_id] = tab_config
        
        # Get save location
        config_path = input("Save configuration to [termis.yml]: ") or "termis.yml"
        
        # Write configuration to file
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        print(f"Configuration saved to {config_path}")
        return config_path, config
    
    @staticmethod
    def _configure_tab(tab_id: str) -> Dict[str, Any]:
        """Configure a single tab.
        
        Args:
            tab_id: ID of the tab to configure
            
        Returns:
            Tab configuration dictionary
        """
        tab_config = {}
        
        tab_config['title'] = input(f"Title for tab '{tab_id}' [optional]: ")
        tab_config['root'] = input(f"Root directory for tab '{tab_id}' [optional]: ")
        tab_config['reuse'] = input(f"Reuse existing tab with same title? (y/n) [n]: ").lower() == 'y'
        
        # Configure panes
        pane_count = int(input(f"Number of panes for tab '{tab_id}': "))
        tab_config['panes'] = ConfigWizard._configure_panes(pane_count)
        
        return tab_config
    
    @staticmethod
    def _configure_panes(pane_count: int) -> List[Dict[str, Any]]:
        """Configure multiple panes.
        
        Args:
            pane_count: Number of panes to configure
            
        Returns:
            List of pane configurations
        """
        panes = []
        
        for j in range(pane_count):
            pane = {}
            
            # Basic pane configuration
            pane['position'] = input(f"Position for pane {j+1} (e.g., '1/1', '1/2'): ")
            pane['title'] = input(f"Title for pane {j+1} [optional]: ")
            
            # Badge configuration
            badge = input(f"Badge for pane {j+1} [optional]: ")
            if badge:
                theme = input(f"Badge theme (default/success/error/warning/info/primary/secondary/dark/light) [default]: ")
                if theme and theme in BADGE_THEMES:
                    pane['badge'] = {
                        'text': badge,
                        'theme': theme
                    }
                else:
                    pane['badge'] = badge
            
            # Directory and profile configuration
            pane['working_directory'] = input(f"Working directory for pane {j+1} [optional]: ")
            pane['profile'] = input(f"Profile for pane {j+1} [optional, defaults to tab profile]: ")
            
            # Dependencies configuration
            if j > 0:
                add_dep = input(f"Does this pane depend on other panes? (y/n) [n]: ").lower() == 'y'
                if add_dep:
                    dependencies = []
                    while True:
                        dep_pos = input("Enter position of dependency (empty to finish): ")
                        if not dep_pos:
                            break
                        dependencies.append(dep_pos)
                    
                    if dependencies:
                        pane['depends_on'] = dependencies
            
            # Commands configuration
            commands = []
            print(f"Enter commands for pane {j+1} (empty line to finish):")
            while True:
                cmd = input("> ")
                if not cmd:
                    break
                commands.append(cmd)
            
            if commands:
                pane['commands'] = commands
            
            # Tool integrations
            tools = ConfigWizard._configure_tools()
            if tools:
                pane['tools'] = tools
            
            panes.append(pane)
        
        return panes
    
    @staticmethod
    def _configure_tools() -> Dict[str, Any]:
        """Configure tool integrations for a pane.
        
        Returns:
            Tool configurations dictionary
        """
        tools = {}
        
        add_tools = input("Configure tool integrations? (y/n) [n]: ").lower() == 'y'
        if not add_tools:
            return tools
            
        # VS Code configuration
        if input("Configure VS Code integration? (y/n) [n]: ").lower() == 'y':
            vscode = {}
            vscode['files'] = input("Files to open (space-separated) [optional]: ").split()
            vscode['new_window'] = input("Open in new window? (y/n) [n]: ").lower() == 'y'
            if vscode:
                tools['vscode'] = vscode
        
        # Git configuration
        if input("Configure Git integration? (y/n) [n]: ").lower() == 'y':
            git = {}
            git['clone'] = input("Repository to clone [optional]: ")
            git['checkout'] = input("Branch to checkout [optional]: ")
            git['pull'] = input("Pull updates? (y/n) [n]: ").lower() == 'y'
            if git:
                tools['git'] = git
        
        # Docker configuration
        if input("Configure Docker integration? (y/n) [n]: ").lower() == 'y':
            docker = {}
            if input("Configure docker-compose? (y/n) [n]: ").lower() == 'y':
                docker['compose'] = input("docker-compose command (e.g., 'up -d'): ")
                docker['compose_file'] = input("Path to docker-compose.yml [optional]: ")
            if input("Configure docker run? (y/n) [n]: ").lower() == 'y':
                run = {
                    'image': input("Docker image: "),
                    'detach': input("Run in detached mode? (y/n) [n]: ").lower() == 'y',
                    'interactive': input("Run in interactive mode? (y/n) [n]: ").lower() == 'y'
                }
                docker['run'] = run
            if docker:
                tools['docker'] = docker
                
        return tools