import pandas as pd
import numpy as np

# 例: カメラの位置と向きのデータ
df = pd.DataFrame({
    "frame": [0, 1, 2, 3, 4],
    "cam_x": [0.0, 0.5, 1.0, 0.7, 0.4],
    "cam_z": [0.0, 0.0, 0.0, 0.0, 0.0],
    # yaw は「どっちを向いているか」（ラジアン）
    # ここでは全部 +x 方向を向いているケースで仮定
    "yaw":   [0.0, 0.0, 0.0, 0.0, 0.0],
})

# 1. 向きベクトル（前方向）の算出
#    yaw を使って、カメラの「前向き」単位ベクトル f = (cos(yaw), sin(yaw)) を作る
df["fx"] = np.cos(df["yaw"])
df["fz"] = np.sin(df["yaw"])

# 2. フレーム間の移動ベクトル d_t = C_t - C_{t-1}
df["dx"] = df["cam_x"].diff()  # x方向の変化量
df["dz"] = df["cam_z"].diff()  # z方向の変化量

# 3. 一つ前のフレームの前向きベクトル f_{t-1} を用意
prev_fx = df["fx"].shift(1)
prev_fz = df["fz"].shift(1)

# 4. 移動ベクトル d_t を f_{t-1} に投影（= 内積）する
#    s_t = dx * fx_{t-1} + dz * fz_{t-1}
df["step_forward_component"] = df["dx"] * prev_fx + df["dz"] * prev_fz

# 5. 「手前に下がったか？」の判定
#    前向き成分がマイナスなら後退（手前に下がっている）
#    ノイズ対策で少ししきい値を入れる（例: -0.01 未満）
threshold = -0.01
df["moved_backward"] = df["step_forward_component"] < threshold

print(df[["frame", "cam_x", "cam_z",
          "dx", "dz",
          "step_forward_component", "moved_backward"]])