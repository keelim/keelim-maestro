#!/usr/bin/env node
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = new Set(process.argv.slice(2));
const checkMode = args.has('--check');
const jsonMode = args.has('--json');
const archivedRepos = new Set(['toto']);

function main() {
  const repos = discoverRepos();
  const observations = repos.flatMap(readRepoVersions);
  const grouped = groupByPackage(observations);
  const shared = [...grouped.entries()]
    .map(([name, items]) => summarizePackage(name, items))
    .filter((row) => row.repoCount > 1)
    .sort((a, b) => statusRank(a.status) - statusRank(b.status) || a.name.localeCompare(b.name));
  const visibleRows = checkMode ? shared.filter((row) => row.status !== 'aligned') : shared;

  if (jsonMode) {
    console.log(JSON.stringify({ repos: repos.map((repo) => repo.name), rows: visibleRows }, null, 2));
    process.exit(0);
  }

  console.log('[dep-freshness] local lockfile version radar');
  console.log(`[dep-freshness] repos scanned: ${repos.map((repo) => repo.name).join(', ')}`);
  console.log(`[dep-freshness] shared packages: ${shared.length}`);
  console.log(`[dep-freshness] mismatches: ${shared.filter((row) => row.status !== 'aligned').length}`);

  if (visibleRows.length === 0) {
    console.log(checkMode ? 'No repo-to-repo version mismatches found.' : 'No shared package versions found.');
    process.exit(0);
  }

  printTable(
    ['Package', 'Status', 'Versions by repo'],
    visibleRows.map((row) => [
      row.name,
      row.status,
      row.versions.map((version) => `${version.version}: ${version.repos.join(', ')}`).join('; ')
    ])
  );

  process.exit(0);
}

function discoverRepos() {
  const childRepos = readdirSync(repoRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .filter((entry) => !entry.name.startsWith('.') && !archivedRepos.has(entry.name))
    .map((entry) => ({ name: entry.name, path: join(repoRoot, entry.name) }))
    .filter((entry) => existsSync(join(entry.path, '.git')))
    .sort((a, b) => a.name.localeCompare(b.name));

  return [{ name: 'root', path: repoRoot }, ...childRepos];
}

function readRepoVersions(repo) {
  const observations = [];

  for (const lockfile of findLockfiles(repo.path)) {
    const rel = relative(repo.path, lockfile);
    const text = readFileSync(lockfile, 'utf8');
    if (rel.endsWith('bun.lock')) {
      observations.push(...parseBunLock(text, repo.name, rel));
    } else if (rel.endsWith('uv.lock')) {
      observations.push(...parseUvLock(text, repo.name, rel));
    } else if (rel.endsWith('libs.versions.toml')) {
      observations.push(...parseGradleVersions(text, repo.name, rel));
    }
  }

  return observations;
}

function findLockfiles(repoPath) {
  const names = ['bun.lock', 'uv.lock', 'gradle/libs.versions.toml', 'libs.versions.toml'];
  return names.map((name) => join(repoPath, name)).filter((path) => existsSync(path));
}

function parseBunLock(text, repo, source) {
  const observations = [];
  const packageEntry = /^ {4}"([^"]+)": \["([^"]+?)"/gm;
  let match;

  while ((match = packageEntry.exec(text)) !== null) {
    const name = match[1];
    const descriptor = match[2];
    const version = versionFromDescriptor(name, descriptor);
    if (version) observations.push({ manager: 'bun', name, version, repo, source });
  }

  return dedupeObservations(observations);
}

function versionFromDescriptor(name, descriptor) {
  if (descriptor.startsWith(`${name}@`)) {
    const version = descriptor.slice(name.length + 1);
    if (isVersionLike(version)) return normalizeVersion(version);
  }

  const splitAt = descriptor.lastIndexOf('@');
  if (splitAt > 0) {
    const version = descriptor.slice(splitAt + 1);
    if (isVersionLike(version)) return normalizeVersion(version);
  }

  return null;
}

function parseUvLock(text, repo, source) {
  const observations = [];
  const packageBlocks = text.split(/\n\[\[package\]\]\n/g).slice(1);

  for (const block of packageBlocks) {
    const name = block.match(/^name = "([^"]+)"/m)?.[1];
    const version = block.match(/^version = "([^"]+)"/m)?.[1];
    if (name && version) observations.push({ manager: 'uv', name: `pypi:${name}`, version, repo, source });
  }

  return dedupeObservations(observations);
}

function parseGradleVersions(text, repo, source) {
  const observations = [];
  const versionsBlock = text.match(/\[versions\]([\s\S]*?)(?:\n\[|$)/)?.[1] ?? '';
  const versionByAlias = new Map();
  for (const match of versionsBlock.matchAll(/^([A-Za-z0-9_.-]+)\s*=\s*"([^"]+)"/gm)) {
    versionByAlias.set(match[1], match[2]);
  }

  const librariesBlock = text.match(/\[libraries\]([\s\S]*?)(?:\n\[|$)/)?.[1] ?? '';
  for (const line of librariesBlock.split('\n')) {
    const alias = line.match(/^([A-Za-z0-9_.-]+)\s*=/)?.[1];
    if (!alias) continue;

    const group = line.match(/group\s*=\s*"([^"]+)"/)?.[1];
    const name = line.match(/name\s*=\s*"([^"]+)"/)?.[1];
    const inlineVersion = line.match(/version\s*=\s*"([^"]+)"/)?.[1];
    const versionRef = line.match(/version\.ref\s*=\s*"([^"]+)"/)?.[1];
    const version = inlineVersion ?? (versionRef ? versionByAlias.get(versionRef) : null);

    if (group && name && version) {
      observations.push({ manager: 'gradle', name: `maven:${group}:${name}`, version, repo, source });
    } else if (versionByAlias.has(alias)) {
      observations.push({ manager: 'gradle', name: `gradle:${alias}`, version: versionByAlias.get(alias), repo, source });
    }
  }

  return dedupeObservations(observations);
}

function groupByPackage(observations) {
  const grouped = new Map();
  for (const observation of observations) {
    const rows = grouped.get(observation.name) ?? [];
    rows.push(observation);
    grouped.set(observation.name, rows);
  }
  return grouped;
}

function summarizePackage(name, observations) {
  const byRepo = new Map();
  for (const observation of observations) {
    byRepo.set(observation.repo, observation.version);
  }

  const byVersion = new Map();
  for (const [repo, version] of byRepo.entries()) {
    const repos = byVersion.get(version) ?? [];
    repos.push(repo);
    byVersion.set(version, repos);
  }

  const versions = [...byVersion.entries()]
    .map(([version, repos]) => ({ version, repos: repos.sort() }))
    .sort((a, b) => compareVersionText(a.version, b.version));
  const majors = new Set(versions.map((entry) => semverMajor(entry.version)).filter((major) => major !== null));
  const status = versions.length === 1 ? 'aligned' : majors.size > 1 ? 'major-lag' : 'mismatch';

  return {
    name,
    status,
    repoCount: byRepo.size,
    versions
  };
}

function dedupeObservations(observations) {
  const seen = new Set();
  return observations.filter((observation) => {
    const key = `${observation.repo}\0${observation.source}\0${observation.name}\0${observation.version}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function isVersionLike(version) {
  return /^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$/.test(version);
}

function normalizeVersion(version) {
  return version.replace(/^\^|^~/, '');
}

function semverMajor(version) {
  const match = version.match(/^(\d+)\./);
  return match ? Number(match[1]) : null;
}

function compareVersionText(a, b) {
  return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
}

function statusRank(status) {
  return { 'major-lag': 0, mismatch: 1, aligned: 2 }[status] ?? 3;
}

function printTable(headers, rows) {
  const widths = headers.map((header, column) =>
    Math.min(96, Math.max(header.length, ...rows.map((row) => String(row[column]).length)))
  );
  const renderCell = (value, index) => {
    const text = String(value);
    const clipped = text.length > widths[index] ? `${text.slice(0, widths[index] - 3)}...` : text;
    return clipped.padEnd(widths[index]);
  };
  const render = (cells) => `| ${cells.map(renderCell).join(' | ')} |`;
  console.log(render(headers));
  console.log(render(widths.map((width) => '-'.repeat(width))));
  for (const row of rows) console.log(render(row));
}

main();
