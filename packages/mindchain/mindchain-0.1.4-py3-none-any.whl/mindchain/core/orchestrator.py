"""
Agent Orchestrator for MindChain

This module provides orchestration capabilities for multi-agent workflows.
"""

import asyncio
import logging
import uuid
from typing import Dict, List, Any, Callable, Awaitable, Optional, Union, Tuple

from .agent import Agent, AgentConfig
from ..mcp.mcp import MCP
from .errors import OrchestrationError

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Orchestrates multi-agent workflows and task delegation.
    
    The AgentOrchestrator manages the coordination between multiple agents,
    allowing them to work together to solve complex tasks through delegation
    and sequential or parallel execution patterns.
    """
    
    def __init__(self, mcp: MCP):
        """
        Initialize the orchestrator with a Master Control Program instance.
        
        Args:
            mcp: The Master Control Program that supervises the agents
        """
        self.mcp = mcp
        self.workflows: Dict[str, Any] = {}
        logger.info("AgentOrchestrator initialized")
    
    def create_workflow(self, name: str, description: str = "") -> str:
        """
        Creates a new workflow for multi-agent collaboration.
        
        Args:
            name: Name of the workflow
            description: Optional description of the workflow purpose
            
        Returns:
            workflow_id: Unique identifier for the workflow
        """
        workflow_id = str(uuid.uuid4())
        self.workflows[workflow_id] = {
            'name': name,
            'description': description,
            'steps': [],
            'status': 'created',
            'created_at': asyncio.get_event_loop().time(),
            'results': {}
        }
        logger.info(f"Created workflow '{name}' with ID: {workflow_id}")
        return workflow_id
    
    def add_step(
        self, 
        workflow_id: str, 
        agent_id: str, 
        task_prompt: str, 
        step_name: str = "", 
        depends_on: List[str] = None
    ) -> str:
        """
        Adds a step to an existing workflow.
        
        Args:
            workflow_id: ID of the workflow to add the step to
            agent_id: ID of the agent that will execute this step
            task_prompt: The prompt/task for the agent to execute
            step_name: Optional name for this step
            depends_on: List of step IDs that must complete before this step runs
            
        Returns:
            step_id: Unique identifier for this workflow step
        """
        if workflow_id not in self.workflows:
            raise OrchestrationError(f"Workflow with ID {workflow_id} does not exist")
            
        if not self.mcp.get_agent(agent_id):
            raise OrchestrationError(f"Agent with ID {agent_id} is not registered with the MCP")
            
        step_id = str(uuid.uuid4())
        
        # Default empty list if None
        if depends_on is None:
            depends_on = []
            
        # Validate that all dependencies exist in this workflow
        for dep_id in depends_on:
            if not any(step['id'] == dep_id for step in self.workflows[workflow_id]['steps']):
                raise OrchestrationError(f"Dependency step {dep_id} does not exist in workflow {workflow_id}")
        
        step = {
            'id': step_id,
            'name': step_name or f"Step {len(self.workflows[workflow_id]['steps']) + 1}",
            'agent_id': agent_id,
            'task_prompt': task_prompt,
            'depends_on': depends_on,
            'status': 'pending',
            'created_at': asyncio.get_event_loop().time(),
            'completed_at': None,
            'result': None
        }
        
        self.workflows[workflow_id]['steps'].append(step)
        logger.info(f"Added step '{step['name']}' to workflow '{self.workflows[workflow_id]['name']}'")
        return step_id
    
    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Gets information about a workflow.
        
        Args:
            workflow_id: ID of the workflow to retrieve
            
        Returns:
            workflow: Dictionary containing workflow details
            
        Raises:
            OrchestrationError: If the workflow does not exist
        """
        if workflow_id not in self.workflows:
            raise OrchestrationError(f"Workflow with ID {workflow_id} does not exist")
        return self.workflows[workflow_id]
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        List all workflows managed by this orchestrator.
        
        Returns:
            List of workflow information dictionaries
        """
        return [
            {
                'id': wf_id,
                'name': wf['name'],
                'description': wf['description'],
                'status': wf['status'],
                'created_at': wf['created_at'],
                'step_count': len(wf['steps'])
            }
            for wf_id, wf in self.workflows.items()
        ]
    
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Executes a workflow by running all steps in the appropriate order.
        
        Args:
            workflow_id: ID of the workflow to execute
            
        Returns:
            results: Dictionary containing the results of all steps
            
        Raises:
            OrchestrationError: If the workflow does not exist or execution fails
        """
        if workflow_id not in self.workflows:
            raise OrchestrationError(f"Workflow with ID {workflow_id} does not exist")
            
        workflow = self.workflows[workflow_id]
        workflow['status'] = 'running'
        workflow['results'] = {}
        
        try:
            # Build dependency graph for execution
            remaining_steps = workflow['steps'].copy()
            completed_steps = set()
            
            logger.info(f"Starting execution of workflow '{workflow['name']}'")
            
            # Continue until all steps are processed
            while remaining_steps:
                # Find steps that have all dependencies satisfied
                ready_steps = [
                    step for step in remaining_steps
                    if all(dep in completed_steps for dep in step['depends_on'])
                ]
                
                if not ready_steps:
                    raise OrchestrationError(
                        f"Workflow execution deadlocked - circular dependency detected in workflow {workflow_id}"
                    )
                
                # Execute ready steps (in parallel if there are multiple)
                execution_tasks = []
                for step in ready_steps:
                    execution_tasks.append(self._execute_step(workflow_id, step))
                    
                # Wait for all ready steps to complete
                await asyncio.gather(*execution_tasks)
                
                # Move completed steps from remaining to completed
                for step in ready_steps:
                    completed_steps.add(step['id'])
                    remaining_steps.remove(step)
            
            # Update workflow status
            workflow['status'] = 'completed'
            logger.info(f"Successfully completed workflow '{workflow['name']}'")
            
            return workflow['results']
            
        except Exception as e:
            workflow['status'] = 'failed'
            error_msg = f"Workflow execution failed: {str(e)}"
            logger.error(error_msg)
            raise OrchestrationError(error_msg) from e
    
    async def _execute_step(self, workflow_id: str, step: Dict[str, Any]) -> None:
        """
        Executes a single step in a workflow.
        
        Args:
            workflow_id: ID of the workflow this step belongs to
            step: The step definition dictionary
            
        Returns:
            None - updates the step and workflow directly
        """
        workflow = self.workflows[workflow_id]
        agent_id = step['agent_id']
        agent = self.mcp.get_agent(agent_id)
        
        if not agent:
            step['status'] = 'failed'
            error_msg = f"Agent with ID {agent_id} is no longer registered with the MCP"
            logger.error(error_msg)
            raise OrchestrationError(error_msg)
        
        # Update task prompt with previous step results if referenced
        task_prompt = step['task_prompt']
        for prev_step_id, prev_result in workflow['results'].items():
            if f"{{result:{prev_step_id}}}" in task_prompt:
                task_prompt = task_prompt.replace(f"{{result:{prev_step_id}}}", str(prev_result))
        
        step['status'] = 'running'
        logger.info(f"Executing step '{step['name']}' with agent '{agent.name}'")
        
        try:
            # Execute the task through MCP supervision
            result = await self.mcp.supervise_execution(
                agent_id=agent_id,
                task=lambda: agent.run(task_prompt)
            )
            
            # Update step and workflow results
            step['status'] = 'completed'
            step['completed_at'] = asyncio.get_event_loop().time()
            step['result'] = result
            workflow['results'][step['id']] = result
            logger.info(f"Step '{step['name']}' completed successfully")
            
        except Exception as e:
            step['status'] = 'failed'
            error_msg = f"Step execution failed: {str(e)}"
            logger.error(error_msg)
            raise OrchestrationError(error_msg) from e
    
    def create_sequential_workflow(
        self, 
        name: str, 
        description: str, 
        agent_ids: List[str], 
        prompts: List[str]
    ) -> str:
        """
        Helper method to create a sequential workflow where steps run one after another.
        
        Args:
            name: Name of the workflow
            description: Description of the workflow
            agent_ids: List of agent IDs to participate in the workflow
            prompts: List of prompts for each step (must match length of agent_ids)
            
        Returns:
            workflow_id: Unique identifier for the created workflow
        """
        if len(agent_ids) != len(prompts):
            raise OrchestrationError("The number of agent IDs must match the number of prompts")
            
        workflow_id = self.create_workflow(name, description)
        
        previous_step_id = None
        for i, (agent_id, prompt) in enumerate(zip(agent_ids, prompts)):
            step_name = f"Step {i+1}"
            depends_on = [previous_step_id] if previous_step_id else []
            
            # Replace placeholders for previous results
            if previous_step_id and "{previous_result}" in prompt:
                prompt = prompt.replace("{previous_result}", f"{{result:{previous_step_id}}}")
            
            step_id = self.add_step(
                workflow_id=workflow_id,
                agent_id=agent_id,
                task_prompt=prompt,
                step_name=step_name,
                depends_on=depends_on if previous_step_id else []
            )
            previous_step_id = step_id
            
        return workflow_id
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Deletes a workflow by ID.
        
        Args:
            workflow_id: ID of the workflow to delete
            
        Returns:
            success: True if deleted successfully, False otherwise
        """
        if workflow_id not in self.workflows:
            return False
            
        workflow_name = self.workflows[workflow_id]['name']
        del self.workflows[workflow_id]
        logger.info(f"Deleted workflow '{workflow_name}' with ID: {workflow_id}")
        return True
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """
        Attempts to cancel a running workflow.
        
        Args:
            workflow_id: ID of the workflow to cancel
            
        Returns:
            success: True if canceled successfully, False otherwise
        """
        if workflow_id not in self.workflows:
            return False
            
        workflow = self.workflows[workflow_id]
        if workflow['status'] not in ('running', 'pending'):
            return False
            
        workflow['status'] = 'cancelled'
        logger.info(f"Cancelled workflow '{workflow['name']}' with ID: {workflow_id}")
        return True