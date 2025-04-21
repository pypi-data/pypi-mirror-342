# core/folder_scanner/result.py

from dataclasses import dataclass
from typing import List
from .base import FolderInfo

@dataclass
class FolderScanResult:
    folders_info: List[FolderInfo]
    ignored_folders: List[str]
    ignored_symlinks: List[str]
