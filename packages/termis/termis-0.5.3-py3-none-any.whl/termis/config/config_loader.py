"""Configuration loader module."""

import json
import os
import re
import yaml
import logging
from typing import Dict, Any, Optional

from ..exceptions.termis_exceptions import ConfigurationError

logger = logging.getLogger('termis.config')

class ConfigLoader:
    """Handles config loading with support for includes and environment variables."""
    
    @staticmethod
    def read_config(config_path: str, tag: str = '!ENV', dry_run: bool = False) -> Dict[str, Any]:
        """Read and parse configuration from a YAML file.
        
        Args:
            config_path: Path to the configuration file
            tag: Environment variable tag to process
            dry_run: Whether to run in dry-run mode
            
        Returns:
            Dict containing the parsed configuration
            
        Raises:
            ConfigurationError: If config file doesn't exist or has invalid format
        """
        if not os.path.isfile(config_path):
            raise ConfigurationError(f"Config file does not exist at {config_path}")

        # REGEX for ${word}
        tag_regex = re.compile(r'.*?\${(\w+)}.*?')
        loader = yaml.FullLoader
        loader.add_implicit_resolver(tag, tag_regex, None)
        
        def env_variables(loader, node):
            """Process environment variables in configuration."""
            scalar = loader.construct_scalar(node)
            match = tag_regex.findall(scalar)
            if match:
                value = scalar
                for g in match:
                    value = value.replace(f'${{{g}}}', os.environ.get(g, g))
                return value
            return scalar
        
        def include_constructor(loader, node):
            """Process include directives in configuration."""
            include_path = loader.construct_scalar(node)
            
            # Handle relative paths
            if not os.path.isabs(include_path):
                base_dir = os.path.dirname(os.path.abspath(config_path))
                include_path = os.path.join(base_dir, include_path)
                
            if not os.path.exists(include_path):
                raise ConfigurationError(f"Included file does not exist: {include_path}")
                
            with open(include_path, 'r') as f:
                return yaml.load(f, Loader=loader)
        
        # Add constructors
        loader.add_constructor(tag, env_variables)
        loader.add_constructor('!include', include_constructor)
        
        try:
            with open(config_path) as file:
                config = yaml.load(file, Loader=loader)
                
                if dry_run:
                    logger.info(f"Dry run: Loaded config from {config_path}")
                    logger.info(f"Config structure: {json.dumps(ConfigLoader.sanitize_config(config), indent=2)}")
                
                return config
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML config: {e}")
            raise ConfigurationError(f"Error parsing YAML config: {e}")
    
    @staticmethod
    def load_profile(profile_name: str, profiles_dir: str) -> Dict[str, Any]:
        """Load a global profile configuration.
        
        Args:
            profile_name: Name of the profile to load
            profiles_dir: Directory containing profile configurations
            
        Returns:
            Dict containing the profile configuration
            
        Raises:
            ConfigurationError: If profile doesn't exist or has invalid format
        """
        if not os.path.exists(profiles_dir):
            raise ConfigurationError(f"Global profiles directory does not exist: {profiles_dir}")
            
        profile_path = os.path.join(profiles_dir, f"{profile_name}.yml")
        if not os.path.exists(profile_path):
            raise ConfigurationError(f"Profile does not exist: {profile_path}")
            
        return ConfigLoader.read_config(profile_path)
    
    @staticmethod
    def sanitize_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive data from config for logging purposes."""
        if isinstance(config, dict):
            return {k: ConfigLoader.sanitize_config(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [ConfigLoader.sanitize_config(i) for i in config]
        else:
            return config