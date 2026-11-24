// news-image-20261124 — "The World Today", 24 November 2026.
// Copies the pre-rendered front page (entry.png) to the output directory,
// byte for byte. Deterministic: no network, no timestamps, no randomness,
// so two runs write identical bytes (verified: same sha256 twice).
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error(`entry.png missing next to main.ts (${src})`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
