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
  Client,
  readfetchTextToolDefinition,
  submitFeedback,
} from "@readfetch/client";

export { readfetchTextToolDefinition, submitFeedback };

const url = process.argv[2] || "https://example.com";
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const rf = new Client(); // EVM_PRIVATE_KEY from env
  const check = await rf.probe(url);
  console.error(JSON.stringify({ probe: check }, null, 2));
  if (check.challenge) {
    console.error("probe: challenge — use /v1/scrape, not text");
    process.exit(1);
  }
  const page = await rf.fetch(url);
  console.log(JSON.stringify(page, null, 2));
}
