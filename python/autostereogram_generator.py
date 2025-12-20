from PIL import Image
import numpy as np

# 深さマップの読み込み（grayscale）
depth = Image.open("depth_map.png").convert("L")
depth_arr = np.array(depth)

# ベースの繰り返しパターン（noiseなど）
pattern = Image.open("pattern.png")
pattern_arr = np.array(pattern)

h, w = depth_arr.shape
pw, ph, _ = pattern_arr.shape

output = np.zeros((h, w, 3), dtype=np.uint8)

# 設定値
max_offset = 20  # 最大ずらす幅

for y in range(h):
    for x in range(w):
        d = depth_arr[y, x] / 255.0      # 0-1 の深さ
        offset = int(d * max_offset)     # ずらす量
        src_x = (x + offset) % pw         # パターン内の位置
        output[y, x] = pattern_arr[y % ph, src_x]

Image.fromarray(output).save("autostereogram.png")