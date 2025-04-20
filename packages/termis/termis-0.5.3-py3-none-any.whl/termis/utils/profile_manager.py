"""Profile management utilities."""

import os
import re
import shutil
import logging
import yaml
from typing import List, Tuple
from ..exceptions.termis_exceptions import ConfigurationError

logger = logging.getLogger('termis.utils')

class ProfileManager:
    """Manages global profile configuration files."""
    
    @staticmethod
    def save_to_global_profile(config_path: str, profile_name: str, profiles_dir: str) -> bool:
        """Save a configuration to the global profiles directory.
        
        Args:
            config_path: Path to the configuration file
            profile_name: Name for the profile
            profiles_dir: Directory to store global profiles
            
        Returns:
            True if profile was saved successfully
            
        Raises:
            ConfigurationError: If profile name is invalid or config doesn't exist
        """
        if not os.path.exists(config_path):
            raise ConfigurationError(f"Configuration file does not exist: {config_path}")
            
        # Ensure the profile name is valid
        if not profile_name or not re.match(r'^[a-zA-Z0-9_-]+$', profile_name):
            raise ConfigurationError(
                f"Invalid profile name: {profile_name}. "
                "Use alphanumeric characters, underscores, and hyphens only."
            )
        
        # Create target path
        target_path = os.path.join(profiles_dir, f"{profile_name}.yml")
        
        # Check if profile already exists
        if os.path.exists(target_path):
            overwrite = input(f"Profile '{profile_name}' already exists. Overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                print("Operation cancelled.")
                return False
        
        # Copy the file to the profiles directory
        try:
            shutil.copy2(config_path, target_path)
            print(f"Configuration saved to global profile: {profile_name}")
            return True
        except Exception as e:
            logger.error(f"Error saving to global profile: {e}")
            raise ConfigurationError(f"Failed to save global profile: {e}")
    
    @staticmethod
    def list_global_profiles(profiles_dir: str) -> List[Tuple[str, str, str]]:
        """List all available global profiles.
        
        Args:
            profiles_dir: Directory containing global profiles
            
        Returns:
            List of tuples containing (profile_name, display_name, description)
        """
        if not os.path.exists(profiles_dir):
            print("No global profiles found.")
            return []
            
        profiles = []
        for file in os.listdir(profiles_dir):
            if file.endswith('.yml'):
                profile_name = file[:-4]  # Remove .yml extension
                profile_path = os.path.join(profiles_dir, file)
                
                # Try to get metadata from the profile
                try:
                    with open(profile_path) as f:
                        config = yaml.safe_load(f)
                    metadata = config.get('metadata', {})
                    name = metadata.get('name', profile_name)
                    description = metadata.get('description', '')
                    profiles.append((profile_name, name, description))
                except:
                    # If we can't read the config, just use the filename
                    profiles.append((profile_name, profile_name, ''))
        
        return sorted(profiles)
    
    @staticmethod
    def print_profiles_list(profiles: List[Tuple[str, str, str]]) -> None:
        """Print a formatted list of profiles.
        
        Args:
            profiles: List of profile tuples (name, display_name, description)
        """
        if not profiles:
            print("No global profiles found.")
            return
            
        print("Available global profiles:")
        print("=" * 60)
        for profile_name, name, description in profiles:
            print(f"{profile_name:20} | {name}")
            if description:
                print(f"{' ':20} | {description}")
            print("-" * 60)