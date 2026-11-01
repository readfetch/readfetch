/**
 * Vercel AI SDK tool() — uses @readfetch/client.
 *
 *   npm install @readfetch/client ai zod
 *   export EVM_PRIVATE_KEY=0x…
 *   node readfetch_vercel_ai_tool.mjs 'https://example.com'
 */

import { tool } from "ai";
import { z } from "zod";
import { pathToFileURL } from "node:url";
import { readfetchText } from "@readfetch/client";

export const readfetchTextTool = tool({
  description:
    "Read a public URL and return main article text as Markdown (readfetch.com, x402 on Base).",
  parameters: z.object({
    url: z.string().url(),
  }),
  execute: async ({ url }) => readfetchText(url),
});

const url = process.argv[2] || "https://example.com";
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  readfetchText(url).then((data) => console.log(JSON.stringify(data, null, 2)));
}
