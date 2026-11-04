# MCP host configs (stdio signing proxy)

Package: **`@readfetch/mcp-x402-proxy@0.1.14`** · Node.js 20+ · [GitHub](https://github.com/readfetch/mcp-x402-proxy)

**Default path:** `readfetch_probe` (no wallet; optional ~400-char `preview` on HTML pages) → `readfetch_text` with the same `url`. If probe reports `challenge: true`, use `readfetch_scrape`. After a confusing call, **`readfetch_feedback`** — bind with `request_id` from **`X-Request-Id`** ([docs#feedback](https://readfetch.com/docs#feedback)).

| Mode | `EVM_PRIVATE_KEY` | What works |
|------|-------------------|------------|
| Probe only | omitted | `readfetch_probe`, `readfetch_feedback`, and `tools/list` |
| Paid tools | set (dedicated low-balance wallet on Base + USDC) | All catalog tools; capped by `READFETCH_MAX_PAYMENT_USD` (default `$1` per authorization) |

Restart the client after editing config. **Never commit a real private key** — use `~/.cursor/mcp.json` or OS keychain patterns for secrets.

## Cursor

**File:** `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project — do not put keys in git)

```json
{
  "mcpServers": {
    "readfetch": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@readfetch/mcp-x402-proxy@0.1.14"]
    }
  }
}
```

Paid tools — add `env`:

```json
"env": { "EVM_PRIVATE_KEY": "0xYOUR_KEY" }
```

## Claude Desktop

**File:** macOS `~/Library/Application Support/Claude/claude_desktop_config.json` · Windows `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "readfetch": {
      "command": "npx",
      "args": ["-y", "@readfetch/mcp-x402-proxy@0.1.14"]
    }
  }
}
```

## Claude Code

**File:** project `.mcp.json` or user config · CLI:

```bash
claude mcp add readfetch -- npx -y @readfetch/mcp-x402-proxy@0.1.14
```

Same JSON shape as Claude Desktop under `mcpServers.readfetch`.

## VS Code

**File:** `.vscode/mcp.json`

```json
{
  "servers": {
    "readfetch": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@readfetch/mcp-x402-proxy@0.1.14"]
    }
  }
}
```

## Windsurf

**File:** `~/.codeium/windsurf/mcp_config.json`

```json
{
  "mcpServers": {
    "readfetch": {
      "command": "npx",
      "args": ["-y", "@readfetch/mcp-x402-proxy@0.1.14"]
    }
  }
}
```

## Continue

**File:** `~/.continue/config.json` — add under `experimental.modelContextProtocolServers` (or the MCP block your Continue version documents):

```json
{
  "name": "readfetch",
  "command": "npx",
  "args": ["-y", "@readfetch/mcp-x402-proxy@0.1.14"]
}
```

## Cline

**File:** `cline_mcp_settings.json`

```json
{
  "mcpServers": {
    "readfetch": {
      "command": "npx",
      "args": ["-y", "@readfetch/mcp-x402-proxy@0.1.14"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

CLI: `cline mcp add readfetch --yes -- npx -y @readfetch/mcp-x402-proxy@0.1.14`

## Goose

**File:** Goose MCP settings (stdio server entry)

```json
{
  "readfetch": {
    "command": "npx",
    "args": ["-y", "@readfetch/mcp-x402-proxy@0.1.14"]
  }
}
```

## Remote MCP (ChatGPT, hosted bridges)

**Does not fit.** Remote MCP servers cannot attach `PAYMENT-SIGNATURE` on paid `tools/call`. Do **not** point a host at `https://readfetch.com/mcp` alone and expect payment to work.

Use instead:

- **This stdio proxy** on a machine you control, or
- **REST** via **`readfetch-client`** / **`@readfetch/client`** from your tool executor (x402 handled for you).
