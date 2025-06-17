"""
Main Application Entry Point
Mục đích: Bootstrap và run Cursor GraphRAG MCP Server
"""

import asyncio
import sys
from pathlib import Path

# Add src to Python path for imports
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from handlers.mcp_handler import MCPServerBootstrap
from utils.logger import setup_logger
from utils.config import get_config


async def main():
    """
    Application entry point - SOLID compliant
    SRP: ONLY bootstrap and run
    """
    # Setup logging first
    try:
        config = get_config()
        logger = setup_logger("cursor_graphrag_memory", config.log_level)
    except Exception as e:
        # Fallback to basic logging if config fails
        logger = setup_logger("cursor_graphrag_memory", "INFO")
        logger.warning(f"Failed to load config, using defaults: {e}")
    
    logger.info("Starting Cursor GraphRAG Memory System...")
    
    try:
        # Create and initialize bootstrap
        bootstrap = MCPServerBootstrap()
        await bootstrap.initialize()
        
        # Run server
        await bootstrap.run()
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down gracefully...")
        print("\n🛴 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


def run_server():
    """
    Synchronous entry point for external calls
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error running server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Print startup banner
    print("🧠 Cursor GraphRAG Memory System - MCP Server")
    print("Version: 1.0.0")
    print("Architecture: Enhanced with Document/Code Tracking")
    print("Capabilities: Auto-impact analysis, Smart recommendations, Dependency tracking")
    print("="*80)
    
    # Run the server
    run_server()
