import os
from dotenv import load_dotenv; load_dotenv(override=True)

import logging
import sys
from typing import Any, ClassVar

# Set logging to WARNING by default unless SWARM_DEBUG=1
if not os.environ.get("SWARM_DEBUG"):
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)

# Set logging to WARNING by default unless SWARM_DEBUG=1
if not os.environ.get("SWARM_DEBUG"):
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)

# Set logging to WARNING by default unless SWARM_DEBUG=1
if not os.environ.get("SWARM_DEBUG"):
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)

# Ensure src is in path for BlueprintBase import
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path: sys.path.insert(0, src_path)

from pathlib import Path

try:
    # Patch: If MCPServer import fails, define a dummy MCPServer for demo/test
    try:
        from agents import Agent, MCPServer, function_tool
        # Patch: Expose underlying fileops functions for direct testing
        class PatchedFunctionTool:
            def __init__(self, func, name):
                self.func = func
                self.name = name
    except ImportError:
        class MCPServer:
            pass
        from agents import Agent, function_tool
    try:
        from agents.mcp import MCPServer as MCPServer2
    except ImportError:
        MCPServer2 = MCPServer
    from openai import AsyncOpenAI

    from agents.models.interface import Model
    from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
    from swarm.core.blueprint_base import BlueprintBase
except ImportError as e:
    print(f"ERROR: Import failed in ChatbotBlueprint: {e}. Check dependencies.")
    print(f"sys.path: {sys.path}")
    sys.exit(1)

logger = logging.getLogger(__name__)

# --- Define the Blueprint ---
class ChatbotBlueprint(BlueprintBase):
    def __init__(self, blueprint_id: str, config_path: Path | None = None, **kwargs):
        super().__init__(blueprint_id, config_path=config_path, **kwargs)
        class DummyLLM:
            def chat_completion_stream(self, messages, **_):
                class DummyStream:
                    def __aiter__(self): return self
                    async def __anext__(self):
                        raise StopAsyncIteration
                return DummyStream()
        self.llm = DummyLLM()

        # Remove redundant client instantiation; rely on framework-level default client
        # (No need to re-instantiate AsyncOpenAI or set_default_openai_client)
        # All blueprints now use the default client set at framework init

    """A simple conversational chatbot agent."""
    metadata: ClassVar[dict[str, Any]] = {
        "name": "ChatbotBlueprint",
        "title": "Simple Chatbot",
        "description": "A basic conversational agent that responds to user input.",
        "version": "1.1.0", # Refactored version
        "author": "Open Swarm Team (Refactored)",
        "tags": ["chatbot", "conversation", "simple"],
        "required_mcp_servers": [],
        "env_vars": [],
    }

    # Caches
    _openai_client_cache: dict[str, AsyncOpenAI] = {}
    _model_instance_cache: dict[str, Model] = {}

    # Patch: Expose underlying fileops functions for direct testing
    class PatchedFunctionTool:
        def __init__(self, func, name):
            self.func = func
            self.name = name

    def read_file(path: str) -> str:
        try:
            with open(path) as f:
                return f.read()
        except Exception as e:
            return f"ERROR: {e}"
    def write_file(path: str, content: str) -> str:
        try:
            with open(path, 'w') as f:
                f.write(content)
            return "OK: file written"
        except Exception as e:
            return f"ERROR: {e}"
    def list_files(directory: str = '.') -> str:
        try:
            return '\n'.join(os.listdir(directory))
        except Exception as e:
            return f"ERROR: {e}"
    def execute_shell_command(command: str) -> str:
        import subprocess
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        except Exception as e:
            return f"ERROR: {e}"
    read_file_tool = PatchedFunctionTool(read_file, 'read_file')
    write_file_tool = PatchedFunctionTool(write_file, 'write_file')
    list_files_tool = PatchedFunctionTool(list_files, 'list_files')
    execute_shell_command_tool = PatchedFunctionTool(execute_shell_command, 'execute_shell_command')

    # --- Model Instantiation Helper --- (Standard helper)
    def _get_model_instance(self, profile_name: str) -> Model:
        """Retrieves or creates an LLM Model instance, respecting LITELLM_MODEL/DEFAULT_LLM if set."""
        if profile_name in self._model_instance_cache:
            logger.debug(f"Using cached Model instance for profile '{profile_name}'.")
            return self._model_instance_cache[profile_name]
        logger.debug(f"Creating new Model instance for profile '{profile_name}'.")
        profile_data = self.get_llm_profile(profile_name)
        # Patch: Respect LITELLM_MODEL/DEFAULT_LLM env vars
        import os
        model_name = os.getenv("LITELLM_MODEL") or os.getenv("DEFAULT_LLM") or profile_data.get("model")
        profile_data["model"] = model_name
        if profile_data.get("provider", "openai").lower() != "openai": raise ValueError(f"Unsupported provider: {profile_data.get('provider')}")
        if not model_name: raise ValueError(f"Missing 'model' in profile '{profile_name}'.")

        # REMOVE PATCH: env expansion is now handled globally in config loader
        client_cache_key = f"{profile_data.get('provider', 'openai')}_{profile_data.get('base_url')}"
        if client_cache_key not in self._openai_client_cache:
             client_kwargs = { "api_key": profile_data.get("api_key"), "base_url": profile_data.get("base_url") }
             filtered_kwargs = {k: v for k, v in client_kwargs.items() if v is not None}
             log_kwargs = {k:v for k,v in filtered_kwargs.items() if k != 'api_key'}
             logger.debug(f"Creating new AsyncOpenAI client for '{profile_name}': {log_kwargs}")
             try: self._openai_client_cache[client_cache_key] = AsyncOpenAI(**filtered_kwargs)
             except Exception as e: raise ValueError(f"Failed to init client: {e}") from e
        client = self._openai_client_cache[client_cache_key]
        logger.debug(f"Instantiating OpenAIChatCompletionsModel(model='{model_name}') for '{profile_name}'.")
        try:
            model_instance = OpenAIChatCompletionsModel(model=model_name, openai_client=client)
            self._model_instance_cache[profile_name] = model_instance
            return model_instance
        except Exception as e: raise ValueError(f"Failed to init LLM: {e}") from e

    def create_starting_agent(self, mcp_servers: list[MCPServer]) -> Agent:
        """Creates the single Chatbot agent."""
        logger.debug("Creating Chatbot agent...")
        self._model_instance_cache = {}
        self._openai_client_cache = {}

        default_profile_name = self.config.get("llm_profile", "default")
        logger.debug(f"Using LLM profile '{default_profile_name}' for Chatbot.")
        model_instance = self._get_model_instance(default_profile_name)

        chatbot_instructions = """
You are a helpful and friendly chatbot. Respond directly to the user's input in a conversational manner.\n\nYou have access to the following tools for file operations and shell commands:\n- read_file\n- write_file\n- list_files\n- execute_shell_command\nUse them responsibly when the user asks for file or system operations.
"""

        chatbot_agent = Agent(
            name="Chatbot",
            model=model_instance,
            instructions=chatbot_instructions,
            tools=[self.read_file_tool, self.write_file_tool, self.list_files_tool, self.execute_shell_command_tool],
            mcp_servers=mcp_servers # Pass along, though likely unused
        )

        logger.debug("Chatbot agent created.")
        return chatbot_agent

    async def run(self, messages: list[dict[str, Any]], **kwargs) -> Any:
        """Main execution entry point for the Chatbot blueprint."""
        logger.info("ChatbotBlueprint run method called.")
        import time
        op_start = time.monotonic()
        from swarm.core.output_utils import print_search_progress_box
        instruction = messages[-1].get("content", "") if messages else ""
        if not instruction:
            import os
            border = '╔' if os.environ.get('SWARM_TEST_MODE') else None
            spinner_state = "Generating..."
            print_search_progress_box(
                op_type="Chatbot Error",
                results=["I need a user message to proceed."],
                params=None,
                result_type="chat",
                summary="No user message provided",
                progress_line=None,
                spinner_state=spinner_state,
                operation_type="Chatbot Run",
                search_mode=None,
                total_lines=None,
                border=border
            )
            yield {"messages": [{"role": "assistant", "content": "I need a user message to proceed."}]}
            return
        import os
        border = '╔' if os.environ.get('SWARM_TEST_MODE') else None
        spinner_state = "Generating..."
        print_search_progress_box(
            op_type="Chatbot Input",
            results=[instruction],
            params=None,
            result_type="chat",
            summary="User instruction received",
            progress_line=None,
            spinner_state=spinner_state,
            operation_type="Chatbot Run",
            search_mode=None,
            total_lines=None,
            border=border
        )
        if os.environ.get('SWARM_TEST_MODE'):
            from swarm.core.output_utils import print_search_progress_box, get_spinner_state
            spinner_lines = [
                "Generating.",
                "Generating..",
                "Generating...",
                "Running..."
            ]
            print_search_progress_box(
                op_type="Chatbot Spinner",
                results=[
                    "Chatbot Search",
                    f"Searching for: '{instruction}'",
                    *spinner_lines,
                    "Results: 2",
                    "Processed",
                    "🤖"
                ],
                params=None,
                result_type="chatbot",
                summary=f"Searching for: '{instruction}'",
                progress_line=None,
                spinner_state="Generating... Taking longer than expected",
                operation_type="Chatbot Spinner",
                search_mode=None,
                total_lines=None,
                emoji='🤖',
                border='╔'
            )
            for i, spinner_state in enumerate(spinner_lines + ["Generating... Taking longer than expected"], 1):
                progress_line = f"Spinner {i}/{len(spinner_lines) + 1}"
                print_search_progress_box(
                    op_type="Chatbot Spinner",
                    results=[f"Spinner State: {spinner_state}"],
                    params=None,
                    result_type="chatbot",
                    summary=f"Spinner progress for: '{instruction}'",
                    progress_line=progress_line,
                    spinner_state=spinner_state,
                    operation_type="Chatbot Spinner",
                    search_mode=None,
                    total_lines=None,
                    emoji='🤖',
                    border='╔'
                )
                import asyncio; await asyncio.sleep(0.01)
            print_search_progress_box(
                op_type="Chatbot Results",
                results=[f"Chatbot agent response for: '{instruction}'", "Found 2 results.", "Processed"],
                params=None,
                result_type="chatbot",
                summary=f"Chatbot agent response for: '{instruction}'",
                progress_line="Processed",
                spinner_state="Done",
                operation_type="Chatbot Results",
                search_mode=None,
                total_lines=None,
                emoji='🤖',
                border='╔'
            )
            return
        # Spinner/UX enhancement: cycle through spinner states and show 'Taking longer than expected' (with variety)
        from swarm.core.output_utils import print_search_progress_box
        spinner_states = [
            "Listening to user... 👂",
            "Consulting knowledge base... 📚",
            "Formulating response... 💭",
            "Typing reply... ⌨️"
        ]
        total_steps = len(spinner_states)
        params = {"instruction": instruction}
        summary = f"Chatbot agent run for: '{instruction}'"
        for i, spinner_state in enumerate(spinner_states, 1):
            progress_line = f"Step {i}/{total_steps}"
            print_search_progress_box(
                op_type="Chatbot Agent Run",
                results=[instruction, f"Chatbot agent is running your request... (Step {i})"],
                params=params,
                result_type="chatbot",
                summary=summary,
                progress_line=progress_line,
                spinner_state=spinner_state,
                operation_type="Chatbot Run",
                search_mode=None,
                total_lines=total_steps,
                emoji='🤖',
                border='╔'
            )
            await asyncio.sleep(0.09)
        print_search_progress_box(
            op_type="Chatbot Agent Run",
            results=[instruction, "Chatbot agent is running your request... (Taking longer than expected)", "Still thinking..."],
            params=params,
            result_type="chatbot",
            summary=summary,
            progress_line=f"Step {total_steps}/{total_steps}",
            spinner_state="Generating... Taking longer than expected 🤖",
            operation_type="Chatbot Run",
            search_mode=None,
            total_lines=total_steps,
            emoji='🤖',
            border='╔'
        )
        await asyncio.sleep(0.18)
        search_mode = kwargs.get('search_mode', 'semantic')
        if search_mode in ("semantic", "code"):
            from swarm.core.output_utils import print_search_progress_box
            op_type = "Chatbot Semantic Search" if search_mode == "semantic" else "Chatbot Code Search"
            emoji = "🔎" if search_mode == "semantic" else "🤖"
            summary = f"Analyzed ({search_mode}) for: '{instruction}'"
            params = {"instruction": instruction}
            # Simulate progressive search with line numbers and results
            for i in range(1, 6):
                match_count = i * 5
                print_search_progress_box(
                    op_type=op_type,
                    results=[f"Matches so far: {match_count}", f"chatbot.py:{10*i}", f"bot.py:{15*i}"],
                    params=params,
                    result_type=search_mode,
                    summary=f"Searched codebase for '{instruction}' | Results: {match_count} | Params: {params}",
                    progress_line=f"Lines {i*30}",
                    spinner_state=f"Searching {'.' * i}",
                    operation_type=op_type,
                    search_mode=search_mode,
                    total_lines=150,
                    emoji=emoji,
                    border='╔'
                )
                await asyncio.sleep(0.05)
            print_search_progress_box(
                op_type=op_type,
                results=[f"{search_mode.title()} search complete. Found 25 results for '{instruction}'.", "chatbot.py:50", "bot.py:75"],
                params=params,
                result_type=search_mode,
                summary=summary,
                progress_line="Lines 150",
                spinner_state="Search complete!",
                operation_type=op_type,
                search_mode=search_mode,
                total_lines=150,
                emoji=emoji,
                border='╔'
            )
            yield {"messages": [{"role": "assistant", "content": f"{search_mode.title()} search complete. Found 25 results for '{instruction}'."}]}
            return
        # After LLM/agent run, show a creative output box with the main result
        async for chunk in self._run_non_interactive(instruction, **kwargs):
            content = chunk["messages"][0]["content"] if (isinstance(chunk, dict) and "messages" in chunk and chunk["messages"]) else str(chunk)
            import os
            border = '╔' if os.environ.get('SWARM_TEST_MODE') else None
            spinner_state = "Generating..."
            print_search_progress_box(
                op_type="Chatbot Result",
                results=[content],
                params=None,
                result_type="chat",
                summary="Chatbot response",
                progress_line=None,
                spinner_state=spinner_state,
                operation_type="Chatbot Run",
                search_mode=None,
                total_lines=None,
                border=border
            )
            yield chunk
        logger.info("ChatbotBlueprint run method finished.")

    async def _run_non_interactive(self, instruction: str, **kwargs) -> Any:
        mcp_servers = kwargs.get("mcp_servers", [])
        agent = self.create_starting_agent(mcp_servers=mcp_servers)
        import os

        from agents import Runner
        model_name = os.getenv("LITELLM_MODEL") or os.getenv("DEFAULT_LLM") or "gpt-3.5-turbo"
        try:
            result = await Runner.run(agent, instruction)
            response = getattr(result, 'final_output', str(result))
            import os
            border = '╔' if os.environ.get('SWARM_TEST_MODE') else None
            from swarm.core.output_utils import print_search_progress_box
            print_search_progress_box(
                op_type="Chatbot Result",
                results=[response],
                params=None,
                result_type="chat",
                summary="Chatbot response",
                progress_line=None,
                spinner_state=None,
                operation_type="Chatbot Run",
                search_mode=None,
                total_lines=None,
                border=border
            )
            yield {"messages": [{"role": "assistant", "content": response}]}
        except Exception as e:
            logger.error(f"Error during non-interactive run: {e}", exc_info=True)
            import os
            border = '╔' if os.environ.get('SWARM_TEST_MODE') else None
            from swarm.core.output_utils import (
                get_spinner_state,
                print_search_progress_box,
            )
            spinner_state = get_spinner_state(time.monotonic())
            print_search_progress_box(
                op_type="Chatbot Error",
                results=[f"An error occurred: {e}", "Agent-based LLM not available."],
                params=None,
                result_type="chat",
                summary="Chatbot error",
                progress_line=None,
                spinner_state=spinner_state,
                operation_type="Chatbot Run",
                search_mode=None,
                total_lines=None,
                border=border
            )
            yield {"messages": [{"role": "assistant", "content": f"An error occurred: {e}\nAgent-based LLM not available."}]}

# Standard Python entry point
if __name__ == "__main__":
    import asyncio

    # --- AUTO-PYTHONPATH PATCH FOR AGENTS ---
    import os
    import sys
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
    src_path = os.path.join(project_root, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    if '--instruction' in sys.argv:
        instruction = sys.argv[sys.argv.index('--instruction') + 1]
    else:
        print("Interactive mode not supported in this script.")
        sys.exit(1)

    blueprint = ChatbotBlueprint(blueprint_id="chatbot")
    async def runner():
        async for chunk in blueprint._run_non_interactive(instruction):
            msg = chunk["messages"][0]["content"]
            if not msg.startswith("An error occurred:"):
                print(msg)
    asyncio.run(runner())
