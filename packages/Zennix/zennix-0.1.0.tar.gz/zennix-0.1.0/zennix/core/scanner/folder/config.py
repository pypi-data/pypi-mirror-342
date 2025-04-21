# core/folder_scanner/config.py

from dataclasses import dataclass, field
from typing import List, Set, Callable

@dataclass
class ScanConfig:
    max_depth: int = 10
    max_items: int = 1000
    ignore_hidden: bool = True
    excluded_folders: Set[str] = field(default_factory=set)
    plugins: List[Callable] = field(default_factory=list)
