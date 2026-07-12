import re

def clean_ocr_text_with_english_removal(text: str, allowlist: set[str] = set()) -> str:
    """
    OCR文字列からノイズ（長音、連続記号、短い英語など）と
    原則すべての英字を除去する関数。

    allowlist: 残しておきたい英単語（例："AI", "CPU"など）
    """
    # 1. 長音の連続「ーーー」などを削除
    text = re.sub(r'ー{2,}', '', text)

    # 2. 無意味な連続記号（＝・…・.）を削除
    text = re.sub(r'[＝・\.]{2,}', '', text)

    # 3. 制御文字をスペースに変換
    text = re.sub(r'[\r\n\t]', ' ', text)

    # 4. 空白の正規化
    text = re.sub(r'\s{2,}', ' ', text)

    # 5. allowlistに含まれない英単語・英文字を削除
    # 英単語抽出→残すべきものを残し、それ以外を削除
    def english_remover(match):
        word = match.group(0)
        return word if word in allowlist else ''
    
    text = re.sub(r'[a-zA-Z]+', english_remover, text)

    # 6. 最終的な空白整理
    text = text.strip()
    return text