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

def draw_text_on_image(img: Image.Image, text: str) -> Image.Image:
    """
    【学習フォーカス対象】
    渡された画像オブジェクトに対して、中央揃えでテキスト（日本語対応）を描画する関数。
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
    font_size = 56  # 文字サイズ
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

    # 2. テキストのサイズ測定と描画位置 (中央揃え) の計算
    # textbboxでテキストの境界ボックスを取得 (左, 上, 右, 下)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 左右中央に配置するX座標
    x = (width - text_width) // 2
    # 上下中央に配置するY座標 (bboxの基準線のオフセットbbox[1]を考慮)
    y = (height - text_height) // 2 - bbox[1]

    # 3. テキストの背面となる「黒半透明の座布団（矩形）」を描画
    padding = 24
    draw.rectangle(
        [
            x - padding,
            y + bbox[1] - padding,
            x + text_width + padding,
            y + bbox[3] + padding
        ],
        fill=(0, 0, 0, 160)  # RGBAのAに相当する値(160)で半透明の黒を指定
    )

    # 4. 文字自体（白）を上から重ねて描画
    draw.text(
        (x, y),
        text,
        fill="white",
        font=font
    )

    return img

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="1980x480のバナー画像に文字を重ねるツール")
    parser.add_argument("--text", type=str, default="こんにちは、Pillow！", help="描画するテキスト")
    parser.add_argument("--output", type=str, default="banner_output.png", help="出力ファイル名")
    
    args = parser.parse_args()
    
    # 背景画像を生成
    background = generate_background_image(width=1980, height=480)
    
    # 画像にテキストを描画
    result_img = draw_text_on_image(background, args.text)
    
    # 保存
    result_img.save(args.output)
    print(f"画像が正常に生成されました: {args.output}")
