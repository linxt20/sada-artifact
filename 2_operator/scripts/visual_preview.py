"""Visual preview artifact generation for TA++ skill v10."""

from __future__ import annotations

import json
import math
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


DEFAULT_WIDTH = 1600
DEFAULT_HEIGHT = 2200
DEFAULT_DENSITY = "ocr"
DEFAULT_OVERVIEW_ROWS = 60
DEFAULT_ROWS_PER_IMAGE = 60


def layout_profile(density: str = DEFAULT_DENSITY) -> dict[str, Any]:
    if density == "readable":
        return {
            "density": "readable",
            "padding": 30,
            "title_height": 70,
            "header_height": 42,
            "min_row_height": 52,
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


def choose_preview_columns(frame: pd.DataFrame, text_cols: Sequence[str], max_columns: int = 6) -> list[str]:
    selected: list[str] = []
    for column in frame.columns:
        name = str(column)
        lower = name.lower()
        if lower in {"id", "row_id", "visit_id", "number", "ticket_id"} or lower.endswith("_id"):
            selected.append(name)
            break
    for name in text_cols:
        if name in frame.columns and name not in selected:
            selected.append(str(name))
    structured: list[str] = []
    for column in frame.columns:
        name = str(column)
        if name in selected:
            continue
        if pd.api.types.is_numeric_dtype(frame[column]):
            structured.append(name)
            continue
        unique = int(frame[column].nunique(dropna=True))
        if 1 < unique <= min(50, max(10, len(frame) // 5)):
            structured.append(name)
    result = []
    for name in selected[:1] + structured[: max_columns - 2] + selected[1:]:
        if name in frame.columns and name not in result:
            result.append(name)
    return result[: max(1, max_columns)]


def select_preview_rows(frame: pd.DataFrame, text_cols: Sequence[str], sample_rows: int) -> list[int]:
    target = min(max(0, int(sample_rows)), len(frame))
    if target <= 0:
        return []
    text_col = next((col for col in text_cols if col in frame.columns), None)
    if not text_col:
        return list(range(target))
    lengths = frame[text_col].fillna("").astype(str).str.len()
    eligible = frame[text_col].notna()
    if int(eligible.sum()) < 3:
        return list(range(target))
    short_cut = float(lengths[eligible].quantile(1 / 3))
    long_cut = float(lengths[eligible].quantile(2 / 3))
    masks = [
        eligible & (lengths <= short_cut),
        eligible & (lengths > short_cut) & (lengths <= long_cut),
        eligible & (lengths > long_cut),
    ]
    selected: list[int] = []
    base_quota = max(1, target // 3)
    for bucket_id, mask in enumerate(masks):
        available = frame.index[mask].tolist()
        take = min(len(available), base_quota if bucket_id < 2 else target - len(selected))
        if take > 0:
            sampled = frame.loc[available].sample(n=take, random_state=41 + bucket_id).index.tolist()
            selected.extend(int(frame.index.get_loc(idx)) for idx in sampled)
    if len(selected) < target:
        remaining = [idx for idx in range(len(frame)) if idx not in set(selected)]
        selected.extend(remaining[: target - len(selected)])
    return sorted(dict.fromkeys(selected))[:target]


def max_rows_for_resolution(height: int, density: str = DEFAULT_DENSITY) -> int:
    profile = layout_profile(density)
    available_height = height - int(profile["padding"]) * 2 - int(profile["title_height"]) - int(profile["header_height"])
    return max(1, available_height // int(profile["min_row_height"]))


def estimate_image_tokens(width: int, height: int, image_count: int) -> dict[str, Any]:
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


def estimate_image_tokens_for_pages(pages: Sequence[dict[str, Any]]) -> dict[str, Any]:
    totals = {
        "rough_high_detail_tile_total": 0,
        "rough_area_patch_total": 0,
        "pages": [],
    }
    for page in pages:
        width = int(page.get("width", DEFAULT_WIDTH))
        height = int(page.get("height", DEFAULT_HEIGHT))
        estimate = estimate_image_tokens(width, height, 1)
        totals["rough_high_detail_tile_total"] += int(estimate["rough_high_detail_tile_total"])
        totals["rough_area_patch_total"] += int(estimate["rough_area_patch_total"])
        totals["pages"].append({"path": page.get("path"), "width": width, "height": height, **estimate})
    return totals


def _column_widths(columns: Sequence[str], width: int, profile: dict[str, Any]) -> dict[str, int]:
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
            flexible.append(str(column))
    remaining = max(180, content_width - used)
    for column in flexible:
        widths[column] = max(180, remaining // max(1, len(flexible)))
    return widths


def _wrap_for_width(text: str, pixel_width: int, font: ImageFont.ImageFont, draw: ImageDraw.ImageDraw) -> list[str]:
    if not text:
        return [""]
    average = max(5.0, draw.textlength("abcdefghijklmnopqrstuvwxyz", font=font) / 26)
    chars_per_line = max(8, int(pixel_width / average))
    lines: list[str] = []
    for paragraph in text.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=chars_per_line, break_long_words=True) or [""])
    return lines


def render_preview_page(
    frame: pd.DataFrame,
    row_positions: Sequence[int],
    columns: Sequence[str],
    output_path: Path,
    *,
    query: str,
    page_number: int,
    page_count: int,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    density: str = DEFAULT_DENSITY,
) -> dict[str, int]:
    profile = layout_profile(density)
    padding = int(profile["padding"])
    title_height = int(profile["title_height"])
    header_height = int(profile["header_height"])
    min_row_height = int(profile["min_row_height"])
    line_step = int(profile["line_step"])
    available_height = height - padding * 2 - title_height - header_height
    if bool(profile.get("stretch_rows")):
        row_height = max(min_row_height, available_height // max(1, len(row_positions)))
    else:
        row_height = min_row_height
    content_height = padding * 2 + title_height + header_height + row_height * max(1, len(row_positions))
    actual_height = min(height, content_height) if bool(profile.get("adaptive_height")) else height
    image = Image.new("RGB", (width, actual_height), "#f8fafc")
    draw = ImageDraw.Draw(image)
    title_font = load_font(int(profile["title_font"]), bold=True)
    header_font = load_font(int(profile["header_font"]), bold=True)
    cell_font = load_font(int(profile["cell_font"]))
    small_font = load_font(int(profile["small_font"]))
    widths = _column_widths(columns, width, profile)
    draw.text((padding, max(6, padding - 6)), "TA++ v10 visual preview", font=title_font, fill="#0f172a")
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
        col_width = widths[str(column)]
        draw.text((x + 4, y + max(4, (header_height - int(profile["header_font"])) // 2)), str(column)[:28], font=header_font, fill="#0f172a")
        draw.line([x, y, x, actual_height - padding], fill="#cbd5e1")
        x += col_width
    draw.line([width - padding, y, width - padding, actual_height - padding], fill="#cbd5e1")
    y += header_height
    for display_idx, row_pos in enumerate(row_positions):
        row = frame.iloc[int(row_pos)]
        fill = "#ffffff" if display_idx % 2 == 0 else "#f1f5f9"
        draw.rectangle([padding, y, width - padding, y + row_height], fill=fill, outline="#cbd5e1")
        x = padding
        for column in columns:
            col_width = widths[str(column)]
            limit = int(profile["text_cell_limit"] if str(column) in {str(col) for col in columns[-1:]} else profile["other_cell_limit"])
            value = clean_cell(row.get(column, ""), limit)
            lines = _wrap_for_width(value, col_width - 12, cell_font, draw)
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


def generate_visual_preview(
    frame: pd.DataFrame,
    workdir: Path,
    *,
    query: str,
    text_cols: Sequence[str],
    source_table: str | Path,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    density: str = DEFAULT_DENSITY,
    overview_rows: int = DEFAULT_OVERVIEW_ROWS,
    rows_per_image: int = DEFAULT_ROWS_PER_IMAGE,
    max_columns: int = 6,
) -> dict[str, Any]:
    preview_dir = Path(workdir) / "visual_preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    columns = choose_preview_columns(frame, text_cols, max_columns=max_columns)
    selected_rows = select_preview_rows(frame, text_cols, overview_rows)
    max_rows = max_rows_for_resolution(height, density)
    effective_rows = max(1, min(int(rows_per_image), max_rows))
    page_count = int(math.ceil(len(selected_rows) / effective_rows)) if selected_rows else 0
    pages: list[dict[str, Any]] = []
    for page_idx in range(page_count):
        start = page_idx * effective_rows
        end = min(len(selected_rows), start + effective_rows)
        rows = selected_rows[start:end]
        page_path = preview_dir / f"overview_page_{page_idx + 1:03d}.png"
        page_dims = render_preview_page(
            frame,
            rows,
            columns,
            page_path,
            query=query,
            page_number=page_idx + 1,
            page_count=page_count,
            width=width,
            height=height,
            density=density,
        )
        pages.append({"path": page_path.name, "rows": rows, "bytes": int(page_path.stat().st_size), **page_dims})
    manifest = {
        "kind": "visual_preview",
        "skill_version": "skill_v10",
        "mode": "fixed_resolution_table_images",
        "source_table": str(source_table),
        "query": query,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "max_resolution": {"width": int(width), "height": int(height)},
        "density": density,
        "layout_profile": layout_profile(density),
        "row_sampling": {"strategy": "text_length_stratified", "requested_rows": int(overview_rows), "returned_rows": len(selected_rows)},
        "requested_rows_per_image": int(rows_per_image),
        "rows_per_image": int(effective_rows),
        "max_rows_per_image_at_resolution": int(max_rows),
        "columns": columns,
        "text_cols": list(text_cols),
        "pages": pages,
        "png_total_bytes": int(sum(page["bytes"] for page in pages)),
        "rough_image_token_estimates": estimate_image_tokens_for_pages(pages),
        "limitations": [
            "lossy visual preview",
            "not authoritative for strict tagging",
            "not authoritative for exact counts or numeric calculations",
        ],
        "raw_data_required_for": ["tagging", "exact_counts", "joins", "numeric_calculation"],
    }
    manifest_path = preview_dir / "visual_preview_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest["manifest_path"] = str(manifest_path)
    return manifest