# Academic PDF to Markdown Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and run an offline batch converter that turns the 81 academic PDFs in `knowledge/source/論文_pdf/` into structured Markdown in `knowledge/source/論文_md/`, records quality signals, and supplies evidence for deciding whether low-cost API refinement is necessary.

**Architecture:** A small Python package converts every PDF page into a common coordinate-bearing block model, routes only poor text-layer pages through Tesseract, reconstructs page reading order, removes running matter and footnotes, extracts academic sections, and renders a fixed Markdown schema. A CLI isolates failures per paper and writes an atomic batch report; API refinement remains outside the first implementation and is considered only after reviewing offline quality evidence.

**Tech Stack:** Python 3.11, PyMuPDF, pytesseract, Pillow, Tesseract `chi_sim+eng`, pytest, standard-library dataclasses/argparse/json/tempfile.

---

## File map

- Create `requirements-paper-converter.txt`: reproducible converter-only Python dependencies.
- Create `scripts/paper_converter/__init__.py`: package exports and converter version.
- Create `scripts/paper_converter/models.py`: shared immutable block/page/metadata/quality/result models.
- Create `scripts/paper_converter/preflight.py`: dependency checks and per-page native-text quality metrics.
- Create `scripts/paper_converter/extraction.py`: native PyMuPDF block extraction and page routing.
- Create `scripts/paper_converter/ocr.py`: 300-DPI page rendering and Tesseract box conversion.
- Create `scripts/paper_converter/layout.py`: column classification and reading-order reconstruction.
- Create `scripts/paper_converter/cleanup.py`: repeated running-matter, page number, and footnote filtering.
- Create `scripts/paper_converter/structure.py`: filename/first-page metadata and academic section extraction.
- Create `scripts/paper_converter/render.py`: fixed Markdown output and atomic file writing.
- Create `scripts/paper_converter/quality.py`: observable confidence scores and warnings.
- Create `scripts/paper_converter/pipeline.py`: one-paper conversion orchestration.
- Create `scripts/convert_papers_to_markdown.py`: batch CLI and JSON report orchestration.
- Create `tests/paper_converter/`: focused unit and integration tests matching the modules above.
- Generate `knowledge/source/論文_md/*.md`: offline conversion results, never inputs.
- Generate `knowledge/source/論文_md/_conversion_report.json`: batch evidence used for API assessment.
- Create `docs/superpowers/reports/2026-07-11-pdf-conversion-api-assessment.md`: offline findings and API recommendation.

### Task 1: Shared models and dependency preflight

**Files:**
- Create: `requirements-paper-converter.txt`
- Create: `scripts/paper_converter/__init__.py`
- Create: `scripts/paper_converter/models.py`
- Create: `scripts/paper_converter/preflight.py`
- Test: `tests/paper_converter/test_preflight.py`

- [ ] **Step 1: Write the failing preflight tests**

```python
from scripts.paper_converter.models import BoundingBox, TextBlock
from scripts.paper_converter.preflight import native_text_metrics, should_ocr


def test_native_text_metrics_accepts_readable_chinese():
    blocks = [TextBlock(0, BoundingBox(10, 10, 500, 100), "家庭暴力防治研究" * 20, 12.0, "native")]
    metrics = native_text_metrics(blocks, page_width=600, page_height=800)
    assert metrics.character_count == 160
    assert metrics.valid_character_ratio == 1.0
    assert should_ocr(metrics) is False


def test_empty_or_garbled_page_routes_to_ocr():
    assert should_ocr(native_text_metrics([], 600, 800)) is True
    blocks = [TextBlock(0, BoundingBox(0, 0, 10, 10), "\ufffd\ufffd\ufffd", 8.0, "native")]
    assert should_ocr(native_text_metrics(blocks, 600, 800)) is True
```

- [ ] **Step 2: Run the tests and verify the missing-module failure**

Run: `python3 -m pytest tests/paper_converter/test_preflight.py -v`

Expected: FAIL during collection because `scripts.paper_converter` does not exist.

- [ ] **Step 3: Add exact dependency pins and common dataclasses**

```text
PyMuPDF==1.27.2.2
pytesseract==0.3.13
Pillow==12.2.0
```

Implement frozen `BoundingBox`, `TextBlock`, `TextMetrics`, `PageContent`, `PaperMetadata`, `StructuredPaper`, `QualityScores`, and `ConversionResult` dataclasses. `TextBlock` fields must match the tests: `page_number`, `bbox`, `text`, `font_size`, and `source`; `BoundingBox` exposes `width`, `height`, `center_x`, and normalized coordinate helpers. `StructuredPaper` owns `metadata`, `abstract`, `body`, `references`, and their evidence states; `ConversionResult` owns the input/output paths, page statistics, layout labels, rendered Markdown, quality scores, warnings, errors, status, and elapsed time used by the JSON report.

- [ ] **Step 4: Implement deterministic text metrics and OCR thresholding**

```python
VALID_CHARACTER = re.compile(r"[\u3400-\u9fffA-Za-z0-9]")


def native_text_metrics(blocks, page_width, page_height):
    text = "".join(block.text for block in blocks)
    visible = [char for char in text if not char.isspace()]
    valid = sum(bool(VALID_CHARACTER.match(char)) for char in visible)
    replacement = text.count("\ufffd")
    return TextMetrics(
        character_count=len(visible),
        valid_character_ratio=valid / max(1, len(visible)),
        replacement_character_ratio=replacement / max(1, len(visible)),
        block_count=len(blocks),
    )


def should_ocr(metrics):
    return (
        metrics.character_count < 80
        or metrics.valid_character_ratio < 0.55
        or metrics.replacement_character_ratio > 0.05
    )
```

Add `check_dependencies()` that verifies importable Python packages, the `tesseract` executable, and both `chi_sim` and `eng`; return actionable error strings rather than secrets or environment dumps.

- [ ] **Step 5: Run focused tests**

Run: `python3 -m pytest tests/paper_converter/test_preflight.py -v`

Expected: 2 passed.

- [ ] **Step 6: Commit the foundation**

```bash
git add requirements-paper-converter.txt scripts/paper_converter tests/paper_converter/test_preflight.py
git commit -m "feat: add paper conversion data model and preflight"
```

### Task 2: Native extraction and page-level OCR fallback

**Files:**
- Create: `scripts/paper_converter/extraction.py`
- Create: `scripts/paper_converter/ocr.py`
- Test: `tests/paper_converter/test_extraction.py`

- [ ] **Step 1: Write failing extraction tests using temporary PDFs**

```python
import fitz
from scripts.paper_converter.extraction import extract_pages


def test_extract_pages_keeps_native_page_and_ocrs_blank_page(tmp_path, monkeypatch):
    path = tmp_path / "mixed.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Readable native English text " * 10)
    doc.new_page()
    doc.save(path)
    monkeypatch.setattr(
        "scripts.paper_converter.extraction.ocr_page",
        lambda document, number: [],
    )
    pages = extract_pages(path)
    assert pages[0].source == "native"
    assert pages[1].source == "ocr"
```

Add a second test that monkeypatches `pytesseract.image_to_data` and asserts OCR rows with confidence below 30 are discarded while retained rows become `TextBlock(source="ocr")` with PDF-coordinate bounding boxes.

- [ ] **Step 2: Verify tests fail because extraction functions are absent**

Run: `python3 -m pytest tests/paper_converter/test_extraction.py -v`

Expected: FAIL importing `extract_pages` or `ocr_page`.

- [ ] **Step 3: Implement native span extraction**

Use `page.get_text("dict", sort=False)`. Convert every non-empty text span to a `TextBlock`, preserve the span font size, join spans belonging to the same PyMuPDF line, and retain page width/height/rotation in `PageContent`. Do not trust PyMuPDF's global sort order; layout owns ordering.

- [ ] **Step 4: Implement 300-DPI OCR box extraction**

Render with `fitz.Matrix(300 / 72, 300 / 72)`, create a Pillow image directly from pixmap bytes, call `pytesseract.image_to_data(..., lang="chi_sim+eng", config="--psm 3", output_type=Output.DICT)`, group accepted words by `(block_num, par_num, line_num)`, and scale OCR pixel coordinates back to PDF coordinates.

- [ ] **Step 5: Implement per-page routing and explicit OCR failure state**

For each page, calculate native metrics; call `ocr_page` only if `should_ocr` is true. An OCR exception produces `PageContent(source="ocr", blocks=[], errors=[...])` and does not silently reuse known-bad native text.

- [ ] **Step 6: Run extraction tests**

Run: `python3 -m pytest tests/paper_converter/test_extraction.py -v`

Expected: all tests pass.

- [ ] **Step 7: Commit extraction**

```bash
git add scripts/paper_converter/extraction.py scripts/paper_converter/ocr.py tests/paper_converter/test_extraction.py
git commit -m "feat: extract native text with page-level OCR fallback"
```

### Task 3: Layout classification and reading order

**Files:**
- Create: `scripts/paper_converter/layout.py`
- Test: `tests/paper_converter/test_layout.py`

- [ ] **Step 1: Write failing synthetic-layout tests**

```python
from scripts.paper_converter.layout import classify_layout, order_blocks
from scripts.paper_converter.models import BoundingBox, TextBlock


def block(x0, y0, x1, y1, text, size=10):
    return TextBlock(0, BoundingBox(x0, y0, x1, y1), text, size, "native")


def test_two_columns_read_left_before_right():
    blocks = [
        block(320, 100, 560, 150, "右一"), block(40, 180, 280, 230, "左二"),
        block(40, 100, 280, 150, "左一"), block(320, 180, 560, 230, "右二"),
    ]
    assert classify_layout(blocks, 600, 800) == "two_column"
    assert [b.text for b in order_blocks(blocks, 600, 800)] == ["左一", "左二", "右一", "右二"]


def test_cross_column_heading_precedes_both_columns():
    blocks = [
        block(80, 30, 520, 70, "一、研究背景", 18),
        block(40, 100, 280, 150, "左"), block(320, 100, 560, 150, "右"),
    ]
    assert [b.text for b in order_blocks(blocks, 600, 800)] == ["一、研究背景", "左", "右"]
```

Add single-column and narrow-left-sidebar fixtures so the classification vocabulary covers `single_column`, `two_column`, `spanning_two_column`, and `sidebar_complex`.

- [ ] **Step 2: Run and verify missing layout functions**

Run: `python3 -m pytest tests/paper_converter/test_layout.py -v`

Expected: FAIL importing the layout functions.

- [ ] **Step 3: Implement explainable gutter detection**

Ignore the top and bottom 8% for classification. Build horizontal occupancy intervals from blocks wider than 15% and narrower than 60% of the page. A stable empty band within 40–60% of page width, supported by blocks on both sides, is a two-column gutter. A narrow peripheral cluster plus a wide main cluster is `sidebar_complex`; otherwise use `single_column`.

- [ ] **Step 4: Implement segmented reading order**

Split spanning blocks (width at least 68% of the page or crossing the gutter by more than 10% on both sides) from column blocks. Sweep from top to bottom: output spanning blocks at their Y position, then order intervening blocks by left column Y followed by right column Y. Single-column pages use `(y0, x0)`. Preserve an `ambiguous_layout` warning when no stable split exists.

- [ ] **Step 5: Run layout tests**

Run: `python3 -m pytest tests/paper_converter/test_layout.py -v`

Expected: all tests pass.

- [ ] **Step 6: Commit layout support**

```bash
git add scripts/paper_converter/layout.py tests/paper_converter/test_layout.py
git commit -m "feat: reconstruct academic page reading order"
```

### Task 4: Running matter and footnote cleanup

**Files:**
- Create: `scripts/paper_converter/cleanup.py`
- Test: `tests/paper_converter/test_cleanup.py`

- [ ] **Step 1: Write failing cleanup tests**

Create a three-page fixture where `政法论坛 2022年第3期` repeats above 8% page height, changing page numbers repeat below 94%,正文 occupies the middle, and a small-font `① 参见……` block follows a bottom separator. Assert the repeated header, page number, and footnote are removed, while inline `正文引用①仍保留` and a final `参考文献` section remain.

- [ ] **Step 2: Run and verify failure**

Run: `python3 -m pytest tests/paper_converter/test_cleanup.py -v`

Expected: FAIL importing cleanup functions.

- [ ] **Step 3: Implement repeated-line normalization**

Normalize spaces, replace standalone Arabic/Roman page numbers with `<PAGE>`, and count short top/bottom strings across pages. Treat a candidate as running matter only when it occurs on at least `max(2, ceil(page_count * 0.4))` pages in the same vertical zone.

- [ ] **Step 4: Implement conservative footnote filtering**

A block is a removable footnote only when all are true: it is below 72% page height, its font is at most 85% of the page body median, and it begins with a footnote marker or lies below a detected separator. Stop footnote removal after an independent `参考文献|文献|References` heading. Ambiguous blocks remain and add `possible_footnote_leak`.

- [ ] **Step 5: Run cleanup tests**

Run: `python3 -m pytest tests/paper_converter/test_cleanup.py -v`

Expected: all tests pass.

- [ ] **Step 6: Commit cleanup**

```bash
git add scripts/paper_converter/cleanup.py tests/paper_converter/test_cleanup.py
git commit -m "feat: remove running matter and page footnotes"
```

### Task 5: Academic metadata and section extraction

**Files:**
- Create: `scripts/paper_converter/structure.py`
- Test: `tests/paper_converter/test_structure.py`

- [ ] **Step 1: Write failing extraction tests**

```python
from scripts.paper_converter.structure import parse_filename, extract_structure


def test_filename_supplies_title_and_author_candidates():
    title, authors = parse_filename("家庭暴力的正当防卫-陈兴良.pdf")
    assert title == "家庭暴力的正当防卫"
    assert authors == ["陈兴良"]


def test_extracts_fixed_academic_sections(sample_ordered_pages):
    paper = extract_structure(sample_ordered_pages, "家庭暴力的正当防卫-陈兴良.pdf")
    assert paper.metadata.title == "家庭暴力的正当防卫"
    assert paper.metadata.authors == ["陈兴良"]
    assert paper.metadata.institutions == ["北京大学"]
    assert paper.metadata.journal == "政法论坛"
    assert paper.metadata.published_at == "2022-05"
    assert paper.abstract.startswith("家庭暴力是")
    assert paper.body.startswith("在通常情况下")
    assert paper.references.startswith("[1]")
```

Add tests for underscore filenames, multiple authors, missing abstract (`原文未載` only when the first body heading is confidently found), uncertain abstract (`未識別`), Chinese/English reference headings, and author-biography institution lines.

- [ ] **Step 2: Run and verify missing structure functions**

Run: `python3 -m pytest tests/paper_converter/test_structure.py -v`

Expected: FAIL importing structure functions.

- [ ] **Step 3: Implement filename and first-page candidate extraction**

Split at the final `-` or `_` only when the suffix resembles 1–4 Chinese names or `本刊编辑部`. Normalize spaces in title candidates. Rank first-page title blocks using font size, top position, centeredness, width, and similarity to the filename title; rank author blocks below the title using filename agreement.

- [ ] **Step 4: Implement journal, date, institution, and boundaries**

Recognize journal/volume headers and `YYYY年M月`, English month, or `YYYY年第N期`; normalize dates to `YYYY-MM` or `YYYY`. Search author biography and parenthesized affiliation lines for `大学|学院|研究院|研究所|法院|检察院|中心|机构`. Extract abstract and references using anchored headings, and preserve heading candidates for Markdown rendering.

- [ ] **Step 5: Run structure tests**

Run: `python3 -m pytest tests/paper_converter/test_structure.py -v`

Expected: all tests pass.

- [ ] **Step 6: Commit structure extraction**

```bash
git add scripts/paper_converter/structure.py tests/paper_converter/test_structure.py
git commit -m "feat: extract academic metadata and sections"
```

### Task 6: Markdown rendering and observable quality scoring

**Files:**
- Create: `scripts/paper_converter/render.py`
- Create: `scripts/paper_converter/quality.py`
- Test: `tests/paper_converter/test_render_quality.py`

- [ ] **Step 1: Write failing renderer and score tests**

Assert exact heading order `#`, `## 作者`, `## 作者機構`, `## 期刊`, `## 發表時間`, `## 摘要`, `## 正文`, `## 文獻`; assert an absent source section renders `原文未載`, an uncertain field renders `未識別`, a Chinese numbered body heading becomes `###`, and an output file is unchanged if a simulated write fails before `os.replace`.

Score fixtures must show that OCR errors, missing metadata, `ambiguous_layout`, very short body text, and missing pages reduce only their documented score components and appear in warnings.

- [ ] **Step 2: Run and verify failure**

Run: `python3 -m pytest tests/paper_converter/test_render_quality.py -v`

Expected: FAIL importing renderer/scorer functions.

- [ ] **Step 3: Implement fixed Markdown rendering and paragraph joining**

Render all eight sections unconditionally. Join adjacent wrapped Chinese lines unless the previous line ends in sentence punctuation or the next line matches a list/heading/legal-article pattern. Escape accidental Markdown headings in ordinary text. Use `tempfile.NamedTemporaryFile(dir=target.parent)` followed by `os.replace` for atomic output.

- [ ] **Step 4: Implement quality scores**

Return 0–1 `metadata`, `layout`, `completeness`, and weighted `total` scores. Base metadata on field evidence; layout on classified-page fraction and ambiguity warnings; completeness on processed-page fraction, body length relative to extracted text, and OCR errors. Record thresholds and weights as named module constants so the report is reproducible.

- [ ] **Step 5: Run focused tests**

Run: `python3 -m pytest tests/paper_converter/test_render_quality.py -v`

Expected: all tests pass.

- [ ] **Step 6: Commit rendering and quality**

```bash
git add scripts/paper_converter/render.py scripts/paper_converter/quality.py tests/paper_converter/test_render_quality.py
git commit -m "feat: render paper markdown with quality signals"
```

### Task 7: One-paper pipeline and resilient batch CLI

**Files:**
- Create: `scripts/paper_converter/pipeline.py`
- Create: `scripts/convert_papers_to_markdown.py`
- Test: `tests/paper_converter/test_pipeline_cli.py`

- [ ] **Step 1: Write failing pipeline and CLI tests**

Use temporary input/output directories with two tiny PDFs. Monkeypatch pipeline conversion so one succeeds and one raises `EncryptedPdfError`. Assert the CLI returns a nonzero partial-failure exit code, writes one Markdown, records both files in `_conversion_report.json`, and never stops after the failed file. Add tests for default skip, `--overwrite`, one-file `--input`, and `--report-only` not writing Markdown.

- [ ] **Step 2: Run and verify failure**

Run: `python3 -m pytest tests/paper_converter/test_pipeline_cli.py -v`

Expected: FAIL because pipeline and CLI are absent.

- [ ] **Step 3: Implement one-paper orchestration**

`convert_paper(input_path) -> ConversionResult` must call extraction, layout, cross-page cleanup, structure extraction, quality scoring, and rendering-data creation in that order. Define explicit exception types for dependency, encrypted PDF, damaged PDF, OCR, and output errors. Include elapsed milliseconds and converter version.

- [ ] **Step 4: Implement the batch CLI**

Use repository-relative defaults based on `Path(__file__).resolve().parents[1]`. Sort PDFs by Unicode filename, isolate every call with `try/except`, preserve earlier report entries for skipped successes, and atomically write UTF-8 JSON with `ensure_ascii=False, indent=2`. Exit 0 for all success/skipped, 1 for partial document failures, and 2 for CLI/dependency errors.

- [ ] **Step 5: Run pipeline tests and the entire suite**

Run: `python3 -m pytest tests/paper_converter/test_pipeline_cli.py -v`

Expected: all focused tests pass.

Run: `python3 -m pytest tests/paper_converter -v`

Expected: all converter tests pass.

- [ ] **Step 6: Commit the runnable converter**

```bash
git add scripts/paper_converter/pipeline.py scripts/convert_papers_to_markdown.py tests/paper_converter/test_pipeline_cli.py
git commit -m "feat: add resilient academic PDF batch converter"
```

### Task 8: Calibrate against representative real PDFs

**Files:**
- Modify: converter modules whose measured heuristic is wrong
- Create: `tests/paper_converter/fixtures/expected_samples.json`
- Create: `tests/paper_converter/test_real_samples.py`

- [ ] **Step 1: Select and record four fixtures without copying source PDFs**

Reference repository-relative source names in JSON for: `家庭暴力的正当防卫-陈兴良.pdf` (standard journal), `司法为何淡化家庭暴力-贺欣肖惠娜.pdf` (sidebar plus two columns), the lowest-density first-page document, and one temporary image-only derivative created under pytest's temporary directory to force OCR.

- [ ] **Step 2: Write failing real-sample assertions**

For each real source assert known title/author, body length above a conservative threshold, first body paragraph prefix, no repeated journal header on later pages, no isolated page numbers, and reference preservation when present. For the OCR fixture assert `ocr_page_count >= 1` and recovered Chinese text contains the seeded sentence.

- [ ] **Step 3: Run real-sample tests and inspect failures**

Run: `python3 -m pytest tests/paper_converter/test_real_samples.py -v`

Expected: initial failures identify concrete threshold or boundary mistakes rather than import/runtime errors.

- [ ] **Step 4: Make the smallest evidence-based heuristic corrections**

Change only constants or rules tied to observed failures. Add a regression assertion for every correction; do not add filename-specific branches.

- [ ] **Step 5: Re-run all converter tests**

Run: `python3 -m pytest tests/paper_converter -v`

Expected: all tests pass, including four representative samples.

- [ ] **Step 6: Commit calibrated rules**

```bash
git add scripts/paper_converter tests/paper_converter
git commit -m "test: calibrate converter on representative papers"
```

### Task 9: Run all 81 PDFs offline and assess API necessity

**Files:**
- Generate: `knowledge/source/論文_md/*.md`
- Generate: `knowledge/source/論文_md/_conversion_report.json`
- Create: `docs/superpowers/reports/2026-07-11-pdf-conversion-api-assessment.md`

- [ ] **Step 1: Verify prerequisites and run the full suite**

Run: `python3 -m pytest tests/paper_converter -v`

Expected: all tests pass.

Run: `python3 scripts/convert_papers_to_markdown.py --check`

Expected: Python dependencies, Tesseract, `chi_sim`, and `eng` all report available.

- [ ] **Step 2: Perform the offline full run**

Run: `python3 scripts/convert_papers_to_markdown.py --overwrite`

Expected: 81 inputs attempted; one Markdown per successful input; report written even if individual papers fail.

- [ ] **Step 3: Validate output invariants mechanically**

Run a checker that asserts output count matches successful report entries, every Markdown has the eight headings in order, no output is empty, no unexpected files were written into `論文_pdf`, and report page totals match PyMuPDF page counts.

- [ ] **Step 4: Inspect stratified quality samples**

Read at least three highest-, three middle-, and all lowest-confidence results, plus every result with OCR or hard warnings. Record metadata errors, column-order errors, footnote leaks, over-deletion, and reference-boundary errors with filenames and report signals.

- [ ] **Step 5: Write the API assessment**

Create `docs/superpowers/reports/2026-07-11-pdf-conversion-api-assessment.md` containing corpus statistics, error categories, representative evidence, which problems deterministic rules can fix, which might benefit from a small structured-output model, privacy/cost constraints, and one of three recommendations: `offline sufficient`, `metadata-only API`, or `targeted page/API refinement`.

- [ ] **Step 6: Test API only if the offline evidence supports it**

If the recommendation is not `offline sufficient`, use current official OpenAI documentation to choose the lowest-cost model that supports the required structured output. Test only representative low-confidence first-page text/block summaries, measure exact tokens/cost and accuracy changes, and append results to the assessment. Do not implement `--api-refine` unless the measured improvement is material and repeatable.

- [ ] **Step 7: Run final verification**

Run: `python3 -m pytest tests/paper_converter -v`

Expected: all tests pass.

Run: `git diff --check`

Expected: no whitespace errors in files created or modified by this plan.

- [ ] **Step 8: Commit the assessment separately from generated corpus files**

```bash
git add docs/superpowers/reports/2026-07-11-pdf-conversion-api-assessment.md
git commit -m "docs: assess API need for paper conversion"
```

Generated Markdown and `_conversion_report.json` remain available in the user-authorized output directory. Add them to version control only if the user explicitly requests corpus outputs to be tracked.
