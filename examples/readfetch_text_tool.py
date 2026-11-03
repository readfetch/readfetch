#!/usr/bin/env python3
"""LangChain / crewAI / LlamaIndex — wrap `Client.fetch` in your @tool decorator.

  pip install readfetch-client
  export EVM_PRIVATE_KEY=0x…   # or pass private_key= to Client()
  python readfetch_text_tool.py 'https://example.com'
"""

from __future__ import annotations

import json
import sys

from readfetch import Client
from readfetch_client import submit_feedback

try:
    from langchain_core.tools import tool

    @tool
    def readfetch_text_tool(url: str) -> str:
        """Read the main article text from a public URL (readfetch.com, x402)."""
        page = Client(private_key="0x…").fetch(url)  # funded account with USDC on Base
        return json.dumps(page, ensure_ascii=False)
except ImportError:
    readfetch_text_tool = None  # type: ignore[misc, assignment]


def main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    rf = Client()  # uses EVM_PRIVATE_KEY from the environment
    check = rf.probe(url)
    print(json.dumps({"probe": check}, indent=2))
    if check.get("challenge"):
        print("probe: challenge — use /v1/scrape, not text", file=sys.stderr)
        raise SystemExit(1)
    page = rf.fetch(url)
    print(json.dumps(page, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
