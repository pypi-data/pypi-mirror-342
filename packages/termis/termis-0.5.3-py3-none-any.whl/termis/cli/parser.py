"""Command-line argument parsing module."""

import argparse
import textwrap
from typing import Dict, Any

def parse_arguments() -> Dict[str, Any]:
    """Parse command-line arguments.
    
    Returns:
        Dictionary of parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Workflow automation and layouts for iTerm',
        epilog=textwrap.dedent("""\
        For details on creating configuration files, please head to:

        https://github.com/smithg09/termis
        """),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument('-c', '--config', 
                       help='Path to the configuration file')
    parser.add_argument('-v', '--version', 
                       help='Show version', 
                       action='store_true')
    parser.add_argument('-n', '--new', 
                       help='Run in new window', 
                       action='store_true')
    parser.add_argument('-p', '--profile', 
                       help='Use a profile from ~/.termis/profiles')
    parser.add_argument('-w', '--wizard', 
                       help='Run interactive configuration wizard', 
                       action='store_true')
    parser.add_argument('-d', '--dry-run', 
                       help='Show what would happen without executing', 
                       action='store_true')
    parser.add_argument('-l', '--log-level', 
                       help='Set logging level (debug, info, warning, error)', 
                       default='info')
    parser.add_argument('-s', '--save-global', 
                       help='Save current configuration to global profiles with given name')
    parser.add_argument('-g', '--global-list', 
                       help='List all available global profiles', 
                       action='store_true')
    parser.add_argument('-t', '--tools-check', 
                       help='Check availability of development tools', 
                       action='store_true')

    return vars(parser.parse_args())