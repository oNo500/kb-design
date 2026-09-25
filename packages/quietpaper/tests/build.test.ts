import { afterEach, expect, test } from "bun:test";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, readlinkSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const packageRoot = resolve(import.meta.dir, "..");
const temporary: string[] = [];
afterEach(() => {
  for (const path of temporary.splice(0)) rmSync(path, { recursive: true, force: true });
});

function fixture() {
  const root = mkdtempSync(join(tmpdir(), "quietpaper-test-"));
  temporary.push(root);
  const source = join(root, "package");
  mkdirSync(source);
  for (const name of ["build.ts", "src", "theme"])
    cpSync(join(packageRoot, name), join(source, name), { recursive: true });
  symlinkSync(join(packageRoot, "node_modules"), join(source, "node_modules"), "dir");
  const vault = join(root, "vault with spaces");
  mkdirSync(join(vault, ".obsidian"), { recursive: true });
  writeFileSync(join(vault, "article.md"), "User article\n");
  writeFileSync(join(vault, ".obsidian", "appearance.json"), '{"cssTheme":"other"}\n');
  const run = (...args: string[]) => Bun.spawnSync({
    cmd: [process.execPath, join(source, "build.ts"), ...args],
    cwd: root,
    stdout: "pipe", stderr: "pipe",
  });
  return { root, source, vault, run };
}

function snapshot(root: string, prefix = ""): Record<string, string> {
  return Object.fromEntries(readdirSync(join(root, prefix), { withFileTypes: true }).flatMap(entry => {
    const name = join(prefix, entry.name);
    return entry.isSymbolicLink() ? [[name, `symlink:${readlinkSync(join(root, name))}`]]
      : entry.isDirectory() ? Object.entries(snapshot(root, name))
      : [[name, readFileSync(join(root, name)).toString("base64")]];
  }));
}

test("build from outside the package uses package inputs and stays inside the package", () => {
  const { root, source, vault, run } = fixture();
  const before = snapshot(vault);
  const result = run("build");
  expect(result.exitCode).toBe(0);
  expect(readFileSync(join(source, "theme/theme.css"), "utf8")).toContain("--ctp-");
  expect(existsSync(join(root, "theme"))).toBe(false);
  expect(existsSync(join(root, "src"))).toBe(false);
  expect(snapshot(vault)).toEqual(before);
});

test("sync and deploy reject missing or misspelled targets before any writes", () => {
  const { source, vault, run } = fixture();
  const before = snapshot(source);
  for (const args of [["sync"], ["deploy"], ["deploy", "--vaul", vault], ["sync", "--vault"]]) {
    expect(run(...args).exitCode).not.toBe(0);
    expect(snapshot(source)).toEqual(before);
  }
  expect(readdirSync(join(vault, ".obsidian"))).toEqual(["appearance.json"]);
});

test("deploy and sync write only the two theme files and preserve user content and selection", () => {
  const { source, vault, run } = fixture();
  const before = snapshot(vault);
  for (const command of ["deploy", "sync"]) {
    const result = run(command, "--vault", vault);
    expect(result.exitCode).toBe(0);
    const after = snapshot(vault);
    const expected = { ...before };
    for (const name of ["theme.css", "manifest.json"])
      expected[join(".obsidian/themes/quietpaper", name)] = readFileSync(join(source, "theme", name)).toString("base64");
    expect(after).toEqual(expected);
  }
});

test("nonexistent targets and directories without Obsidian configuration are rejected", () => {
  const { root, source, vault, run } = fixture();
  const before = snapshot(source);
  const missing = join(root, "missing");
  for (const target of [missing, root, join(vault, "article.md")])
    expect(run("deploy", "--vault", target).exitCode).not.toBe(0);
  expect(existsSync(missing)).toBe(false);
  expect(snapshot(source)).toEqual(before);
});

test("deployment rejects symbolic links that could redirect the write set", () => {
  for (const path of [".obsidian", ".obsidian/themes", ".obsidian/themes/quietpaper", ".obsidian/themes/quietpaper/theme.css", ".obsidian/themes/quietpaper/manifest.json"]) {
    const { root, vault, run } = fixture();
    const outside = join(root, "outside");
    const isFile = path.endsWith(".css") || path.endsWith(".json");
    if (isFile) writeFileSync(outside, "protected"); else mkdirSync(outside);
    const target = join(vault, path);
    rmSync(target, { recursive: true, force: true });
    mkdirSync(resolve(target, ".."), { recursive: true });
    symlinkSync(outside, target, isFile ? "file" : "dir");
    expect(run("deploy", "--vault", vault).exitCode).not.toBe(0);
    if (isFile) expect(readFileSync(outside, "utf8")).toBe("protected");
    else expect(readdirSync(outside)).toEqual([]);
  }
});

test("a failed build never deploys the previous CSS", () => {
  const { source, vault, run } = fixture();
  expect(run("deploy", "--vault", vault).exitCode).toBe(0);
  const before = snapshot(vault);
  writeFileSync(join(source, "src/theme.css"), '@import "missing-file.css";');
  expect(run("deploy", "--vault", vault).exitCode).not.toBe(0);
  expect(snapshot(vault)).toEqual(before);
});

test("missing build artifacts leave an existing theme untouched", () => {
  const { source, vault, run } = fixture();
  expect(run("deploy", "--vault", vault).exitCode).toBe(0);
  const before = snapshot(vault);
  rmSync(join(source, "theme/manifest.json"));
  expect(run("sync", "--vault", vault).exitCode).not.toBe(0);
  expect(snapshot(vault)).toEqual(before);
});
