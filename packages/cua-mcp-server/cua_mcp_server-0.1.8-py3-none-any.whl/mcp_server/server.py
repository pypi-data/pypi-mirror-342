import asyncio
import logging
import os
import sys
import traceback
from typing import Any, Dict, List, Optional, Union

# Configure logging to output to stderr for debug visibility
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp-server")

# More visible startup message
logger.debug("MCP Server module loading...")

try:
    from mcp.server.fastmcp import Context, FastMCP

    logger.debug("Successfully imported FastMCP")
except ImportError as e:
    logger.error(f"Failed to import FastMCP: {e}")
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

try:
    from computer import Computer
    from agent import ComputerAgent, LLMProvider, LLM, AgentLoop

    logger.debug("Successfully imported Computer and Agent modules")
except ImportError as e:
    logger.error(f"Failed to import Computer/Agent modules: {e}")
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

# Global computer instance for reuse
global_computer = None


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean value from environment variable."""
    return os.getenv(key, str(default)).lower() in ("true", "1", "yes")


def serve() -> FastMCP:
    """Create and configure the MCP server."""
    server = FastMCP("cua-agent")

    @server.tool()
    async def run_cua_task(ctx: Context, task: str) -> str:
        """
        Run a Computer-Use Agent (CUA) task and return the results.

        Args:
            ctx: The MCP context
            task: The instruction or task for the agent to perform

        Returns:
            A string containing the agent's response
        """
        global global_computer

        try:
            logger.info(f"Starting CUA task: {task}")

            # Initialize computer if needed
            if global_computer is None:
                global_computer = Computer(verbosity=logging.INFO)
                await global_computer.run()

            # Determine which loop to use
            loop_str = os.getenv("CUA_AGENT_LOOP", "OMNI")
            if loop_str == "OPENAI":
                loop = AgentLoop.OPENAI
            elif loop_str == "ANTHROPIC":
                loop = AgentLoop.ANTHROPIC
            else:
                loop = AgentLoop.OMNI

            # Determine provider
            provider_str = os.getenv("CUA_MODEL_PROVIDER", "ANTHROPIC")
            provider = getattr(LLMProvider, provider_str)

            # Get model name (if specified)
            model_name = os.getenv("CUA_MODEL_NAME", None)

            # Get base URL for provider (if needed)
            provider_base_url = os.getenv("CUA_PROVIDER_BASE_URL", None)

            # Create agent with the specified configuration
            agent = ComputerAgent(
                computer=global_computer,
                loop=loop,
                model=LLM(
                    provider=provider,
                    name=model_name,
                    provider_base_url=provider_base_url,
                ),
                save_trajectory=False,
                only_n_most_recent_images=int(os.getenv("CUA_MAX_IMAGES", "3")),
                verbosity=logging.INFO,
            )

            # Collect all results
            full_result = ""
            async for result in agent.run(task):
                logger.info(f"Agent step complete: {result.get('id', 'unknown')}")

                # Add response ID to output
                full_result += f"\n[Response ID: {result.get('id', 'unknown')}]\n"

                # Extract and concatenate text responses
                if "text" in result:
                    # Handle both string and dict responses
                    text_response = result.get("text", "")
                    if isinstance(text_response, str):
                        full_result += f"Response: {text_response}\n"
                    else:
                        # If it's a dict or other structure, convert to string representation
                        full_result += f"Response: {str(text_response)}\n"

                # Log detailed information
                if "tools" in result:
                    tools_info = result.get("tools")
                    logger.debug(f"Tools used: {tools_info}")
                    full_result += f"\nTools used: {tools_info}\n"

                # Process output if available
                outputs = result.get("output", [])
                for output in outputs:
                    output_type = output.get("type")
                    if output_type == "reasoning":
                        logger.debug(f"Reasoning: {output}")
                        full_result += f"\nReasoning: {output.get('content', '')}\n"
                    elif output_type == "computer_call":
                        logger.debug(f"Computer call: {output}")
                        action = output.get("action", "")
                        result_value = output.get("result", "")
                        full_result += f"\nComputer Action: {action}\nResult: {result_value}\n"

                # Add separator between steps
                full_result += "\n" + "-" * 40 + "\n"

            logger.info(f"CUA task completed successfully")
            return full_result or "Task completed with no text output."

        except Exception as e:
            error_msg = f"Error running CUA task: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            return f"Error during task execution: {str(e)}"

    @server.tool()
    async def run_multi_cua_tasks(ctx: Context, tasks: List[str]) -> str:
        """
        Run multiple CUA tasks in sequence and return the combined results.

        Args:
            ctx: The MCP context
            tasks: List of tasks to run in sequence

        Returns:
            Combined results from all tasks
        """
        results = []

        for i, task in enumerate(tasks):
            logger.info(f"Running task {i+1}/{len(tasks)}: {task}")
            result = await run_cua_task(ctx, task)
            results.append(f"Task {i+1}: {task}\nResult: {result}\n")

        return "\n".join(results)

    return server


server = serve()


def main():
    """Run the MCP server."""
    try:
        logger.debug("Starting MCP server...")
        server.run()
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
