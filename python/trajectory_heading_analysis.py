import pandas as pd
import numpy as np

# 仮のデータフレーム: 各フレームの x, y 座標があるとする
df = pd.DataFrame({
    "frame": [0, 1, 2, 3, 4, 5],
    "x":     [0.0, 1.0, 2.0, 2.5, 2.0, 1.5],
    "y":     [0.0, 0.1, 0.2, 0.5, 0.8, 1.0],
})

# 1. 差分ベクトル（フレーム間の移動）
df["dx"] = df["x"].diff()   # x方向の変化量
df["dy"] = df["y"].diff()   # y方向の変化量

# 2. 各区間の進行方向角度（ラジアン）
#    atan2(dy, dx) はベクトル (dx, dy) の向きの角度を返す
df["heading_rad"] = np.arctan2(df["dy"], df["dx"])

# 3. 連続する区間の方向変化量
df["delta_heading"] = df["heading_rad"].diff()

# 4. 角度差を -π〜π に正規化（例えば 190° → -170° に変換）
df["delta_heading"] = (df["delta_heading"] + np.pi) % (2*np.pi) - np.pi

# 5. 蛇行の強さの指標（例）
#    - 絶対値の平均 → 1フレームごとの平均的な曲がり具合
#    - 絶対値の合計 → 全区間でどれくらい曲がったか
zigzag_mean = df["delta_heading"].abs().mean(skipna=True)
zigzag_sum  = df["delta_heading"].abs().sum(skipna=True)

print(df[["frame", "x", "y", "dx", "dy", "heading_rad", "delta_heading"]])
print("蛇行度(平均 abs Δheading):", zigzag_mean)
print("蛇行度(総量   abs Δheading):", zigzag_sum)