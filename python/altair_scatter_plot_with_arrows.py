"""
Altair を使って
  1. 点を散布図に描画し
  2. 点と点を矢印で結ぶ
フルサンプルコード。

- points_df: 点のリスト
- arrows_df: どの点からどの点へ矢印を引くか
を別々に定義し、merge で結合して座標を作る構成。
"""

import altair as alt
import pandas as pd
import numpy as np

# --- 0. Altair の制限をゆるめる（行数が多い場合に備えて） ---
alt.data_transformers.disable_max_rows()


# --- 1. 点データの定義 ---------------------------------------
# id: 点の名前
# x, y: 座標
points_df = pd.DataFrame(
    {
        "id": ["A", "B", "C", "D"],
        "x":  [0.1, 0.4, 0.8, 0.6],
        "y":  [0.2, 0.7, 0.5, 0.1],
    }
)

# --- 2. 矢印（どの点からどの点へ結ぶか）の定義 ---------------
# from_id: 矢印の始点となる点の id
# to_id:   矢印の終点となる点の id
arrows_def = pd.DataFrame(
    {
        "from_id": ["A", "B", "C"],
        "to_id":   ["B", "C", "D"],
    }
)


# --- 3. from/to の id から座標を join して矢印用のDFを作る -----

# from_id をキーにして始点の座標を付与
arrows = (
    arrows_def
    .merge(
        points_df.add_prefix("from_"),  # from_id, from_x, from_y
        left_on="from_id",
        right_on="from_id",
        how="left",
    )
    # to_id をキーにして終点の座標を付与
    .merge(
        points_df.add_prefix("to_"),    # to_id, to_x, to_y
        left_on="to_id",
        right_on="to_id",
        how="left",
    )
)

# 安全のため、必要な列だけに絞る
arrows = arrows[
    [
        "from_id",
        "to_id",
        "from_x",
        "from_y",
        "to_x",
        "to_y",
    ]
]


# --- 4. 矢印の向き（角度）を計算 ------------------------------
# 三角形マーカーを回転させるために atan2 で角度（度数）を計算。
#   dx = 終点x - 始点x
#   dy = 終点y - 始点y
#   angle = atan2(dy, dx) を度数法に変換
dx = arrows["to_x"] - arrows["from_x"]
dy = arrows["to_y"] - arrows["from_y"]
arrows["angle_deg"] = np.degrees(np.arctan2(dy, dx))


# --- 5. 各レイヤー（点・矢印の線・矢印の先端）を定義 ----------

# 5-1. ベースの散布図（点）
points_layer = (
    alt.Chart(points_df)
    .mark_point(size=100)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=(0.0, 1.0))),
        y=alt.Y("y:Q", scale=alt.Scale(domain=(0.0, 1.0))),
        tooltip=["id", "x", "y"],
    )
)

# 5-2. 点のラベル（A, B, C, ...）
labels_layer = (
    alt.Chart(points_df)
    .mark_text(
        dx=8,  # 点からのオフセット（横方向）
        dy=-8, # 点からのオフセット（縦方向）
    )
    .encode(
        x="x:Q",
        y="y:Q",
        text="id:N",
    )
)

# 5-3. 矢印の「線」部分
arrows_line_layer = (
    alt.Chart(arrows)
    .mark_line()
    .encode(
        x="from_x:Q",
        y="from_y:Q",
        x2="to_x:Q",
        y2="to_y:Q",
        tooltip=["from_id", "to_id"],
    )
)

# 5-4. 矢印の「先端」（三角形マーカー）
arrows_head_layer = (
    alt.Chart(arrows)
    .mark_point(
        shape="triangle",  # 三角形マーカー
        size=200,          # 大きさ
    )
    .encode(
        x="to_x:Q",
        y="to_y:Q",
        angle="angle_deg:Q",  # ここで向きを指定
        tooltip=["from_id", "to_id"],
    )
)


# --- 6. レイヤーを重ねて一つのチャートにする -------------------
chart = (
    points_layer
    + labels_layer
    + arrows_line_layer
    + arrows_head_layer
).properties(
    width=400,
    height=400,
    title="Altair: 点と点を矢印で結ぶ散布図",
).interactive()  # ズーム・パンなどを有効化


# --- 7. 表示方法 ------------------------------------------------
# Jupyter Notebook / JupyterLab なら最後に chart を評価するだけ。
# スクリプトで HTML に出力したい場合は以下:
if __name__ == "__main__":
    # 例: chart を HTML ファイルに保存
    chart.save("scatter_with_arrows.html")
    print("scatter_with_arrows.html をブラウザで開いてください。")