# Integrations — clients, MCP, frameworks

How to integrate readfetch: **REST clients**, **MCP**, **402 payment**, **claims & feedback**, and **agent frameworks**. Host-specific MCP JSON: [HOSTS.md](./HOSTS.md). Live page: **[readfetch.com/integrations](https://readfetch.com/integrations)**.

| Need | Section |
|------|---------|
| Node / Python (x402 handled) | [Official REST clients](#official-rest-clients) |
| Cursor, Claude, VS Code, … | [MCP](#mcp-cursor-claude-etc) · [HOSTS.md](./HOSTS.md) |
| LangChain, n8n, Vercel AI SDK | [Agent frameworks](#agent-frameworks) · [examples/](./examples/README.md) |
| Repo / registry map | [REPOS.md](./REPOS.md) |
| Short agent drop-in | [AGENTS.md](./AGENTS.md) |

---

## Free preflight

`POST https://readfetch.com/v1/probe` is the free endpoint — no wallet, no 402, no x402. Every other catalogue route is paid (poll crawl jobs with `GET /v1/crawl/{id}` after a paid `POST /v1/crawl`; see Claims and Feedback sections for dispute paths).

```python
# pip install readfetch-client
from readfetch import Client

print(Client().probe("https://example.com"))
```

MCP: **`readfetch_probe`** with the same body — no `EVM_PRIVATE_KEY` on the signing proxy.

If `challenge` is false, pay for `POST /v1/text` with the same `url` (or read the **`preview`** on the probe response — up to ~400 characters). If `challenge` is true, use `/v1/scrape` (or `/v1/scrape/residential`).

Residential is a **path**, not a JSON knob: same body as `/v1/scrape`, URL **`/v1/scrape/residential`**. Body `egress` keys are not in the catalogue and are ignored if sent.

---

## Paid calls (x402 v2)

Use official clients (`readfetch-client` / `@readfetch/client` **0.1.15+**) or **`@readfetch/mcp-x402-proxy`** — pass `private_key` / `EVM_PRIVATE_KEY` once; the 402 → pay → retry loop is automatic.

Every 402 includes **`extensions.bazaar`** for CDP/agentic.market discovery and a **`resource`** object with `tags` and `serviceName`.

Example body: `{"url": "https://www.python.org/about/"}` — use **`readfetch-client`**, **`@readfetch/client`**, or **`@readfetch/mcp-x402-proxy`** (see below). Direct HTTP without a signing client stops at **402**.

---

## Official REST clients

| Install | Registry | Source |
|---------|----------|--------|
| `pip install readfetch-client` | [PyPI](https://pypi.org/project/readfetch-client/) | [readfetch/client-py](https://github.com/readfetch/client-py) |
| `npm install @readfetch/client` | [npm](https://www.npmjs.com/package/@readfetch/client) | [readfetch/client-js](https://github.com/readfetch/client-js) |

**Environment:** `EVM_PRIVATE_KEY` (or constructor `private_key` / `privateKey`) before paid calls. **`Client().probe(url)` is free** — no key. Optional: `READFETCH_MAX_PAYMENT_USD` (default `1`), `READFETCH_BASE_URL` (production host only unless `READFETCH_DEV=1`).

### Python

```python
# pip install readfetch-client
from readfetch import Client

rf = Client(private_key="0x…")  # funded account with USDC on Base
check = Client().probe("https://example.com")  # free
if not check.get("challenge"):
    print(rf.fetch("https://example.com")["text"])
# other routes: await rf.call("scrape", {"url": "…"})
```

See [client-py README](https://github.com/readfetch/client-py/blob/main/README.md) for async helpers, `quote()`, `submit_feedback`, every catalog route.

### Node

```javascript
// npm install @readfetch/client
import { Client } from "@readfetch/client";

const rf = new Client({ privateKey: "0x…" });
const check = await new Client().probe("https://example.com");
if (!check.challenge) {
  console.log((await rf.fetch("https://example.com")).text);
}
// await rf.call("scrape", { url: "…" });
```

See [client-js README](https://github.com/readfetch/client-js/blob/main/README.md) for `paymentConfig()`, `quote()`, `submitClaim()`, every catalog route.

---

## MCP (Cursor, Claude, etc.)

Tools at `POST https://readfetch.com/mcp` (streamable HTTP). Default: **`readfetch_probe`** then **`readfetch_text`**. **`readfetch_feedback`** — bind `request_id` from **`X-Request-Id`**.

Most hosts **cannot** attach `PAYMENT-SIGNATURE` on `tools/call`. Use the **stdio signing proxy**:

```json
{
  "mcpServers": {
    "readfetch": {
      "command": "npx",
      "args": ["-y", "@readfetch/mcp-x402-proxy@0.1.15"],
      "env": { "EVM_PRIVATE_KEY": "0x…" }
    }
  }
}
```

Package: [`@readfetch/mcp-x402-proxy`](https://www.npmjs.com/package/@readfetch/mcp-x402-proxy) · [GitHub](https://github.com/readfetch/mcp-x402-proxy) · [HOSTS.md](./HOSTS.md) · [/.well-known/mcp.json](https://readfetch.com/.well-known/mcp.json)

---

## Agent frameworks

One client per language — wrap in your `@tool` / `tool()`. No separate LangChain/CrewAI package.

| Stack | Client | Example |
|-------|--------|---------|
| Python (`@tool`) | `readfetch-client` | [readfetch_text_tool.py](./examples/readfetch_text_tool.py) |
| PydanticAI | `readfetch-client` | [readfetch_pydantic_ai_tool.py](./examples/readfetch_pydantic_ai_tool.py) |
| Node | `@readfetch/client` | [readfetch_text_tool.mjs](./examples/readfetch_text_tool.mjs) |
| Vercel AI SDK | `@readfetch/client` + `ai` | [readfetch_vercel_ai_tool.mjs](./examples/readfetch_vercel_ai_tool.mjs) |
| n8n | Code node + `@readfetch/client` | [n8n-readfetch-text.json](./examples/n8n-readfetch-text.json) |
| MCP-only hosts | `@readfetch/mcp-x402-proxy@0.1.15` | [HOSTS.md](./HOSTS.md) · [mcp.cursor.json](./examples/mcp.cursor.json) |

Recipes: **[readfetch.com/examples](https://readfetch.com/examples)**.

---

## Integrator feedback (not billing)

| Issue | What to use |
|-------|-------------|
| Paid delivery (`truncated`, or `wrong_content` after manual review) | `POST /v1/claims` with **`RECEIPT`** + EIP-191 signature — [docs#claims](https://readfetch.com/docs#claims) |
| Confusing 402, MCP, docs, or site copy | `POST /v1/feedback` with **`X-Request-Id`** — [docs#feedback](https://readfetch.com/docs#feedback) |

Clients: `submit_feedback` / `submitFeedback`. MCP: **`readfetch_feedback`** (`integration`, `docs`, `site`, `other`). Feedback never auto-credits.

Every JSON API response includes **`readfetch.support`**; see `/llms.txt` and `/SKILL.md`.

### Claims

Only **`truncated`** is auto-approved for credits. **`empty`** returns 422 — probe before paying or escalate to `/v1/scrape`. See [SKILL.md](https://readfetch.com/SKILL.md).

### Errors

- **`billed: false`** — nothing was charged; read **`hint`**. On **`/v1/fetch`**, origin 4xx/5xx and empty bodies can still be **`billed: true`** — only transport failures and bot-check pages are unbilled.
- Non-2xx: `{ "status", "error", "hint", "billed" }`.
- Do not scrape this GitHub repo for API behavior; use **OpenAPI** and **x402-resources.json** on the live host.
