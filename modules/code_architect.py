import os
from pathlib import Path

class WholeCodebaseArchitect:
    def __init__(self, root_dir: str):
        """Initializes the architect module targeted at a specific local directory."""
        self.root_dir = Path(root_dir)

    def scan_repository(self, allowed_extensions=None) -> str:
        """
        Traverses the local project directory structure and indexes code files, 
        maintaining structural context for cross-file refactoring.
        """
        if allowed_extensions is None:
            allowed_extensions = {'.py', '.js', '.ts', '.json', '.dockerfile', '.yml', '.yaml'}

        repo_representation = []

        if not self.root_dir.exists():
            return "Error: Local repository path does not exist."

        for root, _, files in os.walk(self.root_dir):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in allowed_extensions:
                    try:
                        relative_path = file_path.relative_to(self.root_dir)
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        repo_representation.append(f"### FILE: {relative_path}\n{content}\n")
                    except Exception:
                        continue

        return "\n".join(repo_representation)
