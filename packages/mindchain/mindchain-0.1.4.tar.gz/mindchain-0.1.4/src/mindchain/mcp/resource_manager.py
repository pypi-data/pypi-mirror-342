"""
Resource Manager for the MCP

This module handles resource allocation, tracking, and limits for the system.
"""
import logging
import time
from typing import Dict, Any, List, Optional, cast

logger = logging.getLogger(__name__)

class ResourceManager:
    """
    Manages system resources and enforces resource limits
    """
    
    def __init__(self, resource_limits: Dict[str, Any]) -> None:
        """
        Initialize the resource manager with limits
        
        Args:
            resource_limits: Dictionary of resource limits
        """
        self.limits = self._load_default_limits()
        self.limits.update(resource_limits)
        
        # Current resource usage
        self.current_usage = {
            "agents": 0,
            "tokens_used": 0,
            "active_tasks": 0,
        }
        
        # Rate limiting trackers
        self.api_call_timestamps: List[float] = []
        
        logger.info("Resource Manager initialized with limits: %s", self.limits)
    
    def _load_default_limits(self) -> Dict[str, Any]:
        """Load default resource limits"""
        return {
            "max_agents": 10,
            "max_tokens_per_request": 4000,
            "max_total_tokens": 100000,
            "max_concurrent_tasks": 5,
            "max_api_calls_per_minute": 60,
        }
    
    def can_allocate_agent(self) -> bool:
        """
        Check if a new agent can be allocated
        
        Returns:
            can_allocate: Whether allocation is possible
        """
        return self.current_usage["agents"] < self.limits.get("max_agents", 10)
    
    def allocate_agent(self) -> bool:
        """
        Allocate resources for a new agent
        
        Returns:
            success: Whether allocation was successful
        """
        if not self.can_allocate_agent():
            logger.warning("Agent allocation failed: maximum number of agents reached")
            return False
        
        self.current_usage["agents"] += 1
        logger.debug("Agent allocated. Current count: %d", self.current_usage["agents"])
        return True
    
    def deallocate_agent(self) -> None:
        """Deallocate resources for an agent that is being removed"""
        self.current_usage["agents"] = max(0, self.current_usage["agents"] - 1)
        logger.debug("Agent deallocated. Current count: %d", self.current_usage["agents"])
    
    def can_execute_task(self) -> bool:
        """
        Check if a new task can be started
        
        Returns:
            can_execute: Whether task execution is possible
        """
        return self.current_usage["active_tasks"] < self.limits.get("max_concurrent_tasks", 5)
    
    def start_task(self) -> bool:
        """
        Allocate resources for a new task
        
        Returns:
            success: Whether allocation was successful
        """
        if not self.can_execute_task():
            logger.warning("Task start failed: maximum concurrent tasks reached")
            return False
        
        self.current_usage["active_tasks"] += 1
        logger.debug("Task started. Active tasks: %d", self.current_usage["active_tasks"])
        return True
    
    def complete_task(self) -> None:
        """Mark a task as completed and release its resources"""
        self.current_usage["active_tasks"] = max(0, self.current_usage["active_tasks"] - 1)
        logger.debug("Task completed. Active tasks: %d", self.current_usage["active_tasks"])
    
    def can_use_tokens(self, token_count: int) -> bool:
        """
        Check if tokens can be consumed
        
        Args:
            token_count: Number of tokens to be used
            
        Returns:
            can_use: Whether token usage is allowed
        """
        # Check if this request would exceed per-request limit
        if token_count > self.limits.get("max_tokens_per_request", 4000):
            logger.warning("Token usage denied: exceeds max tokens per request")
            return False
        
        # Check if this would exceed total token limit
        future_total = self.current_usage["tokens_used"] + token_count
        if future_total > self.limits.get("max_total_tokens", 100000):
            logger.warning("Token usage denied: would exceed max total tokens")
            return False
        
        return True
    
    def use_tokens(self, token_count: int) -> bool:
        """
        Record token usage
        
        Args:
            token_count: Number of tokens used
            
        Returns:
            success: Whether token usage was recorded
        """
        if not self.can_use_tokens(token_count):
            return False
        
        self.current_usage["tokens_used"] += token_count
        logger.debug("Tokens used: %d. Total usage: %d", 
                    token_count, self.current_usage["tokens_used"])
        return True
    
    def record_api_call(self) -> bool:
        """
        Record an API call for rate limiting
        
        Returns:
            allowed: Whether the API call was allowed
        """
        current_time = time.time()
        max_calls = self.limits.get("max_api_calls_per_minute", 60)
        
        # Remove timestamps older than 1 minute
        one_minute_ago = current_time - 60
        self.api_call_timestamps = [ts for ts in self.api_call_timestamps if ts > one_minute_ago]
        
        # Check if we're at the limit
        if len(self.api_call_timestamps) >= max_calls:
            logger.warning("API call denied: rate limit reached")
            return False
        
        # Record this call
        self.api_call_timestamps.append(current_time)
        return True
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """
        Get current resource usage statistics
        
        Returns:
            usage: Dictionary of resource usage
        """
        return {
            "agents": self.current_usage["agents"],
            "active_tasks": self.current_usage["active_tasks"],
            "tokens_used": self.current_usage["tokens_used"],
            "api_calls_last_minute": len(self.api_call_timestamps),
        }
    
    def get_resource_limits(self) -> Dict[str, Any]:
        """
        Get current resource limits
        
        Returns:
            limits: Dictionary of resource limits
        """
        return self.limits.copy()