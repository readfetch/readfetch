#!/usr/bin/env python3
"""LangChain / crewAI / LlamaIndex — wrap `readfetch_text` in your @tool decorator.

  pip install readfetch-client
  export EVM_PRIVATE_KEY=0x…
  python readfetch_text_tool.py 'https://example.com'
"""

from __future__ import annotations

import asyncio
import json
import sys

from readfetch_client import probe_with_meta, readfetch_text, submit_feedback

try:
    from langchain_core.tools import tool

    @tool
    def readfetch_text_tool(url: str) -> str:
        """Read the main article text from a public URL (readfetch.com, x402)."""
        data = asyncio.run(readfetch_text(url))
        return json.dumps(data, ensure_ascii=False)
except ImportError:
    readfetch_text_tool = None  # type: ignore[misc, assignment]


async def _main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    check, request_id = await probe_with_meta(url)
    if request_id:
        print(f"readfetch X-Request-Id (probe): {request_id}", file=sys.stderr)
    if check.get("challenge"):
        print("probe: challenge — use /v1/scrape, not text", file=sys.stderr)
        raise SystemExit(1)
    data = await readfetch_text(url)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    # Example: await submit_feedback(request_id, "integration", "…") if request_id


if __name__ == "__main__":
    asyncio.run(_main())
