"""
Agents package for ChatKit backend.

Provides:
- LLM provider factory
- Robotics tutor agent
"""

from .factory import create_model
from .tutor import create_tutor_agent

__all__ = [
    "create_model",
    "create_tutor_agent",
]
