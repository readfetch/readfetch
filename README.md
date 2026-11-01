# readfetch

**Web reading for AI agents** — text, maps, rendered Markdown, raw HTTP, PDFs, sections, diffs,
screenshots, search, and bounded crawl. Pay per call in **USDC on Base** via **[x402](https://docs.cdp.coinbase.com/x402/welcome)**.
No API key; reading routes charge only when content is delivered (`billed: true`); **`/v1/fetch`** when the origin answers.

**Live service:** [https://readfetch.com](https://readfetch.com)

> This repository is **documentation and discovery links only**. The running service and its
> implementation are not open source.

## Documentation map

| Document | What it covers |
|----------|----------------|
| **[INTEGRATIONS.md](./INTEGRATIONS.md)** | **Integrator guide** — clients, MCP, 402, frameworks, claims, feedback, relays |
| [AGENTS.md](./AGENTS.md) | Short drop-in for AI agents |
| [HOSTS.md](./HOSTS.md) | MCP `mcpServers` JSON per host (Cursor, Claude, …) |
| [REPOS.md](./REPOS.md) | GitHub · npm · PyPI for clients and proxy |
| [examples/](./examples/README.md) | LangChain, PydanticAI, Vercel AI, n8n, MCP snippet |

**On the site:** [readfetch.com/integrations](https://readfetch.com/integrations) · [readfetch.com/examples](https://readfetch.com/examples) · [readfetch.com/docs](https://readfetch.com/docs)

---

## Clients & integrations (app code)

Official packages (**0.1.12+**) — all published routes, x402 signing, `call()` / `quote()`, feedback and claims helpers:

```bash
pip install readfetch-client          # Python → github.com/readfetch/client-py
npm install @readfetch/client         # Node   → github.com/readfetch/client-js
```

**MCP hosts** (Cursor, Claude Desktop, …) — most cannot sign x402 on the remote MCP URL. Use the stdio proxy:

```bash
npx -y @readfetch/mcp-x402-proxy@0.1.12
```

Copy-paste host configs: [HOSTS.md](./HOSTS.md). **Full client + MCP guide:** [INTEGRATIONS.md](./INTEGRATIONS.md).

| Package | npm / PyPI | GitHub |
|---------|------------|--------|
| `@readfetch/client` | [npm](https://www.npmjs.com/package/@readfetch/client) | [client-js](https://github.com/readfetch/client-js) |
| `readfetch-client` | [PyPI](https://pypi.org/project/readfetch-client/) | [client-py](https://github.com/readfetch/client-py) |
| `@readfetch/mcp-x402-proxy` | [npm](https://www.npmjs.com/package/@readfetch/mcp-x402-proxy) | [mcp-x402-proxy](https://github.com/readfetch/mcp-x402-proxy) |

**Agents (drop-in):** [AGENTS.md](./AGENTS.md) · [CLAUDE.md](./CLAUDE.md)

---

## Start here (free)

```bash
curl -sS -X POST https://readfetch.com/v1/probe \
  -H 'content-type: application/json' \
  -d '{"url":"https://example.com"}'
```

`/v1/probe` is free: metadata plus an optional **`preview`** (~400 characters of `/v1/text` extraction when HTML and not a bot wall) before you pay.

## Pay and call (curl)

1. **`POST /v1/probe`** (free) — then **`/v1/text`** or **`/v1/scrape`** from the result.
2. On **402**, read the quote in the body and `PAYMENT-REQUIRED` header.
3. Sign the USDC authorization (x402 v2), retry with **`PAYMENT-SIGNATURE`**.

Prefer clients over hand-rolled 402: [INTEGRATIONS.md](./INTEGRATIONS.md).

## Endpoints (USD per call)

| Route | Price | Role |
|-------|-------|------|
| `/v1/fetch` | $0.003 | Raw HTTP / APIs |
| `/v1/section`, `/v1/diff`, `/v1/screenshot`, `/v1/crawl` | $0.003 | Section, change detection, screenshot, async crawl |
| `/v1/text`, `/v1/map`, `/v1/scrape`, `/v1/pdf`, `/v1/search` | $0.005 | Text, site map, render, PDF, search |
| `/v1/batch` | $0.0015/page | Up to 50 URLs, one payment |
| `/v1/scrape/residential` | $0.02 | Render via residential egress |
| `/v1/probe` | free | Preview before pay |
| `GET /v1/crawl/{id}` | free | Poll async crawl jobs |

Residential is **`POST /v1/scrape/residential`** (same JSON as scrape), not an `egress` body field. Details: [INTEGRATIONS.md](./INTEGRATIONS.md).

Authoritative prices and JSON schemas: [x402-resources.json](https://readfetch.com/.well-known/x402-resources.json).

## Discovery for agents

| Resource | URL |
|----------|-----|
| **Integrations (this repo)** | [INTEGRATIONS.md](./INTEGRATIONS.md) |
| Routing doc | [SKILL.md](https://readfetch.com/SKILL.md) |
| LLMs index | [llms.txt](https://readfetch.com/llms.txt) |
| x402 catalog | [/.well-known/x402-resources.json](https://readfetch.com/.well-known/x402-resources.json) |
| Service manifest | [/.well-known/service.json](https://readfetch.com/.well-known/service.json) |
| OpenAPI | [/openapi.json](https://readfetch.com/openapi.json) |
| MCP | `POST https://readfetch.com/mcp` · [manifest](https://readfetch.com/.well-known/mcp.json) · [HOSTS.md](./HOSTS.md) |
| REST clients | [INTEGRATIONS.md](./INTEGRATIONS.md) · [REPOS.md](./REPOS.md) |
| Framework recipes | [examples/](./examples/README.md) |
| Agent drop-ins | [AGENTS.md](./AGENTS.md) · [CLAUDE.md](./CLAUDE.md) |

Listed on **[CDP Bazaar](https://docs.cdp.coinbase.com/x402/bazaar)** and
**[agentic.market](https://agentic.market/)** (search: `readfetch`).

## Beta feedback

After a confusing call, agents should `POST /v1/feedback` with the **`X-Request-Id`** from that response (`readfetch_feedback` over MCP). Categories: `integration`, `docs`, `site`, `other`.

Paid delivery disputes use **`POST /v1/claims`** with the `RECEIPT` header and signature — not feedback. See [readfetch.com/docs#feedback](https://readfetch.com/docs#feedback).

## License

Text in this repository is © readfetch operators. You may link to and quote it with attribution.
The **readfetch.com service, APIs, and backend code are not licensed for reuse or self-hosting**
from this repo.
