#!/usr/bin/env python3
"""PydanticAI tool — uses readfetch-client for x402 payment.

  pip install readfetch-client pydantic-ai
  export EVM_PRIVATE_KEY=0x…
  python readfetch_pydantic_ai_tool.py 'https://example.com'
"""

from __future__ import annotations

import asyncio
import json
import sys

from readfetch import Client

try:
    from pydantic_ai import Agent, RunContext
except ImportError as exc:
    raise SystemExit('pip install "pydantic-ai"') from exc


async def _readfetch_text(url: str) -> str:
    rf = Client()
    page = await rf.text(url)
    return json.dumps(page, ensure_ascii=False)


agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="Use readfetch_text when the user wants article text from a URL.",
)


@agent.tool
async def readfetch_text_tool(ctx: RunContext[None], url: str) -> str:
    """Read main article Markdown from a public URL via readfetch.com (x402 on Base)."""
    return await _readfetch_text(url)


async def _main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    result = await agent.run(f"Read this URL and summarize in one sentence: {url}")
    print(result.output)


if __name__ == "__main__":
    asyncio.run(_main())
