import sys

import anyio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)


async def run_agent(prompt: str) -> None:
    """Run the agent with the given prompt."""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print("\n--- Result ---")
            print(message.result)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python agent.py '<prompt>'")
        print("Example: python agent.py 'List all Python files and summarize what they do'")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    anyio.run(run_agent, prompt)


if __name__ == "__main__":
    main()
