import argparse
from swarm.blueprints.geese.blueprint_geese import GeeseBlueprint

def main():
    parser = argparse.ArgumentParser(description="Run the Geese Blueprint")
    parser.add_argument('--message', dest='prompt', nargs='?', default=None, help='Prompt for the agent (optional, aliased as --message for compatibility)')
    parser.add_argument('--config', type=str, help='Path to config file', default=None)
    parser.add_argument('--agent-mcp', action='append', help='Agent to MCP assignment, e.g. --agent-mcp agent1:mcpA,mcpB')
    parser.add_argument('--model', type=str, help='Model name (overrides DEFAULT_LLM envvar)', default=None)
    args = parser.parse_args()

    agent_mcp_assignments = None
    if args.agent_mcp:
        agent_mcp_assignments = {}
        for assignment in args.agent_mcp:
            agent, mcps = assignment.split(':', 1)
            agent_mcp_assignments[agent] = [m.strip() for m in mcps.split(',')]

    blueprint = GeeseBlueprint(
        blueprint_id='geese',
        config_path=args.config,
        agent_mcp_assignments=agent_mcp_assignments
    )
    import asyncio
    messages = []
    if args.prompt:
        # PATCH: Always use blueprint.run for progressive UX
        messages = [{"role": "user", "content": args.prompt}]
        import asyncio
        from swarm.blueprints.geese.blueprint_geese import SPINNER_STATES, SLOW_SPINNER, display_operation_box
        import time
        async def run_and_print():
            spinner_idx = 0
            spinner_start = time.time()
            async for chunk in blueprint.run(messages, model=args.model):
                if isinstance(chunk, dict) and (chunk.get("progress") or chunk.get("matches") or chunk.get("spinner_state")):
                    elapsed = time.time() - spinner_start
                    spinner_state = chunk.get("spinner_state")
                    if not spinner_state:
                        spinner_state = SLOW_SPINNER if elapsed > 10 else SPINNER_STATES[spinner_idx % len(SPINNER_STATES)]
                    spinner_idx += 1
                    op_type = chunk.get("type", "search")
                    result_count = len(chunk.get("matches", [])) if chunk.get("matches") is not None else None
                    box_content = f"Matches so far: {result_count}" if result_count is not None else str(chunk)
                    display_operation_box(
                        title="Searching Filesystem" if chunk.get("progress") else "Geese Output",
                        content=box_content,
                        result_count=result_count,
                        params={k: v for k, v in chunk.items() if k not in {'matches', 'progress', 'total', 'truncated', 'done', 'spinner_state'}},
                        progress_line=chunk.get('progress'),
                        total_lines=chunk.get('total'),
                        spinner_state=spinner_state,
                        emoji="🔍" if chunk.get("progress") else "💡"
                    )
                else:
                    if isinstance(chunk, dict) and 'content' in chunk:
                        print(chunk['content'], end="")
                    else:
                        print(chunk, end="")
        asyncio.run(run_and_print())
        return

    # Set DEFAULT_LLM envvar if --model is given
    import os
    if args.model:
        os.environ['DEFAULT_LLM'] = args.model

    async def run_and_print():
        spinner_idx = 0
        spinner_start = time.time()
        from swarm.blueprints.geese.blueprint_geese import GeeseBlueprint, SPINNER_STATES, SLOW_SPINNER, display_operation_box
        import time
        async for chunk in blueprint.run(messages, model=args.model):
            # If chunk is a dict with progress info, show operation box
            if isinstance(chunk, dict) and (chunk.get("progress") or chunk.get("matches") or chunk.get("spinner_state")):
                elapsed = time.time() - spinner_start
                spinner_state = chunk.get("spinner_state")
                if not spinner_state:
                    spinner_state = SLOW_SPINNER if elapsed > 10 else SPINNER_STATES[spinner_idx % len(SPINNER_STATES)]
                spinner_idx += 1
                op_type = chunk.get("type", "search")
                result_count = len(chunk.get("matches", [])) if chunk.get("matches") is not None else None
                box_content = f"Matches so far: {result_count}" if result_count is not None else str(chunk)
                display_operation_box(
                    title="Searching Filesystem" if chunk.get("progress") else "Geese Output",
                    content=box_content,
                    result_count=result_count,
                    params={k: v for k, v in chunk.items() if k not in {'matches', 'progress', 'total', 'truncated', 'done', 'spinner_state'}},
                    progress_line=chunk.get('progress'),
                    total_lines=chunk.get('total'),
                    spinner_state=spinner_state,
                    emoji="🔍" if chunk.get("progress") else "💡"
                )
            else:
                if isinstance(chunk, dict) and 'content' in chunk:
                    print(chunk['content'], end="")
                else:
                    print(chunk, end="")
    asyncio.run(run_and_print())

if __name__ == "__main__":
    main()
