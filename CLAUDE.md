# readfetch (Claude Code)

Same rules as [AGENTS.md](./AGENTS.md):

- Probe free → text or scrape from `challenge`.
- REST: 402 → `PAYMENT-SIGNATURE` retry; `billed: false` ≠ paid success.
- MCP: `npx -y @readfetch/mcp-x402-proxy@0.1.12` — not bare `https://readfetch.com/mcp` for paid tools.
- Confusing call: `readfetch_feedback` or `POST /v1/feedback` with `X-Request-Id` — not claims.
- REST clients: `readfetch-client` / `@readfetch/client` — [INTEGRATIONS.md](./INTEGRATIONS.md) · [REPOS.md](./REPOS.md).
- Host JSON: [HOSTS.md](./HOSTS.md).
