from __future__ import annotations

from pathlib import Path
from typing import Optional

from docx import Document


SCENARIO_TITLE = "911 CALL QUALITY ASSESSMENT"


def build_single_scenario_template(*, input_docx: str, output_docx: str, scenario_index: int = 1) -> None:
    """
    Builds a template containing only one scenario (default: second scenario) from a report docx
    that contains multiple scenario blocks.
    """
    in_path = Path(input_docx)
    out_path = Path(output_docx)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    doc = Document(str(in_path))
    matching = [p for p in doc.paragraphs if p.text.strip() == SCENARIO_TITLE]
    if len(matching) <= scenario_index:
        raise ValueError(
            f"Expected at least {scenario_index + 1} scenarios, found {len(matching)} occurrences "
            f"of '{SCENARIO_TITLE}'."
        )

    start_para_el = matching[scenario_index]._p  # python-docx internal element for the paragraph

    body = doc.element.body
    children = list(body)
    start_idx = None
    for i, child in enumerate(children):
        if child is start_para_el:
            start_idx = i
            break

    if start_idx is None:
        # Fallback: don't modify layout if we can't find the exact element identity.
        raise RuntimeError("Could not locate scenario start element in doc body.")

    # Remove all children before the scenario start.
    for child in children[:start_idx]:
        body.remove(child)

    doc.save(str(out_path))


def main() -> None:
    # Default inputs based on the expected source report file name.
    repo_root = Path(__file__).resolve().parent.parent
    input_docx = repo_root / "call-grading-report.docx"
    output_docx = repo_root / "templates" / "call-grading-template.docx"

    if not input_docx.exists():
        raise SystemExit(f"Missing input docx: {input_docx}")

    build_single_scenario_template(input_docx=str(input_docx), output_docx=str(output_docx), scenario_index=1)
    print(f"Template written to: {output_docx}")


if __name__ == "__main__":
    main()

