"""
MindChain Framework

A comprehensive platform for building, deploying, and managing AI agents
with a unique Master Control Program (MCP) supervision layer.
"""

from .version import __version__

from .mcp.mcp import MCP
from .core.agent import Agent, AgentConfig, AgentStatus
from .core.orchestrator import AgentOrchestrator
from .memory.memory_manager import MemoryManager
from .core.errors import MindChainError, MCPError, AgentError

__all__ = [
    'MCP',
    'Agent',
    'AgentConfig',
    'AgentStatus',
    'AgentOrchestrator',
    'MemoryManager',
    'MindChainError',
    'MCPError',
    'AgentError',
    '__version__',
]
