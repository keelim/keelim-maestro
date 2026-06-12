#!/usr/bin/env python3
"""Build the html-report-generator block-model input from improvements.json.

Mapping (renderer supports top-level blocks only):
- metrics: totals + per-project cards
- sections: one narrative section per project (dimension distribution)
- tables: one table per project with all selected items
- findings: P1 highlights only (top 3-5 per project), P1 -> high
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BASE_DIR = REPO_ROOT / "docs" / "research" / "improvements-2026-06"

PROJECT_LABELS = {
    "all": "all — Kotlin 멀티 Android 앱 모노레포",
    "android-support": "android-support — Play Store 배포 GitHub Action (TypeScript)",
    "Keelim-Knowledge-Vault": "Keelim-Knowledge-Vault — Obsidian 지식 저장소",
    "keelim-plugin": "keelim-plugin — Claude Code 스킬 플러그인 (Python)",
    "keelim-vercel": "keelim-vercel — Next.js 16 관리 대시보드",
    "rich": "rich — FastAPI + Next.js 주식 정량분석 풀스택",
    "youtube": "youtube — Python CLI + Remotion 영상 자동화",
    "all-web-ui": "all-web-ui — React 19 공유 UI 컴포넌트 라이브러리",
}
SEVERITY_TO_RENDERER = {"P1": "high", "P2": "medium", "P3": "low"}
HIGHLIGHTS_PER_PROJECT = 4
RECOMMENDATION_LIMIT = 200


def truncate(text: str, limit: int) -> str:
    clean = " ".join(text.split())
    return clean if len(clean) <= limit else clean[: limit - 1] + "…"


def severity_counts(items: list[dict]) -> dict[str, int]:
    counts = {"P1": 0, "P2": 0, "P3": 0}
    for item in items:
        counts[item["severity"]] += 1
    return counts


def build_metrics(by_project: dict[str, list[dict]], total: int) -> list[dict]:
    p1_total = sum(severity_counts(items)["P1"] for items in by_project.values())
    metrics = [
        {"label": "Total items", "value": str(total), "note": f"{len(by_project)} sub-projects"},
        {"label": "P1 (즉시 조치)", "value": str(p1_total), "note": "전체 프로젝트 합계"},
    ]
    for project, items in by_project.items():
        counts = severity_counts(items)
        metrics.append(
            {
                "label": project,
                "value": str(len(items)),
                "note": f"P1 {counts['P1']} · P2 {counts['P2']} · P3 {counts['P3']}",
            }
        )
    return metrics


def build_sections(by_project: dict[str, list[dict]]) -> list[dict]:
    sections = []
    for project, items in by_project.items():
        dims: dict[str, dict[str, int]] = {}
        for item in items:
            entry = dims.setdefault(item["dimension"], {"total": 0, "P1": 0})
            entry["total"] += 1
            if item["severity"] == "P1":
                entry["P1"] += 1
        counts = severity_counts(items)
        bullet_list = [
            f"{dim}: {info['total']}건 (P1 {info['P1']})"
            for dim, info in sorted(dims.items(), key=lambda kv: -kv[1]["total"])
        ]
        sections.append(
            {
                "heading": f"{PROJECT_LABELS.get(project, project)} — {len(items)} items",
                "body": (
                    f"{project} 프로젝트에서 {len(items)}건의 개선 항목을 수집했다. "
                    f"우선순위 분포는 P1 {counts['P1']}건, P2 {counts['P2']}건, P3 {counts['P3']}건이다. "
                    f"상세 목록은 아래 '{project} — Improvement Items' 테이블 참조."
                ),
                "items": bullet_list,
            }
        )
    return sections


def build_tables(by_project: dict[str, list[dict]]) -> list[dict]:
    tables = []
    for project, items in by_project.items():
        rows = [
            [
                item["id"],
                item["severity"],
                item["dimension"],
                item["title"],
                item["file_path"],
                truncate(item["recommendation"], RECOMMENDATION_LIMIT),
            ]
            for item in items
        ]
        tables.append(
            {
                "title": f"{project} — Improvement Items ({len(items)})",
                "columns": ["ID", "Sev", "Dimension", "Title", "File", "Recommendation"],
                "rows": rows,
            }
        )
    return tables


def build_findings(by_project: dict[str, list[dict]]) -> list[dict]:
    findings = []
    for project, items in by_project.items():
        p1_items = [i for i in items if i["severity"] == "P1"][:HIGHLIGHTS_PER_PROJECT]
        for item in p1_items:
            findings.append(
                {
                    "severity": SEVERITY_TO_RENDERER[item["severity"]],
                    "title": f"[{item['id']}] {item['title']}",
                    "body": (
                        f"{item['description']}\n\n"
                        f"위치: {item['file_path']}\n\n"
                        f"권고: {item['recommendation']}"
                    ),
                }
            )
    return findings


def main() -> int:
    source = BASE_DIR / "improvements.json"
    if not source.exists():
        print(f"not found: {source}", file=sys.stderr)
        return 1
    data = json.loads(source.read_text(encoding="utf-8"))
    items = data["items"]

    by_project: dict[str, list[dict]] = {}
    for item in items:
        by_project.setdefault(item["project"], []).append(item)

    p1_total = sum(severity_counts(v)["P1"] for v in by_project.values())
    report = {
        "title": "Keelim Maestro Improvement Backlog",
        "subtitle": f"{len(by_project)} sub-projects · {len(items)} items · 2026-06",
        "summary": (
            f"keelim-maestro 저장소의 하위 프로젝트 {len(by_project)}개를 차원별 병렬 분석으로 "
            f"점검해 총 {len(items)}건의 개선 항목을 수집했다. 모든 항목은 실제 파일 경로 증거를 "
            f"갖고 있으며 P1(즉시)/P2(중요)/P3(개선) 우선순위와 예상 작업량(S/M/L)이 부여되어 있다.\n\n"
            f"P1 항목은 총 {p1_total}건으로, 아래 Findings 섹션에 프로젝트별 대표 P1 항목을 "
            f"하이라이트했다. 전체 목록은 프로젝트별 테이블과 "
            f"docs/research/improvements-2026-06/improvements.json 에서 확인할 수 있다."
        ),
        "metadata": {
            "Generated": data.get("generated", "2026-06"),
            "Repository": "keelim-maestro",
            "Sub-projects": ", ".join(by_project),
            "Total items": str(len(items)),
            "Method": "dimension-parallel subagent analysis + dedupe + priority cut",
        },
        "metrics": build_metrics(by_project, len(items)),
        "sections": build_sections(by_project),
        "tables": build_tables(by_project),
        "findings": build_findings(by_project),
        "appendix": [
            {
                "heading": "Severity / Effort 기준",
                "items": [
                    "P1: 버그·보안·데이터 정합성 등 즉시 조치 필요",
                    "P2: 품질·유지보수성에 중요한 영향",
                    "P3: 점진적 개선 항목",
                    "Effort S/M/L: 예상 작업량 (S: 1시간 내, M: 반나절, L: 1일 이상)",
                ],
            },
            {
                "heading": "방법론",
                "body": (
                    "프로젝트당 6개 분석 차원(예: 아키텍처, 코드 품질, 테스트, 보안, 성능, DX)으로 "
                    "분할해 차원별 전담 분석 에이전트가 소스를 직접 읽고 raw JSON으로 수집했다. "
                    "집계 단계에서 필수 필드·파일 경로 실존 검증, 2단계 중복 제거(정확 키 + 제목 토큰 "
                    "Jaccard 0.6), 프로젝트별 우선순위 컷(severity → effort → 차원 라운드로빈)을 적용했다."
                ),
            },
            {
                "heading": "데이터 소스",
                "items": [
                    "전체 데이터: docs/research/improvements-2026-06/improvements.json",
                    "차원별 원본: docs/research/improvements-2026-06/raw/",
                    "동반 요약: docs/research/improvement-items-2026-06.md",
                ],
            },
        ],
    }

    output = BASE_DIR / "report-input.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {output} ({len(items)} items, {len(report['findings'])} highlights)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
