"""
Agent base class implementation
"""
import uuid
import logging
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum

from .errors import AgentError
from ..memory.memory_manager import MemoryManager

logger = logging.getLogger(__name__)

class AgentStatus(str, Enum):
    """Enum representing the possible states of an agent"""
    INITIALIZING = "initializing"
    IDLE = "idle"
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    TERMINATED = "terminated"


@dataclass
class AgentConfig:
    """Configuration for an agent"""
    name: str
    description: str = ""
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    tools: List[str] = field(default_factory=list)
    system_prompt: str = "You are a helpful AI assistant."
    metadata: Dict[str, Any] = field(default_factory=dict)


class Agent:
    """
    Base Agent class that encapsulates LLM-powered agent capabilities
    """
    
    def __init__(self, config: AgentConfig, memory_manager: Optional[MemoryManager] = None):
        """
        Initialize the agent with the given configuration
        
        Args:
            config: Agent configuration parameters
            memory_manager: Optional memory manager for the agent
        """
        self.id = str(uuid.uuid4())
        self.config = config
        self.name = config.name
        self.status = AgentStatus.INITIALIZING
        self.memory = memory_manager or MemoryManager()
        self.tools = {}  # Will be populated by tool registry
        self.current_task = None
        self._last_response = None
        self._history = []
        
        logger.info(f"Agent {self.name} ({self.id}) initialized")
        self.status = AgentStatus.IDLE
        
    def reset(self):
        """Reset the agent's state"""
        self._history = []
        self._last_response = None
        self.current_task = None
        self.status = AgentStatus.IDLE
        self.memory.clear_short_term()
        logger.info(f"Agent {self.id} has been reset")
    
    def add_tool(self, tool_name: str, tool_fn: Callable) -> None:
        """
        Add a tool to the agent's available toolset
        
        Args:
            tool_name: Name of the tool
            tool_fn: The tool function to be called
        """
        self.tools[tool_name] = tool_fn
        logger.debug(f"Tool '{tool_name}' added to agent {self.id}")
    
    def remove_tool(self, tool_name: str) -> bool:
        """
        Remove a tool from the agent's available toolset
        
        Args:
            tool_name: Name of the tool to remove
            
        Returns:
            success: Whether the tool was successfully removed
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            logger.debug(f"Tool '{tool_name}' removed from agent {self.id}")
            return True
        return False
    
    async def run(self, user_input: str) -> str:
        """
        Run the agent on a given user input
        
        Args:
            user_input: The user's input to process
            
        Returns:
            response: The agent's response
        """
        if self.status == AgentStatus.ERROR:
            raise AgentError(f"Agent {self.id} is in an error state and cannot process requests")
        
        if self.status == AgentStatus.TERMINATED:
            raise AgentError(f"Agent {self.id} has been terminated")
        
        try:
            self.status = AgentStatus.ACTIVE
            self.current_task = user_input
            
            # Add user input to history
            self._history.append({"role": "user", "content": user_input})
            
            # Retrieve relevant context from memory
            context = await self.memory.retrieve_relevant(user_input)
            
            # Process input and generate response
            response = await self._generate_response(user_input, context)
            
            # Store the interaction in memory
            await self.memory.store({
                "input": user_input,
                "response": response,
                "timestamp": self._get_current_timestamp()
            })
            
            # Update status and return response
            self._last_response = response
            self._history.append({"role": "assistant", "content": response})
            self.status = AgentStatus.IDLE
            return response
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"Error in agent {self.id}: {str(e)}")
            raise AgentError(f"Agent execution error: {str(e)}") from e
    
    async def _generate_response(self, user_input: str, context: List[Dict[str, Any]]) -> str:
        """
        Generate a response based on user input and context
        
        Args:
            user_input: The user's input
            context: Context information from memory
            
        Returns:
            response: The generated response
        """
        # This is a placeholder - in a real implementation, this would call the LLM
        # with proper prompt construction including system prompt, context, and history
        
        # Example implementation:
        messages = [
            {"role": "system", "content": self.config.system_prompt}
        ]
        
        # Add context if available
        if context:
            context_str = "\n\n".join([item.get("content", "") for item in context])
            messages.append({"role": "system", "content": f"Relevant context: {context_str}"})
        
        # Add conversation history (limited to last few exchanges)
        messages.extend(self._history[-6:])  # Add last 3 exchanges (6 messages)
        
        # In a real implementation, this would call the LLM API
        # response = await call_llm_api(
        #     model=self.config.model_name, 
        #     messages=messages,
        #     temperature=self.config.temperature,
        #     max_tokens=self.config.max_tokens
        # )
        
        # For now, just return a placeholder response
        return f"Agent {self.name} processed: {user_input[:30]}...\nThis is a simulated response for demonstration purposes."
    
    def _get_current_timestamp(self) -> int:
        """Get the current timestamp in seconds"""
        import time
        return int(time.time())
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a tool by name with the given arguments
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Arguments to pass to the tool
            
        Returns:
            result: The result of the tool execution
        """
        if tool_name not in self.tools:
            raise AgentError(f"Tool '{tool_name}' not available to agent {self.id}")
        
        try:
            logger.debug(f"Agent {self.id} executing tool '{tool_name}'")
            tool_fn = self.tools[tool_name]
            result = await tool_fn(**kwargs) if callable(tool_fn) else None
            return result
        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {str(e)}")
            raise AgentError(f"Tool execution error: {str(e)}") from e
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent
        
        Returns:
            status: Dictionary with agent status information
        """
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "tools_count": len(self.tools),
            "history_length": len(self._history)
        }