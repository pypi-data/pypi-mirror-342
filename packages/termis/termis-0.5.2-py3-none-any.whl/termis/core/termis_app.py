"""Main Termis application class."""

import os
import logging
import asyncio
from typing import Dict, Any, Optional
import iterm2

from ..config.config_loader import ConfigLoader
from ..exceptions.termis_exceptions import TermisException, ConfigurationError
from .iterm_manager import ITermManager
from ..utils.constants import DEFAULT_CONFIG, GLOBAL_PROFILES_DIR, VERSION
from ..utils.profile_manager import ProfileManager
from ..cli.parser import parse_arguments
from ..cli.wizard import ConfigWizard
from .command_executor import CommandExecutor
from ..integrations.tools_coordinator import ToolsCoordinator

logger = logging.getLogger('termis.app')

class TermisApp:
    """Main Termis application class."""
    
    def __init__(self):
        """Initialize Termis application."""
        self.iterm_manager = ITermManager()
        self.config_loader = ConfigLoader()
        self.profile_manager = ProfileManager()
        self.command_executor = CommandExecutor()
    
    async def activate(self, connection: iterm2.Connection, args: Dict[str, Any]) -> None:
        """Main entry point for the application.
        
        Args:
            connection: iTerm2 connection
            args: Command line arguments
        """
        try:
            if args.get('version'):
                print(VERSION)
                return
            
            # Set logging level
            log_level = args.get('log_level', 'info').upper()
            logger.setLevel(getattr(logging, log_level, logging.INFO))
            
            # Handle available tools
            if args.get('tools_check'):                
                print("Checking available development tools:")
                
                for tool in ToolsCoordinator.TOOLS_MAP.keys():
                    integration = ToolsCoordinator.get_tool_integration(tool)
                    available = integration.is_available()
                    status = "Available" if available else "Not available"
                    print(f"  {tool:10}: {status}")       
                return
            
            # Handle wizard mode
            if args.get('wizard'):
                config_path, config = await self._handle_wizard_mode()
                return
            
            # Handle global profiles list
            if args.get('global_list'):
                profiles = self.profile_manager.list_global_profiles(GLOBAL_PROFILES_DIR)
                self.profile_manager.print_profiles_list(profiles)
                return
            
            # Handle save to global profile
            if args.get('save_global'):
                config_path = args.get('config') if args.get('config') is not None else DEFAULT_CONFIG
                try:
                    self.profile_manager.save_to_global_profile(config_path, args.get('save_global'), GLOBAL_PROFILES_DIR)
                    return
                except ConfigurationError as e:
                    logger.error(f"Failed to save global profile: {e}")
                    print(f"Error: {e}")
                    return
            
            # Load configuration
            config = await self._load_configuration(args)
            if not config:
                return
            
            # Get profile name to use
            profile_name = config.get('profile') or 'Default'
            dry_run = args.get('dry_run', False)
            
            # Get iTerm2 app instance and window
            app = await iterm2.async_get_app(connection, True)
            initial_win = await self.iterm_manager.get_current_window(
                app, connection, args.get('new'), profile_name
            )
            
            if dry_run:
                logger.info("Dry run mode: No actions will be taken")
                logger.info(f"Would use profile: {profile_name}")
                logger.info(f"Would configure {len(config.get('tabs', {}))} tabs")
            
            # Process tabs
            await self._process_tabs(config.get('tabs', {}), initial_win, profile_name, dry_run)
            
            if dry_run:
                logger.info("Dry run completed successfully")
                
        except TermisException as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"Unexpected error: {e}")
    
    async def _handle_wizard_mode(self) -> tuple[str, Dict[str, Any]]:
        """Handle wizard mode configuration.
        
        Returns:
            Tuple of (config_path, config_dict)
        """
        config_path, config = ConfigWizard.run_wizard()
        print(f"Configuration created at {config_path}")
        
        # Ask if user wants to save it as a global profile
        save_global = input("Would you like to save this configuration as a global profile? (y/n): ")
        if save_global.lower() == 'y':
            profile_name = input("Enter profile name: ")
            try:
                self.profile_manager.save_to_global_profile(config_path, profile_name, GLOBAL_PROFILES_DIR)
            except ConfigurationError as e:
                logger.error(f"Failed to save global profile: {e}")
                print(f"Error: {e}")
        
        print("Run 'termis' to apply this configuration.")
        return config_path, config
    
    async def _load_configuration(self, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Load configuration from file or profile.
        
        Args:
            args: Command line arguments
            
        Returns:
            Configuration dictionary or None if loading failed
        """
        # Load profile if specified
        profile_config = None
        if args.get('profile'):
            try:
                profile_config = self.config_loader.load_profile(args.get('profile'), GLOBAL_PROFILES_DIR)
                logger.info(f"Loaded profile: {args.get('profile')}")
            except ConfigurationError as e:
                logger.error(f"Failed to load profile: {e}")
                print(f"Error: {e}")
                return None
        
        # Determine config path
        config_path = args.get('config') if args.get('config') is not None else DEFAULT_CONFIG
        
        # Use profile as config if profile is specified but no config file exists
        if profile_config and not os.path.exists(config_path):
            return profile_config
            
        try:
            # Load main configuration
            config = self.config_loader.read_config(config_path, dry_run=args.get('dry_run', False))
            
            # Merge with profile if specified
            if profile_config:
                # Deep merge profile config with main config
                for key, value in profile_config.items():
                    if key not in config:
                        config[key] = value
                    elif isinstance(value, dict) and isinstance(config[key], dict):
                        # Merge dictionaries recursively
                        config[key] = {**value, **config[key]}
            
            return config
            
        except ConfigurationError as e:
            logger.error(f"Failed to load configuration: {e}")
            print(f"Error: {e}")
            return None
    
    async def _process_tabs(self, tabs_config: Dict[str, Any], window: iterm2.Window,
                          profile_name: str, dry_run: bool = False) -> Dict[str, Any]:
        """Process all tabs in parallel.
        
        Args:
            tabs_config: Tab configurations
            window: iTerm2 window instance
            profile_name: Profile to use
            dry_run: Whether to run in dry-run mode
            
        Returns:
            Dictionary of tab results
        """
        tab_results = {}
        first_tab = True
        
        # Create a list of tasks for processing tabs
        tasks = []
        
        for tab_id, tab_config in tabs_config.items():
            task = asyncio.create_task(
                self._process_tab(tab_id, tab_config, window, profile_name, first_tab, dry_run)
            )
            tasks.append((tab_id, task))
            first_tab = False
        
        # Wait for all tasks to complete
        for tab_id, task in tasks:
            try:
                result = await task
                if result:
                    tab_results[tab_id] = result
            except Exception as e:
                logger.error(f"Error in tab '{tab_id}': {e}")
        
        return tab_results
    
    async def _process_tab(self, tab_id: str, tab_config: Dict[str, Any], 
                         window: iterm2.Window, profile_name: str,
                         first_tab: bool = False, dry_run: bool = False) -> Optional[Dict[str, Any]]:
        """Process a single tab configuration.
        
        Args:
            tab_id: ID of the tab
            tab_config: Tab configuration
            window: iTerm2 window instance
            profile_name: Profile to use
            first_tab: Whether this is the first tab
            dry_run: Whether to run in dry-run mode
            
        Returns:
            Dictionary with tab and session references or None
        """
        try:
            root_path = tab_config.get('root')
            tab_panes = tab_config.get('panes', [])
            
            # Skip if no panes are defined
            if len(tab_panes) <= 0:
                return None
                
            # Create or reuse tab based on configuration
            if first_tab:
                curr_tab = window.current_tab
            else:
                curr_tab = await self.iterm_manager.create_tab_with_config(
                    window, tab_config, tab_id, profile_name, dry_run
                )
                
            if dry_run:
                logger.info(f"Dry run: Would configure tab '{tab_id}' with {len(tab_panes)} panes")
                return None
            
            # Process commands for each pane
            for pane in tab_panes:
                commands = pane.get('commands', [])
                
                # Add working directory command if root path is specified
                if root_path and not pane.get('working_directory'):
                    pane['root'] = root_path
                
                # Format commands
                pane['commands'] = await self.command_executor.format_commands(
                    commands, pane.get('prompt', '')
                )
            
            # Render the panes for this tab
            sessions_ref = await self.iterm_manager.render_tab_panes(
                curr_tab, tab_panes, profile_name, dry_run
            )
            
            # Return the tab and session references
            return {
                'tab': curr_tab,
                'sessions': sessions_ref
            }
            
        except Exception as e:
            logger.error(f"Error processing tab '{tab_id}': {e}")
            if not dry_run:
                raise TermisException(f"Failed to process tab '{tab_id}': {e}")
            return None