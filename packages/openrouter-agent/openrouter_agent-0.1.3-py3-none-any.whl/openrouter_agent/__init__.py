"""
OpenRouter Agent for Pydantic AI

A Python library that extends the Pydantic AI framework to support OpenRouter models.
"""

# Import classes for easy access
from .agent import OpenRouterModel, OpenRouterAgent, Agent

# Export all the important classes
__all__ = ["OpenRouterModel", "OpenRouterAgent", "Agent"]

# Version information
__version__ = "0.1.0"