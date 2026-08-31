"""Render fixed-resolution table previews for TA++ v10 feasibility checks.

The output bundle contains PNG preview pages, an equivalent text preview,
a vision-model prompt, metrics, and a short report.
"""

from __future__ import annotations

import argparse
import json
import math
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


DEFAULT_INPUT = Path(
    "lab8/benchmark_data/newData/datasets_skill_v9_copy/healthcare_visit_notes/healthcare_visit_notes.xlsx"
)
DEFAULT_OUTPUT_DIR = Path("lab8/skill-v10/prototypes/visual_preview_feasibility")
DEFAULT_QUERY = "What visit-note signals suggest high urgency?"
PAGE_PADDING = 30
TITLE_HEIGHT = 70
HEADER_HEIGHT = 42
MIN_ROW_HEIGHT = 52


def layout_profile(density: str) -> dict[str, Any]:
    if density == "ocr":
        return {
            "density": "ocr",
            "padding": 16,
            "title_height": 44,
            "header_height": 28,
            "min_row_height": 32,
            "title_font": 18,
            "header_font": 11,
            "cell_font": 10,
            "small_font": 9,
            "line_step": 12,
            "text_cell_limit": 420,
            "other_cell_limit": 90,
            "stretch_rows": False,
            "adaptive_height": True,
            "preferred_widths": {
                "visit_id": 72,
                "department": 118,
                "urgency": 76,
                "age_group": 64,
                "visit_duration_min": 94,
            },
        }
    if density == "compact":
        return {
            "density": "compact",
            "padding": 22,
            "title_height": 56,
            "header_height": 34,
            "min_row_height": 40,
            "title_font": 20,
            "header_font": 13,
            "cell_font": 11,
            "small_font": 10,
            "line_step": 14,
            "text_cell_limit": 320,
            "other_cell_limit": 90,
            "stretch_rows": False,
            "adaptive_height": True,
            "preferred_widths": {
                "visit_id": 82,
                "department": 136,
                "urgency": 92,
                "age_group": 76,
                "visit_duration_min": 112,
            },
        }
    return {
        "density": "readable",
        "padding": PAGE_PADDING,
        "title_height": TITLE_HEIGHT,
        "header_height": HEADER_HEIGHT,
        "min_row_height": MIN_ROW_HEIGHT,
        "title_font": 24,
        "header_font": 16,
        "cell_font": 14,
        "small_font": 12,
        "line_step": 18,
        "text_cell_limit": 240,
        "other_cell_limit": 90,
        "stretch_rows": True,
        "adaptive_height": False,
        "preferred_widths": {
            "visit_id": 92,
            "department": 160,
            "urgency": 112,
            "age_group": 96,
            "visit_duration_min": 130,
        },
    }


def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".csv":
        for encoding in ("utf-8-sig", "utf-8", "latin1", "cp1252"):
            try:
                return pd.read_csv(path, encoding=encoding)
            except UnicodeDecodeError:
                continue
        return pd.read_csv(path, encoding="latin1")
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported input extension: {suffix}")


def load_font(size: int, *, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def clean_cell(value: Any, limit: int) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = " ".join(str(value).replace("\r", " ").replace("\n", " ").split())
    return text[: max(0, limit - 3)] + "..." if len(text) > limit else text


def choose_columns(frame: pd.DataFrame, text_col: str, max_columns: int) -> list[str]:
    preferred = ["visit_id", "department", "urgency", "age_group", "visit_duration_min", text_col]
    selected = [column for column in preferred if column in frame.columns]
    if selected:
        return selected[:max_columns]
    return [str(column) for column in frame.columns[:max_columns]]


def select_preview_rows(frame: pd.DataFrame, text_col: str, sample_rows: int) -> pd.DataFrame:
    target = min(max(0, sample_rows), len(frame))
    if target == 0:
        return frame.head(0).copy()
    if text_col not in frame.columns:
        return frame.sample(n=target, random_state=17).sort_index().copy()

    lengths = frame[text_col].fillna("").astype(str).str.len()
    eligible = frame[text_col].notna()
    if int(eligible.sum()) < 3:
        return frame.sample(n=target, random_state=17).sort_index().copy()

    short_cut = float(lengths[eligible].quantile(1 / 3))
    long_cut = float(lengths[eligible].quantile(2 / 3))
    masks = [
        eligible & (lengths <= short_cut),
        eligible & (lengths > short_cut) & (lengths <= long_cut),
        eligible & (lengths > long_cut),
    ]
    selected: list[Any] = []
    base_quota = max(1, target // 3)
    for bucket_id, mask in enumerate(masks):
        available = frame.index[mask].tolist()
        take = min(len(available), base_quota if bucket_id < 2 else target - len(selected))
        if take > 0:
            selected.extend(frame.loc[available].sample(n=take, random_state=41 + bucket_id).index.tolist())
    if len(selected) < target:
        remaining = frame.index.difference(pd.Index(selected)).tolist()
        selected.extend(remaining[: target - len(selected)])
    ordered = sorted(dict.fromkeys(selected), key=lambda item: frame.index.get_loc(item))[:target]
    return frame.loc[ordered].copy()


def estimate_text_tokens(text: str) -> int:
    return int(math.ceil(len(text) / 4))


def estimate_image_tokens(width: int, height: int, image_count: int) -> dict[str, Any]:
    # These are rough planning estimates only. Real accounting must come from the target provider.
    scale = min(2048 / width, 2048 / height, 1)
    scaled_width = width * scale
    scaled_height = height * scale
    normalize = 768 / min(scaled_width, scaled_height)
    tile_width = scaled_width * normalize
    tile_height = scaled_height * normalize
    tiles_per_image = math.ceil(tile_width / 512) * math.ceil(tile_height / 512)
    high_detail_per_image = 85 + 170 * tiles_per_image

    area = width * height
    area_target = 1_150_000
    area_scale = min(1, math.sqrt(area_target / area))
    area_width = width * area_scale
    area_height = height * area_scale
    area_per_image = math.ceil((area_width * area_height) / 750)
    return {
        "rough_high_detail_tile_total": int(high_detail_per_image * image_count),
        "rough_high_detail_tiles_per_image": int(tiles_per_image),
        "rough_high_detail_tile_dims": [int(round(tile_width)), int(round(tile_height))],
        "rough_area_patch_total": int(area_per_image * image_count),
        "rough_area_patch_resized_dims": [int(round(area_width)), int(round(area_height))],
    }


def estimate_image_tokens_for_pages(image_files: list[dict[str, Any]]) -> dict[str, Any]:
    totals = {"rough_high_detail_tile_total": 0, "rough_area_patch_total": 0, "pages": []}
    for item in image_files:
        estimate = estimate_image_tokens(int(item["width"]), int(item["height"]), 1)
        totals["rough_high_detail_tile_total"] += int(estimate["rough_high_detail_tile_total"])
        totals["rough_area_patch_total"] += int(estimate["rough_area_patch_total"])
        totals["pages"].append({**item, **estimate})
    return totals


def column_widths(columns: list[str], width: int, profile: dict[str, Any]) -> dict[str, int]:
    padding = int(profile["padding"])
    content_width = width - padding * 2
    preferred = dict(profile["preferred_widths"])
    widths: dict[str, int] = {}
    flexible: list[str] = []
    used = 0
    for column in columns:
        if column in preferred:
            widths[column] = preferred[column]
            used += preferred[column]
        else:
            flexible.append(column)
    remaining = max(180, content_width - used)
    for column in flexible:
        widths[column] = max(180, remaining // max(1, len(flexible)))
    return widths


def wrap_for_width(text: str, pixel_width: int, font: ImageFont.ImageFont, draw: ImageDraw.ImageDraw) -> list[str]:
    if not text:
        return [""]
    average = max(5.0, draw.textlength("abcdefghijklmnopqrstuvwxyz", font=font) / 26)
    chars_per_line = max(8, int(pixel_width / average))
    lines: list[str] = []
    for paragraph in text.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=chars_per_line, break_long_words=True) or [""])
    return lines


def render_page(
    page_frame: pd.DataFrame,
    *,
    columns: list[str],
    query: str,
    output_path: Path,
    page_number: int,
    page_count: int,
    width: int,
    height: int,
    density: str,
) -> dict[str, int]:
    profile = layout_profile(density)
    padding = int(profile["padding"])
    title_height = int(profile["title_height"])
    header_height = int(profile["header_height"])
    min_row_height = int(profile["min_row_height"])
    line_step = int(profile["line_step"])
    available_height = height - padding * 2 - title_height - header_height
    if bool(profile.get("stretch_rows")):
        row_height = max(min_row_height, available_height // max(1, len(page_frame)))
    else:
        row_height = min_row_height
    content_height = padding * 2 + title_height + header_height + row_height * max(1, len(page_frame))
    actual_height = min(height, content_height) if bool(profile.get("adaptive_height")) else height
    image = Image.new("RGB", (width, actual_height), "#f8fafc")
    draw = ImageDraw.Draw(image)
    title_font = load_font(int(profile["title_font"]), bold=True)
    header_font = load_font(int(profile["header_font"]), bold=True)
    cell_font = load_font(int(profile["cell_font"]))
    small_font = load_font(int(profile["small_font"]))
    widths = column_widths(columns, width, profile)

    draw.text((padding, max(6, padding - 6)), "TA++ v10 visual preview feasibility", font=title_font, fill="#0f172a")
    draw.text(
        (padding, max(24, padding + int(profile["title_font"]) + 2)),
        f"Query: {query} | page {page_number}/{page_count} | {density} | {width}x{actual_height}px",
        font=small_font,
        fill="#475569",
    )

    y = padding + title_height
    x = padding
    draw.rectangle([padding, y, width - padding, y + header_height], fill="#dbeafe", outline="#93c5fd")
    for column in columns:
        col_width = widths[column]
        draw.text((x + 4, y + max(4, (header_height - int(profile["header_font"])) // 2)), str(column)[:28], font=header_font, fill="#0f172a")
        draw.line([x, y, x, actual_height - padding], fill="#cbd5e1")
        x += col_width
    draw.line([width - padding, y, width - padding, actual_height - padding], fill="#cbd5e1")

    y += header_height
    urgency_fill = {"High": "#fee2e2", "Medium": "#fef3c7", "Low": "#dcfce7"}
    for display_idx, (_row_index, row) in enumerate(page_frame.iterrows()):
        fill = urgency_fill.get(clean_cell(row.get("urgency", ""), 40), "#ffffff" if display_idx % 2 == 0 else "#f1f5f9")
        draw.rectangle([padding, y, width - padding, y + row_height], fill=fill, outline="#cbd5e1")
        x = padding
        for column in columns:
            col_width = widths[column]
            limit = int(profile["text_cell_limit"] if column == "reason_for_visit" else profile["other_cell_limit"])
            value = clean_cell(row.get(column, ""), limit)
            lines = wrap_for_width(value, col_width - 12, cell_font, draw)
            max_lines = max(1, (row_height - 6) // line_step)
            shown = lines[:max_lines]
            if len(lines) > max_lines and shown:
                shown[-1] = shown[-1][: max(0, len(shown[-1]) - 3)] + "..."
            for line_id, line in enumerate(shown):
                draw.text((x + 4, y + 4 + line_id * line_step), line, font=cell_font, fill="#111827")
            x += col_width
        y += row_height
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, optimize=True)
    return {"width": int(width), "height": int(actual_height), "row_height": int(row_height)}


def max_rows_for_resolution(height: int, density: str) -> int:
    profile = layout_profile(density)
    available_height = height - int(profile["padding"]) * 2 - int(profile["title_height"]) - int(profile["header_height"])
    return max(1, available_height // int(profile["min_row_height"]))


def build_text_preview(sample: pd.DataFrame, columns: list[str], query: str) -> str:
    records = []
    for row_index, row in sample.iterrows():
        record = {column: clean_cell(row.get(column, ""), 700) for column in columns}
        record["_row_index"] = int(row_index) if isinstance(row_index, int) else str(row_index)
        records.append(record)
    return json.dumps({"query": query, "preview_records": records}, ensure_ascii=False, indent=2)


def build_prompt(query: str, image_paths: list[Path], metrics: dict[str, Any]) -> str:
    image_list = "\n".join(f"- {path.name}" for path in image_paths)
    return f"""You are evaluating a fixed-resolution visual preview for TA++ v10.

Task: {query}

Inputs:
{image_list}

Use the images only as a lossy data preview. Infer recurring signals, candidate facet families, and useful schema slots. Do not tag exact rows, compute exact counts, or quote precise values from the image. If a candidate facet requires strict row-level evidence, mark it as requiring raw-text tagging.

Return strict JSON with this shape:
{{
  "image_readability": "good|partial|poor",
  "likely_useful_for": ["schema_planning", "analysis_preview", "quality_check"],
  "not_safe_for": ["row_level_tagging", "exact_counts", "numeric_calculation"],
  "candidate_facets": [
    {{"name": "...", "why_visible_in_preview": "...", "requires_raw_data_for_tagging": true}}
  ],
  "v10_decision": {{"keep_visual_preview": true, "reason": "..."}}
}}

Preview metrics:
{json.dumps(metrics, ensure_ascii=False, indent=2)}
"""


def write_report(output_dir: Path, metrics: dict[str, Any]) -> None:
    image_files = ", ".join(item["path"] for item in metrics["image_files"])
    report = f"""# V10 Visual Preview Feasibility Report

Generated at: {metrics['generated_at']}

## Dataset

- Input: `{metrics['input']}`
- Query: {metrics['query']}
- Rows total: {metrics['rows_total']}
- Rows previewed: {metrics['rows_previewed']}
- Columns previewed: {', '.join(metrics['columns_previewed'])}

## Direct Comparison

- Equivalent text preview: {metrics['equivalent_text_preview_chars']} chars, roughly {metrics['equivalent_text_preview_est_tokens_chars_div4']} text tokens at chars/4.
- Visual preview: {metrics['image_count']} fixed-size PNG page(s), {metrics['fixed_resolution_px']['width']}x{metrics['fixed_resolution_px']['height']} px, files: {image_files}.
- PNG bytes are {metrics['png_total_bytes']}; actual vision tokens/latency are provider-specific and must be measured with the target model.

## Initial Interpretation

This looks feasible as a bounded preview channel for schema planning, category proposal, and analysis reading. It should reduce raw text copied into prompt bodies and cap preview context size.

It is not sufficient for strict row-level tagging, exact counts, joins, or numeric calculations. Those stages must keep the raw source table or row-level text payload as the authority.
"""
    (output_dir / "report.md").write_text(report, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render fixed-resolution visual data previews for TA++ v10 feasibility.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--sample-rows", type=int, default=60)
    parser.add_argument("--rows-per-image", type=int, default=30)
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=2200)
    parser.add_argument("--text-col", default="reason_for_visit")
    parser.add_argument("--max-columns", type=int, default=6)
    parser.add_argument(
        "--density",
        choices=["readable", "compact", "ocr"],
        default="readable",
        help="Layout density. 'ocr' is a high-information-density preview inspired by OCR-style visual text compression.",
    )
    args = parser.parse_args()

    frame = read_table(args.input).reset_index(drop=True)
    columns = choose_columns(frame, args.text_col, args.max_columns)
    sample = select_preview_rows(frame, args.text_col, args.sample_rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    text_preview = build_text_preview(sample, columns, args.query)
    (args.output_dir / "equivalent_text_preview.json").write_text(text_preview, encoding="utf-8")

    max_rows_per_image = max_rows_for_resolution(args.height, args.density)
    effective_rows_per_image = max(1, min(args.rows_per_image, max_rows_per_image))
    if effective_rows_per_image < args.rows_per_image:
        print(
            json.dumps(
                {
                    "pagination_adjustment": "rows_per_image_reduced_to_fit_canvas",
                    "requested_rows_per_image": int(args.rows_per_image),
                    "effective_rows_per_image": int(effective_rows_per_image),
                    "height": int(args.height),
                    "density": args.density,
                    "min_row_height": int(layout_profile(args.density)["min_row_height"]),
                },
                ensure_ascii=False,
            )
        )
    page_count = int(math.ceil(len(sample) / effective_rows_per_image))
    image_paths: list[Path] = []
    image_file_items: list[dict[str, Any]] = []
    for page_id in range(page_count):
        start = page_id * effective_rows_per_image
        end = min(len(sample), start + effective_rows_per_image)
        image_path = args.output_dir / f"preview_page_{page_id + 1:02d}.png"
        dims = render_page(
            sample.iloc[start:end],
            columns=columns,
            query=args.query,
            output_path=image_path,
            page_number=page_id + 1,
            page_count=page_count,
            width=args.width,
            height=args.height,
            density=args.density,
        )
        image_paths.append(image_path)
        image_file_items.append({"path": image_path.name, "bytes": int(image_path.stat().st_size), **dims})

    metrics = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input": str(args.input),
        "query": args.query,
        "rows_total": int(len(frame)),
        "rows_previewed": int(len(sample)),
        "columns_previewed": columns,
        "density": args.density,
        "layout_profile": layout_profile(args.density),
        "fixed_resolution_px": {"width": int(args.width), "height": int(args.height)},
        "requested_rows_per_image": int(args.rows_per_image),
        "rows_per_image": int(effective_rows_per_image),
        "max_rows_per_image_at_resolution": int(max_rows_per_image),
        "image_count": len(image_paths),
        "image_files": image_file_items,
        "png_total_bytes": int(sum(path.stat().st_size for path in image_paths)),
        "rough_image_token_estimates": estimate_image_tokens_for_pages(image_file_items),
        "equivalent_text_preview_chars": len(text_preview),
        "equivalent_text_preview_est_tokens_chars_div4": estimate_text_tokens(text_preview),
        "prompt_mode": "image_preview_for_schema_planning_only; raw data remains required for strict tagging and calculations",
    }
    (args.output_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.output_dir / "visual_prompt.md").write_text(build_prompt(args.query, image_paths, metrics), encoding="utf-8")
    write_report(args.output_dir, metrics)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())