#!/usr/bin/env python3
"""Automate codemap generation and update documentation index for child repositories."""

import os
import re
import sys
import subprocess
from datetime import date
from pathlib import Path

from improvements.docs_root import archive_path, archive_root

# Child repositories to process
CHILD_REPOS = [
    "all",
    "all-web-ui",
    "android-support",
    "Keelim-Knowledge-Vault",
    "keelim-plugin",
    "keelim-vercel",
    "rich"
]

def run_cmd(args, cwd=None):
    print(f"Running: {' '.join(args)}")
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {' '.join(args)}")
        print(result.stderr)
        return False
    return True

def main():
    today = date.today().isoformat()
    root_dir = Path(__file__).resolve().parent.parent
    generator_script = root_dir / "keelim-plugin/skills/codebase-codemap/scripts/generate_codemap.py"
    docs_root = archive_root(root_dir)
    output_dir = archive_path(docs_root, "CODEMAPS", "projects")
    if not docs_root.is_dir():
        print(f"Local archive not found: {docs_root}; set KEELIM_DOCS_DIR.", file=sys.stderr)
        return 1

    if not generator_script.exists():
        print(f"Generator script not found at {generator_script}", file=sys.stderr)
        return 1

    # Step 1: Generate codemaps
    stats = {}
    failures = 0
    for repo in CHILD_REPOS:
        repo_path = root_dir / repo
        if not repo_path.is_dir() or not any(repo_path.iterdir()):
            print(f"Child repository directory {repo_path} does not exist, skipping.")
            continue

        codemap_file = archive_path(docs_root, "CODEMAPS", "projects", f"{repo}.md")
        print(f"--- Generating codemap for: {repo} ---")
        success = run_cmd([
            "python3",
            str(generator_script),
            str(repo_path),
            "--output-dir",
            str(output_dir),
            "--allow-outside-output"
        ], cwd=str(root_dir))

        if not success:
            print(f"Failed to generate codemap for {repo}", file=sys.stderr)
            failures += 1
            continue

        # Parse generated codemap file to extract scanned files and shape
        if codemap_file.exists():
            content = codemap_file.read_text(encoding="utf-8")
            
            files_scanned = None
            shape = None
            
            files_match = re.search(r"-\s*Files scanned:\s*(\d+)", content)
            if files_match:
                files_scanned = int(files_match.group(1))
                
            shape_match = re.search(r"-\s*Detected shape:\s*(.+)", content)
            if shape_match:
                shape = shape_match.group(1).strip()
                
            stats[repo] = {
                "files_scanned": files_scanned,
                "shape": shape
            }
            print(f"Successfully processed {repo}: {files_scanned} files, shape: {shape}")

    if failures:
        return 1

    # Step 2: Update the local codemap index table
    projects_readme = archive_path(docs_root, "CODEMAPS", "projects", "README.md")
    if projects_readme.exists():
        content = projects_readme.read_text(encoding="utf-8")
        
        # We need to reconstruct the snapshot table
        new_table_rows = []
        for repo in sorted(CHILD_REPOS):
            if repo in stats:
                files_count = f"{stats[repo]['files_scanned']:,}"
                shape_str = stats[repo]['shape']
            else:
                files_count = "—"
                shape_str = "Unknown"
            
            # Format row: | `repo` | [repo.md](repo.md) | files_count | shape_str |
            new_table_rows.append(f"| `{repo}` | [{repo}.md]({repo}.md) | {files_count} | {shape_str} |")
            
        new_table_str = "\n".join(new_table_rows)
        
        # Replace the existing table
        # Table structure matches:
        # ## Generated Snapshots
        # 
        # | Project | Codemap | Files scanned | Shape |
        # | --- | --- | ---: | --- |
        # <rows>
        # 
        pattern = r"(## Generated Snapshots\s*\n\s*\|[^\n]+\n\s*\|[^\n]+\n)([\s\S]*?)(?=\n\n|\n##|$)"
        replacement = r"\1" + new_table_str
        
        updated_content = re.sub(pattern, replacement, content)
        
        # Update Last updated: YYYY-MM-DD
        updated_content = re.sub(r"Last updated:\s*\d{4}-\d{2}-\d{2}", f"Last updated: {today}", updated_content)
        
        projects_readme.write_text(updated_content, encoding="utf-8")
        print(f"Updated {projects_readme}")

    # Step 3: Update other workspace codemap dates
    doc_files = [
        "CODEMAPS/README.md",
        "CODEMAPS/WORKSPACE.md",
        "CODEMAPS/keelim-maestro.md"
    ]
    for doc in doc_files:
        doc_path = archive_path(docs_root, doc)
        if doc_path.exists():
            content = doc_path.read_text(encoding="utf-8")
            
            # Replace Last updated: YYYY-MM-DD
            updated_content = re.sub(r"Last updated:\s*\d{4}-\d{2}-\d{2}", f"Last updated: {today}", content)

            # Replace comment: <!-- Generated: YYYY-MM-DD ... -->
            updated_content = re.sub(r"Generated:\s*\d{4}-\d{2}-\d{2}", f"Generated: {today}", updated_content)
            
            doc_path.write_text(updated_content, encoding="utf-8")
            print(f"Updated {doc_path}")

    print("--- Codemap refresh and documentation update complete! ---")
    return 0

if __name__ == "__main__":
    sys.exit(main())
