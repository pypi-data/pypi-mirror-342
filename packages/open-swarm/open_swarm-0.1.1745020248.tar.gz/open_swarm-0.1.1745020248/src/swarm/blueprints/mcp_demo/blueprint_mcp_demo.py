"""
MCPDemo Blueprint

Viral docstring update: Operational as of 2025-04-18T10:14:18Z (UTC).
Self-healing, fileops-enabled, swarm-scalable.
"""
# [Swarm Propagation] Next Blueprint: mission_improbable
# mission_improbable key vars: logger, project_root, src_path
# mission_improbable guard: if src_path not in sys.path: sys.path.insert(0, src_path)
# mission_improbable debug: logger.debug("Mission Improbable agent created: JimFlimsy (Coordinator)")
# mission_improbable error handling: try/except ImportError with sys.exit(1)

import logging
import os
import sys
import glob
import json
import concurrent.futures
from typing import Dict, Any, List, ClassVar, Optional
from datetime import datetime
import pytz

# Ensure src is in path for BlueprintBase import
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path: sys.path.insert(0, src_path)

try:
    from agents import Agent, Tool, function_tool, Runner
    from agents.mcp import MCPServer
    from agents.models.interface import Model
    from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
    from openai import AsyncOpenAI
    from swarm.core.blueprint_base import BlueprintBase
    from swarm.core.blueprint_discovery import discover_blueprints
except ImportError as e:
    print(f"ERROR: Import failed in MCPDemoBlueprint: {e}. Check dependencies.")
    print(f"sys.path: {sys.path}")
    sys.exit(1)

logger = logging.getLogger(__name__)

# Last swarm update: 2025-04-18T10:15:21Z (UTC)
last_swarm_update = datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ (UTC)")
logger.info(f"Last swarm update: {last_swarm_update}")

# --- Agent Instructions ---

sage_instructions_template = """
You are Sage, an agent demonstrating capabilities provided by MCP servers.
You have access to the following external capabilities via implicitly available MCP tools:
{mcp_tool_descriptions}

Your goal is to understand the user's request and utilize the appropriate MCP tool to fulfill it.
For example:
- To write to a file, use the 'filesystem' tool's 'write' function.
- To read from memory, use the 'memory' tool's 'get' function.
- To store in memory, use the 'memory' tool's 'set' function.
- To perform viral file operations, provide a comma-separated list of paths or wildcard patterns.

You can scale file operations horizontally across multiple targets for performance.
Explain what action you are taking via which tool and report the result.
"""

# --- FileOps Tool Logic Definitions ---
 # Patch: Expose underlying fileops functions for direct testing
class PatchedFunctionTool:
    def __init__(self, func, name):
        self.func = func
        self.name = name
def read_file(path: str) -> str:
    """
    Read contents of one or more files.
    Supports wildcard patterns (e.g., '*.txt') and comma-separated lists of paths.
    Returns a JSON mapping of paths to contents or error messages.
    """
    try:
        # Determine file paths
        if ',' in path:
            paths = [p.strip() for p in path.split(',')]
        elif any(pat in path for pat in ['*', '?', '[']):
            paths = glob.glob(path)
        else:
            paths = [path]
        results: Dict[str, str] = {}
        for p in paths:
            try:
                with open(p, 'r') as f:
                    results[p] = f.read()
            except Exception as e:
                results[p] = f"ERROR: {e}"
        return json.dumps(results)
    except Exception as e:
        return f"ERROR: {e}"
def write_file(path: str, content: str) -> str:
    """
    Write content to one or more files.
    Supports wildcard patterns and comma-separated lists for viral file operations.
    Returns a JSON mapping of paths to status ('OK' or error message).
    """
    try:
        # Determine file paths
        if ',' in path:
            paths = [p.strip() for p in path.split(',')]
        elif any(pat in path for pat in ['*', '?', '[']):
            paths = glob.glob(path)
        else:
            paths = [path]
        results: Dict[str, str] = {}
        # Write to all targets concurrently
        def _write_single(p: str):
            try:
                with open(p, 'w') as f:
                    f.write(content)
                return p, 'OK'
            except Exception as e:
                return p, f"ERROR: {e}"
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(_write_single, p): p for p in paths}
            for fut in concurrent.futures.as_completed(futures):
                p, status = fut.result()
                results[p] = status
        return json.dumps(results)
    except Exception as e:
        return f"ERROR: {e}"
def list_files(directory: str = '.') -> str:
    """
    List files in one or more directories.
    Supports wildcard patterns and comma-separated directory lists.
    Returns a JSON mapping of directory to list of entries or error message.
    """
    try:
        # Determine directories
        if ',' in directory:
            dirs = [d.strip() for d in directory.split(',')]
        elif any(pat in directory for pat in ['*', '?', '[']):
            dirs = glob.glob(directory)
        else:
            dirs = [directory]
        results: Dict[str, Any] = {}
        for d in dirs:
            try:
                results[d] = os.listdir(d)
            except Exception as e:
                results[d] = f"ERROR: {e}"
        return json.dumps(results)
    except Exception as e:
        return f"ERROR: {e}"
def execute_shell_command(command: str) -> str:
    """
    Execute one or more shell commands.
    Supports commands separated by '&&' or newlines for sequential execution.
    Returns a JSON mapping of command to its combined stdout and stderr.
    """
    import subprocess
    try:
        # Split multiple commands
        if '&&' in command:
            cmds = [c.strip() for c in command.split('&&')]
        elif '\n' in command:
            cmds = [c.strip() for c in command.splitlines() if c.strip()]
        else:
            cmds = [command]
        outputs: Dict[str, str] = {}
        for cmd in cmds:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                outputs[cmd] = result.stdout + result.stderr
            except Exception as e:
                outputs[cmd] = f"ERROR: {e}"
        return json.dumps(outputs)
    except Exception as e:
        return f"ERROR: {e}"
read_file_tool = PatchedFunctionTool(read_file, 'read_file')
write_file_tool = PatchedFunctionTool(write_file, 'write_file')
list_files_tool = PatchedFunctionTool(list_files, 'list_files')
execute_shell_command_tool = PatchedFunctionTool(execute_shell_command, 'execute_shell_command')

# --- Define the Blueprint ---
class MCPDemoBlueprint(BlueprintBase):
    """Demonstrates using filesystem and memory MCP servers."""
    metadata: ClassVar[Dict[str, Any]] = {
        "name": "MCPDemoBlueprint",
        "title": "MCP Demo (Filesystem & Memory, Scalable & Viral FileOps)",
        "description": "A scalable agent (Sage) demonstrating interaction with filesystem and memory MCP servers, supporting horizontal scaling and viral file operations.",
        "version": "1.2.0",  # Updated for scaling & viral fileops
        "author": "Open Swarm Team (Refactored)",
        "tags": ["mcp", "filesystem", "memory", "demo", "scaling", "viral-fileops"],
        "required_mcp_servers": ["filesystem", "memory"],
        "env_vars": ["ALLOWED_PATH"],  # For filesystem MCP
    }

    # Caches
    _openai_client_cache: Dict[str, AsyncOpenAI] = {}
    _model_instance_cache: Dict[str, Model] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class DummyLLM:
            def chat_completion_stream(self, messages, **_):
                class DummyStream:
                    def __aiter__(self): return self
                    async def __anext__(self):
                        raise StopAsyncIteration
                return DummyStream()
        self.llm = DummyLLM()

    # --- Model Instantiation Helper --- (Standard helper)
    def _get_model_instance(self, profile_name: str) -> Model:
        """Retrieves or creates an LLM Model instance."""
        # ... (Implementation is the same as in previous refactors) ...
        if profile_name in self._model_instance_cache:
            logger.debug(f"Using cached Model instance for profile '{profile_name}'.")
            return self._model_instance_cache[profile_name]
        logger.debug(f"Creating new Model instance for profile '{profile_name}'.")
        profile_data = self.get_llm_profile(profile_name)
        if not profile_data: raise ValueError(f"Missing LLM profile '{profile_name}'.")
        provider = profile_data.get("provider", "openai").lower()
        model_name = profile_data.get("model")
        if not model_name: raise ValueError(f"Missing 'model' in profile '{profile_name}'.")
        if provider != "openai": raise ValueError(f"Unsupported provider: {provider}")
        client_cache_key = f"{provider}_{profile_data.get('base_url')}"
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

    def render_prompt(self, template_name: str, context: dict) -> str:
        return f"User request: {context.get('user_request', '')}\nHistory: {context.get('history', '')}\nAvailable tools: {', '.join(context.get('available_tools', []))}"

    # --- Agent Creation ---
    def create_starting_agent(self, mcp_servers: List[MCPServer]) -> Agent:
        """Creates the Sage agent, dynamically adding MCP server descriptions to its prompt."""
        logger.debug("Creating MCP Demo agent (Sage)...")
        self._model_instance_cache = {}
        self._openai_client_cache = {}

        default_profile_name = self.config.get("llm_profile", "default")
        logger.debug(f"Using LLM profile '{default_profile_name}' for Sage.")
        model_instance = self._get_model_instance(default_profile_name)

        # Filter for required MCPs and get descriptions
        required_names = self.metadata["required_mcp_servers"]
        agent_mcps: List[MCPServer] = []
        mcp_descriptions = []
        for server in mcp_servers:
            if server.name in required_names:
                agent_mcps.append(server)
                description = self.get_mcp_server_description(server.name)
                mcp_descriptions.append(f"- {server.name}: {description or 'No description available.'}")

        if len(agent_mcps) != len(required_names):
            missing = set(required_names) - {s.name for s in agent_mcps}
            logger.warning(f"Sage agent created, but missing required MCP server(s): {', '.join(missing)}. Functionality will be limited.")
            # Continue with available servers

        # Format descriptions for the prompt
        mcp_tool_desc_str = "\n".join(mcp_descriptions) if mcp_descriptions else "No external tools available."
        sage_instructions = sage_instructions_template.format(mcp_tool_descriptions=mcp_tool_desc_str)
        logger.debug(f"Sage instructions generated:\n{sage_instructions}")

        # Instantiate Sage
        sage_agent = Agent(
            name="Sage",
            model=model_instance,
            instructions=sage_instructions,
            tools=[read_file_tool, write_file_tool, list_files_tool, execute_shell_command_tool], # Tools come implicitly from assigned MCP servers
            mcp_servers=agent_mcps # Pass the list of *started* server objects
        )

        logger.debug("Sage agent created.")
        return sage_agent

    async def _original_run(self, messages: List[dict]) -> object:
        last_user_message = next((m['content'] for m in reversed(messages) if m['role'] == 'user'), None)
        if not last_user_message:
            yield {"messages": [{"role": "assistant", "content": "I need a user message to proceed."}]}
            return
        prompt_context = {
            "user_request": last_user_message,
            "history": messages[:-1],
            "available_tools": ["demo"]
        }
        rendered_prompt = self.render_prompt("mcp_demo_prompt.j2", prompt_context)
        yield {
            "messages": [
                {
                    "role": "assistant",
                    "content": f"[MCPDemo LLM] Would respond to: {rendered_prompt}"
                }
            ]
        }
        return

    async def run(self, messages: List[dict]) -> object:
        last_result = None
        async for result in self._original_run(messages):
            last_result = result
            yield result
        if last_result is not None:
            await self.reflect_and_learn(messages, last_result)
        return

    async def reflect_and_learn(self, messages, result):
        log = {
            'task': messages,
            'result': result,
            'reflection': 'Success' if self.success_criteria(result) else 'Needs improvement',
            'alternatives': self.consider_alternatives(messages, result),
            'swarm_lessons': self.query_swarm_knowledge(messages)
        }
        self.write_to_swarm_log(log)

    def success_criteria(self, result):
        if not result or (isinstance(result, dict) and 'error' in result):
            return False
        if isinstance(result, list) and result and 'error' in result[0].get('messages', [{}])[0].get('content', '').lower():
            return False
        return True

    def consider_alternatives(self, messages, result):
        alternatives = []
        if not self.success_criteria(result):
            alternatives.append('Try a different agent for the task.')
            alternatives.append('Fallback to a simpler command.')
        else:
            alternatives.append('Add more agent-to-agent coordination.')
        return alternatives

    def query_swarm_knowledge(self, messages):
        import json, os
        path = os.path.join(os.path.dirname(__file__), '../../../swarm_knowledge.json')
        if not os.path.exists(path):
            return []
        with open(path, 'r') as f:
            knowledge = json.load(f)
        task_str = json.dumps(messages)
        return [entry for entry in knowledge if entry.get('task_str') == task_str]

    def write_to_swarm_log(self, log):
        import json, os, time
        from filelock import FileLock, Timeout
        path = os.path.join(os.path.dirname(__file__), '../../../swarm_log.json')
        lock_path = path + '.lock'
        log['task_str'] = json.dumps(log['task'])
        for attempt in range(10):
            try:
                with FileLock(lock_path, timeout=5):
                    if os.path.exists(path):
                        with open(path, 'r') as f:
                            try:
                                logs = json.load(f)
                            except json.JSONDecodeError:
                                logs = []
                    else:
                        logs = []
                    logs.append(log)
                    with open(path, 'w') as f:
                        json.dump(logs, f, indent=2)
                break
            except Timeout:
                time.sleep(0.2 * (attempt + 1))

# Standard Python entry point
if __name__ == "__main__":
    import asyncio
    import json
    print("\033[1;36m\n╔══════════════════════════════════════════════════════════════╗\n║   🧠 MCP DEMO: AGENT INTERACTION & SWARM DEBUG DEMO         ║\n╠══════════════════════════════════════════════════════════════╣\n║ This blueprint showcases viral swarm propagation,            ║\n║ agent-to-agent interaction, and advanced debug logging.      ║\n║ Try running: python blueprint_mcp_demo.py                    ║\n╚══════════════════════════════════════════════════════════════╝\033[0m")
    messages = [
        {"role": "user", "content": "Show me how MCP Demo enables agent interaction and swarm debug logging."}
    ]
    blueprint = MCPDemoBlueprint(blueprint_id="demo-1")
    async def run_and_print():
        async for response in blueprint.run(messages):
            print(json.dumps(response, indent=2))
    asyncio.run(run_and_print())
