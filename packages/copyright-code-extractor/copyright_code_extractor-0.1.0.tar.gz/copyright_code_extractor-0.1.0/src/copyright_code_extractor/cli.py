import typer
from pathlib import Path
from typing_extensions import Annotated
from typing import Optional
import logging

from rich.console import Console
from rich.logging import RichHandler

from .config import load_config, Settings, DEFAULT_CONFIG_FILENAME
from .extractor import run_extraction
from . import __init__ as root_package # To potentially get version later

# Setup logging with Rich for nice output
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
)
logger = logging.getLogger("copyright_code_extractor")

app = typer.Typer(
    name="copyright-code-extractor",
    help="A tool to extract source code for China Software Copyright application.",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    if value:
        # TODO: Dynamically get version from pyproject.toml or package metadata
        try:
            from importlib import metadata
            version = metadata.version("copyright-code-extractor")
        except metadata.PackageNotFoundError:
            version = "0.1.0" # Fallback or read from pyproject.toml directly
        console.print(f"Copyright Code Extractor version: {version}")
        raise typer.Exit()


@app.command()
def extract(
    project_path: Annotated[
        Path,
        typer.Argument(
            ..., # Ellipsis means it's required
            help="Path to the root directory of the project to analyze.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    output_file: Annotated[
        Optional[Path],
        typer.Option(
            "-o",
            "--output",
            help="Path to save the generated DOCX file.",
            resolve_path=True,
        ),
    ] = None,
    lines: Annotated[
        Optional[int],
        typer.Option(
            "-l",
            "--lines",
            help="Total number of lines to extract (overrides config file).",
        ),
    ] = None,
    extract_all_flag: Annotated[
        Optional[bool],
        typer.Option(
            "--all",
            help="Extract all lines for 'first 30 + last 30 pages' rule (overrides config file).",
        ),
    ] = None,
    config_file: Annotated[
        Optional[Path],
        typer.Option(
            "-c",
            "--config",
            help=f"Path to a custom configuration file (default: {DEFAULT_CONFIG_FILENAME} in project root).",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "-v",
            "--verbose",
            help="Enable verbose logging.",
        ),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show the application version and exit.",
        ),
    ] = None,
):
    """Extract source code lines from a project directory."""
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled.")

    try:
        settings = load_config(project_path, config_file_override=config_file)

        # Override settings from command line if provided
        if output_file:
            settings.output_file = output_file
        if lines is not None:
            settings.lines_to_extract = lines
        if extract_all_flag is not None:
            settings.extract_all = extract_all_flag

        # Make sure output path is absolute if provided relatively
        if not settings.output_file.is_absolute():
            settings.output_file = (Path.cwd() / settings.output_file).resolve()

        logger.info(f"Starting extraction for project at: {settings.project_root}")
        run_extraction(settings)
        logger.info(f"✅ Extraction complete. Output saved to: {settings.output_file}")

    except Exception as e:
        logger.error(f"❌ An error occurred during extraction: {e}", exc_info=verbose)
        # Optionally re-raise if needed for debugging or specific exit codes
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app() 
