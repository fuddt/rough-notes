以下、そのままコピペして .md ファイルにできる形で2本出す。
順番はこうする。
	1.	Windows での導入手順
	2.	Visual Studio から使う運用手順

まず前提をはっきり言う。

Visual Studio 版といっても、Doxygen 自体は Visual Studio の機能ではない。
本体は別ツール。
Visual Studio から「実行しやすくする」「開きやすくする」「運用に組み込む」だけ。

なので構造はこうなる。
	•	Doxygen を Windows に入れる
	•	Graphviz を Windows に入れる
	•	Doxyfile をプロジェクトに置く
	•	Visual Studio から外部ツール or バッチで呼ぶ

これが現実的。

⸻

1. Windows版 DOXYGEN_SETUP_WINDOWS.md

# Doxygen 導入手順書（Windows版 / C++ プロジェクト向け）

## 目的

この手順書の目的は、Windows 環境で Doxygen を導入し、巨大な C++ プロジェクトの構造を可視化できるようにすることです。

特に以下を把握するために使います。

- クラス一覧
- 継承関係
- 名前空間
- ファイル構成
- include 依存関係

コメントが少ないプロジェクトでも、構造把握には十分役立ちます。

---

## 1. 配置方針

### 1-1. どこに何を置くか

プロジェクトルート直下に、以下のような構成を作るのを推奨します。

```text
your-project/
├── src/
├── include/
├── docs/
│   └── doxygen/
│       ├── Doxyfile
│       └── html/         ← Doxygen の生成物
├── tools/
│   └── generate_doxygen.bat
└── README.md

置くファイル
	•	docs/doxygen/Doxyfile
	•	Doxygen の設定ファイル
	•	tools/generate_doxygen.bat
	•	Windows で実行するためのバッチファイル
	•	docs/doxygen/html/
	•	生成先ディレクトリ
	•	手動で作らなくてもよい

⸻

2. Doxygen をインストールする

2-1. 公式サイトから入れる

Windows では、まず Doxygen 本体をインストールします。

インストール後、以下のような場所に入ることが多いです。

C:\Program Files\doxygen\bin\doxygen.exe

2-2. インストール確認

コマンドプロンプトで以下を実行します。

doxygen --version

もし doxygen が見つからない場合は、PATH が通っていない可能性があります。

その場合は以下どちらかで対応します。
	•	doxygen.exe のあるフォルダを PATH に追加する
	•	バッチファイルでフルパス指定する

⸻

3. Graphviz をインストールする

継承図や依存図を出すには Graphviz が必要です。

インストール後、以下のような場所に入ることが多いです。

C:\Program Files\Graphviz\bin\dot.exe

3-1. インストール確認

コマンドプロンプトで以下を実行します。

dot -V

バージョンが表示されれば OK です。

⸻

4. ディレクトリを作る

プロジェクトルート直下に以下を作成します。

your-project/
├── docs/
│   └── doxygen/
└── tools/

Windows エクスプローラで手動作成してよいです。

⸻

5. Doxyfile を作る

コマンドプロンプトで、プロジェクトルートへ移動して以下を実行します。

doxygen -g docs\doxygen\Doxyfile

これで以下が作成されます。

your-project\docs\doxygen\Doxyfile


⸻

6. Doxyfile を編集する

docs\doxygen\Doxyfile をテキストエディタで開いて、最低限以下を設定します。

# ----------------------------------------
# 基本情報
# ----------------------------------------
PROJECT_NAME           = "YourProject"
OUTPUT_DIRECTORY       = docs/doxygen

# ----------------------------------------
# 入力対象
# 必要に応じて調整する
# ----------------------------------------
INPUT                  = src include
RECURSIVE              = YES
FILE_PATTERNS          = *.h *.hpp *.hh *.c *.cc *.cpp

# ----------------------------------------
# コメントが少なくても情報を出す
# ----------------------------------------
EXTRACT_ALL            = YES
EXTRACT_PRIVATE        = YES
EXTRACT_STATIC         = YES
EXTRACT_LOCAL_CLASSES  = YES
HIDE_UNDOC_CLASSES     = NO
HIDE_UNDOC_MEMBERS     = NO

# ----------------------------------------
# HTML 出力
# ----------------------------------------
GENERATE_HTML          = YES
GENERATE_LATEX         = NO

# ----------------------------------------
# ソース参照
# ----------------------------------------
SOURCE_BROWSER         = YES
INLINE_SOURCES         = NO

# ----------------------------------------
# Graphviz(dot) を使った図
# ----------------------------------------
HAVE_DOT               = YES
CLASS_DIAGRAMS         = YES
COLLABORATION_GRAPH    = YES
INCLUDE_GRAPH          = YES
INCLUDED_BY_GRAPH      = YES
CALL_GRAPH             = NO
CALLER_GRAPH           = NO

DOT_GRAPH_MAX_NODES    = 80
MAX_DOT_GRAPH_DEPTH    = 3
DOT_IMAGE_FORMAT       = svg

# ----------------------------------------
# C++ 向け補助
# ----------------------------------------
OPTIMIZE_OUTPUT_FOR_C  = NO
BUILTIN_STL_SUPPORT    = YES
EXTRACT_ANON_NSPACES   = YES


⸻

7. INPUT を自プロジェクトに合わせて修正する

ここは重要です。

たとえば構成が以下なら:

your-project/
├── app/
├── core/
├── framework/
├── include/
└── third_party/

こうします。

INPUT = app core framework include

注意

third_party や外部依存は最初は入れないでください。
ノイズが増えすぎます。

⸻

8. バッチファイルを作る

tools\generate_doxygen.bat を作成します。

@echo off
REM ==========================================
REM Doxygen ドキュメント生成バッチ
REM プロジェクトルートから実行する前提ではなく、
REM この bat がどこから呼ばれても動くようにしている
REM ==========================================

REM この bat ファイル自身があるディレクトリへ移動
cd /d %~dp0

REM tools\ の1つ上、つまりプロジェクトルートへ移動
cd ..

REM Doxygen 実行
doxygen docs\doxygen\Doxyfile

REM エラーがあれば止める
if errorlevel 1 (
    echo.
    echo Doxygen generation failed.
    pause
    exit /b 1
)

echo.
echo Doxygen generation completed.

REM 生成した HTML を開く
start "" docs\doxygen\html\index.html

pause


⸻

9. 実行する

エクスプローラから以下をダブルクリックします。

tools\generate_doxygen.bat

またはコマンドプロンプトで実行します。

tools\generate_doxygen.bat

成功すると、以下が生成されます。

docs\doxygen\html\index.html


⸻

10. 最初に見るべき場所

Doxygen を生成したら、まず以下の順で見てください。

10-1. Classes

クラス一覧を見る。

10-2. Class Hierarchy

継承構造を見る。

10-3. Files

ファイル構成を見る。

10-4. Namespaces

名前空間の切り方を見る。

10-5. 特定クラスの詳細ページ

基底クラス、派生クラス、メンバ関数、定義場所を見る。

⸻

11. よくある失敗

11-1. Doxygen は入れたが Graphviz を入れていない

図が思ったように出ません。

11-2. PATH が通っていない

doxygen や dot が見つからない場合があります。

11-3. 全ディレクトリを対象にしている

外部ライブラリまで含めると読めなくなります。

11-4. Call Graph まで最初から有効にしている

巨大プロジェクトでは重くなりやすいです。

⸻

12. Git 管理の方針

12-1. 管理するもの
	•	docs/doxygen/Doxyfile
	•	tools/generate_doxygen.bat

12-2. 管理しないもの
	•	docs/doxygen/html/
	•	docs/doxygen/latex/

.gitignore に以下を追加することを推奨します。

docs/doxygen/html/
docs/doxygen/latex/


⸻

13. チェックリスト

初回セットアップ
	•	Doxygen をインストールした
	•	Graphviz をインストールした
	•	docs\doxygen\ を作成した
	•	tools\generate_doxygen.bat を作成した
	•	docs\doxygen\Doxyfile を作成した
	•	INPUT を自プロジェクト向けに修正した
	•	バッチを実行した
	•	index.html が開いた

初回探索
	•	Classes を見た
	•	Class Hierarchy を見た
	•	基底クラスをいくつか見つけた
	•	Factory / Manager / Controller を見つけた
	•	自分の担当ユースケースを1本追った

⸻

14. この運用の位置づけ

この手順の目的は、完璧な設計文書を作ることではありません。
目的は、巨大 C++ プロジェクトへの新規参画時に、構造把握の初速を上げることです。

Doxygen は万能ではありません。
しかし、クラス図が無い現場、コメントが少ない現場では、かなり有効な探索ツールです。

---

# 2. Visual Studio版 `DOXYGEN_SETUP_VISUAL_STUDIO.md`

```md
# Doxygen 運用手順書（Visual Studio 版 / C++ プロジェクト向け）

## 目的

この手順書の目的は、Windows に導入した Doxygen を Visual Studio から使いやすくし、C++ プロジェクトの構造把握を効率化することです。

重要なのは、Doxygen は Visual Studio の標準機能ではなく、外部ツールとして連携するという点です。

この手順書では以下を扱います。

- Visual Studio から Doxygen を実行する
- Visual Studio から生成結果を開きやすくする
- プロジェクト内に最小限の運用ファイルを置く

---

## 1. 前提

この手順を始める前に、以下が終わっている前提です。

- Doxygen が Windows にインストールされている
- Graphviz がインストールされている
- `docs/doxygen/Doxyfile` が作成済み
- `tools/generate_doxygen.bat` が作成済み

まだなら、先に Windows 版導入手順を実施してください。

---

## 2. 推奨するプロジェクト配置

```text
your-project/
├── src/
├── include/
├── docs/
│   └── doxygen/
│       ├── Doxyfile
│       └── html/
├── tools/
│   └── generate_doxygen.bat
└── YourSolution.sln

Visual Studio のソリューションファイルと同じルート、またはその近くに置くのが望ましいです。

理由:
	•	パスが分かりやすい
	•	他メンバーも使いやすい
	•	外部ツール設定が説明しやすい

⸻

3. まずバッチ単体で動作確認する

Visual Studio に組み込む前に、以下が動くことを確認します。

tools\generate_doxygen.bat

これで docs\doxygen\html\index.html が生成されることを確認してください。

ここが失敗するなら、Visual Studio 連携に進んでも詰まります。

⸻

4. Visual Studio から外部ツールとして実行する

4-1. 外部ツールの設定画面を開く

Visual Studio のメニューから以下を開きます。

Tools
  → External Tools...


⸻

4-2. 新しい外部ツールを追加する

Add を押して、以下のように設定します。

Title

Generate Doxygen

Command

バッチファイルのフルパスを指定します。

例:

C:\your-project\tools\generate_doxygen.bat

Arguments

空欄でよいです。



Initial directory

プロジェクトルートを指定します。

例:

C:\your-project


⸻

4-3. これで何が起きるか

Visual Studio から Generate Doxygen を実行すると、
登録したバッチファイルが呼ばれます。

その結果として:
	1.	Doxygen が実行される
	2.	HTML が生成される
	3.	index.html が開く

⸻

5. バッチファイルの推奨版

Visual Studio から呼ばれる前提なら、以下のようにしておくと安定します。

tools\generate_doxygen.bat

@echo off
REM ==========================================
REM Visual Studio からでも単体実行でも動く Doxygen 生成バッチ
REM ==========================================

REM bat ファイル自身のある場所へ移動
cd /d %~dp0

REM プロジェクトルートへ移動
cd ..

echo.
echo [1/2] Generating Doxygen documents...
doxygen docs\doxygen\Doxyfile

if errorlevel 1 (
    echo.
    echo Doxygen generation failed.
    pause
    exit /b 1
)

echo.
echo [2/2] Opening generated HTML...
start "" docs\doxygen\html\index.html

echo.
echo Done.
exit /b 0

この構成の意図
	•	cd /d %~dp0
	•	bat ファイル自身の場所へ移動する
	•	cd ..
	•	tools\ から 1 つ上のプロジェクトルートへ移動する
	•	カレントディレクトリ依存を減らす
	•	Visual Studio から呼んでも動きやすくするため

⸻

6. Visual Studio からの実行方法

メニューから以下を選びます。

Tools
  → Generate Doxygen

これでバッチが起動します。

⸻

7. よくある詰まりどころ

7-1. Command に doxygen.exe を直接入れてしまう

それでも動く場合はあります。
ただし、パスやカレントディレクトリの問題で詰まりやすいです。

最初は generate_doxygen.bat を噛ませた方が安定します。

⸻

7-2. Initial directory を適当にしている

Visual Studio 側の作業ディレクトリが想定と違うと壊れます。

ただし、今回の bat は自分で cd しているため、依存をかなり減らしています。

⸻

7-3. ソリューションの場所とプロジェクトルートがズレている

たとえば以下のようなケースです。

repo/
├── solution/
│   └── YourSolution.sln
└── product/
    ├── src/
    ├── include/
    ├── docs/
    └── tools/

この場合は Command や Initial directory をその構造に合わせて設定し直す必要があります。

⸻

8. Visual Studio のソリューションに補助ファイルを見せる

Doxyfile や bat をソリューションエクスプローラで見えるようにしたい場合があります。

その場合は、以下を「既存項目として追加」します。
	•	docs\doxygen\Doxyfile
	•	tools\generate_doxygen.bat

これをやる意味
	•	チームメンバーが場所を見失いにくい
	•	右クリックから開きやすい
	•	現場で「どこに設定あるの？」が減る

注意

これは Visual Studio 上で見せるだけで、ビルド対象にするわけではありません。

⸻

9. 必要なら Visual Studio のタスクっぽく扱う

本気で運用するなら、以下の2つを分けて考えます。

9-1. 個人用途
	•	Tools -> Generate Doxygen で十分

9-2. チーム用途
	•	tools\generate_doxygen.bat をリポジトリ管理
	•	docs\doxygen\Doxyfile をリポジトリ管理
	•	README に実行方法を書く

最初から MSBuild に無理やり組み込む必要はありません。

⸻

10. MSBuild / ビルドイベントに入れるべきか

結論から言うと、最初は入れない方がいいです。

理由:
	•	毎回ビルド時に Doxygen が走ると重い
	•	開発者全員に同じ負荷をかける
	•	エラー原因の切り分けがしにくくなる

つまり、以下の順が正しいです。
	1.	まずは手動実行
	2.	使えると分かったらチーム共有
	3.	本当に必要なら CI 側で生成を検討

いきなりビルドイベント連携はやりすぎです。

⸻

11. どうしても Visual Studio のビルド後イベントでやりたい場合

推奨はしませんが、やるなら以下の形です。

11-1. プロジェクトのプロパティを開く

Project
  → Properties
  → Build Events
  → Post-Build Event

11-2. コマンド例

call "$(SolutionDir)tools\generate_doxygen.bat"

注意

この方法は以下の問題があります。
	•	ビルドのたびに走る
	•	生成が重い
	•	Doxygen エラーと C++ ビルドエラーが混ざる
	•	開発者全員に強制される

なので、常用には向きません。

⸻

12. Visual Studio から見るときのおすすめ導線

Doxygen を Visual Studio と一緒に使うときは、以下の流れが効率的です。

Step 1

Visual Studio で気になる基底クラス名を見つける

Step 2

Generate Doxygen を実行する

Step 3

ブラウザでそのクラスのページを開く

Step 4

継承関係を確認する

Step 5

再び Visual Studio に戻って、実装クラスを開く

つまり役割分担はこうです。
	•	Visual Studio
	•	実コード編集
	•	定義ジャンプ
	•	デバッグ
	•	Doxygen
	•	全体構造の俯瞰
	•	継承関係の可視化
	•	索引

⸻

13. チームに共有するときの最低限の説明

以下だけ README に書いておけば十分です。

# Doxygen の使い方

## 目的
C++ プロジェクトのクラス構造・継承関係を把握するために使う

## 必要なもの
- Doxygen
- Graphviz

## 設定ファイル
- docs/doxygen/Doxyfile

## 実行方法
- tools/generate_doxygen.bat を実行
- または Visual Studio の Tools -> Generate Doxygen

## 出力先
- docs/doxygen/html/index.html


⸻

14. 運用上の結論

Visual Studio 連携の本質は、Doxygen を IDE の一部に見せることではありません。
本質は、巨大 C++ コードベースの構造把握を、普段の開発導線の中に差し込むことです。

そのため、最初の現実解はこれです。
	•	Doxyfile を置く
	•	bat を置く
	•	Visual Studio の External Tools に登録する

これで十分です。

逆に、最初からビルドイベントや CI に詰め込むのは過剰です。
まずは自分が速くなることを優先してください。

---

必要なら次に、
**[「Visual Studio の External Tools 設定画面に何を入れるかを、項目ごとに画像なしで超具体的に書いた版」](chatgpt://followup-prompt?start_index=11146&end_index=11211)**
も出せる。