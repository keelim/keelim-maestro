#!/usr/bin/env node
/**
 * Validate a read-only, ordered cross-repository changeset manifest.
 *
 * This command inspects repository state and required-check declarations. It
 * never checks out commits, runs checks, executes rollback text, pushes, or
 * updates root pointers.
 */

import { constants, accessSync, existsSync, readFileSync, realpathSync } from 'node:fs';
import { delimiter, isAbsolute, join, relative, resolve, sep } from 'node:path';
import { spawnSync } from 'node:child_process';

const ENTRY_FIELDS = new Set(['repo', 'commit', 'requiredChecks', 'order', 'rollback']);
const TOP_LEVEL_FIELDS = new Set(['version', 'changes']);

function usage() {
  console.log(
    'Usage: bun scripts/validate-changeset-manifest.mjs [--workspace path] manifest.json'
  );
}

function parseArgs(argv) {
  let workspace = process.cwd();
  let manifestPath = null;
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--workspace') {
      if (!argv[index + 1]) throw new Error('--workspace requires a path');
      workspace = resolve(argv[index + 1]);
      index += 1;
    } else if (arg === '-h' || arg === '--help') {
      usage();
      process.exit(0);
    } else if (arg.startsWith('-')) {
      throw new Error(`unknown option: ${arg}`);
    } else if (manifestPath) {
      throw new Error('exactly one manifest path is required');
    } else {
      manifestPath = resolve(arg);
    }
  }
  if (!manifestPath) throw new Error('manifest path is required');
  return { workspace, manifestPath };
}

function runGit(repoPath, args) {
  return spawnSync('git', ['-C', repoPath, ...args], { encoding: 'utf8' });
}

function resolvesInside(basePath, candidatePath) {
  try {
    const fromBase = relative(realpathSync(basePath), realpathSync(candidatePath));
    const escapesBase = fromBase === '..' || fromBase.startsWith(`..${sep}`);
    return !escapesBase && !isAbsolute(fromBase);
  } catch {
    return false;
  }
}

function commandExists(command) {
  if (command.includes('/')) return false;
  for (const directory of (process.env.PATH || '').split(delimiter)) {
    if (!directory) continue;
    try {
      accessSync(join(directory, command), constants.X_OK);
      return true;
    } catch {
      // Keep looking through PATH.
    }
  }
  return false;
}

function tokenizeCheck(command) {
  if (/[\n\r;&|><`]/.test(command) || command.includes('$(')) return null;
  const tokens = [];
  let token = '';
  let quote = null;
  for (const character of command.trim()) {
    if (quote) {
      if (character === quote) quote = null;
      else token += character;
    } else if (character === '"' || character === "'") {
      quote = character;
    } else if (/\s/.test(character)) {
      if (token) {
        tokens.push(token);
        token = '';
      }
    } else {
      token += character;
    }
  }
  if (quote) return null;
  if (token) tokens.push(token);
  return tokens;
}

function packageScripts(repoPath) {
  const packagePath = join(repoPath, 'package.json');
  if (!existsSync(packagePath)) return {};
  try {
    const value = JSON.parse(readFileSync(packagePath, 'utf8'));
    return value.scripts && typeof value.scripts === 'object' ? value.scripts : {};
  } catch {
    return {};
  }
}

function validateCheckCommand(command, repoPath) {
  const tokens = tokenizeCheck(command);
  if (!tokens || tokens.length === 0) return 'must be a simple command without shell operators';

  const executable = tokens[0];
  if (executable.startsWith('./')) {
    const target = resolve(repoPath, executable);
    if (!existsSync(target)) return `command path does not exist: ${executable}`;
    return resolvesInside(repoPath, target) ? null : 'check target must stay inside the repo';
  }
  if (!commandExists(executable)) return `command is not available on PATH: ${executable}`;

  if (['bun', 'npm', 'pnpm'].includes(executable) && tokens[1] === 'run') {
    const script = tokens[2];
    if (!script) return `${executable} run requires a package script name`;
    if (!(script in packageScripts(repoPath))) return `package script does not exist: ${script}`;
  }

  if (['sh', 'bash', 'node', 'python', 'python3'].includes(executable)) {
    const candidate = tokens.slice(1).find((token) => !token.startsWith('-'));
    if (candidate && (candidate.includes('/') || /\.(?:sh|mjs|cjs|js|py)$/.test(candidate))) {
      const target = resolve(repoPath, candidate);
      if (isAbsolute(candidate)) {
        return 'check target must stay inside the repo';
      }
      if (!existsSync(target)) {
        return `check target does not exist in repo: ${candidate}`;
      }
      if (!resolvesInside(repoPath, target)) {
        return 'check target must stay inside the repo';
      }
    }
  }
  return null;
}

function repoPathFor(workspace, repo) {
  if (typeof repo !== 'string' || !repo.trim() || isAbsolute(repo)) return null;
  const path = resolve(workspace, repo);
  const fromWorkspace = relative(workspace, path);
  if (
    fromWorkspace === '..' ||
    fromWorkspace.startsWith(`..${sep}`) ||
    isAbsolute(fromWorkspace)
  ) {
    return null;
  }
  if (existsSync(path) && !resolvesInside(workspace, path)) return null;
  return path;
}

function validateEntry(entry, index, workspace) {
  const label = `changes[${index}]`;
  const errors = [];
  if (!entry || typeof entry !== 'object' || Array.isArray(entry)) {
    return { errors: [`${label} must be an object`], repo: null, order: null };
  }
  for (const field of Object.keys(entry)) {
    if (!ENTRY_FIELDS.has(field)) errors.push(`${label} has unknown field: ${field}`);
  }
  for (const field of ENTRY_FIELDS) {
    if (!(field in entry)) errors.push(`${label} missing field: ${field}`);
  }

  const repoPath = repoPathFor(workspace, entry.repo);
  if (!repoPath) {
    errors.push(`${label}.repo must resolve inside the workspace from a relative path`);
  }
  else if (!existsSync(repoPath)) errors.push(`${label}.repo does not exist: ${entry.repo}`);

  if (typeof entry.commit !== 'string' || !/^[0-9a-f]{40}$/.test(entry.commit)) {
    errors.push(`${label}.commit must be a full 40-character lowercase Git SHA`);
  }
  if (!Number.isInteger(entry.order) || entry.order < 1) {
    errors.push(`${label}.order must be a positive integer`);
  }
  if (typeof entry.rollback !== 'string' || !entry.rollback.trim()) {
    errors.push(`${label}.rollback must be a non-empty operator instruction`);
  }
  if (!Array.isArray(entry.requiredChecks) || entry.requiredChecks.length === 0) {
    errors.push(`${label}.requiredChecks must be a non-empty array`);
  } else {
    const seen = new Set();
    for (const check of entry.requiredChecks) {
      if (typeof check !== 'string' || !check.trim()) {
        errors.push(`${label}.requiredChecks entries must be non-empty strings`);
        continue;
      }
      if (seen.has(check)) errors.push(`${label}.requiredChecks duplicates: ${check}`);
      seen.add(check);
      if (repoPath && existsSync(repoPath)) {
        const commandError = validateCheckCommand(check, repoPath);
        if (commandError) errors.push(`${label}.requiredChecks ${commandError}`);
      }
    }
  }

  if (repoPath && existsSync(repoPath)) {
    const topLevel = runGit(repoPath, ['rev-parse', '--show-toplevel']);
    if (
      topLevel.status !== 0 ||
      realpathSync(topLevel.stdout.trim()) !== realpathSync(repoPath)
    ) {
      errors.push(`${label}.repo is not an autonomous Git repository root: ${entry.repo}`);
    } else {
      const status = runGit(repoPath, ['status', '--porcelain=v1', '--untracked-files=normal']);
      if (status.status !== 0) errors.push(`${label}.repo status could not be read`);
      else if (status.stdout.trim()) errors.push(`${label}.repo working tree is not clean: ${entry.repo}`);

      if (typeof entry.commit === 'string' && /^[0-9a-f]{40}$/.test(entry.commit)) {
        const exists = runGit(repoPath, ['cat-file', '-e', `${entry.commit}^{commit}`]);
        if (exists.status !== 0) errors.push(`${label}.commit is not present in ${entry.repo}`);
        const head = runGit(repoPath, ['rev-parse', 'HEAD']);
        if (head.status !== 0 || head.stdout.trim() !== entry.commit) {
          errors.push(`${label}.commit does not match ${entry.repo} HEAD`);
        }
      }
    }
  }
  return { errors, repo: entry.repo, order: entry.order };
}

function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(`[changeset] ${error.message}`);
    usage();
    return 2;
  }

  let manifest;
  try {
    manifest = JSON.parse(readFileSync(args.manifestPath, 'utf8'));
  } catch (error) {
    console.error(`[changeset] cannot read manifest: ${error.message}`);
    return 1;
  }
  const errors = [];
  if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest)) {
    errors.push('manifest must be an object');
    manifest = {};
  }
  for (const field of Object.keys(manifest)) {
    if (!TOP_LEVEL_FIELDS.has(field)) errors.push(`manifest has unknown field: ${field}`);
  }
  if (manifest.version !== 1) errors.push('manifest.version must equal 1');
  if (!Array.isArray(manifest.changes) || manifest.changes.length === 0) {
    errors.push('manifest.changes must be a non-empty array');
  }

  const results = Array.isArray(manifest.changes)
    ? manifest.changes.map((entry, index) => validateEntry(entry, index, args.workspace))
    : [];
  for (const result of results) errors.push(...result.errors);

  const repos = results.map((result) => result.repo).filter(Boolean);
  if (new Set(repos).size !== repos.length) errors.push('manifest repo values must be unique');
  const orders = results.map((result) => result.order).filter(Number.isInteger);
  if (new Set(orders).size !== orders.length) errors.push('manifest order values must be unique');
  const expectedOrders = Array.from({ length: results.length }, (_, index) => index + 1);
  if (orders.length !== results.length || orders.slice().sort((a, b) => a - b).some((v, i) => v !== expectedOrders[i])) {
    errors.push(`manifest orders must be contiguous from 1 to ${results.length}`);
  }

  if (errors.length) {
    for (const error of errors) console.error(`[changeset] FAIL: ${error}`);
    return 1;
  }
  console.log(
    `[changeset] OK (${results.length} repo${results.length === 1 ? '' : 's'}; inspection only, no checks executed)`
  );
  return 0;
}

process.exitCode = main();
