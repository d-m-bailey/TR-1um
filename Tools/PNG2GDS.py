#!/usr/bin/env python3
# ----- ------ ----- ----- ------ ----- ----- ------ -----
# OpenSUSI jun1okamura <jun1okamura@gmail.com>
# LICENSE: Apache License Version 2.0, January 2004,
#          http://www.apache.org/licenses/
# ----- ------ ----- ----- ------ ----- ----- ------ -----

import argparse
import re
from pathlib import Path

from PIL import Image
import klayout.db as pya


MAX_WIDTH_PX = 155
MAX_HEIGHT_PX = 80
PIXEL_SIZE_UM = 2.0
LAYER = (13, 0)


def normalize_cell_name(text: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_]+", "_", text.strip())
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "LOGO"


def make_top_cell_name(output_path: Path) -> str:
    stem = normalize_cell_name(output_path.stem.upper())
    return f"TOP_{stem}"


def crop_to_content(image: Image.Image) -> Image.Image:
    """
    白背景(255)を前提に、非白画素の外接BBoxで切り出す。
    何も描かれていない場合は元画像を返す。
    """
    mask = image.point(lambda p: 0 if p >= 255 else 255)
    bbox = mask.getbbox()

    if bbox is None:
        return image

    return image.crop(bbox)


def load_and_prepare_image(path: Path) -> Image.Image:
    """
    1. PNGをグレースケールで読む
    2. 二値化
    3. データがある領域だけ切り出す
    4. 横155px以下、縦80px以下に収まる最大倍率で等倍スケール
    5. 白キャンバス中央に配置
    """
    image = Image.open(path).convert("L")
    image = image.point(lambda p: 255 if p > 128 else 0)

    content = crop_to_content(image)
    content_w, content_h = content.size

    if content_w <= 0 or content_h <= 0:
        return Image.new("L", (MAX_WIDTH_PX, MAX_HEIGHT_PX), 255)

    scale_x = MAX_WIDTH_PX / content_w
    scale_y = MAX_HEIGHT_PX / content_h
    scale = min(scale_x, scale_y)

    resized_w = max(1, round(content_w * scale))
    resized_h = max(1, round(content_h * scale))

    resized = content.resize(
        (resized_w, resized_h),
        Image.Resampling.NEAREST,
    )

    canvas = Image.new("L", (MAX_WIDTH_PX, MAX_HEIGHT_PX), 255)
    offset_x = (MAX_WIDTH_PX - resized_w) // 2
    offset_y = (MAX_HEIGHT_PX - resized_h) // 2
    canvas.paste(resized, (offset_x, offset_y))

    return canvas


def write_gds_from_image(image: Image.Image, output_path: Path) -> str:
    width, height = image.size

    layout = pya.Layout()
    layout.dbu = 0.001  # 1nm database unit

    top_cell_name = make_top_cell_name(output_path)
    top_cell = layout.create_cell(top_cell_name)
    layer_index = layout.layer(*LAYER)

    pixels = image.load()

    # 原点をBBOX中心に合わせる
    center_x_um = width * PIXEL_SIZE_UM / 2.0
    center_y_um = height * PIXEL_SIZE_UM / 2.0

    for y in range(height):
        for x in range(width):
            if pixels[x, y] < 128:
                gx = x * PIXEL_SIZE_UM - center_x_um
                gy = (height - 1 - y) * PIXEL_SIZE_UM - center_y_um

                box = pya.Box(
                    int(round(gx / layout.dbu)),
                    int(round(gy / layout.dbu)),
                    int(round((gx + PIXEL_SIZE_UM) / layout.dbu)),
                    int(round((gy + PIXEL_SIZE_UM) / layout.dbu)),
                )
                top_cell.shapes(layer_index).insert(box)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    layout.write(str(output_path))

    return top_cell_name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a PNG into a centered GDSII logo. "
            "The content area is scaled to fit within 155 px width "
            "and 80 px height while preserving aspect ratio. "
            "The output GDS contains a single top cell only."
        )
    )
    parser.add_argument("--input", required=True, help="Input PNG file")
    parser.add_argument("--output", required=True, help="Output GDSII file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    image = load_and_prepare_image(input_path)
    top_cell_name = write_gds_from_image(image, output_path)

    print(f"Input PNG : {input_path}")
    print(f"Output GDS: {output_path}")
    print(f"Canvas    : {MAX_WIDTH_PX}x{MAX_HEIGHT_PX} px")
    print(f"Pixel size: {PIXEL_SIZE_UM} um")
    print("Scale rule: fit within 155 px width and 80 px height")
    print("Origin    : centered at GDS BBOX center")
    print(f"Top cell  : {top_cell_name}")
    print("Hierarchy : none")


if __name__ == "__main__":
    main()