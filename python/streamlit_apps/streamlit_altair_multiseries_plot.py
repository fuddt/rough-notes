import streamlit as st
import altair as alt
import pandas as pd

# ▼ 元データ例（x と y1〜10）
df = pd.DataFrame({
    "x": range(50),
    **{f"y{i}": [v * i * 0.1 for v in range(50)] for i in range(1, 11)}
})

# ▼ y1〜y10 を long 形式にまとめる
#   id_vars="x"  → そのまま残す列
#   value_vars   → y1〜y10 を1列に
df_long = df.melt(
    id_vars="x",
    value_vars=[f"y{i}" for i in range(1, 11)],
    var_name="series",   # y1, y2, ... が入るラベル列
    value_name="y"        # y の値
)

# ▼ Altair 散布図
chart = (
    alt.Chart(df_long)
    .mark_circle(size=55)
    .encode(
        x=alt.X("x:Q", axis=None),
        y=alt.Y("y:Q", axis=None),
        color=alt.Color("series:N"),   # series 列ごとに色分け
    )
    .interactive()  # ← ズーム・パンだけ付く
)

# ▼ Streamlit で描画
st.altair_chart(chart, use_container_width=True)