import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, copyFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const source = dirname(fileURLToPath(import.meta.url));
const fixture = mkdtempSync(join(tmpdir(), 'maestro-policy-'));
const env = { ...process.env, GIT_CONFIG_NOSYSTEM: '1', GIT_CONFIG_GLOBAL: '/dev/null' };
const git = (...args) => execFileSync('git', args, { cwd: fixture, env, encoding: 'utf8' });
const sh = (script, ...args) => execFileSync('sh', [join(fixture, 'scripts', script), ...args], {
  cwd: fixture, env, encoding: 'utf8',
});

try {
  git('init', '--quiet', '--initial-branch=main');
  mkdirSync(join(fixture, 'scripts'));
  for (const name of ['repository-policy.sh', 'update-subrepos.sh', 'report-trusted-baseline.sh']) {
    copyFileSync(join(source, name), join(fixture, 'scripts', name));
  }
  writeFileSync(join(fixture, '.gitmodules'), '');
  writeFileSync(join(fixture, 'package.json'), '{"workspaces":[\n"all-web-ui"\n]}\n');
  writeFileSync(join(fixture, 'pyproject.toml'), '[tool.uv.workspace]\nmembers = [\n"rich",\n]\n');
  for (const repo of ['rich', 'all-web-ui']) {
    mkdirSync(join(fixture, repo));
    git('-C', repo, 'init', '--quiet', '--initial-branch=main');
    git('-C', repo, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
      '-c', 'commit.gpgsign=false', 'commit', '--quiet', '--allow-empty', '-m', 'fixture');
  }
  writeFileSync(join(fixture, 'rich', 'local-work.txt'), 'uncommitted local work\n');
  const richRow = () => sh('report-trusted-baseline.sh').split('\n').find(line => line.startsWith('| `rich` |'));
  const row = richRow();
  assert.match(row, /local-only/);
  assert.match(row, /dirty/);
  assert.match(row, /\| no \| rich \|/);
  assert.match(row, /\| local-only \| none \|$/);
  assert.doesNotMatch(row, /no-origin-remote|no-upstream|dirty-working-tree/);
  assert.match(sh('update-subrepos.sh', 'status'), /^rich\s+.*remote=none policy=local-only$/m);
  assert.match(sh('update-subrepos.sh', 'dry-run'), /\[skip\] rich\s+local-only policy/);

  // Check a clean repository too: dirty-tree skipping must not mask the policy.
  writeFileSync(join(fixture, 'rich', '.git', 'info', 'exclude'), '/local-work.txt\n');
  assert.equal(git('-C', 'rich', 'status', '--porcelain'), '');
  // Reintroducing a URL must not silently reactivate synchronization.
  for (const repo of ['rich', 'all-web-ui']) {
    git('-C', repo, 'remote', 'add', 'origin', `https://github.com/example/${repo}.git`);
  }
  assert.match(richRow(), /unexpected-remote-on-local-only/);
  mkdirSync(join(fixture, 'bin'));
  env.POLICY_REAL_GIT = execFileSync('which', ['git'], { encoding: 'utf8' }).trim();
  env.POLICY_GIT_LOG = join(fixture, 'network-attempts.log');
  writeFileSync(join(fixture, 'bin', 'git'), `#!/bin/sh
for argument in "$@"; do
  case "$argument" in
    fetch|pull|push) printf '%s\\n' "$*" >> "$POLICY_GIT_LOG"; exit 0 ;;
  esac
done
exec "$POLICY_REAL_GIT" "$@"
`, { mode: 0o700 });
  env.PATH = `${join(fixture, 'bin')}:${env.PATH}`;
  const dry = sh('update-subrepos.sh', 'dry-run');
  assert.match(dry, /\[skip\] rich\s+local-only policy/);
  assert.match(dry, /\[dry-run\] all-web-ui\s+would fetch origin/);
  const update = sh('update-subrepos.sh', 'update');
  assert.match(update, /\[skip\] rich\s+local-only policy/);
  const networkAttempts = readFileSync(env.POLICY_GIT_LOG, 'utf8');
  assert.doesNotMatch(networkAttempts, /-C rich\s/);
  assert.match(networkAttempts, /-C all-web-ui fetch --prune origin/);
  assert.match(networkAttempts, /-C all-web-ui pull --ff-only origin main/);
  assert.equal(readFileSync(join(fixture, 'rich', 'local-work.txt'), 'utf8'), 'uncommitted local work\n');
  console.log('Repository policy tests passed (local work retained; Rich never synchronized; other repos unchanged).');
} finally {
  rmSync(fixture, { recursive: true, force: true });
}
