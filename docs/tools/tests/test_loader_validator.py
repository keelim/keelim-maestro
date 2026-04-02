import textwrap
from pathlib import Path

from keelim_knowledge.graph.loader import load_workspace
from keelim_knowledge.graph.validator import validate_workspace


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def make_workspace(root: Path) -> Path:
    knowledge_root = root / "docs" / "knowledge"
    write_file(
        knowledge_root / "schema.yaml",
        """
        node_types:
          - Workspace
          - Subproject
          - Module
          - TableColumn
        relation_types:
          - CONTAINS
          - STORED_IN
          - USES
        """,
    )
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
          rich:
            path: ../../rich
            analyzer: python
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
        knowledge_root / "relationships" / "workspace.yaml",
        """
        - id: edge:workspace:all
          relation_type: CONTAINS
          from: workspace:keelim-maestro
          to: subproject:all
        """,
    )
    write_file(
        knowledge_root / "generated" / "all.json",
        """
        {
          "subproject": "all",
          "nodes": [
            {
              "id": "all:module:core-data",
              "node_type": "Module",
              "name": "core:data",
              "path": "all/core/data"
            }
          ],
          "edges": [
            {
              "id": "edge:subproject:all:module",
              "relation_type": "CONTAINS",
              "from": "subproject:all",
              "to": "all:module:core-data"
            }
          ]
        }
        """,
    )
    return knowledge_root / "config.yaml"


def test_loader_reads_manual_and_generated_entries(tmp_path: Path) -> None:
    config_path = make_workspace(tmp_path)

    graph = load_workspace(config_path)

    node_ids = {entry.node.id for entry in graph.node_entries}
    edge_ids = {entry.edge.id for entry in graph.edge_entries}
    assert "workspace:keelim-maestro" in node_ids
    assert "subproject:all" in node_ids
    assert "all:module:core-data" in node_ids
    assert "edge:workspace:all" in edge_ids
    assert "edge:subproject:all:module" in edge_ids


def test_validator_flags_duplicates_and_dangling_edges(tmp_path: Path) -> None:
    config_path = make_workspace(tmp_path)
    knowledge_root = config_path.parent
    write_file(
        knowledge_root / "nodes" / "subprojects" / "all-duplicate.yaml",
        """
        id: subproject:all
        node_type: Subproject
        name: all duplicate
        path: all
        """,
    )
    write_file(
        knowledge_root / "relationships" / "dangling.yaml",
        """
        - id: edge:dangling
          relation_type: USES
          from: subproject:all
          to: service:missing
        """,
    )

    result = validate_workspace(config_path)

    assert not result.is_valid
    assert any("duplicate node id: subproject:all" in issue for issue in result.issues)
    assert any("missing target node: service:missing" in issue for issue in result.issues)


def test_validator_rejects_unsupported_types_and_missing_column_metadata(tmp_path: Path) -> None:
    config_path = make_workspace(tmp_path)
    knowledge_root = config_path.parent
    write_file(
        knowledge_root / "nodes" / "tables" / "bad-column.yaml",
        """
        id: column:products:status
        node_type: TableColumn
        name: products.status
        path: all/core/data
        """,
    )
    write_file(
        knowledge_root / "relationships" / "bad-relation.yaml",
        """
        - id: edge:bad
          relation_type: WRITES
          from: subproject:all
          to: all:module:core-data
        """,
    )

    result = validate_workspace(config_path)

    assert not result.is_valid
    assert any("missing table metadata for column node: column:products:status" in issue for issue in result.issues)
    assert any("missing column_name metadata for column node: column:products:status" in issue for issue in result.issues)
    assert any("unsupported relation type: WRITES" in issue for issue in result.issues)
