"""
Master Control Program (MCP) module

This module contains the implementation of the Master Control Program,
which serves as the supervisory layer for the agent system.
"""

from .mcp import MCP
from .policies import PolicyManager
from .resource_manager import ResourceManager
from .metrics import AgentMetrics

__all__ = ['MCP', 'PolicyManager', 'ResourceManager', 'AgentMetrics']
