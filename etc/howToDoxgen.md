EXTRACT_ALL = YES
SOURCE_BROWSER = YES

EXTRACT_ALL = YES

コメントが書かれていないものも含めて、できるだけ全部ドキュメント対象にする設定。

通常の Doxygen は、コメントがちゃんと付いている関数やクラスを優先して出す。
でも巨大プロジェクトの調査では、コメントがないコードの方が多いことが普通。

これを YES にすると、
	•	クラス
	•	構造体
	•	関数
	•	変数
	•	typedef
	•	enum

などを、コメント不足でも拾いやすくなる。


# 生成対象をこのフォルダ配下だけに限定
INPUT = src/moduleA

# 配下のサブフォルダも対象にする
RECURSIVE = YES

# 対象にする拡張子を必要なものだけに絞る
FILE_PATTERNS = *.h *.hpp *.c *.cpp

# さらに除外したいディレクトリやファイルがあれば指定
EXCLUDE = src/moduleA/test src/moduleA/mock

# パターンで除外したい場合
EXCLUDE_PATTERNS = */generated/* */temp/*