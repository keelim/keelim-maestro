import textwrap
from pathlib import Path

from keelim_knowledge.analyzers.kotlin_analyzer import KotlinAnalyzer
from keelim_knowledge.analyzers.python_analyzer import PythonAnalyzer
from keelim_knowledge.analyzers.typescript_analyzer import TypeScriptAnalyzer


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def test_kotlin_analyzer_extracts_modules_and_screens(tmp_path: Path) -> None:
    write_file(
        tmp_path / "settings.gradle.kts",
        """
        include(
            ":app-main",
            ":core:data",
            ":feature:settings-theme",
        )
        """,
    )

    artifact = KotlinAnalyzer().analyze(tmp_path)

    node_types = {(node.id, node.node_type) for node in artifact.nodes}
    assert ("all:module:app-main", "Module") in node_types
    assert ("all:module:core-data", "Module") in node_types
    assert ("all:screen:feature-settings-theme", "UIScreen") in node_types


def test_python_analyzer_extracts_endpoints_and_services(tmp_path: Path) -> None:
    write_file(
        tmp_path / "app" / "api" / "admin.py",
        """
        from fastapi import APIRouter
        from app.services.weekly_review import generate_ai_summary

        router = APIRouter(prefix="/api/admin", tags=["admin"])

        @router.get("/me")
        def admin_me():
            return generate_ai_summary()
        """,
    )

    artifact = PythonAnalyzer().analyze(tmp_path)

    endpoint_ids = {node.id for node in artifact.nodes if node.node_type == "APIEndpoint"}
    service_ids = {node.id for node in artifact.nodes if node.node_type == "Service"}
    assert "rich:endpoint:get:/api/admin/me" in endpoint_ids
    assert "rich:service:weekly_review.generate_ai_summary" in service_ids


def test_typescript_analyzer_extracts_tables_routes_and_pages(tmp_path: Path) -> None:
    write_file(
        tmp_path / "lib" / "db.ts",
        """
        export const products = pgTable('products', {
          id: serial('id').primaryKey(),
        });
        """,
    )
    write_file(tmp_path / "app" / "dashboard" / "page.tsx", "export default function Page() { return null; }")
    write_file(tmp_path / "app" / "api" / "products" / "route.ts", "export async function GET() { return Response.json({ ok: true }); }")

    artifact = TypeScriptAnalyzer().analyze(tmp_path)

    node_types = {(node.id, node.node_type) for node in artifact.nodes}
    assert ("keelim-vercel:table:products", "DatabaseTable") in node_types
    assert ("column:products:id", "TableColumn") in node_types
    assert ("keelim-vercel:screen:/dashboard", "UIScreen") in node_types
    assert ("keelim-vercel:endpoint:route:/api/products", "APIEndpoint") in node_types
    edge_types = {(edge.relation_type, edge.source, edge.target) for edge in artifact.edges}
    assert ("READS", "keelim-vercel:endpoint:route:/api/products", "entity:product") in edge_types
