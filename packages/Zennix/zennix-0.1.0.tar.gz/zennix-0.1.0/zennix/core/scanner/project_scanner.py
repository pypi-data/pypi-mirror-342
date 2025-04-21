# zennix/core/project_scanner.py

import os
import re
from zennix.core.utils.logger import get_logger
from zennix.core.models.project_metadata import ProjectMetadata, FileInfo, SymbolInfo
from zennix.core.scanner.folder.base import FolderScanner, FolderInfo
from typing import List, Dict, Optional, Tuple
from collections import Counter
from zennix.core.scanner.folder.base import ScanConfig


logger = get_logger("scanner")

class ProjectScanner:
    def __init__(self, project_path: str, deep_scan: bool):
        self. scan_state = {}
        self.project_path = os.path.abspath(project_path)
        self.deep_scan = deep_scan
        self.ignored_folders = {".git", "__pycache__", "venv", ".venv", "node_modules", "dist", "build", ".idea", ".vscode"}

        if not os.path.exists(self.project_path):
            raise FileNotFoundError(f"Path does not exist: {self.project_path}")
        if not os.path.isdir(self.project_path):
            raise NotADirectoryError(f"Expected directory, got file: {self.project_path}")
        
        config = ScanConfig(
            max_depth=20 if deep_scan else 5,
            max_items=2000 if deep_scan else 500,
            excluded_folders=self.ignored_folders
        )

        self.folder_scanner = FolderScanner(
            project_path=self.project_path,
            config=config
        )

        logger.info(f"🛰️  Scanner initialized for path: {self.project_path} (deep={self.deep_scan})")

    def scan(self) -> ProjectMetadata:
        logger.info("🧠 Starting intelligent project scan...")

        self._scan_filesystem()
        self._analyze_structure()
        self._infer_intent()
        self._extract_knowledge()
        self._generate_metadata()

        return self.metadata

    def _scan_filesystem(self):
        logger.info("📂 Scanning filesystem...")
        folders_info, ignored_folders, ignored_symlinks = self.folder_scanner.scan()
        files_info = self._scan_files(folders_info)

        self.scan_state.update({
            "folders": folders_info,
            "files": files_info,
            "ignored_folders": ignored_folders,
            "ignored_symlinks": ignored_symlinks,
        })

    def _analyze_structure(self):
        logger.info("🧱 Analyzing project structure...")
        languages, primary_lang = self._detect_languages(self.scan_state["files"])
        entry_points = self._find_entry_points(self.scan_state["files"])
        docs = self._extract_documents()

        self.scan_state.update({
            "languages": languages,
            "primary_language": primary_lang,
            "entry_points": entry_points,
            "documentation": docs,
        })

    def _infer_intent(self):
        logger.info("🔮 Inferring project intent...")

        # Example heuristic: if it has `cli.py`, no frontend, and entry is main.py => CLI tool
        structure = self.scan_state.get("folders", [])
        files = self.scan_state.get("files", [])
        entry = self.scan_state.get("entry_points", [])

        # TODO: smarter logic with a classifier or LLM in the future
        intent = "CLI tool" if any("cli.py" in f.path for f in files) else "Unknown"

        self.scan_state["intent"] = intent

    def _extract_knowledge(self):
        logger.info("🧠 Extracting symbols and inferred logic...")
        files = self.scan_state["files"]
        self.scan_state["symbols"] = self._extract_symbols(files)

        # Infer additional knowledge later like CI/CD or framework detection
        self.scan_state["dependencies"] = self._detect_dependencies()
        self.scan_state["runtime_envs"] = self._detect_runtime_envs()
        self.scan_state["ci_cd"] = self._detect_ci_cd()
        self.scan_state["dockerfile"], self.scan_state["makefile"] = self._check_dockerfile_makefile()

    def _generate_metadata(self):
        logger.info("🗂️ Generating ProjectMetadata object...")
        self.metadata = ProjectMetadata(
            root_path=self.project_path,
            folders=self.scan_state["folders"],
            files=self.scan_state["files"],
            languages=self.scan_state["languages"],
            primary_language=self.scan_state["primary_language"],
            entry_points=self.scan_state["entry_points"],
            ignored_folders=self.scan_state["ignored_folders"],
            ignored_symlinks=self.scan_state["ignored_symlinks"],
            documentation=self.scan_state["documentation"],
            dependencies=self.scan_state["dependencies"],
            symbols=self.scan_state["symbols"],
            runtime_envs=self.scan_state["runtime_envs"],
            ci_cd=self.scan_state["ci_cd"],
            has_dockerfile=self.scan_state["dockerfile"],
            has_makefile=self.scan_state["makefile"],
        )

    # def scan(self) -> ProjectMetadata:
    #     logger.info("🔍 Starting project scan...\n")

    #     folders_info, ignored_folders, ignored_symlinks = self.folder_scanner.scan()
    #     files_info = self._scan_files(folders_info)
    #     languages, primary_lang = self._detect_languages(files_info)
    #     entry_points = self._find_entry_points(files_info)
    #     documentation_info = self._extract_documents()
    #     dependencies_info = self._detect_dependencies()
    #     symbols_info = self._extract_symbols(files_info)
    #     runtime_envs_info = self._detect_runtime_envs()
    #     ci_cd_info = self._detect_ci_cd()
    #     dockerfile_info, makefile_info = self._check_dockerfile_makefile()

    #     logger.info("✅ Metadata extraction complete")

    #     return ProjectMetadata(
    #         root_path=self.project_path,
    #         folders=folders_info,
    #         files=files_info,
    #         languages=languages,
    #         primary_language=primary_lang,
    #         entry_points=entry_points,
    #         ignored_folders=ignored_folders,
    #         ignored_symlinks=ignored_symlinks,
    #         documentation=documentation_info,
    #         dependencies=dependencies_info,
    #         symbols=symbols_info,
    #         runtime_envs=runtime_envs_info,
    #         ci_cd=ci_cd_info,
    #         has_dockerfile=dockerfile_info,
    #         has_makefile=makefile_info
    #     )

    def _scan_files(self, folders_info: List[FolderInfo]) -> List[FileInfo]:
        logger.info("📄 Scanning files...")
        files = []

        for folder in folders_info:
            folder_path = os.path.join(self.project_path, folder.name)
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    ext = self._get_extension(file)
                    lines = self._count_lines(file_path)
                    relative_path = os.path.relpath(file_path, self.project_path)
                    files.append(FileInfo(path=relative_path, ext=ext, lines=lines))

                    depth = folder.name.count(os.sep)
                    indent = "│   " * depth
                    logger.info(f"{indent}│   └── 📄 {file} ({ext}, {lines} lines)")

        return files

    def _get_extension(self, filename: str) -> str:
        _, ext = os.path.splitext(filename)
        return ext.lower().strip() if ext else "no_ext"

    def _count_lines(self, file_path: str) -> int:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return sum(1 for _ in f)
        except UnicodeDecodeError:
            with open(file_path, "rb") as f:  # count newlines in binary
                return f.read().count(b"\n")
        except Exception as e:
            logger.warning(f"⚠️ Could not read file: {file_path} ({e})")
            return -1  # or None

    def _detect_languages(self, files: List[FileInfo]) -> Tuple[Dict[str, int], str]:

        ext_lang_map = {
            ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".java": "Java",
            ".cpp": "C++", ".c": "C", ".cs": "C#", ".go": "Go", ".rb": "Ruby",
        }

        lang_count = Counter()
        for file in files:
            lang = ext_lang_map.get(file.ext)
            if lang:
                lang_count[lang] += 1

        languages = dict(lang_count)
        primary = lang_count.most_common(1)[0][0] if lang_count else ""

        return languages, primary

    def _find_entry_points(self, files: List[FileInfo]) -> List[str]:
        # Heuristics-based search for entry points
        entry_points = []

        # Common entry point files (a fallback)
        common_entry_files = {"main.py", "index.js", "app.py", "server.py", "run.py", "cli.py"}
        
        # Scan through files and identify possible entry points
        for file in files:
            file_path = file.path
            file_name = os.path.basename(file_path)

            # First, check if the file is in the common entry file list
            if file_name in common_entry_files:
                entry_points.append(file_path)
                continue  # Skip further checks for these files

            # Check if the file contains a 'main' function or entry-like code (Python, JS, etc.)
            if self._contains_main_function(file_path):
                entry_points.append(file_path)

        # Log detected entry points
        if entry_points:
            logger.info(f"🚀 Detected entry points: {entry_points}")
        else:
            logger.info("⚠️ No obvious entry points found.")

        return entry_points

    def _contains_main_function(self, file_path: str) -> bool:
        """Check if the file contains a main function or entry point."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Check for Python main function (if __name__ == "__main__":)
                if re.search(r'\s*if\s+__name__\s*==\s*["\']__main__["\']\s*:', content):
                    return True
                
                # Check for JavaScript main function (function main())
                if re.search(r'\bfunction\s+main\s*\(', content):
                    return True

                # Add more language checks here as needed (e.g., Go, Ruby)

                # Could also check for "run" or "start" functions, or other specific patterns
                if re.search(r'\bdef\s+run\s*\(', content):  # Common for CLI-based Python apps
                    return True

        except Exception as e:
            logger.warning(f"⚠️ Error reading file {file_path}: {e}")

        return False

    def _extract_documents(self):
        """Scan the entire project for documentation files (e.g., README.md, LICENSE, CHANGELOG.md, etc.) and extract metadata."""
        docs = []
        # Common documentation filenames to look for
        doc_filenames = [
            'README.md', 'LICENSE', 'CONTRIBUTING.md', 'CHANGELOG.md', 
            'USAGE.md', 'INSTALL.md', 'TODO.md', 'docs', 'docs/index.rst'
        ]
        
        # Walk through the entire project directory
        for root, dirs, files in os.walk(self.project_path):
            for doc in doc_filenames:
                doc_path = os.path.join(root, doc)
                if os.path.exists(doc_path):
                    file_metadata = self._get_documentation_metadata(doc_path)
                    docs.append(file_metadata)
        
        return docs

    def _get_documentation_metadata(self, doc_path: str) -> Dict[str, Optional[str]]:
        """Helper method to get detailed metadata for a documentation file."""
        # Extract file extension
        _, ext = os.path.splitext(doc_path)
        ext = ext.lower().strip() if ext else "no_ext"

        # Extract basic metadata: file path, extension
        file_metadata = {
            'path': doc_path,
            'ext': ext,
            'purpose': self._detect_documentation_purpose(doc_path),  # Purpose based on file name or content
        }

        return file_metadata

    def _detect_documentation_purpose(self, doc_path: str) -> Optional[str]:
        """Heuristic to determine the purpose of a documentation file based on its name or contents."""
        # Basic checks based on the filename (this could be expanded further)
        if 'README' in doc_path:
            return 'Overview of the project'
        elif 'LICENSE' in doc_path:
            return 'Licensing information'
        elif 'CONTRIBUTING' in doc_path:
            return 'Guidelines for contributing'
        elif 'CHANGELOG' in doc_path:
            return 'Project changelog'
        elif 'USAGE' in doc_path:
            return 'Usage instructions'
        elif 'INSTALL' in doc_path:
            return 'Installation instructions'
        elif 'TODO' in doc_path:
            return 'List of TODOs or roadmap'
        elif 'docs' in doc_path:
            return 'Project documentation files (index or other content)'
        else:
            return 'General documentation'

    def _detect_dependencies(self) -> Dict[str, str]:
        """Detect dependencies from files like requirements.txt, package.json, etc."""
        dep_files = {}
        for dep_file in ['requirements.txt', 'package.json', 'Pipfile']:
            dep_path = os.path.join(self.project_path, dep_file)
            if os.path.exists(dep_path):
                with open(dep_path, 'r') as file:
                    content = file.read()
                    # For simplicity, assuming dependencies are in a basic format, you can extend this
                    if dep_file == 'requirements.txt':
                        dep_files[dep_file] = content
                    elif dep_file == 'package.json':
                        dep_files[dep_file] = content  # Parse dependencies from JSON
                    elif dep_file == 'Pipfile':
                        dep_files[dep_file] = content  # Parse dependencies from Pipfile
        return dep_files
    
    def _extract_symbols(self, files_info: List[FileInfo]) -> List[SymbolInfo]:
        """Extract symbols like functions, classes, and imports from Python files."""
        symbols = []
        
        for file_info in files_info:
            # Skip non-Python files (e.g., .md, .log, .json, .toml, etc.)
            if file_info.ext != ".py":
                continue
            
            file_path = os.path.join(self.project_path, file_info.path)
            symbol_info = SymbolInfo(path=file_path)

            # Only read Python files
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Extract classes, functions, and imports using regex
                symbol_info.classes = re.findall(r'class (\w+)', content)
                symbol_info.functions = re.findall(r'def (\w+)', content)
                symbol_info.imports = re.findall(r'import (\w+)', content)

            symbols.append(symbol_info)
        
        return symbols
    
    def _detect_runtime_envs(self) -> List[str]:
        """Detect runtime environments like Dockerfile, .env, and virtual environments."""
        envs = []
        
        # Check for Dockerfile or .env
        for env_file in ['Dockerfile', '.env']:
            env_path = os.path.join(self.project_path, env_file)
            if os.path.exists(env_path):
                envs.append(env_file)
        
        # Check for virtual environments
        possible_venv_dirs = ['venv', 'env', 'myenv', 'virtualenv']
        for root, dirs, _ in os.walk(self.project_path):
            for dir_name in dirs:
                if dir_name.lower() in possible_venv_dirs:
                    venv_path = os.path.join(root, dir_name)
                    # Check if it contains a 'pyvenv.cfg' file, which is an indicator of a Python virtual environment
                    if os.path.exists(os.path.join(venv_path, 'pyvenv.cfg')):
                        envs.append(f"Virtual Environment: {venv_path}")
        
        return envs

    def _detect_ci_cd(self) -> List[str]:
        """Detect CI/CD configurations (e.g., GitHub Actions, GitLab CI)."""
        ci_cd_files = []
        for ci_file in ['.github', '.gitlab-ci.yml']:
            ci_path = os.path.join(self.project_path, ci_file)
            if os.path.exists(ci_path):
                ci_cd_files.append(ci_path)
        return ci_cd_files

    def _check_dockerfile_makefile(self) -> Tuple[bool, bool]:
        """Check if the project contains Dockerfile and Makefile."""
        has_dockerfile = os.path.exists(os.path.join(self.project_path, 'Dockerfile'))
        has_makefile = os.path.exists(os.path.join(self.project_path, 'Makefile'))
        return has_dockerfile, has_makefile