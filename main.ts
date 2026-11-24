// The World in a Day — 24 November 2026 (Node 22, standard library only).
//
// The front page is drawn by render.py (Pillow) into entry.png beside this
// file. This program's only job is to place that image where the grader
// expects it: $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png when the
// variable is unset (inside the grader's container).
//
//   python3 render.py
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
