# readfetch — agent integration

**Service:** https://readfetch.com · Pay per call in USDC on Base (x402 v2). No API key.

**Integrator lanes:** paid delivery disputes → `POST /v1/claims` (receipt + signature). Confusing 402, MCP, docs, or site → `POST /v1/feedback` with **`X-Request-Id`** from that response (MCP: **`readfetch_feedback`**, free). Not for billing — see https://readfetch.com/docs#feedback.

## Free preflight (always first)

**`POST /v1/probe`** is free — no wallet, no 402. So are `GET /v1/crawl/{id}` (poll a crawl job), `POST /v1/claims` and `POST /v1/feedback`. Everything else is a paid route. MCP **`readfetch_probe`** is the same free probe (no `EVM_PRIVATE_KEY` required).

```bash
curl -sS -X POST https://readfetch.com/v1/probe \
  -H 'content-type: application/json' \
  -d '{"url":"https://example.com"}'
```

Returns status, title, size, `challenge`, and often a **`preview`** (~400 characters). Then pay only if you need the full page.

## Default call path

1. **`POST /v1/probe`** (free) with `{"url":"…"}` — as above.
2. If `challenge` is false → **`POST /v1/text`** with the same `url`.
3. If `challenge` is true → **`POST /v1/scrape`** (then `/v1/scrape/residential` if still blocked).

Residential is **`POST /v1/scrape/residential`** (same JSON as scrape), not an `egress` body field.

Prices and schemas: `/.well-known/x402-resources.json`, `/openapi.json`. Routing table: `/SKILL.md`.

## Paying (REST)

1. POST without payment → **402** + quote in body / `PAYMENT-REQUIRED` (402 `hint` and `discovery.probe` remind you probe is free).
2. **`readfetch-client` / `@readfetch/client`** (or **`@readfetch/mcp-x402-proxy`** for MCP) complete payment and retry automatically.
3. **`billed: false`** means **not charged** — read **`hint`**. On **`/v1/fetch`**, origin 4xx/5xx and empty bodies may still be **`billed: true`** (bot-check pages and transport failures are not). Do not treat `billed: false` as success.

**Clients (recommended):** `pip install readfetch-client` · `npm install @readfetch/client`

```python
from readfetch import Client
rf = Client(private_key="0x…")  # funded account with USDC on Base
print(rf.fetch("https://example.com")["text"])
```

```javascript
import { Client } from "@readfetch/client";
const page = await new Client({ privateKey: "0x…" }).fetch("https://example.com");
```

Free probe: `Client().probe(url)` (Python) / `await new Client().probe(url)` (JS). Paid routes need `EVM_PRIVATE_KEY` or constructor key. Low-level: `@x402/fetch` (JS), `x402[httpx,evm]` (Python), `awal x402 pay` (CLI).

| Package | GitHub |
|---------|--------|
| `readfetch-client` | https://github.com/readfetch/client-py |
| `@readfetch/client` | https://github.com/readfetch/client-js |
| `@readfetch/mcp-x402-proxy` | https://github.com/readfetch/mcp-x402-proxy |

Repo map: [REPOS.md](./REPOS.md)

## MCP (Cursor, Claude Desktop, VS Code, …)

Most hosts **cannot** sign x402 on `POST https://readfetch.com/mcp`. Use the stdio proxy:

```bash
npx -y @readfetch/mcp-x402-proxy@0.1.14
```

- **No env:** `readfetch_probe` + `tools/list` only (**free**); **`readfetch_feedback`** (free) for integration issues — pass `request_id` from the call’s **`X-Request-Id`**.
- **`EVM_PRIVATE_KEY`:** paid tools (`readfetch_text`, …). Use a dedicated low-balance wallet.

Copy-paste configs per host: [HOSTS.md](./HOSTS.md). Source: https://github.com/readfetch/mcp-x402-proxy

## Frameworks

One client per language — wrap in your `@tool` / `tool()`. Examples on GitHub (not separate LangChain/CrewAI packages):

| Stack | Example |
|-------|---------|
| Python (LangChain, crewAI, LlamaIndex, PydanticAI) | [examples/readfetch_text_tool.py](./examples/readfetch_text_tool.py) |
| Node (LangChain.js, OpenAI Agents, Vercel AI SDK) | [examples/readfetch_text_tool.mjs](./examples/readfetch_text_tool.mjs) |
| n8n | [examples/n8n-readfetch-text.json](./examples/n8n-readfetch-text.json) (Code node) |

## Discovery

| Resource | URL |
|----------|-----|
| **Integrations (GitHub)** | [INTEGRATIONS.md](./INTEGRATIONS.md) |
| This file (GitHub) | https://github.com/readfetch/readfetch/blob/main/AGENTS.md |
| Host configs | [HOSTS.md](./HOSTS.md) |
| Integrations (human) | https://readfetch.com/integrations |
| Feedback (API) | https://readfetch.com/docs#feedback |
| LLMs index | https://readfetch.com/llms.txt |
| MCP manifest | https://readfetch.com/.well-known/mcp.json |
