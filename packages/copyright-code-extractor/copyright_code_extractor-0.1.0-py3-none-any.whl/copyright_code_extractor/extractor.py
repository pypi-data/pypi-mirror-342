import logging
from pathlib import Path
from typing import List, Tuple
import re # Import regex module

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn

from .config import Settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def find_source_files(settings: Settings) -> List[Path]:
    """Recursively find source files based on settings."""
    source_files = []
    root_path = settings.effective_source_root
    logger.info(f"Scanning for source files in: {root_path}")

    for path in root_path.rglob("*"):
        if path.is_dir():
            # Check if the directory itself should be ignored
            if settings.is_ignored(path):
                logger.debug(f"Ignoring directory: {path}")
                # TODO: Need to prevent rglob from descending further? -> Handled by file check below
                continue
        elif path.is_file():
            relative_path = path.relative_to(settings.project_root)
            # Check if the file or any of its parent directories are ignored
            if settings.is_ignored(path):
                logger.debug(f"Ignoring file due to pattern: {relative_path}")
                continue

            # Check if the file extension is included
            if not settings.is_included_extension(path):
                logger.debug(f"Ignoring file due to extension: {relative_path}")
                continue

            source_files.append(path)
            logger.debug(f"Found source file: {relative_path}")
        else:
            logger.debug(f"Skipping non-file/non-dir item: {path}")

    logger.info(f"Found {len(source_files)} potential source files.")
    # Sort files for consistent output
    source_files.sort()
    return source_files


def extract_code_lines(files: List[Path], lines_to_extract: int, extract_all: bool) -> Tuple[List[str], int]:
    """Extract lines of code from the list of files, removing comments robustly."""
    all_lines = []
    total_lines_scanned = 0 # Now represents raw lines scanned before comment removal

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                full_content = f.read()
                total_lines_scanned += full_content.count('\n') + 1 # Approx line count

                # 1. Remove C-style multi-line comments (/* ... */) globally
                content_no_multiline = re.sub(r'/\*.*?\*/', '', full_content, flags=re.DOTALL)

                lines_after_multiline = content_no_multiline.splitlines()
                lines_in_file = []

                for line in lines_after_multiline:
                    # 2. Remove single-line comments (//... or #...)
                    line_no_single_comment = re.sub(r"//.*$|#.*$", "", line)

                    # 3. Remove trailing whitespace only (preserves indentation)
                    clean_line = line_no_single_comment.rstrip()

                    # 4. Keep the line only if it's not empty after all removals
                    if clean_line:
                        lines_in_file.append(clean_line)

                if lines_in_file:
                    # Add a header comment indicating the file path
                    relative_path = file_path.name # TODO: Make this relative to project root?
                    all_lines.append(f"// === File: {relative_path} ===")
                    all_lines.extend(lines_in_file)

                if not extract_all and len(all_lines) >= lines_to_extract:
                    logger.info(f"Reached target line count ({lines_to_extract}) while processing {file_path.name}.")
                    break # Stop reading more files if we have enough lines (and not extracting all)

        except Exception as e:
            logger.warning(f"Could not read file {file_path}: {e}")

    # Adjust log message to reflect lines kept *after* comment removal
    logger.info(f"Total non-empty, comment-stripped lines extracted: {len(all_lines)} (processed approx {total_lines_scanned} raw lines)")

    if extract_all:
        # Keep all lines for the 'first 30 + last 30' rule
        return all_lines, total_lines_scanned
    else:
        # Return only the required number of lines from the beginning
        return all_lines[:lines_to_extract], total_lines_scanned


def create_docx(lines: List[str], output_path: Path, lines_per_page: int = 50):
    """Create a DOCX file with the extracted code lines."""
    document = Document()

    # Set font and paragraph style for code (adjust as needed)
    style = document.styles["Normal"]
    font = style.font
    font.name = "Consolas" # Common monospace font
    font.size = Pt(9)

    paragraph_format = style.paragraph_format
    paragraph_format.space_before = Pt(0)
    paragraph_format.space_after = Pt(0)
    paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    paragraph_format.keep_together = True
    paragraph_format.keep_with_next = True

    # Set CJK font if necessary (important for comments in Chinese etc.)
    rpr = style.element.rPr
    c_fonts = rpr.get_or_add_rFonts()
    c_fonts.set(qn("w:eastAsia"), "SimSun") # Example: SimSun (宋体)

    logger.info(f"Writing {len(lines)} lines to {output_path}...")
    line_count_on_page = 0
    for line in lines:
        # Basic sanitization: Replace non-printable characters (except tab)
        cleaned_line = "".join(c if c.isprintable() or c == '\t' else '?' for c in line)
        # Replace tabs with spaces for better alignment in Word
        cleaned_line = cleaned_line.replace("\t", "    ")

        p = document.add_paragraph(cleaned_line)
        p.style = document.styles["Normal"]
        line_count_on_page += 1

        # Add page break approx every `lines_per_page` lines
        # Note: This is approximate due to line wrapping and font metrics
        if line_count_on_page >= lines_per_page:
            document.add_page_break()
            line_count_on_page = 0

    try:
        document.save(output_path)
        logger.info(f"Successfully saved DOCX file: {output_path}")
    except Exception as e:
        logger.error(f"Failed to save DOCX file {output_path}: {e}")
        raise

def run_extraction(settings: Settings):
    """Main function to orchestrate the extraction process."""
    logger.info(f"Starting code extraction for project: {settings.project_root}")
    logger.info(f"Configuration: {settings.model_dump_json(indent=2)}")

    source_files = find_source_files(settings)
    if not source_files:
        logger.warning("No source files found matching the criteria. Exiting.")
        return

    extracted_lines, total_scanned = extract_code_lines(
        source_files, settings.lines_to_extract, settings.extract_all
    )

    if not extracted_lines:
        logger.warning("No code lines were extracted. Exiting.")
        return

    output_path = settings.output_file
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    create_docx(extracted_lines, output_path)

    logger.info("Extraction process completed.") 
