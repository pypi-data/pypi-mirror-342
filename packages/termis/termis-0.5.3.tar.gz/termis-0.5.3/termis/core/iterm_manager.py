"""iTerm2 manager module."""

import logging
from typing import Dict, Any, List, Optional, Tuple
import iterm2

from ..exceptions.termis_exceptions import TermisException
from .command_executor import CommandExecutor

logger = logging.getLogger('termis.iterm')

# Define badge theme colors
BADGE_THEMES = {
    'default': {'fg': (213, 194, 194), 'bg': None},
    'success': {'fg': (76, 175, 80), 'bg': None},
    'error': {'fg': (244, 67, 54), 'bg': None},
    'warning': {'fg': (255, 193, 7), 'bg': None},
    'info': {'fg': (33, 150, 243), 'bg': None},
    'primary': {'fg': (156, 39, 176), 'bg': None},
    'secondary': {'fg': (96, 125, 139), 'bg': None},
    'dark': {'fg': (33, 33, 33), 'bg': None},
    'light': {'fg': (227, 227, 227), 'bg': None},
}

class ITermManager:
    """Manages iTerm2 windows, tabs, and sessions."""
    
    @staticmethod
    async def get_current_window(app: iterm2.App, connection: iterm2.Connection, 
                               new: bool, profile_name: str) -> iterm2.Window:
        """Get the current window or create a new one.
        
        Args:
            app: iTerm2 application instance
            connection: iTerm2 connection
            new: Whether to create a new window
            profile_name: Profile to use for new window
            
        Returns:
            iTerm2 window instance
        """
        try:
            curr_win = app.current_window
            
            if not curr_win or new:
                curr_win = await iterm2.Window.async_create(connection, profile=profile_name)
            
            await curr_win.async_activate()
            return curr_win
            
        except Exception as e:
            logger.error(f"Error getting current window: {e}")
            raise TermisException(f"Failed to get current window: {e}")

    @staticmethod
    async def find_tab_by_title(window: iterm2.Window, title: str) -> Optional[iterm2.Tab]:
        """Find a tab by its title in the given window."""
        for tab in window.tabs:
            tab_title = await tab.async_get_title()
            if tab_title == title:
                return tab
        return None

    @staticmethod
    async def add_badge(session: iterm2.Session, badge_config: Dict[str, Any]) -> None:
        """Apply badge to a session with theme support."""
        try:
            profile = await session.async_get_profile()
            
            # Handle different badge configurations
            if isinstance(badge_config, str):
                badge_text = badge_config
                theme = 'default'
            elif isinstance(badge_config, dict):
                badge_text = badge_config.get('text', '')
                theme = badge_config.get('theme', 'default')
            else:
                return
            
            # Apply the badge text
            await profile.async_set_badge_text(badge_text)
            
            # Apply theme if it exists
            if theme in BADGE_THEMES:
                fg_color = BADGE_THEMES[theme]['fg']
                if fg_color:
                    await profile.async_set_badge_color(iterm2.color.Color(*fg_color))
                    
                bg_color = BADGE_THEMES[theme]['bg']
                if bg_color:
                    await profile.async_set_badge_background_color(iterm2.color.Color(*bg_color))
                    
        except Exception as e:
            logger.error(f"Error adding badge: {e}")

    @staticmethod
    def parse_position(position: str) -> Tuple[int, int, int]:
        """Parse a position string into column, row, and column-in-row components.
        
        Args:
            position: Position string in format "column/row/column-in-row"
            
        Returns:
            Tuple of (column, row, column-in-row)
            
        Raises:
            TermisException: If position format is invalid
        """
        parts = position.split('/')
        
        if len(parts) == 1:
            # Just column specified, default row and column-in-row to 1
            return int(parts[0]), 1, 1
        elif len(parts) == 2:
            # Column and row specified, default column-in-row to 1
            return int(parts[0]), int(parts[1]), 1
        elif len(parts) == 3:
            # All three components specified
            return int(parts[0]), int(parts[1]), int(parts[2])
        else:
            raise TermisException(f"Invalid position format: {position}")

    @staticmethod
    async def create_tab_with_config(window: iterm2.Window, tab_config: Dict[str, Any], 
                                   tab_id: str, profile_name: str, dry_run: bool = False) -> Optional[iterm2.Tab]:
        """Create and configure a tab based on its configuration."""
        try:
            # Check if we should reuse an existing tab with the same title
            tab_title = tab_config.get('title')
            reuse_tab = tab_config.get('reuse', False)
            
            if reuse_tab and tab_title:
                existing_tab = await ITermManager.find_tab_by_title(window, tab_title)
                if existing_tab:
                    if dry_run:
                        logger.info(f"Dry run: Would reuse existing tab with title '{tab_title}'")
                        return None
                    return existing_tab
            
            if dry_run:
                logger.info(f"Dry run: Would create new tab for '{tab_title or tab_id}'")
                return None
                
            # Create a new tab
            new_tab = await window.async_create_tab(profile=profile_name)
            
            # Set tab title if provided
            if tab_title:
                await new_tab.async_set_title(tab_title)
                
            return new_tab
            
        except Exception as e:
            logger.error(f"Error creating tab: {e}")
            raise TermisException(f"Failed to create tab: {e}")

    @staticmethod
    async def render_tab_panes(tab: iterm2.Tab, panes: List[Dict[str, Any]], 
                             profile_name: str, dry_run: bool = False) -> Dict[str, iterm2.Session]:
        """Render panes within a tab with dependencies between panes"""
        if dry_run:
            logger.info(f"Dry run: Would render {len(panes)} panes in tab '{await tab.async_get_title()}'")
            return {}
        
        # Parse all positions and organize panes by position
        column_map = {}  # Structure: {column_num: {row_num: {col_in_row_num: pane}}}
        
        for pane in panes:
            position = pane.get("position", "1/1/1")
            try:
                column, row, column_in_row = ITermManager.parse_position(position)
                
                # Initialize nested dictionaries if needed
                if column not in column_map:
                    column_map[column] = {}
                if row not in column_map[column]:
                    column_map[column][row] = {}
                    
                column_map[column][row][column_in_row] = pane
                # Store the parsed position back in the pane config
                pane["position"] = f"{column}/{row}/{column_in_row}"
            except Exception as e:
                logger.error(f"Invalid position format '{position}': {e}")
                continue
        
        # Track sessions by their position
        sessions = {}
        
        # First, get the initial session in the tab
        current_session = tab.current_session
        sessions["1/1/1"] = current_session
        
        # Keep track of which session should receive focus at the end
        focus_session = current_session
        
        # Process all main columns first (1/1/1, 2/1/1, 3/1/1, etc.)
        columns = sorted(column_map.keys())
        
        # Apply settings to the first column/pane (which already exists)
        if 1 in columns and 1 in column_map[1] and 1 in column_map[1][1]:
            first_pane = column_map[1][1][1]
            
            # Apply profile if specified
            pane_profile = first_pane.get('profile', profile_name)
            if pane_profile != profile_name:
                profile = await iterm2.Profile.async_get(current_session.connection, pane_profile)
                if profile:
                    await current_session.async_set_profile(profile)
            
            # Apply other settings
            if first_pane.get('title'):
                await current_session.async_set_name(first_pane.get('title'))
            
            if first_pane.get('color'):
                await current_session.async_set_color_preset(first_pane.get('color'))
            
            if first_pane.get('badge'):
                await ITermManager.add_badge(current_session, first_pane.get('badge'))
            
            if first_pane.get('focus'):
                focus_session = current_session
            
            # Execute commands
            commands = first_pane.get('commands', [])
            delay = first_pane.get('command_delay', 0)
            working_dir = first_pane.get('working_directory')
            
            if not working_dir and first_pane.get('root'):
                working_dir = first_pane.get('root')
            
            await CommandExecutor.execute_commands(current_session, commands, delay, working_dir, first_pane)
        
        # Create subsequent main columns (vertical splits) sequentially
        previous_column = 1
        for column in [c for c in columns if c > 1]:
            if 1 not in column_map[column] or 1 not in column_map[column][1]:
                continue
            
            pane = column_map[column][1][1]
            pane_profile = pane.get('profile', profile_name)
            
            # Create vertical split from the previous column
            previous_position = f"{previous_column}/1/1"
            parent_session = sessions[previous_position]
            new_session = await parent_session.async_split_pane(vertical=True, profile=pane_profile)
            position = f"{column}/1/1"
            sessions[position] = new_session
            
            # Update previous column for the next iteration
            previous_column = column
            
            # Apply settings
            if pane.get('title'):
                await new_session.async_set_name(pane.get('title'))
            
            if pane.get('color'):
                await new_session.async_set_color_preset(pane.get('color'))
            
            if pane.get('badge'):
                await ITermManager.add_badge(new_session, pane.get('badge'))
            
            if pane.get('focus'):
                focus_session = new_session
            
            # Execute commands
            commands = pane.get('commands', [])
            delay = pane.get('command_delay', 0)
            working_dir = pane.get('working_directory')
            
            if not working_dir and pane.get('root'):
                working_dir = pane.get('root')
            
            await CommandExecutor.execute_commands(new_session, commands, delay, working_dir, pane)
        
        # Now process rows within each column
        for column in columns:
            rows = sorted([r for r in column_map.get(column, {}).keys() if r > 1])
            
            if not rows:
                continue
                
            # Get the first row's parent (column's main pane)
            parent_position = f"{column}/1/1"
            parent_session = sessions.get(parent_position)
            
            if not parent_session:
                logger.warning(f"Parent session not found for {parent_position}")
                continue
                
            # Create rows sequentially within this column
            previous_row = 1
            for row in rows:
                if 1 not in column_map[column][row]:
                    continue
                
                # Get the first pane in this row
                pane = column_map[column][row][1]
                pane_profile = pane.get('profile', profile_name)
                
                # For first row in column, split from the column's main pane
                # For subsequent rows, split from the previous row
                parent_position = f"{column}/{previous_row}/1"
                parent_session = sessions.get(parent_position)
                
                if not parent_session:
                    logger.warning(f"Parent session not found for {parent_position}")
                    continue
                
                # Create horizontal split from the parent
                new_session = await parent_session.async_split_pane(vertical=False, profile=pane_profile)
                position = f"{column}/{row}/1"
                sessions[position] = new_session
                
                # Update previous row for next iteration
                previous_row = row
                
                # Apply settings
                if pane.get('title'):
                    await new_session.async_set_name(pane.get('title'))
                
                if pane.get('color'):
                    await new_session.async_set_color_preset(pane.get('color'))
                
                if pane.get('badge'):
                    await ITermManager.add_badge(new_session, pane.get('badge'))
                
                if pane.get('focus'):
                    focus_session = new_session
                
                # Execute commands
                commands = pane.get('commands', [])
                delay = pane.get('command_delay', 0)
                working_dir = pane.get('working_directory')
                
                if not working_dir and pane.get('root'):
                    working_dir = pane.get('root')
                
                await CommandExecutor.execute_commands(new_session, commands, delay, working_dir, pane)
        
        # Finally, process columns within rows (the third level of hierarchy)
        for column in columns:
            for row in column_map.get(column, {}).keys():
                cols_in_row = sorted([c for c in column_map[column][row].keys() if c > 1])
                
                if not cols_in_row:
                    continue
                    
                # Create columns sequentially within this row
                previous_col_in_row = 1
                for col_in_row in cols_in_row:
                    pane = column_map[column][row][col_in_row]
                    pane_profile = pane.get('profile', profile_name)
                    
                    # Get parent - the previous column in this row
                    parent_position = f"{column}/{row}/{previous_col_in_row}"
                    parent_session = sessions.get(parent_position)
                    
                    if not parent_session:
                        logger.warning(f"Parent session not found for {parent_position}")
                        continue
                    
                    # Create vertical split within the row
                    new_session = await parent_session.async_split_pane(vertical=True, profile=pane_profile)
                    position = f"{column}/{row}/{col_in_row}"
                    sessions[position] = new_session
                    
                    # Update previous column for next iteration
                    previous_col_in_row = col_in_row
                    
                    # Apply settings
                    if pane.get('title'):
                        await new_session.async_set_name(pane.get('title'))
                    
                    if pane.get('color'):
                        await new_session.async_set_color_preset(pane.get('color'))
                    
                    if pane.get('badge'):
                        await ITermManager.add_badge(new_session, pane.get('badge'))
                    
                    if pane.get('focus'):
                        focus_session = new_session
                    
                    # Execute commands
                    commands = pane.get('commands', [])
                    delay = pane.get('command_delay', 0)
                    working_dir = pane.get('working_directory')
                    
                    if not working_dir and pane.get('root'):
                        working_dir = pane.get('root')
                    
                    await CommandExecutor.execute_commands(new_session, commands, delay, working_dir, pane)
        
        # Set focus to the specified session
        await focus_session.async_activate()
        
        return sessions
