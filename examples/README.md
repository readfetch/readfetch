# Framework examples

Thin wrappers around **`readfetch-client`** / **`@readfetch/client`** (**0.1.15+**) — `Client(private_key=…)` then `fetch(url)` or `await client.call(…)`; probe first with `Client().probe(url)` (free).

**Hub:** [INTEGRATIONS.md](../INTEGRATIONS.md) · [readfetch.com/integrations](https://readfetch.com/integrations)

| File | Use with |
|------|----------|
| [readfetch_text_tool.py](./readfetch_text_tool.py) | LangChain, crewAI, LlamaIndex — **`readfetch-client`** |
| [readfetch_text_tool.mjs](./readfetch_text_tool.mjs) | LangChain.js, OpenAI Agents SDK — **`@readfetch/client`** |
| [readfetch_pydantic_ai_tool.py](./readfetch_pydantic_ai_tool.py) | PydanticAI |
| [readfetch_vercel_ai_tool.mjs](./readfetch_vercel_ai_tool.mjs) | Vercel AI SDK `tool()` |
| [n8n-readfetch-text.json](./n8n-readfetch-text.json) | n8n Code node scaffold |
| [mcp.cursor.json](./mcp.cursor.json) | Cursor MCP snippet |

**MCP hosts:** [HOSTS.md](../HOSTS.md) · [`@readfetch/mcp-x402-proxy@0.1.15`](https://github.com/readfetch/mcp-x402-proxy).

**Repos:** [REPOS.md](../REPOS.md) · [AGENTS.md](../AGENTS.md) · [CLAUDE.md](../CLAUDE.md)

## Python

```bash
pip install readfetch-client langchain-core
export EVM_PRIVATE_KEY=0x…
python readfetch_text_tool.py 'https://example.com'
```

## Node

```bash
npm install @readfetch/client
export EVM_PRIVATE_KEY=0x…
node readfetch_text_tool.mjs 'https://example.com'
```
