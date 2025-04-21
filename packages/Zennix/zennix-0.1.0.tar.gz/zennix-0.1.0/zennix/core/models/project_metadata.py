from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from pprint import pformat
from zennix.core.scanner.folder.base import FolderInfo

@dataclass
class FileInfo:
    path: str
    ext: str
    lines: int

@dataclass
class SymbolInfo:
    path: str
    functions: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)

@dataclass
class ProjectMetadata:
    name: str = ""
    slug: str = ""
    root_path: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_monorepo: bool = False
    module_type: str = ""

    languages: Dict[str, int] = field(default_factory=dict)
    primary_language: str = ""
    runtime_envs: List[str] = field(default_factory=list)

    folders: List[FolderInfo] = field(default_factory=list)
    files: List[FileInfo] = field(default_factory=list)
    entry_points: List[str] = field(default_factory=list)

    symbols: List[SymbolInfo] = field(default_factory=list)

    documentation: Dict[str, Optional[str]] = field(default_factory=dict)
    dependency_files: List[str] = field(default_factory=list)
    dependencies: Dict[str, str] = field(default_factory=dict)

    config: Dict[str, bool] = field(default_factory=dict)

    git: Dict[str, Optional[str]] = field(default_factory=dict)
    cli: Dict[str, Optional[str]] = field(default_factory=dict)
    tests: Dict[str, Optional[str]] = field(default_factory=dict)
    llm: Dict[str, Optional[str]] = field(default_factory=dict)

    has_dockerfile: bool = False
    has_makefile: bool = False
    ci_cd: List[str] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)

    ignored_folders: List[str] = field(default_factory=list)
    ignored_symlinks: List[str] = field(default_factory=list)

    def summary(self) -> str:
        summary_lines = [
            f"\n📦 Project Summary ({self.created_at}):",
            f"• Root Path: {self.root_path}",
            f"• Primary Language: {self.primary_language}",
            f"• Languages: {', '.join([f'{k} ({v})' for k, v in self.languages.items()]) or 'None'}",
            f"• Entry Points: {', '.join(self.entry_points) or 'None'}",
            f"• Total Folders: {len(self.folders)}",
            f"• Total Files: {len(self.files)}",
        ]

        # Optional fields shown only if they exist
        if self.runtime_envs:
            summary_lines.append(f"• Runtime Envs: {', '.join(self.runtime_envs)}")
        if self.dependency_files:
            summary_lines.append(f"• Dependency Files: {', '.join(self.dependency_files)}")
        if self.dependencies:
            summary_lines.append(f"• Dependencies: {pformat(self.dependencies)}")
        if self.symbols:
            summary_lines.append(f"• Symbols Parsed: {len(self.symbols)} files")

        return "\n".join(summary_lines)
