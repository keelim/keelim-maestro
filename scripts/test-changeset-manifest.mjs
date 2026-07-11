#!/usr/bin/env node

import assert from 'node:assert/strict';
import {
  appendFileSync,
  mkdirSync,
  mkdtempSync,
  symlinkSync,
  writeFileSync
} from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const validator = new URL('./validate-changeset-manifest.mjs', import.meta.url).pathname;
const workspace = mkdtempSync(join(tmpdir(), 'changeset-manifest-'));
const repo = join(workspace, 'alpha');
mkdirSync(join(repo, 'scripts'), { recursive: true });
writeFileSync(
  join(repo, 'package.json'),
  `${JSON.stringify({ scripts: { check: 'node --check index.mjs' } }, null, 2)}\n`
);
writeFileSync(join(repo, 'index.mjs'), 'export const value = 1;\n');
writeFileSync(join(repo, 'scripts', 'verify.sh'), '#!/bin/sh\nexit 0\n');

function git(...args) {
  const result = spawnSync('git', args, { cwd: repo, encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  return result.stdout.trim();
}

git('init', '-q');
git('add', '.');
git(
  '-c',
  'user.name=Manifest Test',
  '-c',
  'user.email=manifest@example.invalid',
  '-c',
  'commit.gpgsign=false',
  'commit',
  '-qm',
  'fixture'
);
const commit = git('rev-parse', 'HEAD');
const manifestPath = join(workspace, 'changeset.json');

function writeManifest(change) {
  writeFileSync(
    manifestPath,
    `${JSON.stringify({ version: 1, changes: [change] }, null, 2)}\n`
  );
}

function validate() {
  return spawnSync(process.execPath, [validator, '--workspace', workspace, manifestPath], {
    encoding: 'utf8'
  });
}

const validChange = {
  repo: 'alpha',
  commit,
  requiredChecks: ['bun run check', 'sh scripts/verify.sh'],
  order: 1,
  rollback: `git revert ${commit}`
};

writeManifest(validChange);
let result = validate();
assert.equal(result.status, 0, result.stderr);
assert.match(result.stdout, /OK \(1 repo/);
assert.equal(git('rev-parse', 'HEAD'), commit, 'validation must not change HEAD');
assert.equal(git('status', '--porcelain'), '', 'validation must not dirty a repo');

appendFileSync(join(repo, 'index.mjs'), 'export const dirty = true;\n');
result = validate();
assert.equal(result.status, 1);
assert.match(result.stderr, /working tree is not clean/);
git('restore', 'index.mjs');

writeManifest({ ...validChange, order: 2, requiredChecks: ['bun run missing'] });
result = validate();
assert.equal(result.status, 1);
assert.match(result.stderr, /orders must be contiguous/);
assert.match(result.stderr, /package script does not exist: missing/);

const outsideRepo = mkdtempSync(join(tmpdir(), 'changeset-external-'));
writeFileSync(join(outsideRepo, 'index.mjs'), 'export const outside = true;\n');
function outsideGit(...args) {
  const command = spawnSync('git', args, { cwd: outsideRepo, encoding: 'utf8' });
  assert.equal(command.status, 0, command.stderr);
  return command.stdout.trim();
}
outsideGit('init', '-q');
outsideGit('add', '.');
outsideGit(
  '-c',
  'user.name=Manifest Test',
  '-c',
  'user.email=manifest@example.invalid',
  '-c',
  'commit.gpgsign=false',
  'commit',
  '-qm',
  'external fixture'
);
symlinkSync(outsideRepo, join(workspace, 'escape'), 'dir');
writeManifest({
  ...validChange,
  repo: 'escape',
  commit: outsideGit('rev-parse', 'HEAD'),
  requiredChecks: ['git status']
});
result = validate();
assert.equal(result.status, 1);
assert.match(result.stderr, /must resolve inside the workspace/);

writeFileSync(join(workspace, 'outside-check.sh'), '#!/bin/sh\nexit 0\n');
writeManifest({ ...validChange, requiredChecks: ['sh ../outside-check.sh'] });
result = validate();
assert.equal(result.status, 1);
assert.match(result.stderr, /check target must stay inside the repo/);

console.log('[test-changeset-manifest] 5 scenarios passed');
