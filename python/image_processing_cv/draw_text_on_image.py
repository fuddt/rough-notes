import argparse
import os
from PIL import Image, ImageDraw, ImageFont

def generate_background_image(width: int, height: int) -> Image.Image:
    """
    指定されたサイズのグラデーション背景画像を新規生成する関数。
    (青 #16213e から 紫 #0f3460 への水平グラデーション)
    """
    img = Image.new("RGB", (width, height), "#1a1a2e")
    draw = ImageDraw.Draw(img)
    
    # グラデーションを描画（左から右へ）
    for x in range(width):
        r = int(0x16 + (0x0f - 0x16) * (x / width))
        g = int(0x21 + (0x34 - 0x21) * (x / width))
        b = int(0x3e + (0x60 - 0x3e) * (x / width))
        draw.line([(x, 0), (x, height)], fill=(r, g, b))
        
    return img

def draw_text_on_image(
    img: Image.Image,
    top_left_text: str = None,
    top_left_show: bool = True,
    top_right_text: str = None,
    top_right_show: bool = True,
    top_center_text: str = None,
    top_center_show: bool = True,
) -> Image.Image:
    """
    渡された画像オブジェクトに対して、指定された上部3箇所（左上、右上、中央上）に
    テキストを描画する関数。
    """
    # 描画用のオブジェクトを作成
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # 1. フォントの設定 (macOSの代表的な日本語フォントのパスを指定)
    font_paths = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    
    font = None
    font_size = 32  # 文字サイズ (中央の56pxより小さめ)
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, size=font_size)
                break
            except Exception:
                continue
                
    if font is None:
        print("警告: 日本語フォントが見つかりませんでした。デフォルトフォントを使用します。")
        font = ImageFont.load_default()

    margin = 24
    padding = 12

    # 各位置での描画処理用の設定
    # (テキスト, 表示フラグ, 基準X座標を計算するラムダ式)
    positions = [
        (top_left_text, top_left_show, lambda tw: margin),
        (top_right_text, top_right_show, lambda tw: width - tw - margin),
        (top_center_text, top_center_show, lambda tw: (width - tw) // 2),
    ]

    for text, show, get_base_x in positions:
        # テキストが指定されており、かつ表示ON設定の場合のみ描画
        if not text or not show:
            continue

        # テキストのサイズ測定
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        base_x = get_base_x(text_width)
        base_y = margin

        # 実際の描画位置 (bboxの基準線オフセットを考慮)
        x = base_x - bbox[0]
        y = base_y - bbox[1]

        # テキストの背面となる「黒半透明の座布団（矩形）」を描画
        draw.rectangle(
            [
                base_x - padding,
                base_y - padding,
                base_x + text_width + padding,
                base_y + text_height + padding
            ],
            fill=(0, 0, 0, 160)  # RGBAのAに相当する値(160)で半透明の黒を指定
        )

        # 文字自体（白）を上から重ねて描画
        draw.text(
            (x, y),
            text,
            fill="white",
            font=font
        )

    return img

if __name__ == "__main__":
    # 背景画像を生成 (1920x480)
    background = generate_background_image(width=1920, height=480)
    
    # 画像にテキストを描画 (左上、右上、中央上の動作検証用デモ)
    result_img = draw_text_on_image(
        background,
        top_left_text="左上テキスト",
        top_left_show=True,
        top_right_text="右上テキスト (ON)",
        top_right_show=True,
        top_center_text="中央上テキスト",
        top_center_show=True
    )
    
    # 保存
    output_path = "banner_output.png"
    result_img.save(output_path)
    print(f"画像が正常に生成されました: {output_path}")

