
JSONにファイルパスを記述するときの注意事項

項目	内容	悪い例	良い例	備考
パス区切り文字	Windowsパスの \ は JSON ではエスケープ文字のため、そのまま書かない	"C:\temp\test\data.txt"	"C:\\temp\\test\\data.txt"	最重要事項
パス区切り文字の推奨	可能であれば / を使う	"C:\temp\test\data.txt"	"C:/temp/test/data.txt"	Windowsでも / で扱えることが多く、安全性が高い
# の扱い	# は JSON 文字列としては使用可能	なし	"C:/work/#sample/data.txt"	# 自体はJSON上問題ない
ダブルクォート	" を文字列中に含める場合はエスケープする	"note": "a "test" file"	"note": "a \"test\" file"	パス項目より説明文項目で起きやすい
改行	文字列中に生の改行を入れない	複数行に分かれた文字列	\n を使う	生改行は JSON 構文エラーの原因
タブ・制御文字	生タブや不可視の制御文字を含めない	コピペ由来の不可視文字入り	制御文字を除去した文字列	見た目では気づきにくい
文字コード	JSONファイルは UTF-8 で保存する	Shift_JIS など混在	UTF-8	日本語パスを扱う場合は特に重要
全角文字	全角文字は JSON 上は使用可能だが、運用上は注意する	"C:/work/test(file)/a.txt" と "C:/work/test（file）/a.txt" を混同	使用する文字種を統一する	半角と全角は別文字
日本語ファイル名	日本語は使用可能だが、環境依存の文字化けに注意する	文字コード未統一のまま運用	UTF-8 統一で使用	C++ 側の文字列処理にも注意
Windows使用禁止文字	Windowsのファイル名に使えない文字を含めない	test?.txt	test.txt	`< > : “ / \
末尾スペース・末尾ピリオド	Windowsで不安定なため避ける	"file " "file."	"file"	JSONではなくOS側の制約
予約名	Windowsの予約名をファイル名に使わない	"CON.txt"	"config.txt"	CON, NUL, PRN, AUX, COM1 など
相対パス / 絶対パス	どちらを許可するか仕様で明記する	基準不明の "../data/input.txt"	「相対パスは実行ファイル基準」など明記	曖昧にすると不具合の原因になる
.. の扱い	親ディレクトリ参照を許可するか決める	"../config/settings.json" を無制限に許可	許可可否を仕様で明記	セキュリティ上も注意
URLとの区別	ファイルパスとURLを混同しない	"file:///C:/work/data.txt" を通常パスとして扱う	"C:/work/data.txt"	path が URL なのか OS パスなのか定義する
前後空白	パス文字列の前後に空白を入れない	" C:/temp/data.txt "	"C:/temp/data.txt"	存在確認や比較で失敗しやすい
独自コメント解釈	# や // をコメントとして扱う独自実装をしない	JSON風自作パーサ	標準JSONライブラリを使用	JSONはJSONとして読む
読み込み後の正規化	読み込み後にパスを正規化する	生文字列のまま比較	区切り文字統一、前後空白除去など	実装側の品質に関わる
エラーハンドリング	パース失敗時は何文字目で失敗したかを出力する	"parse error" だけ	位置・原因を含めて出力	切り分けが容易になる

⸻

推奨ルール

以下のルールを採用することを推奨する。

1. JSONファイルは UTF-8 で保存する。
2. ファイルパスの区切り文字は / を推奨する。
3. Windows形式の \ を使用する場合は \\ としてエスケープする。
4. path 項目は OSファイルパス として扱い、URLとは混同しない。
5. 相対パスを許可する場合は、基準ディレクトリを仕様で明記する。
6. 全角文字や日本語は使用可能とするが、文字種の混在に注意する。
7. Windowsの使用禁止文字・予約名は使用しない。
8. 読み込み後にパスの正規化を行う。
9. JSONは標準の JSON ライブラリで読み込み、自作のコメント解釈を入れない。

⸻

記述例

推奨例

{
  "input_path": "C:/work/data/input.txt",
  "output_path": "C:/work/result/output.txt"
}

Windows形式を使う場合

{
  "input_path": "C:\\work\\data\\input.txt",
  "output_path": "C:\\work\\result\\output.txt"
}

# を含む場合

{
  "input_path": "C:/work/#sample/input.txt"
}

⸻