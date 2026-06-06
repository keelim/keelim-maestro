#!/usr/bin/env node
import { spawn } from 'node:child_process';
import { existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const rootDir = process.cwd();
const SUMMARY_FLAG = '--summary';
const TIMEOUT_MS = 8000;
const ARCHIVED_REPOS = new Set(['toto']);

const args = new Set(process.argv.slice(2));
if (!args.has(SUMMARY_FLAG)) {
  console.log('Usage: node scripts/dep-audit.mjs --summary');
}

const repos = discoverRepos(rootDir);
const results = [];

for (const repo of repos) {
  if (existsSync(join(repo.path, 'package.json'))) {
    results.push(await runJsAudit(repo));
  }
  if (existsSync(join(repo.path, 'uv.lock')) || existsSync(join(repo.path, 'pyproject.toml'))) {
    results.push(await runPythonAudit(repo));
  }
}

printSummary(results);
process.exit(0);

function discoverRepos(root) {
  const entries = [
    {
      name: 'root',
      path: root
    },
    ...readdirSync(root, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .filter((entry) => !entry.name.startsWith('.') && !ARCHIVED_REPOS.has(entry.name))
      .map((entry) => ({
        name: entry.name,
        path: join(root, entry.name)
      }))
      .filter((entry) => existsSync(join(entry.path, '.git')))
  ];

  return entries.filter(
    (entry) =>
      existsSync(join(entry.path, 'package.json')) ||
      existsSync(join(entry.path, 'uv.lock')) ||
      existsSync(join(entry.path, 'pyproject.toml'))
  );
}

async function runJsAudit(repo) {
  const result = await runCommand('bun', ['audit', '--json'], repo.path);
  return formatAuditResult(repo, 'js', 'bun audit --json', result);
}

async function runPythonAudit(repo) {
  const availability = await runCommand('python3', ['-m', 'pip_audit', '--version'], repo.path);
  if (availability.exitCode !== 0) {
    return {
      repo: repo.name,
      ecosystem: 'python',
      command: 'python3 -m pip_audit',
      status: 'skipped',
      vulnerabilities: 0,
      reason: 'pip-audit is not available locally'
    };
  }

  const result = await runCommand(
    'python3',
    ['-m', 'pip_audit', '--format=json'],
    repo.path
  );
  return formatAuditResult(repo, 'python', 'python3 -m pip_audit --format=json', result);
}

function formatAuditResult(repo, ecosystem, command, result) {
  if (result.timedOut) {
    return {
      repo: repo.name,
      ecosystem,
      command,
      status: 'skipped',
      vulnerabilities: 0,
      reason: `timed out after ${TIMEOUT_MS}ms`
    };
  }

  if (result.exitCode !== 0 && result.stdout.trim().length === 0) {
    return {
      repo: repo.name,
      ecosystem,
      command,
      status: 'skipped',
      vulnerabilities: 0,
      reason: summarizeFailure(result.stderr)
    };
  }

  const parsed = parseAuditJson(ecosystem, result.stdout);
  return {
    repo: repo.name,
    ecosystem,
    command,
    status: parsed.parseError ? 'skipped' : result.exitCode === 0 ? 'ok' : 'findings',
    vulnerabilities: parsed.vulnerabilities,
    reason: parsed.parseError ?? (result.exitCode === 0 ? 'no findings reported' : 'findings reported')
  };
}

function parseAuditJson(ecosystem, stdout) {
  try {
    const data = JSON.parse(stdout);
    if (ecosystem === 'js') {
      const advisories = Array.isArray(data.advisories)
        ? data.advisories.length
        : typeof data.vulnerabilities === 'object' && data.vulnerabilities !== null
          ? Object.keys(data.vulnerabilities).length
          : Number(data.metadata?.vulnerabilities?.total ?? 0);
      return {
        vulnerabilities: Number.isFinite(advisories) ? advisories : 0
      };
    }

    const dependencies = Array.isArray(data.dependencies) ? data.dependencies : [];
    return {
      vulnerabilities: dependencies.reduce(
        (count, dep) => count + (Array.isArray(dep.vulns) ? dep.vulns.length : 0),
        0
      )
    };
  } catch (error) {
    return {
      vulnerabilities: 0,
      parseError: `could not parse JSON output: ${error.message}`
    };
  }
}

function runCommand(command, commandArgs, cwd) {
  return new Promise((resolve) => {
    let stdout = '';
    let stderr = '';
    let settled = false;
    const child = spawn(command, commandArgs, {
      cwd,
      stdio: ['ignore', 'pipe', 'pipe']
    });
    const timer = setTimeout(() => {
      settled = true;
      child.kill('SIGTERM');
      resolve({ exitCode: null, stdout, stderr, timedOut: true });
    }, TIMEOUT_MS);

    child.stdout.on('data', (chunk) => {
      stdout += chunk;
    });
    child.stderr.on('data', (chunk) => {
      stderr += chunk;
    });
    child.on('error', (error) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({ exitCode: null, stdout, stderr: error.message, timedOut: false });
    });
    child.on('close', (exitCode) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({ exitCode, stdout, stderr, timedOut: false });
    });
  });
}

function printSummary(rows) {
  console.log('[dep-audit] dependency vulnerability audit summary');
  console.log(`[dep-audit] checks: ${rows.length}`);
  console.log('');
  console.log('| Repo | Ecosystem | Status | Vulnerabilities | Reason |');
  console.log('| ---- | --------- | ------ | --------------- | ------ |');
  for (const row of rows) {
    console.log(
      `| ${row.repo} | ${row.ecosystem} | ${row.status} | ${row.vulnerabilities} | ${escapeCell(row.reason)} |`
    );
  }
}

function summarizeFailure(stderr) {
  const line = stripAnsi(stderr)
    .split('\n')
    .map((item) => item.trim())
    .filter(Boolean)
    .find((item) => !/^bun audit v/i.test(item));
  if (!line || line.includes('".env"')) return 'audit command unavailable or network failed';
  return line;
}

function escapeCell(value) {
  return stripAnsi(String(value)).replace(/\|/g, '/');
}

function stripAnsi(value) {
  return value.replace(/\u001b\[[0-9;]*m/g, '');
}
