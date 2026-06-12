#!/usr/bin/env python3
"""Generate a readable, interactive offline HTML viewer from improvements.json.

Unlike the block-model renderer (flat tables), this produces a browsable UI:
search, project/severity/dimension/effort filters, collapsible item cards.
Offline contract is preserved: no external resources, no network APIs,
restrictive CSP; forbidden literal tokens are broken with a zero-width space.
"""

from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BASE_DIR = REPO_ROOT / "docs" / "research" / "improvements-2026-06"
OUTPUT = REPO_ROOT / "docs" / "research" / "improvement-items-viewer-2026-06.html"

FORBIDDEN_TOKENS = ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "sendBeacon", "@import")
ZWSP = "​"

PROJECT_LABELS = {
    "all": "Kotlin Android 모노레포",
    "android-support": "Play Store GitHub Action",
    "Keelim-Knowledge-Vault": "Obsidian 지식 저장소",
    "keelim-plugin": "Claude Code 스킬 플러그인",
    "keelim-vercel": "Next.js 대시보드",
    "rich": "주식 정량분석 풀스택",
    "youtube": "영상 자동화 CLI",
    "all-web-ui": "공유 UI 라이브러리",
}


# The offline validator lowercases the HTML before its substring scan,
# so the match must be broken case-insensitively.
_FORBIDDEN_RE = re.compile(
    "|".join(re.escape(t) for t in FORBIDDEN_TOKENS), re.IGNORECASE
)


def sanitize(value: str) -> str:
    return _FORBIDDEN_RE.sub(lambda m: m.group(0)[:-1] + ZWSP + m.group(0)[-1], value)


def h(value: str) -> str:
    return escape(sanitize(value), quote=True)


CSS = """
:root { --p1:#d92d20; --p1-bg:#fee4e2; --p2:#b54708; --p2-bg:#fef0c7;
  --ink:#1f2430; --muted:#5f6b7a; --line:#e4e8ee; --bg:#f6f7f9; --card:#ffffff;
  --accent:#175cd3; --accent-bg:#eaf1fd; --mono:ui-monospace,SFMono-Regular,Menlo,monospace; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif; }
header { position:sticky; top:0; z-index:10; background:#fff; border-bottom:1px solid var(--line);
  padding:14px 20px 12px; box-shadow:0 1px 4px rgba(16,24,40,.05); }
h1 { margin:0 0 2px; font-size:1.25rem; }
.sub { color:var(--muted); font-size:.85rem; margin-bottom:10px; }
.controls { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
.controls input[type=search] { flex:1 1 240px; max-width:360px; padding:7px 12px;
  border:1px solid var(--line); border-radius:8px; font-size:.9rem; }
.chiprow { display:flex; flex-wrap:wrap; gap:6px; align-items:center; }
.chiplabel { font-size:.75rem; color:var(--muted); margin-right:2px; }
.chip { border:1px solid var(--line); background:#fff; border-radius:999px;
  padding:4px 12px; font-size:.8rem; cursor:pointer; color:var(--ink); }
.chip:hover { border-color:var(--accent); }
.chip.on { background:var(--accent-bg); border-color:var(--accent); color:var(--accent); font-weight:600; }
select { padding:6px 8px; border:1px solid var(--line); border-radius:8px; font-size:.82rem; background:#fff; }
.toolbar { display:flex; gap:8px; align-items:center; margin-left:auto; }
.toolbar button { border:1px solid var(--line); background:#fff; border-radius:8px;
  padding:5px 10px; font-size:.78rem; cursor:pointer; }
.count { font-size:.82rem; color:var(--muted); white-space:nowrap; }
main { max-width:1080px; margin:0 auto; padding:18px 20px 60px; }
.metrics { display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:10px; margin-bottom:18px; }
.metric { background:var(--card); border:1px solid var(--line); border-radius:10px;
  padding:10px 12px; cursor:pointer; }
.metric:hover { border-color:var(--accent); }
.metric.on { border-color:var(--accent); background:var(--accent-bg); }
.metric b { display:block; font-size:1.25rem; }
.metric .lbl { font-size:.78rem; color:var(--muted); }
.metric .note { font-size:.7rem; color:var(--muted); }
.card { background:var(--card); border:1px solid var(--line); border-radius:10px; margin-bottom:8px; }
.card[open] { border-color:#c7d2e4; box-shadow:0 2px 8px rgba(16,24,40,.06); }
.card summary { display:flex; flex-wrap:wrap; gap:8px; align-items:center;
  padding:10px 14px; cursor:pointer; list-style:none; }
.card summary::-webkit-details-marker { display:none; }
.badge { font-size:.7rem; font-weight:700; border-radius:6px; padding:2px 7px; white-space:nowrap; }
.badge.P1 { color:var(--p1); background:var(--p1-bg); }
.badge.P2 { color:var(--p2); background:var(--p2-bg); }
.badge.P3 { color:#475467; background:#eef1f5; }
.iid { font-family:var(--mono); font-size:.75rem; color:var(--muted); white-space:nowrap; }
.ttl { font-weight:600; flex:1 1 320px; font-size:.92rem; }
.tags { display:flex; gap:6px; flex-wrap:wrap; }
.tag { font-size:.7rem; color:var(--muted); background:var(--bg); border:1px solid var(--line);
  border-radius:6px; padding:2px 7px; white-space:nowrap; }
.tag.proj { color:var(--accent); background:var(--accent-bg); border-color:transparent; font-weight:600; }
.bd { padding:2px 16px 14px; border-top:1px solid var(--line); }
.file { font-family:var(--mono); font-size:.78rem; color:#3b4754; background:var(--bg);
  border-radius:6px; padding:6px 10px; margin:10px 0; word-break:break-all; }
.bd p { margin:8px 0; }
.ev { font-family:var(--mono); font-size:.78rem; background:#f2f4f7; border-left:3px solid #c7d2e4;
  border-radius:0 6px 6px 0; padding:8px 10px; margin:8px 0; white-space:pre-wrap; word-break:break-word; color:#3b4754; }
.rec { background:#ecfdf3; border-left:3px solid #12b76a; border-radius:0 6px 6px 0;
  padding:8px 10px; margin:8px 0; font-size:.88rem; }
.rec b { color:#067647; }
.empty { text-align:center; color:var(--muted); padding:40px 0; display:none; }
footer { max-width:1080px; margin:0 auto; padding:0 20px 40px; color:var(--muted); font-size:.78rem; }
@media (max-width:700px) { .ttl { flex-basis:100%; } .toolbar { margin-left:0; } }
"""

JS = """
(function () {
  'use strict';
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var state = { project: '', sev: '', dim: '', effort: '', q: '' };
  var countEl = document.getElementById('count');
  var emptyEl = document.getElementById('empty');

  function apply() {
    var shown = 0;
    var q = state.q.toLowerCase();
    cards.forEach(function (c) {
      var d = c.dataset;
      var ok = (!state.project || d.project === state.project)
        && (!state.sev || d.sev === state.sev)
        && (!state.dim || d.dim === state.dim)
        && (!state.effort || d.effort === state.effort)
        && (!q || d.search.indexOf(q) !== -1);
      c.style.display = ok ? '' : 'none';
      if (ok) shown += 1;
    });
    countEl.textContent = shown + ' / ' + cards.length + '건 표시 중';
    emptyEl.style.display = shown ? 'none' : 'block';
    document.querySelectorAll('[data-group]').forEach(function (el) {
      var g = el.dataset.group, v = el.dataset.value;
      el.classList.toggle('on', state[g] === v);
    });
  }

  document.querySelectorAll('[data-group]').forEach(function (el) {
    el.addEventListener('click', function () {
      var g = el.dataset.group, v = el.dataset.value;
      state[g] = (state[g] === v) ? '' : v;
      apply();
    });
  });

  ['dim', 'effort'].forEach(function (g) {
    var sel = document.getElementById('sel-' + g);
    if (sel) sel.addEventListener('change', function () { state[g] = sel.value; apply(); });
  });

  document.getElementById('search').addEventListener('input', function (e) {
    state.q = e.target.value.trim(); apply();
  });
  document.getElementById('expand').addEventListener('click', function () {
    cards.forEach(function (c) { if (c.style.display !== 'none') c.open = true; });
  });
  document.getElementById('collapse').addEventListener('click', function () {
    cards.forEach(function (c) { c.open = false; });
  });
  document.getElementById('reset').addEventListener('click', function () {
    state = { project: '', sev: '', dim: '', effort: '', q: '' };
    document.getElementById('search').value = '';
    var sd = document.getElementById('sel-dim'); if (sd) sd.value = '';
    var se = document.getElementById('sel-effort'); if (se) se.value = '';
    apply();
  });
  apply();
})();
"""


def build_card(item: dict) -> str:
    evidence = item.get("evidence", "").strip()
    search_blob = " ".join(
        [item["id"], item["title"], item["description"], item["file_path"],
         item["recommendation"], evidence, item["project"], item["dimension"]]
    ).lower()
    parts = [
        f'<details class="card" data-project="{h(item["project"])}" data-sev="{h(item["severity"])}"',
        f' data-dim="{h(item["dimension"])}" data-effort="{h(item.get("effort", "M"))}"',
        f' data-search="{h(search_blob)}">',
        "<summary>",
        f'<span class="badge {h(item["severity"])}">{h(item["severity"])}</span>',
        f'<span class="iid">{h(item["id"])}</span>',
        f'<span class="ttl">{h(item["title"])}</span>',
        '<span class="tags">',
        f'<span class="tag proj">{h(item["project"])}</span>',
        f'<span class="tag">{h(item["dimension"])}</span>',
        f'<span class="tag">effort {h(item.get("effort", "M"))}</span>',
        "</span></summary>",
        '<div class="bd">',
        f'<div class="file">{h(item["file_path"])}</div>',
        f'<p>{h(item["description"])}</p>',
    ]
    if evidence:
        parts.append(f'<div class="ev">{h(evidence)}</div>')
    parts.append(f'<div class="rec"><b>권고</b> · {h(item["recommendation"])}</div>')
    parts.append("</div></details>")
    return "".join(parts)


def main() -> int:
    source = BASE_DIR / "improvements.json"
    if not source.exists():
        print(f"not found: {source}", file=sys.stderr)
        return 1
    data = json.loads(source.read_text(encoding="utf-8"))
    items = data["items"]

    projects: dict[str, list[dict]] = {}
    for item in items:
        projects.setdefault(item["project"], []).append(item)
    dimensions = sorted({i["dimension"] for i in items})
    p1_total = sum(1 for i in items if i["severity"] == "P1")

    metric_cards = [
        '<div class="metric" data-group="sev" data-value="P1">'
        f'<b>{p1_total}</b><span class="lbl">P1 즉시 조치</span>'
        '<span class="note">클릭해 필터</span></div>'
    ]
    for project, p_items in projects.items():
        p1 = sum(1 for i in p_items if i["severity"] == "P1")
        metric_cards.append(
            f'<div class="metric" data-group="project" data-value="{h(project)}">'
            f'<b>{len(p_items)}</b><span class="lbl">{h(project)}</span>'
            f'<span class="note">{h(PROJECT_LABELS.get(project, ""))} · P1 {p1}</span></div>'
        )

    project_chips = "".join(
        f'<button class="chip" data-group="project" data-value="{h(p)}">{h(p)}</button>'
        for p in projects
    )
    sev_chips = "".join(
        f'<button class="chip" data-group="sev" data-value="{s}">{s}</button>'
        for s in ("P1", "P2")
    )
    dim_options = '<option value="">차원: 전체</option>' + "".join(
        f'<option value="{h(d)}">{h(d)}</option>' for d in dimensions
    )
    effort_options = '<option value="">effort: 전체</option>' + "".join(
        f'<option value="{e}">effort {e}</option>' for e in ("S", "M", "L")
    )

    ordered = sorted(
        items, key=lambda i: (i["project"], {"P1": 0, "P2": 1, "P3": 2}[i["severity"]], i["id"])
    )
    cards_html = "\n".join(build_card(i) for i in ordered)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'">
<title>Keelim Maestro Improvement Backlog — Viewer</title>
<style>{CSS}</style>
</head>
<body>
<header>
<h1>Keelim Maestro Improvement Backlog</h1>
<div class="sub">{len(projects)} sub-projects · {len(items)} items · P1 {p1_total} · generated {h(data.get("generated", "2026-06"))} · 카드를 클릭하면 상세가 펼쳐집니다</div>
<div class="controls">
<input type="search" id="search" placeholder="검색 — 제목·설명·파일 경로·권고…">
<span class="chiprow"><span class="chiplabel">프로젝트</span>{project_chips}</span>
<span class="chiprow"><span class="chiplabel">심각도</span>{sev_chips}</span>
<select id="sel-dim">{dim_options}</select>
<select id="sel-effort">{effort_options}</select>
<span class="toolbar">
<button id="expand">모두 펼치기</button>
<button id="collapse">모두 접기</button>
<button id="reset">초기화</button>
<span class="count" id="count"></span>
</span>
</div>
</header>
<main>
<div class="metrics">{"".join(metric_cards)}</div>
{cards_html}
<div class="empty" id="empty">조건에 맞는 항목이 없습니다.</div>
</main>
<footer>
데이터: docs/research/improvements-2026-06/improvements.json · 방법론: (프로젝트 × 차원) 전담 분석 → 검증·중복 제거 → 프로젝트별 100건 우선순위 컷 · 오프라인 단일 파일(외부 통신 없음)
</footer>
<script>{JS}</script>
</body>
</html>
"""
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUTPUT} ({len(items)} cards)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
