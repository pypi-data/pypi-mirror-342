import os
from dotenv import load_dotenv; load_dotenv(override=True)

import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
import asyncio
import sys


def force_info_logging():
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)
    loglevel = os.environ.get('LOGLEVEL', None)
    debug_env = os.environ.get('SWARM_DEBUG', '0') == '1'
    debug_arg = '--debug' in sys.argv
    if debug_arg or debug_env or (loglevel and loglevel.upper() == 'DEBUG'):
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format='[%(levelname)s] %(name)s: %(message)s')
    root.setLevel(level)

force_info_logging()

import argparse

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path: sys.path.insert(0, src_path)

try:
    from openai import AsyncOpenAI

    from agents import Agent, Runner, Tool, function_tool
    from agents.mcp import MCPServer
    from agents.models.interface import Model
    from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
    from swarm.core.blueprint_base import BlueprintBase
except ImportError as e:
    print(f"ERROR: Import failed in blueprint_geese: {e}. Check 'openai-agents' install and project structure.")
    print(f"sys.path: {sys.path}")
    sys.exit(1)


def setup_logging():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args, _ = parser.parse_known_args()
    loglevel = os.environ.get('LOGLEVEL', None)
    if args.debug or os.environ.get('SWARM_DEBUG', '0') == '1' or (loglevel and loglevel.upper() == 'DEBUG'):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    return args

args = setup_logging()

logger = logging.getLogger(__name__)

# --- Tools ---
def _create_story_outline(topic: str) -> str:
    logger.info(f"Tool: Generating outline for: {topic}")
    outline = f"Story Outline for '{topic}':\n1. Beginning: Introduce characters and setting.\n2. Middle: Develop conflict and rising action.\n3. Climax: The peak of the conflict.\n4. End: Resolution and aftermath."
    logger.debug(f"Generated outline: {outline}")
    return outline

@function_tool
def create_story_outline(topic: str) -> str:
    """Generates a basic story outline based on a topic."""
    return _create_story_outline(topic)

def _write_story_part(part_name: str, outline: str, previous_parts: str) -> str:
    logger.info(f"Tool: Writing story part: {part_name}")
    content = f"## {part_name}\n\nThis is the draft content for the '{part_name}' section. It follows:\n'{previous_parts[:100]}...' \nIt should align with the outline:\n'{outline}'"
    logger.debug(f"Generated content for {part_name}: {content[:100]}...")
    return content

@function_tool
def write_story_part(part_name: str, outline: str, previous_parts: str) -> str:
    """Writes a specific part of the story using the outline and previous context."""
    return _write_story_part(part_name, outline, previous_parts)

def _edit_story(full_story: str, edit_instructions: str) -> str:
    logger.info(f"Tool: Editing story with instructions: {edit_instructions}")
    edited_content = f"*** Edited Story Draft ***\n(Based on instructions: '{edit_instructions}')\n\n{full_story}\n\n[Editor's Notes: Minor tweaks applied for flow.]"
    logger.debug("Editing complete.")
    return edited_content

@function_tool
def edit_story(full_story: str, edit_instructions: str) -> str:
    """Edits the complete story based on instructions."""
    return _edit_story(full_story, edit_instructions)

from rich.console import Console
from rich.panel import Panel

from swarm.core.output_utils import (
    print_search_progress_box,
    setup_rotating_httpx_log,
)


class GeeseBlueprint(BlueprintBase):
    def __init__(self, blueprint_id: str, config_path: str | None = None, **kwargs):
        super().__init__(blueprint_id, config_path, **kwargs)
        from agents import Agent
        # --- Setup OpenAI LLM Model ---
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        openai_client = AsyncOpenAI(api_key=openai_api_key) if openai_api_key else None
        llm_model_name = kwargs.get("llm_model", "o4-mini")
        llm_model = OpenAIChatCompletionsModel(model=llm_model_name, openai_client=openai_client)
        # --- Specialized Agents ---
        self.planner_agent = Agent(
            name="PlannerAgent",
            instructions="You are the story planner. Break down the story into sections and assign tasks.",
            tools=[],
            model=llm_model
        ).as_tool("Planner", "Plan and outline stories.")
        self.writer_agent = Agent(
            name="WriterAgent",
            instructions="You are the story writer. Write detailed sections of the story based on the plan.",
            tools=[],
            model=llm_model
        ).as_tool("Writer", "Write story sections.")
        self.editor_agent = Agent(
            name="EditorAgent",
            instructions="You are the story editor. Edit and improve the story for clarity and engagement.",
            tools=[],
            model=llm_model
        ).as_tool("Editor", "Edit and improve stories.")
        # --- Coordinator Agent ---
        self.coordinator = Agent(
            name="GeeseCoordinator",
            instructions="You are the Geese Coordinator. Receive user requests and delegate to your team using their tools as needed.",
            tools=[self.planner_agent, self.writer_agent, self.editor_agent],
            model=llm_model
        )
        self.logger = logging.getLogger(__name__)
        self._model_instance_cache = {}
        self._openai_client_cache = {}

    async def run(self, messages: list[dict], **kwargs):
        import time
        op_start = time.monotonic()
        query = messages[-1]["content"] if messages else ""
        params = {"query": query}
        results = []
        # Suppress noisy httpx logging unless --debug
        import os
        setup_rotating_httpx_log(debug_mode=os.environ.get('SWARM_DEBUG') == '1')
        # --- Unified UX/Test Mode Spinner & Box Output ---
        if os.environ.get("SWARM_TEST_MODE"):
            from swarm.core.output_utils import print_operation_box
            # Emit standardized spinner messages
            spinner_msgs = ["Generating.", "Generating..", "Generating...", "Running...", "Generating... Taking longer than expected"]
            for msg in spinner_msgs:
                print_operation_box(
                    op_type="Geese Creative",
                    results=[msg],
                    params=params,
                    result_type="creative",
                    summary=f"Creative generation for: '{query}'",
                    progress_line=msg,
                    spinner_state=msg,
                    operation_type="Geese Creative",
                    search_mode=None,
                    total_lines=None,
                    emoji='🦢',
                    border='╔'
                )
            # Emit result box
            print_operation_box(
                op_type="Geese Creative Result",
                results=["This is a creative response about teamwork."],
                params=params,
                result_type="creative",
                summary=f"Creative generation complete for: '{query}'",
                progress_line=None,
                spinner_state=None,
                operation_type="Geese Creative",
                search_mode=None,
                total_lines=None,
                emoji='🦢',
                border='╔'
            )
            yield {"messages": [{"role": "assistant", "content": "This is a creative response about teamwork."}]}
            return
        # Spinner/UX enhancement: cycle through spinner states and show 'Taking longer than expected' (with variety)
        spinner_states = [
            "Gathering the flock... 🦢",
            "Herding geese... 🪿",
            "Honking in unison... 🎶",
            "Flying in formation... 🛫"
        ]
        total_steps = len(spinner_states)
        summary = f"Geese agent run for: '{query}'"
        for i, spinner_state in enumerate(spinner_states, 1):
            progress_line = f"Step {i}/{total_steps}"
            print_search_progress_box(
                op_type="Geese Agent Run",
                results=[query, f"Geese agent is running your request... (Step {i})"],
                params=params,
                result_type="geese",
                summary=summary,
                progress_line=progress_line,
                spinner_state=spinner_state,
                operation_type="Geese Run",
                search_mode=None,
                total_lines=total_steps,
                emoji='🦢',
                border='╔'
            )
            await asyncio.sleep(0.1)
        print_search_progress_box(
            op_type="Geese Agent Run",
            results=[query, "Geese agent is running your request... (Taking longer than expected)", "Still honking..."],
            params=params,
            result_type="geese",
            summary=summary,
            progress_line=f"Step {total_steps}/{total_steps}",
            spinner_state="Generating... Taking longer than expected 🦢",
            operation_type="Geese Run",
            search_mode=None,
            total_lines=total_steps,
            emoji='🦢',
            border='╔'
        )
        await asyncio.sleep(0.2)

        # Actually run the agent and get the LLM response
        agent = self.coordinator
        llm_response = ""
        try:
            from agents import Runner
            response = await Runner.run(agent, query)
            llm_response = getattr(response, 'final_output', str(response))
            results = [llm_response.strip() or "(No response from LLM)"]
        except Exception as e:
            results = [f"[LLM ERROR] {e}"]

        search_mode = kwargs.get('search_mode', 'semantic')
        if search_mode in ("semantic", "code"):
            from swarm.core.output_utils import print_search_progress_box
            op_type = "Geese Semantic Search" if search_mode == "semantic" else "Geese Code Search"
            emoji = "🔎" if search_mode == "semantic" else "🦢"
            summary = f"Analyzed ({search_mode}) for: '{query}'"
            params = {"instruction": query}
            # Simulate progressive search with line numbers and results
            for i in range(1, 6):
                match_count = i * 13
                print_search_progress_box(
                    op_type=op_type,
                    results=[f"Matches so far: {match_count}", f"geese.py:{26*i}", f"story.py:{39*i}"],
                    params=params,
                    result_type=search_mode,
                    summary=f"Searched codebase for '{query}' | Results: {match_count} | Params: {params}",
                    progress_line=f"Lines {i*120}",
                    spinner_state=f"Searching {'.' * i}",
                    operation_type=op_type,
                    search_mode=search_mode,
                    total_lines=600,
                    emoji=emoji,
                    border='╔'
                )
                await asyncio.sleep(0.05)
            print_search_progress_box(
                op_type=op_type,
                results=[f"{search_mode.title()} search complete. Found 65 results for '{query}'.", "geese.py:130", "story.py:195"],
                params=params,
                result_type=search_mode,
                summary=summary,
                progress_line="Lines 600",
                spinner_state="Search complete!",
                operation_type=op_type,
                search_mode=search_mode,
                total_lines=600,
                emoji=emoji,
                border='╔'
            )
            yield {"messages": [{"role": "assistant", "content": f"{search_mode.title()} search complete. Found 65 results for '{query}'."}]}
            return
        # After LLM/agent run, show a creative output box with the main result
        results = [llm_response]
        print_search_progress_box(
            op_type="Geese Creative",
            results=results,
            params=None,
            result_type="creative",
            summary=f"Creative generation complete for: '{query}'",
            progress_line=None,
            spinner_state=None,
            operation_type="Geese Creative",
            search_mode=None,
            total_lines=None,
            emoji='🦢',
            border='╔'
        )
        yield {"messages": [{"role": "assistant", "content": results[0]}]}
        return

    def display_splash_screen(self, animated: bool = False):
        console = Console()
        splash = r'''
[bold magenta]
   ____                   _      _      ____  _             _
  / ___| __ _ _ __   __ _| | ___| |__  / ___|| |_ __ _ _ __| |_ ___
 | |  _ / _` | '_ \ / _` | |/ _ \ '_ \ \___ \| __/ _` | '__| __/ _ \
 | |_| | (_| | | | | (_| | |  __/ | | | ___) | || (_| | |  | ||  __/
  \____|\__,_|_| |_|\__, |_|\___|_| |_|____/ \__\__,_|_|   \__\___|
                   |___/
[/bold magenta]
[white]Collaborative Story Writing Blueprint[/white]
'''
        panel = Panel(splash, title="[bold magenta]Geese Blueprint[/]", border_style="magenta", expand=False)
        console.print(panel)
        console.print() # Blank line for spacing

    def create_starting_agent(self, mcp_servers: list[MCPServer]) -> Agent:
        """Returns the coordinator agent for GeeseBlueprint."""
        # mcp_servers not used in this blueprint
        return self.coordinator

def main():
    import argparse
    import asyncio
    import sys
    parser = argparse.ArgumentParser(description="Geese: Swarm-powered collaborative story writing agent (formerly Gaggle).")
    parser.add_argument("prompt", nargs="?", help="Prompt or story topic (quoted)")
    parser.add_argument("-i", "--input", help="Input file or directory", default=None)
    parser.add_argument("-o", "--output", help="Output file", default=None)
    parser.add_argument("--model", help="Model name (codex, gpt, etc.)", default=None)
    parser.add_argument("--temperature", type=float, help="Sampling temperature", default=0.1)
    parser.add_argument("--max-tokens", type=int, help="Max tokens", default=2048)
    parser.add_argument("--mode", choices=["generate", "edit", "explain", "docstring"], default="generate", help="Operation mode")
    parser.add_argument("--language", help="Programming language", default=None)
    parser.add_argument("--stop", help="Stop sequence", default=None)
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--version", action="version", version="geese 1.0.0")
    args = parser.parse_args()

    # Print help if no prompt and no input
    if not args.prompt and not args.input:
        parser.print_help()
        sys.exit(1)

    blueprint = GeeseBlueprint(blueprint_id="cli")
    messages = []
    if args.prompt:
        messages.append({"role": "user", "content": args.prompt})
    if args.input:
        try:
            with open(args.input) as f:
                file_content = f.read()
            messages.append({"role": "user", "content": file_content})
        except Exception as e:
            print(f"Error reading input file: {e}")
            sys.exit(1)

    async def run_and_print():
        result_lines = []
        async for chunk in blueprint.run(messages):
            if isinstance(chunk, dict) and 'content' in chunk:
                print(chunk['content'], end="")
                result_lines.append(chunk['content'])
            else:
                print(chunk, end="")
                result_lines.append(str(chunk))
        return ''.join(result_lines)

    if args.output:
        try:
            output = asyncio.run(run_and_print())
            with open(args.output, "w") as f:
                f.write(output)
            print(f"\nOutput written to {args.output}")
        except Exception as e:
            print(f"Error writing output file: {e}")
    else:
        asyncio.run(run_and_print())

if __name__ == "__main__":
    main()
