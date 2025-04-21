"""
Command Line Interface for the MindChain framework.

This module provides a simple CLI to interact with the MindChain framework.
"""
import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Dict, Any, Optional

from .mcp.mcp import MCP
from .core.agent import Agent, AgentConfig


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


async def run_agent(config_path: Optional[str] = None, query: Optional[str] = None) -> None:
    """Run an agent with the given configuration and query."""
    # Default configuration
    default_config = {
        "name": "DefaultAgent",
        "description": "A default agent created by the MindChain CLI",
        "model_name": "gpt-3.5-turbo",
        "system_prompt": "You are a helpful AI assistant.",
        "temperature": 0.7,
        "max_tokens": 1000,
    }

    # Load configuration if provided
    if config_path:
        try:
            with open(config_path, "r") as f:
                config_data = json.load(f)
            agent_config = AgentConfig(**config_data)
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            sys.exit(1)
    else:
        agent_config = AgentConfig(**default_config)

    # Initialize MCP and agent
    mcp = MCP()
    agent = Agent(agent_config)
    agent_id = mcp.register_agent(agent)
    
    logging.info(f"Agent '{agent_config.name}' initialized with ID: {agent_id}")

    # Process query if provided, otherwise enter interactive mode
    if query:
        response = await mcp.supervise_execution(
            agent_id=agent_id,
            task=lambda: agent.run(query)
        )
        print(f"\n{response}")
    else:
        print(f"MindChain CLI - Agent: {agent_config.name}")
        print("Type 'exit' to quit")
        
        while True:
            try:
                user_input = input("\nYou: ")
                if user_input.lower() in ("exit", "quit", "q"):
                    break
                    
                response = await mcp.supervise_execution(
                    agent_id=agent_id,
                    task=lambda: agent.run(user_input)
                )
                print(f"\nAgent: {response}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error(f"Error: {e}")
    
    # Cleanup
    mcp.unregister_agent(agent_id)
    logging.info("Agent unregistered. Exiting.")


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="MindChain Agentic AI Framework")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Run agent command
    run_parser = subparsers.add_parser("run", help="Run an agent")
    run_parser.add_argument(
        "--config", "-c", 
        help="Path to agent configuration JSON file"
    )
    run_parser.add_argument(
        "--query", "-q", 
        help="Query to send to the agent"
    )
    run_parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose logging"
    )
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Show version information")
    
    args = parser.parse_args()
    
    if args.command == "run":
        setup_logging(args.verbose)
        asyncio.run(run_agent(args.config, args.query))
    elif args.command == "version":
        from . import __version__
        print(f"MindChain version {__version__}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
