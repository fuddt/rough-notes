from PIL import Image, ImageDraw

# 画像を読み込み
image = Image.open('example.jpg')  # 既存の画像ファイル名を指定
draw = ImageDraw.Draw(image)

# 点の座標を指定
point = (100, 150)  # (x, y) 座標
radius = 3  # 点の半径

# 点を描画（赤い円として描画）
draw.ellipse(
    (point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius),
    fill="red",
    outline="red"
)

# 画像を保存
image.save('image_with_point.jpg')  # 新しいファイル名を指定して保存

# 画像を表示
image.show()