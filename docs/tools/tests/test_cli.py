import json
import subprocess
import sys
import textwrap
from pathlib import Path


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def make_project(tmp_path: Path) -> Path:
    knowledge_root = tmp_path / "docs" / "knowledge"
    write_file(
        knowledge_root / "config.yaml",
        """
        workspace:
          id: workspace:keelim-maestro
          knowledge_root: docs/knowledge
        subprojects:
          all:
            path: ../../all
            analyzer: kotlin
        """,
    )
    write_file(
        knowledge_root / "nodes" / "workspace" / "keelim-maestro.yaml",
        """
        id: workspace:keelim-maestro
        node_type: Workspace
        name: keelim-maestro
        path: .
        """,
    )
    write_file(
        knowledge_root / "nodes" / "subprojects" / "all.yaml",
        """
        id: subproject:all
        node_type: Subproject
        name: all
        path: all
        """,
    )
    write_file(
        tmp_path / "all" / "settings.gradle.kts",
        """
        include(
            ":app-main",
            ":core:data",
        )
        """,
    )
    return knowledge_root / "config.yaml"


def test_cli_validate_and_analyze_commands(tmp_path: Path) -> None:
    config_path = make_project(tmp_path)
    pythonpath = str(Path(__file__).resolve().parents[1] / "src")

    validate = subprocess.run(
        [sys.executable, "-m", "keelim_knowledge.cli", "validate", "--config", str(config_path)],
        cwd=tmp_path,
        env={"PYTHONPATH": pythonpath},
        capture_output=True,
        text=True,
        check=False,
    )
    assert validate.returncode == 0, validate.stderr
    assert "Validation passed" in validate.stdout

    analyze = subprocess.run(
        [sys.executable, "-m", "keelim_knowledge.cli", "analyze", "all", "--config", str(config_path)],
        cwd=tmp_path,
        env={"PYTHONPATH": pythonpath},
        capture_output=True,
        text=True,
        check=False,
    )
    assert analyze.returncode == 0, analyze.stderr

    generated_path = config_path.parent / "generated" / "all.json"
    payload = json.loads(generated_path.read_text(encoding="utf-8"))
    assert payload["subproject"] == "all"
    assert any(node["node_type"] == "Module" for node in payload["nodes"])
