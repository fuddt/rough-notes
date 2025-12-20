import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# データを作成
data = {
    "Date": [
        "2024/01/04", "2024/01/05",
        "2024/04/05", "2024/04/06", "2024/04/07", "2024/04/08", "2024/04/09",
        "2024/05/10", "2024/05/24"
    ],
    "Taro": [
        873.66, 684.63,
        549.85, 278.59, 59.64, 274.76, 639.28,
        533.63, 88.58
    ],
    "Jiro": [
        726.21, 451.53,
        444.85, 393.44, 715.99, 195.50, 760.72,
        503.32, 81.70
    ],
    "hanako": [
        133.95, 97.55,
        186.01, 648.40, 678.51, 992.51, 792.77,
        29.15, 686.71
    ]
}

# データフレームを作成し、日付をdatetime型に変換
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])
st.write(df)
# 月ごとに週単位でデータを集計
df['Week'] = df['Date'].dt.to_period('W')
df['Month'] = df['Date'].dt.to_period('M')

# 各担当者ごとのデータを抽出して集計
total_weekly_sum = df.melt(id_vars=['Date', 'Week', 'Month'], value_vars=['Taro', 'Jiro', 'hanako'], var_name='Person', value_name='Value')
total_weekly_sum = total_weekly_sum.groupby(['Person', 'Month', 'Week']).sum(numeric_only=True).reset_index()
st.write(total_weekly_sum)
# Streamlitアプリケーション
st.title("担当者別の月ごとの週単位積み上げ棒グラフ")

# グラフの描画
fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

# 各担当者ごとにグラフを作成
for ax, (person, group) in zip(axes, total_weekly_sum.groupby('Person')):
    person_pivot = group.pivot(index='Month', columns='Week', values='Value').fillna(0)
    person_pivot.plot(kind='bar', stacked=True, ax=ax, legend=False, width=0.7)
    ax.set_title(f"{person}'s weekly stacked bar by month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total value")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

# グラフのカスタマイズ
fig.tight_layout()
axes[-1].legend(title="Week", loc='upper center', bbox_to_anchor=(-0.1, -0.15), ncol=5)

# Streamlitにプロットを表示
st.pyplot(fig)


# figsize パラメータ：

# fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True) の figsize パラメータを調整することで、グラフの横幅を小さくすることにより、グラフ間の距離を縮めることができます。
# fig.tight_layout()：

# fig.tight_layout() はグラフ間の余白を自動的に調整します。この関数のパラメータ pad を使って、余白をさらに縮めることも可能です。


df.melt() は、**データフレームの再構成（リフォーマット）**を行う関数で、列を行に変換することでデータを「縦長」形式に変換します。具体的には、今回のコードで melt() がどのように動作しているか解説します。

元のデータフレーム構造
元のデータフレーム df は次のようになっています：

Date	Taro	Jiro	hanako
2024/01/04	873.66	726.21	133.95
2024/01/05	684.63	451.53	97.55
...	...	...	...
これに対して、Taro, Jiro, hanako という列を持つデータを、melt() 関数を用いて変形し、それぞれの値を1列にまとめた「縦長」形式にします。

melt() の引数の意味
python
コードをコピーする
df.melt(id_vars=['Date', 'Week', 'Month'], value_vars=['Taro', 'Jiro', 'hanako'], var_name='Person', value_name='Value')
この melt() 関数は以下のように動作します：

id_vars=['Date', 'Week', 'Month']:

**保持する列（キー列）**を指定します。この場合、Date, Week, Month の各列をそのまま残し、他の列（Taro, Jiro, hanako）を変換の対象にします。
これらはインデックスのような役割を持つ情報です。
value_vars=['Taro', 'Jiro', 'hanako']:

**変換する列（ピボット対象列）**を指定します。この場合、Taro, Jiro, hanako の各列のデータが変換され、1列にまとめられます。
これにより、複数の列から1つの列にデータが集約されます。
var_name='Person':

元々の列名（Taro, Jiro, hanako）が入る新しい列名を指定します。この場合、新しい列名は 'Person' となります。
新しい列 'Person' には、各担当者の名前（Taro, Jiro, hanako）が入ります。
value_name='Value':

元のデータ（値）が格納される新しい列の名前を指定します。この場合、新しい列名は 'Value' となります。
新しい列 'Value' には、Taro, Jiro, hanako 各列の数値データが順に格納されます。
変換後のデータフレーム構造
melt() を適用すると、データフレームの構造は以下のように変わります：

Date	Week	Month	Person	Value
2024/01/04	2024-01-01	2024-01	Taro	873.66
2024/01/04	2024-01-01	2024-01	Jiro	726.21
2024/01/04	2024-01-01	2024-01	hanako	133.95
2024/01/05	2024-01-01	2024-01	Taro	684.63
2024/01/05	2024-01-01	2024-01	Jiro	451.53
2024/01/05	2024-01-01	2024-01	hanako	97.55
...	...	...	...	...
この変換により、元々の3つの列（Taro, Jiro, hanako）がすべて 'Person' という1つの列にまとまり、その値が 'Value' という列に格納されます。

なぜこの変換が必要なのか？
この「縦長」形式にすることで、pandas の groupby() や matplotlib などのツールで簡単にデータを集計・可視化しやすくなります。各担当者ごとの集計や処理を行う場合、この形式が非常に扱いやすいため、グラフの描画や分析が効率的になります。
