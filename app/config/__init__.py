"""Config package exports the settings instance for easy imports.

Usage:
	from app.config import settings
	print(settings.LOG_LEVEL)
"""

from .settings import settings

__all__ = ["settings"]
