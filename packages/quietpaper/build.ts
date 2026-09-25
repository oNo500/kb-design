import { bundle } from "lightningcss";
import { watch } from "chokidar";
import { flavors } from "@catppuccin/palette";
import { writeFileSync, mkdirSync, readFileSync, lstatSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { parseArgs } from "node:util";

const ROOT = import.meta.dir;
const ENTRY = join(ROOT, "src/theme.css");
const OUT_DIR = join(ROOT, "theme");
const OUT = join(OUT_DIR, "theme.css");
const MANIFEST = join(OUT_DIR, "manifest.json");
const TOKENS_OUT = join(ROOT, "src/tokens/generated.css");

// 暗色档 flavor 选择：mocha（默认深紫黑）/ macchiato（次深）/ frappe（中浅）
// 改这里 → bun run tokens 重生成 generated.css
const DARK_FLAVOR = "mocha" as const;
const LIGHT_FLAVOR = "latte" as const;

type FlavorName = "mocha" | "macchiato" | "frappe" | "latte";

function renderFlavor(flavorName: FlavorName, suffix = ""): string {
  return flavors[flavorName].colorEntries
    .flatMap(([name, { hex, hsl, rgb, accent }]) => {
      const lines = [`  --ctp-${name}${suffix}: ${hex};`];
      // 强调色额外输出 HSL 分量（覆盖 Obsidian --accent-h/s/l）和 RGB triplet
      // （供 Obsidian --callout-* 这类期望 "r, g, b" 格式的变量使用）
      if (accent) {
        const h = hsl.h.toFixed(1);
        const s = (hsl.s * 100).toFixed(1) + "%";
        const l = (hsl.l * 100).toFixed(1) + "%";
        lines.push(
          `  --ctp-${name}-h${suffix}: ${h};`,
          `  --ctp-${name}-s${suffix}: ${s};`,
          `  --ctp-${name}-l${suffix}: ${l};`,
          `  --ctp-${name}-rgb${suffix}: ${rgb.r}, ${rgb.g}, ${rgb.b};`,
        );
      }
      return lines;
    })
    .join("\n");
}

function tokens() {
  // body 上无条件输出两组 -dark / -light 后缀变量，
  // 让 print 这种「必须强制单 flavor」的场景也能用变量而非硬编码 hex
  const css = `/* generated — do not edit, run \`bun run tokens\` (dark flavor: ${DARK_FLAVOR}) */
body {
${renderFlavor(DARK_FLAVOR, "-dark")}
${renderFlavor(LIGHT_FLAVOR, "-light")}
}

.theme-dark {
${renderFlavor(DARK_FLAVOR)}
}

.theme-light {
${renderFlavor(LIGHT_FLAVOR)}
}
`;
  mkdirSync(dirname(TOKENS_OUT), { recursive: true });
  writeFileSync(TOKENS_OUT, css);
  log(`tokens → ${TOKENS_OUT} (dark: ${DARK_FLAVOR})`);
}

function bundleCSS(opts: { minify: boolean; watch: boolean }) {
  const start = performance.now();
  try {
    const { code } = bundle({
      filename: ENTRY,
      minify: opts.minify,
      sourceMap: !opts.minify,
      errorRecovery: false,
    });
    mkdirSync(OUT_DIR, { recursive: true });
    writeFileSync(OUT, code);
    const ms = (performance.now() - start).toFixed(1);
    log(`bundle → ${OUT} (${code.length}B, ${ms}ms)`);
  } catch (e) {
    error("bundle failed", (e as Error).message);
    // watch 模式保留运行让用户改完救回来；一次性 build/deploy 必须中断，
    // 否则 sync 会用上次成功的 theme.css 静默部署，跟代码不一致
    if (!opts.watch) process.exit(1);
  }
}

function build() {
  tokens();
  bundleCSS({ minify: true, watch: false });
}

// Refuse redirection outside the declared theme directory. The vault must
// already be an Obsidian vault; deployment does not create or configure it.
function checkPath(path: string, directory: boolean, required = false) {
  const stat = lstatSync(path, { throwIfNoEntry: false });
  if (!stat) {
    if (required) throw new Error(`required path not found: ${path}`);
    return;
  }
  if (stat.isSymbolicLink() || (directory ? !stat.isDirectory() : !stat.isFile()))
    throw new Error(`expected a regular ${directory ? "directory" : "file"}: ${path}`);
}

function deploymentTarget(vault: string): string {
  const root = resolve(vault);
  checkPath(root, true, true);
  checkPath(join(root, ".obsidian"), true, true);
  const themes = join(root, ".obsidian", "themes");
  const destination = join(themes, "quietpaper");
  checkPath(themes, true);
  checkPath(destination, true);
  for (const name of ["theme.css", "manifest.json"])
    checkPath(join(destination, name), false);
  return destination;
}

function sync(vault: string) {
  const destination = deploymentTarget(vault);
  // Read both inputs before changing an installed theme.
  const css = readFileSync(OUT);
  const manifest = readFileSync(MANIFEST);
  if (!css.length || JSON.parse(manifest.toString()).name !== "quietpaper")
    throw new Error("invalid quietpaper build artifacts");
  mkdirSync(destination, { recursive: true });
  writeFileSync(join(destination, "theme.css"), css);
  writeFileSync(join(destination, "manifest.json"), manifest);
  log(`sync → ${destination}`);
}

function dev() {
  tokens();
  bundleCSS({ minify: false, watch: true });
  log("watching src/ + build.ts ...");
  const watcher = watch([join(ROOT, "src"), join(ROOT, "build.ts")], {
    ignoreInitial: true,
    ignored: (p) => p.endsWith(TOKENS_OUT),
    awaitWriteFinish: { stabilityThreshold: 50, pollInterval: 10 },
  });
  watcher.on("all", (_event, path) => {
    if (path.endsWith(".ts")) tokens();
    bundleCSS({ minify: false, watch: true });
  });
}

function log(msg: string) {
  console.log(`[${time()}] ${msg}`);
}
function error(label: string, msg: string) {
  console.error(`[${time()}] ✗ ${label}: ${msg}`);
}
function time() {
  return new Date().toLocaleTimeString();
}

const USAGE = "bun build.ts <tokens|build|watch|sync|deploy> [--vault <path>]";
try {
  const { values, positionals } = parseArgs({
    args: process.argv.slice(2),
    options: { vault: { type: "string" } },
    allowPositionals: true,
    strict: true,
  });
  const command = positionals[0];
  if (positionals.length !== 1 || !["tokens", "build", "watch", "sync", "deploy"].includes(command!))
    throw new Error(`usage: ${USAGE}`);
  const deploys = command === "sync" || command === "deploy";
  if (deploys && !values.vault?.trim())
    throw new Error("sync/deploy requires --vault <path>; there is no default vault");
  if (!deploys && values.vault !== undefined)
    throw new Error("--vault is only supported by sync/deploy");
  // Validate the explicit destination before generating or writing anything.
  if (deploys) deploymentTarget(values.vault!);
  switch (command) {
    case "tokens": tokens(); break;
    case "build": build(); break;
    case "watch": dev(); break;
    case "sync": sync(values.vault!); break;
    case "deploy": build(); sync(values.vault!); break;
  }
} catch (cause) {
  error("command failed", (cause as Error).message);
  process.exitCode = 1;
}
