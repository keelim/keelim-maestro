from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from keelim_knowledge.analyzers.kotlin_analyzer import KotlinAnalyzer
from keelim_knowledge.analyzers.python_analyzer import PythonAnalyzer
from keelim_knowledge.analyzers.typescript_analyzer import TypeScriptAnalyzer
from keelim_knowledge.graph.loader import load_workspace
from keelim_knowledge.graph.populate import populate_workspace
from keelim_knowledge.graph.validator import validate_workspace
from keelim_knowledge.models import AnalysisArtifact


ANALYZERS = {
    "kotlin": KotlinAnalyzer,
    "python": PythonAnalyzer,
    "typescript": TypeScriptAnalyzer,
}


def _default_config_path() -> Path:
    cwd = Path.cwd()
    candidate = cwd / "../knowledge/config.yaml"
    if candidate.exists():
        return candidate.resolve()
    return (cwd / "docs/knowledge/config.yaml").resolve()


def _resolve_config_path(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    return _default_config_path()


def _load_config(config_path: Path) -> dict:
    graph = load_workspace(config_path)
    return graph.config


def _analyzer_for(config: dict, subproject: str):
    subproject_config = config.get("subprojects", {}).get(subproject)
    if not subproject_config:
        raise KeyError(f"Unknown subproject in config: {subproject}")
    analyzer_type = subproject_config["analyzer"]
    analyzer_cls = ANALYZERS.get(analyzer_type)
    if analyzer_cls is None:
        raise KeyError(f"Unsupported analyzer type: {analyzer_type}")
    return analyzer_cls(), subproject_config


def _write_artifact(config_path: Path, artifact: AnalysisArtifact) -> Path:
    output_path = config_path.parent / "generated" / f"{artifact.subproject}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(artifact.to_mapping(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def _cmd_validate(args: argparse.Namespace) -> int:
    config_path = _resolve_config_path(args.config)
    result = validate_workspace(config_path)
    if result.is_valid:
        print("Validation passed")
        return 0
    for issue in result.issues:
        print(issue, file=sys.stderr)
    return 1


def _cmd_analyze(args: argparse.Namespace) -> int:
    config_path = _resolve_config_path(args.config)
    config = _load_config(config_path)
    analyzer, subproject_config = _analyzer_for(config, args.subproject)
    root = (config_path.parent / subproject_config["path"]).resolve()
    artifact = analyzer.analyze(root)
    output_path = _write_artifact(config_path, artifact)
    print(output_path)
    return 0


def _cmd_stats(args: argparse.Namespace) -> int:
    config_path = _resolve_config_path(args.config)
    graph = load_workspace(config_path)
    print(
        json.dumps(
            {
                "nodes": len(graph.node_entries),
                "edges": len(graph.edge_entries),
                "knowledge_root": str(graph.knowledge_root),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _cmd_populate(args: argparse.Namespace) -> int:
    config_path = _resolve_config_path(args.config)
    summary = populate_workspace(config_path)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def _cmd_query(args: argparse.Namespace) -> int:
    from keelim_knowledge.graph.neo4j_client import Neo4jClient

    client = Neo4jClient.from_env(
        uri=os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        user=os.environ.get("NEO4J_USER", "neo4j"),
        password=os.environ.get("NEO4J_PASSWORD", "neo4j"),
    )
    with client:
        rows = client.run_query(args.query)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


def _cmd_impact(args: argparse.Namespace) -> int:
    from keelim_knowledge.graph.neo4j_client import Neo4jClient

    client = Neo4jClient.from_env(
        uri=os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        user=os.environ.get("NEO4J_USER", "neo4j"),
        password=os.environ.get("NEO4J_PASSWORD", "neo4j"),
    )
    with client:
        payload = client.analyze_entity_impact(args.entity, max_hops=args.max_hops)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="keelim-knowledge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--config")
    validate.set_defaults(func=_cmd_validate)

    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("subproject")
    analyze.add_argument("--config")
    analyze.set_defaults(func=_cmd_analyze)

    stats = subparsers.add_parser("stats")
    stats.add_argument("--config")
    stats.set_defaults(func=_cmd_stats)

    populate = subparsers.add_parser("populate")
    populate.add_argument("--config")
    populate.set_defaults(func=_cmd_populate)

    query = subparsers.add_parser("query")
    query.add_argument("query")
    query.set_defaults(func=_cmd_query)

    impact = subparsers.add_parser("impact")
    impact.add_argument("entity")
    impact.add_argument("--max-hops", type=int, default=3)
    impact.set_defaults(func=_cmd_impact)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # pragma: no cover - CLI guard
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
