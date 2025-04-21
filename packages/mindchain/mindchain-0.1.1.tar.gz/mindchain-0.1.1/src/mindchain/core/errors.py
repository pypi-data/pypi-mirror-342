"""
Error definitions for the MindChain framework
"""

class MindChainError(Exception):
    """Base exception class for all framework errors"""
    pass

class MCPError(MindChainError):
    """Errors related to the Master Control Program"""
    pass

class AgentError(MindChainError):
    """Errors related to agent operations"""
    pass

class MemoryError(MindChainError):
    """Errors related to memory operations"""
    pass

class ToolError(MindChainError):
    """Errors related to tool operations"""
    pass

class ExecutionError(MindChainError):
    """Errors related to task execution"""
    pass

class ResourceExhaustedError(MindChainError):
    """Error raised when a resource limit is reached"""
    pass

class PlanningError(MindChainError):
    """Errors related to planning operations"""
    pass

class OrchestrationError(MindChainError):
    """Errors related to agent orchestration"""
    pass