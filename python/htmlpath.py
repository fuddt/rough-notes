from pathlib import Path

# DBから取得した絶対パス（例）
abs_path = "/home/user/myproject/static/images/sample.jpg"

# staticディレクトリを基準として、相対パスを抽出
relative_path = Path(abs_path).relative_to("/home/user/myproject/static")

# Webアクセス用のURLパスに変換
url_path = f"/static/{relative_path}"

# HTMLに埋め込むなら
html = f'<img src="{url_path}" alt="画像">'