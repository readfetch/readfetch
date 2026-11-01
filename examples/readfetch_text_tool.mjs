#!/usr/bin/env node
/**
 * LangChain.js / OpenAI Agents SDK — import from @readfetch/client.
 *
 *   npm install @readfetch/client
 *   export EVM_PRIVATE_KEY=0x…
 *   node readfetch_text_tool.mjs 'https://example.com'
 */

import { pathToFileURL } from "node:url";
import {
  probeWithMeta,
  readfetchText,
  readfetchTextToolDefinition,
  submitFeedback,
} from "@readfetch/client";

export { readfetchText, readfetchTextToolDefinition, probeWithMeta, submitFeedback };

const url = process.argv[2] || "https://example.com";
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { data: check, requestId } = await probeWithMeta(url);
  if (requestId) {
    console.error(`readfetch X-Request-Id (probe): ${requestId}`);
  }
  if (check.challenge) {
    console.error("probe: challenge — use /v1/scrape, not text");
    process.exit(1);
  }
  const page = await readfetchText(url);
  console.log(JSON.stringify(page, null, 2));
}
