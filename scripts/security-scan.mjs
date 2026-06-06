#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { basename, dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = new Set(process.argv.slice(2));
const reportMode = args.has('--report') || args.has('--json');
const jsonMode = args.has('--json');
const maxFileBytes = 1024 * 1024;
const archivedRepos = new Set(['toto']);
const skipPathParts = new Set([
  '.git',
  '.next',
  '.turbo',
  '.venv',
  'build',
  'coverage',
  'dist',
  'node_modules',
  'out'
]);

const secretPatterns = [
  {
    id: 'private-key-block',
    severity: 'critical',
    regex: /-----BEGIN (?:RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----/g,
    valueIndex: 0
  },
  {
    id: 'aws-secret-access-key',
    severity: 'high',
    regex: /\b(?:AWS_SECRET_ACCESS_KEY|aws_secret_access_key)\b\s*[:=]\s*["']?([A-Za-z0-9/+=]{40})["']?/g,
    valueIndex: 1
  },
  {
    id: 'github-token',
    severity: 'high',
    regex: /\b(gh[pousr]_[A-Za-z0-9_]{36,255})\b/g,
    valueIndex: 1
  },
  {
    id: 'openai-api-key',
    severity: 'high',
    regex: /\b(sk-(?:proj-|admin-)?[A-Za-z0-9_-]{32,})\b/g,
    valueIndex: 1
  },
  {
    id: 'google-api-key',
    severity: 'high',
    regex: /\b(AIza[0-9A-Za-z_-]{35})\b/g,
    valueIndex: 1
  },
  {
    id: 'slack-token',
    severity: 'high',
    regex: /\b(xox[abprs]-[0-9A-Za-z-]{20,})\b/g,
    valueIndex: 1
  },
  {
    id: 'jwt-secret-assignment',
    severity: 'high',
    regex: /\b(?:JWT_SECRET|SUPABASE_SERVICE_ROLE_KEY|SERVICE_ROLE_KEY|SESSION_SECRET)\b\s*[:=]\s*["']?([A-Za-z0-9_.-]{32,})["']?/g,
    valueIndex: 1
  },
  {
    id: 'generic-secret-assignment',
    severity: 'medium',
    regex: /(?:^|[\s{,'"])([A-Z0-9_]*(?:API[_-]?KEY|SECRET|TOKEN|PASSWORD|PASSWD|PRIVATE[_-]?KEY|CREDENTIAL)[A-Z0-9_]*)\b\s*(?:=\s*|:\s+)["']?([^"'\s#;,]{24,})["']?/gi,
    valueIndex: 2,
    validate: (value) => looksLikeRealSecret(value)
  }
];

function main() {
  const repos = discoverChildRepos();
  const findings = [];
  const scanned = [];

  for (const repo of repos) {
    const files = listGitVisibleFiles(repo.path);
    scanned.push({ repo: repo.name, files: files.length });

    for (const file of files) {
      const filePath = join(repo.path, file);
      if (shouldSkipPath(file) || !isTextFile(filePath)) continue;

      const text = readFileSync(filePath, 'utf8');
      const lines = text.split(/\r?\n/);

      for (let index = 0; index < lines.length; index += 1) {
        const line = lines[index];
        for (const pattern of secretPatterns) {
          pattern.regex.lastIndex = 0;
          let match;
          while ((match = pattern.regex.exec(line)) !== null) {
            const value = match[pattern.valueIndex] ?? match[0];
            if (isIgnoredValue(value) || (pattern.validate && !pattern.validate(value))) {
              continue;
            }
            findings.push({
              repo: repo.name,
              severity: pattern.severity,
              finding: pattern.id,
              location: `${file}:${index + 1}`,
              secret: maskSecret(value),
              excerpt: maskLine(line, value)
            });
          }
        }
      }
    }
  }

  if (jsonMode) {
    console.log(JSON.stringify({ scanned, findings }, null, 2));
  } else {
    printReport(scanned, findings, reportMode);
  }

  process.exit(findings.length === 0 ? 0 : 1);
}

function discoverChildRepos() {
  return readdirSync(repoRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .filter((entry) => !entry.name.startsWith('.') && !archivedRepos.has(entry.name))
    .map((entry) => ({ name: entry.name, path: join(repoRoot, entry.name) }))
    .filter((entry) => existsSync(join(entry.path, '.git')))
    .sort((a, b) => a.name.localeCompare(b.name));
}

function listGitVisibleFiles(repoPath) {
  const result = spawnSync('git', ['ls-files', '--cached', '--others', '--exclude-standard', '-z'], {
    cwd: repoPath,
    encoding: 'buffer'
  });

  if (result.status !== 0) {
    const stderr = result.stderr.toString('utf8').trim();
    throw new Error(`git ls-files failed in ${relative(repoRoot, repoPath)}: ${stderr}`);
  }

  return result.stdout
    .toString('utf8')
    .split('\0')
    .filter(Boolean);
}

function shouldSkipPath(file) {
  if (basename(file) === '.gitignore') return true;
  return file.split('/').some((part) => skipPathParts.has(part));
}

function isTextFile(filePath) {
  const stats = statSync(filePath);
  if (!stats.isFile() || stats.size > maxFileBytes) return false;
  if (stats.size === 0) return true;

  const sample = readFileSync(filePath).subarray(0, Math.min(stats.size, 4096));
  if (sample.includes(0)) return false;

  let control = 0;
  for (const byte of sample) {
    if (byte < 7 || (byte > 13 && byte < 32)) control += 1;
  }
  return control / sample.length < 0.05;
}

function looksLikeRealSecret(value) {
  const normalized = value.trim();
  if (normalized.length < 24) return false;
  if (!/[A-Za-z]/.test(normalized) || !/[0-9]/.test(normalized)) return false;
  if (shannonEntropy(normalized) < 3.35) return false;
  return true;
}

function shannonEntropy(value) {
  const counts = new Map();
  for (const char of value) counts.set(char, (counts.get(char) ?? 0) + 1);
  let entropy = 0;
  for (const count of counts.values()) {
    const p = count / value.length;
    entropy -= p * Math.log2(p);
  }
  return entropy;
}

function isIgnoredValue(value) {
  const lower = value.toLowerCase();
  return (
    lower.includes('example') ||
    lower.includes('placeholder') ||
    lower.includes('your_') ||
    lower.includes('changeme') ||
    lower.includes('dummy') ||
    lower.includes('fake') ||
    lower.includes('test') ||
    lower.includes('process.env') ||
    lower.includes('${') ||
    /^[x*_ -]+$/i.test(value)
  );
}

function maskSecret(value) {
  if (value.length <= 8) return '***';
  const head = value.slice(0, 4);
  const tail = value.slice(-4);
  return `${head}...${tail}`;
}

function maskLine(line, value) {
  const masked = line.replace(value, maskSecret(value)).trim();
  return masked.length <= 160 ? masked : `${masked.slice(0, 157)}...`;
}

function printReport(scanned, findings, verbose) {
  console.log('[security-scan] local child repo secret scan');
  console.log(`[security-scan] repos scanned: ${scanned.length}`);
  for (const item of scanned) {
    console.log(`  - ${item.repo}: ${item.files} git-visible files`);
  }
  console.log(`[security-scan] findings: ${findings.length}`);

  if (!verbose && findings.length === 0) return;

  if (findings.length === 0) {
    console.log('\nNo secret-like findings detected.');
    return;
  }

  printTable(
    ['Repo', 'Severity', 'Finding', 'Location', 'Masked secret', 'Excerpt'],
    findings.map((finding) => [
      finding.repo,
      finding.severity,
      finding.finding,
      finding.location,
      finding.secret,
      finding.excerpt
    ])
  );
}

function printTable(headers, rows) {
  const widths = headers.map((header, column) =>
    Math.max(header.length, ...rows.map((row) => String(row[column]).length))
  );
  const render = (cells) =>
    `| ${cells.map((cell, index) => String(cell).padEnd(widths[index])).join(' | ')} |`;
  console.log(render(headers));
  console.log(render(widths.map((width) => '-'.repeat(width))));
  for (const row of rows) console.log(render(row));
}

main();
