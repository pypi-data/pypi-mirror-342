#!/usr/bin/env python3
"""Main entry point for Termis application."""

import os
import logging
import iterm2

from .cli.parser import parse_arguments
from .core.termis_app import TermisApp
from .utils.constants import ERROR_LOG_PATH, GLOBAL_PROFILES_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('termis')

async def activate(connection: iterm2.Connection) -> None:
    """Main activation function for iTerm2 connection.
    
    Args:
        connection: iTerm2 connection instance
    """
    try:
        args = parse_arguments()
    except SystemExit:
        return

    # Create and run the Termis application
    app = TermisApp()
    await app.activate(connection, args)

def main() -> None:
    """Main entry point for the Termis application."""
    # Create necessary directories
    os.makedirs(os.path.dirname(ERROR_LOG_PATH), exist_ok=True)
    os.makedirs(GLOBAL_PROFILES_DIR, exist_ok=True)
    
    # Run the app
    iterm2.run_until_complete(activate)

if __name__ == "__main__":
    main()