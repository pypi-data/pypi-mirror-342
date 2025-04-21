"""
Policy Management for MCP

This module defines the policy enforcement mechanisms for the Master Control Program.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PolicyManager:
    """
    Manages and enforces policies for agent behavior and resource usage
    """
    
    def __init__(self, policy_config: Dict[str, Any]):
        """
        Initialize the policy manager with a configuration
        
        Args:
            policy_config: Configuration for policies
        """
        self.policies = self._load_default_policies()
        self.policies.update(policy_config)
        logger.info("Policy Manager initialized with %d policies", len(self.policies))
    
    def _load_default_policies(self) -> Dict[str, Any]:
        """Load default policy settings"""
        return {
            # Safety policies
            "max_consecutive_errors": 3,
            "default_timeout": 30,
            "allow_external_tools": False,
            "allow_code_execution": False,
            
            # Resource policies
            "max_tokens_per_response": 2000,
            "max_api_calls_per_minute": 20,
            
            # Operational policies
            "auto_recovery_enabled": True,
            "logging_verbosity": "info"
        }
    
    def check_tool_permission(self, agent_id: str, tool_name: str) -> bool:
        """
        Check if an agent is allowed to use a particular tool
        
        Args:
            agent_id: The ID of the agent
            tool_name: The name of the tool
            
        Returns:
            allowed: Whether the agent is allowed to use the tool
        """
        # High-risk tools require explicit permissions
        high_risk_tools = ["web_search", "code_execution", "file_system_access"]
        
        if tool_name in high_risk_tools:
            if tool_name == "web_search" and not self.policies.get("allow_external_tools", False):
                logger.warning(f"Agent {agent_id} denied access to web search tool (external tools not allowed)")
                return False
                
            if tool_name == "code_execution" and not self.policies.get("allow_code_execution", False):
                logger.warning(f"Agent {agent_id} denied access to code execution tool (code execution not allowed)")
                return False
                
            if tool_name == "file_system_access":
                logger.warning(f"Agent {agent_id} denied access to file system (always restricted)")
                return False
        
        return True
    
    def enforce_token_limits(self, content: str) -> str:
        """
        Enforce token limits on content
        
        Args:
            content: The content to check
            
        Returns:
            content: The possibly truncated content
        """
        max_tokens = self.policies.get("max_tokens_per_response", 2000)
        
        # Simple approximation: 1 token ≈ 4 characters
        # In a real implementation, use a proper tokenizer
        max_chars = max_tokens * 4
        
        if len(content) > max_chars:
            truncated = content[:max_chars]
            return truncated + "... [Content truncated due to token limit]"
        
        return content
    
    def get_policy(self, policy_name: str, default: Any = None) -> Any:
        """
        Get a policy value by name
        
        Args:
            policy_name: Name of the policy
            default: Default value if policy not found
            
        Returns:
            value: The policy value
        """
        return self.policies.get(policy_name, default)
    
    def update_policy(self, policy_name: str, value: Any) -> None:
        """
        Update a policy value
        
        Args:
            policy_name: Name of the policy to update
            value: New value for the policy
        """
        self.policies[policy_name] = value
        logger.info(f"Policy '{policy_name}' updated to: {value}")
    
    def get_all_policies(self) -> Dict[str, Any]:
        """
        Get all policies
        
        Returns:
            policies: Dictionary of all policies
        """
        return self.policies.copy()