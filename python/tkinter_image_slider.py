import tkinter as tk
from tkinter import Canvas, Scale, HORIZONTAL
from PIL import Image, ImageTk

# 画像のパスが格納されたリスト（実際のパスに置き換えてください）
image_paths = [
    "image1.jpg",
    "image2.jpg",
    "image3.jpg"
]

def load_image(path):
    """
    指定されたパスから画像を読み込み、PhotoImageに変換して返す関数。
    """
    # 画像を開く（必要に応じてリサイズ等の処理を追加できます）
    img = Image.open(path)
    # Tkinterで扱える形式に変換
    return ImageTk.PhotoImage(img)

def update_image(index):
    """
    スライダーの値（index）に基づいて、キャンバス上の画像を更新する関数。
    """
    global current_image  # 画像の参照を保持してガベージコレクションを防ぐ
    # リストから該当する画像パスを取得
    path = image_paths[int(index)]
    # 新しい画像を読み込む
    current_image = load_image(path)
    # キャンバス上の画像アイテムを更新（itemconfigで画像プロパティを変更）
    canvas.itemconfig(image_on_canvas, image=current_image)

# メインウィンドウの作成
root = tk.Tk()
root.title("スライダーで画像更新")

# キャンバスの作成（適宜サイズを調整してください）
canvas = Canvas(root, width=400, height=400)
canvas.pack()

# 初期画像の読み込みとキャンバスへの描画
current_image = load_image(image_paths[0])
# 画像をキャンバスの中央（x=200, y=200）に描画
image_on_canvas = canvas.create_image(200, 200, image=current_image)

# Scaleウィジェットの作成
# スライダーの値が変わるたびにupdate_image関数が呼ばれる
slider = Scale(root, from_=0, to=len(image_paths)-1, orient=HORIZONTAL, command=update_image)
slider.pack()

# イベントループの開始
root.mainloop()
