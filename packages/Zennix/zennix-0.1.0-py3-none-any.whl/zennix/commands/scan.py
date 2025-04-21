# zennix/commands/scan.py
from typer import Typer, Option, secho, colors
from zennix.core.scanner.project_scanner import ProjectScanner
from zennix.core.utils import file_ops
import os

app = Typer(help="Scan your project and extract structured metadata.")

@app.command()
def scan(
    path: str = Option(".", help="Path to your project"),
    deep: bool = Option(False, help="Enable deep scan including file contents (for future use)"),
):
    """Scan the project and display a summary of its structure."""
    scanner = ProjectScanner(project_path=path, deep_scan=deep)
    metadata = scanner.scan()

    file_ops.save_file(metadata, "data/scan_results", "scan.json") # Save the scan results

    # Show the tree view
    secho("\n📂 Project Structure:\n", fg=colors.CYAN, bold=True)
    folder_map = {folder.name: [] for folder in metadata.folders}
    for file in metadata.files:
        folder_name = os.path.dirname(file.path) or "."
        folder_map.setdefault(folder_name, []).append(file)

    for folder in sorted(folder_map.keys()):
        depth = folder.count(os.sep)
        indent = "│   " * depth
        secho(f"{indent}📁 {folder}/", fg=colors.BRIGHT_BLUE)
        for f in folder_map[folder]:
            file_indent = indent + "│   "
            print(f"{file_indent}└── 📄 {os.path.basename(f.path)} ({f.ext}, {f.lines} lines)")

    # Dynamically print the summary
    secho(metadata.summary(), fg=colors.CYAN, bold=True)

