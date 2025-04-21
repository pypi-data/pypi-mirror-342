"""
Metrics definitions for tracking agent performance and resource usage
"""
from dataclasses import dataclass

@dataclass
class AgentMetrics:
    """Metrics for tracking agent performance and resource usage"""
    created_at: float
    last_active: float
    total_tokens_used: int = 0
    total_api_calls: int = 0
    total_tasks_completed: int = 0
    total_errors: int = 0
    average_response_time: float = 0.0