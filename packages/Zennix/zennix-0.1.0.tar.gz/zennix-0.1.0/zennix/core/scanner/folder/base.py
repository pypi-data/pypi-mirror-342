import os
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

@dataclass
class FolderInfo:
    name: str
    files: int
    ignored: List[str] = field(default_factory=list)
    file_types: Dict[str, int] = field(default_factory=dict)
    size_in_bytes: int = 0
    last_modified: Optional[float] = None
    largest_files: List[str] = field(default_factory=list)

@dataclass
class ScanConfig:
    max_depth: int = 10
    max_items: int = 1000
    ignore_hidden: bool = True
    excluded_folders: set = field(default_factory=set)
    plugins: List = field(default_factory=list)

class FolderScanner:
    def __init__(self, project_path: str, config: ScanConfig):
        self.project_path = os.path.abspath(project_path)
        self.config = config
        default_ignored = {'.git', '__pycache__', 'venv', '.venv', 'node_modules', 'dist', 'build', '.idea', '.vscode'}
        self.ignored_folders = default_ignored.union(config.excluded_folders)
        self.seen_real_paths = set()

    def _is_hidden(self, name: str) -> bool:
        return name.startswith('.')

    def scan(self) -> Tuple[List[FolderInfo], List[str], List[str]]:
        logger.info("📁 Scanning folders...")
        folders, ignored_folders, ignored_symlinks = [], [], []

        for root, dirs, _ in os.walk(self.project_path, topdown=True, followlinks=False):
            try:
                real_root = os.path.realpath(root)
                if real_root in self.seen_real_paths:
                    continue
                self.seen_real_paths.add(real_root)

                rel_root = os.path.relpath(root, self.project_path)
                folder_name = '.' if rel_root == '.' else rel_root
                folder_depth = rel_root.count(os.sep)

                if folder_depth > self.config.max_depth:
                    logger.warning(f"⚠️ Skipping folder (too deep): {folder_name}")
                    continue

                original_dirs = list(dirs)
                dirs[:] = []
                ignored_in_this_folder = []

                for d in original_dirs:
                    full_path = os.path.join(root, d)
                    if d in self.ignored_folders or (self.config.ignore_hidden and self._is_hidden(d)) or os.path.islink(full_path):
                        (ignored_symlinks if os.path.islink(full_path) else ignored_folders).append(full_path)
                        ignored_in_this_folder.append(d)
                    else:
                        dirs.append(d)

                items = os.listdir(root)
                if len(items) > self.config.max_items:
                    logger.warning(f"⚠️ Truncating scan in folder: {folder_name}")
                    items = items[:self.config.max_items]

                files = [f for f in items if os.path.isfile(os.path.join(root, f)) and not self._is_hidden(f)]
                file_count = len(files)
                size = 0
                file_types = {}
                largest = []

                for f in files:
                    path = os.path.join(root, f)
                    try:
                        sz = os.path.getsize(path)
                        size += sz
                        ext = os.path.splitext(f)[1] or 'unknown'
                        file_types[ext] = file_types.get(ext, 0) + 1
                        largest.append((f, sz))
                    except Exception as e:
                        logger.warning(f"Error getting file info: {f} - {e}")

                largest_files = sorted(largest, key=lambda x: x[1], reverse=True)[:5]

                if any(plugin(root, items) for plugin in self.config.plugins):
                    logger.info(f"🚫 Skipping folder due to plugin rule: {folder_name}")
                    continue

                folders.append(FolderInfo(
                    name=folder_name,
                    files=file_count,
                    ignored=ignored_in_this_folder,
                    file_types=file_types,
                    size_in_bytes=size,
                    last_modified=os.path.getmtime(root),
                    largest_files=[name for name, _ in largest_files]
                ))

            except PermissionError:
                logger.warning(f"⚠️ Skipping folder (permission denied): {root}")
                continue

        return folders, ignored_folders, ignored_symlinks
