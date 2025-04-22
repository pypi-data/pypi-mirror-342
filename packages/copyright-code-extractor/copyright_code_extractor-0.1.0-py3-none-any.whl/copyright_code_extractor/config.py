import json
from pathlib import Path
from typing import List, Optional, Set

from pydantic import BaseModel, Field

# Define the default config filename as a constant
DEFAULT_CONFIG_FILENAME = ".copyright-extractor.json"


class Settings(BaseModel):
    """Configuration settings for the code extractor."""

    project_root: Path = Field(..., description="Path to the root of the project to analyze.")
    output_file: Path = Field(
        default=Path("extracted_code.docx"),
        description="Path to save the generated DOCX file.",
    )
    lines_to_extract: int = Field(
        default=3000, description="Total number of code lines to extract."
    )
    extract_all: bool = Field(
        default=False,
        description="Extract all lines instead of the first N lines (for 'first 30 + last 30 pages' rule).",
    )
    source_root: Optional[Path] = Field(
        default=None,
        description="Optional sub-directory within project_root to treat as the source code root.",
    )
    ignore_patterns: List[str] = Field(
        default=[
            ".git",
            ".svn",
            ".hg",
            "__pycache__",
            "node_modules",
            "vendor",
            "build",
            "dist",
            "target", # Rust build output
            ".DS_Store",
            "*.pyc",
            "*.log",
            "*.tmp",
            "*.swp",
            "*.bak",
            ".idea",
            ".vscode",
            ".venv",
            "venv",
            "env",
        ],
        description="List of directory/file patterns to ignore.",
    )
    include_extensions: Optional[List[str]] = Field(
        default=[
            # Web Frontend
            ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".html", ".htm", ".css", ".scss", ".sass", ".less",
            # Backend / General
            ".py", ".java", ".kt", ".scala", ".go", ".rs", ".php", ".rb", ".cs", ".swift", ".m", ".h", ".c", ".cpp", ".hpp",
            # Mobile
            ".dart", # Flutter
            # Other
            # ".sql", ".sh", ".yaml", ".yml", ".json", ".xml", ".gradle", ".properties",
            # Potentially add more as needed
        ],
        description="List of file extensions to include (if None or empty, process all files not ignored).",
    )
    # config_file_name: str = ".copyright-extractor.json" # Removed from model fields

    @property
    def effective_source_root(self) -> Path:
        """Return the absolute path to the effective source root."""
        if self.source_root:
            # Ensure source_root is relative to project_root if provided relatively
            if not self.source_root.is_absolute():
                return (self.project_root / self.source_root).resolve()
            return self.source_root.resolve()
        return self.project_root.resolve()

    def is_ignored(self, path: Path) -> bool:
        """Check if a given path should be ignored based on ignore_patterns."""
        relative_path_parts = path.relative_to(self.project_root).parts
        for pattern in self.ignore_patterns:
            # Simple prefix/exact match for now
            # TODO: Implement more robust glob/pattern matching if needed
            if pattern in relative_path_parts or path.name == pattern:
                return True
        return False

    def is_included_extension(self, path: Path) -> bool:
        """Check if the file extension is in the included list (if defined)."""
        if not self.include_extensions:
            return True # Include all if list is empty or None
        return path.suffix.lower() in self.include_extensions


def load_config(project_root: Path, config_file_override: Optional[Path] = None) -> Settings:
    """Load configuration, prioritizing command-line override, then project file, then defaults."""
    # Use the constant for the default config file name
    config_path = config_file_override or project_root / DEFAULT_CONFIG_FILENAME

    config_data = {"project_root": project_root} # Start with the essential project_root

    if config_path.exists() and config_path.is_file():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                # TODO: Add validation/logging for loaded config
                config_data.update(file_config)
        except Exception as e:
            # TODO: Use Rich for better error reporting
            print(f"Warning: Could not load or parse config file {config_path}: {e}")
            # Proceed with defaults

    # Pydantic will use defaults for keys not present in config_data
    return Settings(**config_data) 
