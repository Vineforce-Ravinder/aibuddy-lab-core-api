import logging

logger = logging.getLogger(__name__)

async def on_startup():
    logger.info("🚀 AI Buddy starting up")
    # Connect DB
    # Init cache
    # Load ML / LLM models

async def on_shutdown():
    logger.info("🛑 AI Buddy shutting down")
    # Close DB
    # Cleanup resources
