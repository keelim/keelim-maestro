import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, existsSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const helper = fileURLToPath(new URL('./local-automation.sh', import.meta.url));
const fixture = mkdtempSync(join(tmpdir(), 'automation-retirement-'));
const bin = join(fixture, 'bin');
const trace = join(fixture, 'retired-command-called');
mkdirSync(bin);

function executable(path, body) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `#!/bin/sh\nset -eu\n${body}\n`, { mode: 0o755 });
}

try {
  const initialized = spawnSync('git', ['init', '-q', fixture], { encoding: 'utf8' });
  assert.equal(initialized.status, 0, initialized.stderr);
  for (const command of ['kubectl', 'curl']) executable(join(bin, command), 'exit 0');
  executable(join(bin, 'lsof'), 'exit 1');
  executable(join(bin, 'gbrain'), 'touch "$AUTOMATION_TEST_TRACE"; exit 99');
  executable(join(fixture, 'tools/agentgateway/scripts/verify-k8s-gateway.sh'), 'exit 0');
  const env = {
    ...process.env,
    PATH: `${bin}:${process.env.PATH ?? ''}`,
    AUTOMATION_TEST_TRACE: trace
  };
  const run = (...args) => spawnSync('sh', [helper, ...args], {
    cwd: fixture, env, encoding: 'utf8'
  });

  const listed = run('list');
  assert.equal(listed.status, 0, listed.stderr);
  for (const owner of ['rich local Kubernetes', 'youtube n8n Kubernetes', 'agentgateway MCP Kubernetes']) {
    assert.ok(listed.stdout.includes(owner), owner);
  }
  assert.doesNotMatch(listed.stdout, /gbrain/i);

  for (const action of ['status', 'verify']) {
    const result = run(action);
    assert.equal(result.status, 0, `${action}: ${result.stdout}\n${result.stderr}`);
  }
  assert.equal(existsSync(trace), false, 'default inspection must not invoke a retired CLI');

  for (const action of ['list', 'status', 'verify', 'start', 'stop', 'standby']) {
    const rejected = run(action, 'gbrain');
    assert.equal(rejected.status, 1, `${action} accepted the retired target`);
  }
  assert.equal(existsSync(trace), false, 'rejected targets must not dispatch a retired CLI');
  console.log('Local automation retirement contract passed (remaining targets retained; no retired CLI invoked).');
} finally {
  rmSync(fixture, { recursive: true, force: true });
}
