"""
Master Control Program (MCP)

The supervisory layer responsible for managing and monitoring all agents in the system.
"""
import logging
import uuid
import time
from typing import Dict, List, Optional, Any, Callable, Coroutine, TypeVar, cast
import asyncio

from ..core.agent import Agent
from ..core.errors import MCPError
from .policies import PolicyManager
from .resource_manager import ResourceManager
from .metrics import AgentMetrics

logger = logging.getLogger(__name__)

T = TypeVar('T')

class MCP:
    """
    Master Control Program - Supervisory layer for the agent system
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MCP with the given configuration
        
        Args:
            config: Configuration parameters for the MCP
        """
        self.config = config or {}
        self.agents: Dict[str, Agent] = {}
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self._init_logging()
        self.policy_manager = PolicyManager(self.config.get('policies', {}))
        self.resource_manager = ResourceManager(self.config.get('resource_limits', {}))
        self.policies = self.config.get('policies', {
            'allow_external_tools': False,
            'allow_code_execution': False,
            'max_tokens_per_response': 2000,
        })
        self.logger.info("MCP initialized with policies: %s", self.policies)
    
    def _init_logging(self):
        """Configure logging system based on configuration"""
        log_level = self.config.get('log_level', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        self.logger = logging.getLogger('MindChain.MCP')
    
    def register_agent(self, agent: Agent) -> str:
        """
        Register an agent with MCP for supervision
        
        Args:
            agent: The agent instance to register
            
        Returns:
            agent_id: Unique ID assigned to the agent
        """
        # Check if we've reached the maximum number of agents
        if not self.resource_manager.can_allocate_agent():
            raise MCPError("Maximum number of agents reached")
        
        # Generate a unique ID for the agent if not already set
        agent_id = agent.id if hasattr(agent, 'id') and agent.id else str(uuid.uuid4())
        agent.id = agent_id
        
        # Store the agent and initialize its metrics
        self.agents[agent_id] = agent
        self.agent_metrics[agent_id] = AgentMetrics(
            created_at=time.time(),
            last_active=time.time()
        )
        
        # Allocate resources for this agent
        self.resource_manager.allocate_agent()
        
        self.logger.info(f"Registered agent '{agent.name}' with ID: {agent_id}")
        
        # Link agent to MCP (if agent has mcp attribute)
        if hasattr(agent, 'mcp'):
            agent.mcp = self
        
        return agent_id
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent from the MCP.
        
        Args:
            agent_id: The ID of the agent to unregister
        
        Returns:
            bool: True if the agent was successfully unregistered, False otherwise
        """
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            self.logger.info(f"Unregistering agent '{agent.name}' with ID: {agent_id}")
            del self.agents[agent_id]
            
            # Also remove metrics and deallocate resources
            if agent_id in self.agent_metrics:
                del self.agent_metrics[agent_id]
                
            self.resource_manager.deallocate_agent()
            return True
        else:
            self.logger.warning(f"Attempted to unregister unknown agent ID: {agent_id}")
            return False
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
        Get an agent by ID.
        
        Args:
            agent_id: The ID of the agent
        
        Returns:
            Optional[Agent]: The agent if found, None otherwise
        """
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all registered agents.
        
        Returns:
            List[Dict[str, Any]]: A list of agent information dictionaries
        """
        return [
            {
                'id': agent_id,
                'name': agent.name,
                'description': agent.config.description,
                'status': agent.status.value if hasattr(agent.status, 'value') else agent.status
            }
            for agent_id, agent in self.agents.items()
        ]
    
    def update_metrics(self, agent_id: str, 
                      tokens_used: int = 0, 
                      api_calls: int = 0,
                      task_completed: bool = False,
                      error_occurred: bool = False,
                      response_time: float = None):
        """
        Update the metrics for an agent
        
        Args:
            agent_id: The agent's unique identifier
            tokens_used: Number of tokens used in this operation
            api_calls: Number of API calls made in this operation
            task_completed: Whether a task was completed
            error_occurred: Whether an error occurred
            response_time: Time taken to generate a response (in seconds)
        """
        if agent_id not in self.agent_metrics:
            self.logger.warning(f"Attempted to update metrics for unregistered agent {agent_id}")
            return
        
        metrics = self.agent_metrics[agent_id]
        metrics.last_active = time.time()
        metrics.total_tokens_used += tokens_used
        metrics.total_api_calls += api_calls
        
        if task_completed:
            metrics.total_tasks_completed += 1
        
        if error_occurred:
            metrics.total_errors += 1
        
        if response_time is not None:
            # Update running average
            if metrics.average_response_time == 0:
                metrics.average_response_time = response_time
            else:
                # Simple moving average
                metrics.average_response_time = (metrics.average_response_time * 0.9) + (response_time * 0.1)
                
        # Update resource manager if tokens were used
        if tokens_used > 0:
            self.resource_manager.use_tokens(tokens_used)
    
    async def supervise_execution(
        self, 
        agent_id: str,
        task: Callable[[], Coroutine[Any, Any, T]]
    ) -> T:
        """
        Supervise the execution of an agent's task.
        
        Args:
            agent_id: The ID of the agent executing the task
            task: An async callable that performs the task
        
        Returns:
            The result of the task execution
        
        Raises:
            ValueError: If the agent ID is invalid
        """
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Invalid agent ID: {agent_id}")
        
        self.logger.debug(f"Supervising execution for agent '{agent.name}' ({agent_id})")
        
        start_time = time.time()
        try:
            # Allocate resources for this task
            self.resource_manager.start_task()
            
            # Execute the task and get the result
            result = await task()
            
            # Record task completion
            self.resource_manager.complete_task()
            
            # Apply policies to the result if needed
            if isinstance(result, str):
                result = self.policy_manager.enforce_token_limits(result)
            
            # Update metrics
            elapsed_time = time.time() - start_time
            self.update_metrics(
                agent_id=agent_id,
                task_completed=True,
                response_time=elapsed_time
            )
            
            return cast(T, result)
        
        except Exception as e:
            # Record task completion (even though it failed)
            self.resource_manager.complete_task()
            
            # Update error metrics
            self.update_metrics(
                agent_id=agent_id,
                error_occurred=True
            )
            
            self.logger.error(
                f"Error during execution of task for agent '{agent.name}': {str(e)}",
                exc_info=True
            )
            raise
    
    def recover_agent(self, agent_id: str) -> bool:
        """
        Attempt to recover an agent that's in an error state
        
        Args:
            agent_id: The agent's unique identifier
            
        Returns:
            success: Whether recovery was successful
        """
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        self.logger.info(f"Attempting to recover agent {agent_id}")
        
        # Example recovery logic - reset agent state
        try:
            agent.reset()
            return True
        except Exception as e:
            self.logger.error(f"Failed to recover agent {agent_id}: {str(e)}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get the overall status of the MCP system
        
        Returns:
            status: Dictionary containing system status information
        """
        # Count agents by status
        status_counts = {}
        for agent in self.agents.values():
            status = agent.status.value if hasattr(agent.status, 'value') else agent.status
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
        
        # Calculate metrics
        total_tokens = sum(m.total_tokens_used for m in self.agent_metrics.values())
        total_tasks = sum(m.total_tasks_completed for m in self.agent_metrics.values())
        total_errors = sum(m.total_errors for m in self.agent_metrics.values())
        
        # Get usage from resource manager
        resource_usage = self.resource_manager.get_resource_usage()
        
        return {
            "total_agents": len(self.agents),
            "agent_status": status_counts,
            "total_tokens_used": total_tokens,
            "total_tasks_completed": total_tasks,
            "total_errors": total_errors,
            "resource_usage": resource_usage,
            "uptime": time.time() - min((m.created_at for m in self.agent_metrics.values()), default=time.time()),
        }
