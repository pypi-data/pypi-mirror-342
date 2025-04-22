"""
Memory Manager for storing and retrieving information for agents
"""
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class MemoryManager:
    """
    Memory Manager handles storage and retrieval of information for agents
    """
    
    def __init__(self) -> None:
        """Initialize the memory manager with empty storage"""
        self.short_term_memory: List[Dict[str, Any]] = []
        self.long_term_memory: List[Dict[str, Any]] = []
        logger.info("Memory Manager initialized")
    
    async def store(self, item: Dict[str, Any]) -> None:
        """
        Store an item in memory
        
        Args:
            item: The item to store
        """
        # In a real implementation, this would use vector embeddings
        # and proper storage mechanisms
        self.short_term_memory.append(item)
        logger.debug(f"Item stored in short-term memory: {item}")
    
    async def retrieve_relevant(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve items relevant to a query
        
        Args:
            query: The query to find relevant items for
            
        Returns:
            relevant_items: List of relevant items
        """
        # In a real implementation, this would use semantic search
        # For now, just return recent items as a simple demonstration
        # Limited to last 5 items to avoid context overflow
        return self.short_term_memory[-5:] if self.short_term_memory else []
    
    def clear_short_term(self) -> None:
        """Clear short-term memory"""
        self.short_term_memory = []
        logger.debug("Short-term memory cleared")
    
    def clear_all(self) -> None:
        """Clear all memory"""
        self.short_term_memory = []
        self.long_term_memory = []
        logger.debug("All memory cleared")
    
    def get_memory_status(self) -> Dict[str, Any]:
        """
        Get the status of the memory system
        
        Returns:
            status: Dictionary with memory status information
        """
        return {
            "short_term_count": len(self.short_term_memory),
            "long_term_count": len(self.long_term_memory)
        }