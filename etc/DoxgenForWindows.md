# Doxygen 導入手順書（Windows 版 / C++ プロジェクト向け）

## 目的

Windows 環境で Doxygen を導入し、巨大な C++ プロジェクトの構造を可視化する。

把握対象：

- クラス一覧
- 継承関係
- 名前空間
- ファイル構成
- include 依存関係

コメントが少ないプロジェクトでも、構造把握には十分機能する。

-----

## 1. 配置方針

### 1-1. ディレクトリ構成

プロジェクトルート直下に以下の構成を作る。

```text
your-project/
├── src/
├── include/
├── docs/
│   └── doxygen/
│       ├── Doxyfile
│       └── html/         ← Doxygen 生成物
├── tools/
│   └── generate_doxygen.bat
└── README.md
```

### 1-2. 各ファイルの役割

|ファイル                        |役割            |
|----------------------------|--------------|
|`docs/doxygen/Doxyfile`     |Doxygen 設定ファイル|
|`tools/generate_doxygen.bat`|Windows 実行用バッチ|
|`docs/doxygen/html/`        |生成先（手動作成不要）   |

-----

## 2. Doxygen のインストール

### 2-1. 公式サイトからインストール

<https://www.doxygen.nl/download.html> よりインストーラを取得して実行する。

インストール後のパス例：

```text
C:\Program Files\doxygen\bin\doxygen.exe
```

### 2-2. インストール確認

コマンドプロンプトで実行する。

```cmd
doxygen --version
```

`doxygen` が見つからない場合は PATH が通っていない。以下いずれかで対応する。

- `doxygen.exe` のあるフォルダを PATH に追加する
- バッチファイルでフルパスを指定する

-----

## 3. Graphviz のインストール

継承図・依存図の出力に必要。

<https://graphviz.org/download/> よりインストーラを取得して実行する。

インストール後のパス例：

```text
C:\Program Files\Graphviz\bin\dot.exe
```

### 3-1. インストール確認

```cmd
dot -V
```

バージョンが表示されれば正常。

-----

## 4. ディレクトリの作成

プロジェクトルート直下に以下を作成する。エクスプローラでの手動作成で構わない。

```text
your-project/
├── docs/
│   └── doxygen/
└── tools/
```

-----

## 5. Doxyfile の生成

コマンドプロンプトでプロジェクトルートへ移動し、以下を実行する。

```cmd
doxygen -g docs\doxygen\Doxyfile
```

以下が生成される。

```text
your-project\docs\doxygen\Doxyfile
```

-----

## 6. Doxyfile の編集

`docs\doxygen\Doxyfile` をテキストエディタで開き、最低限以下を設定する。

```doxyfile
# ----------------------------------------
# 基本情報
# ----------------------------------------
PROJECT_NAME           = "YourProject"
OUTPUT_DIRECTORY       = docs/doxygen

# ----------------------------------------
# 入力対象
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
```

-----

## 7. INPUT をプロジェクトに合わせて修正する

プロジェクト構成が以下の場合：

```text
your-project/
├── app/
├── core/
├── framework/
├── include/
└── third_party/
```

`INPUT` をこのように設定する。

```doxyfile
INPUT = app core framework include
```

> **注意**  
> `third_party` など外部ライブラリは最初は含めない。ノイズが増え、構造把握の妨げになる。

-----

## 8. バッチファイルの作成

`tools\generate_doxygen.bat` を以下の内容で作成する。

```bat
@echo off
REM ==========================================
REM Doxygen ドキュメント生成バッチ
REM どこから呼ばれても動くようにしている
REM ==========================================

REM この bat ファイル自身があるディレクトリへ移動
cd /d %~dp0

REM tools\ の1つ上、つまりプロジェクトルートへ移動
cd ..

REM Doxygen 実行
doxygen docs\doxygen\Doxyfile

REM エラーがあれば中断
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
```

-----

## 9. 実行

エクスプローラから `tools\generate_doxygen.bat` をダブルクリック、またはコマンドプロンプトから実行する。

```cmd
tools\generate_doxygen.bat
```

成功すると以下が生成される。

```text
docs\doxygen\html\index.html
```

-----

## 10. 最初に確認する場所

生成後は以下の順で確認する。

1. **Classes** — クラス一覧
1. **Class Hierarchy** — 継承構造
1. **Files** — ファイル構成
1. **Namespaces** — 名前空間の切り方
1. **個別クラス詳細ページ** — 基底クラス・派生クラス・メンバ関数・定義場所

-----

## 11. よくある失敗

|失敗                       |原因                                        |
|-------------------------|------------------------------------------|
|図が出ない                    |Graphviz を入れていない                          |
|`doxygen` / `dot` が見つからない|PATH が通っていない                              |
|ドキュメントが読みにくい             |外部ライブラリを INPUT に含めている                     |
|生成が極端に重い                 |`CALL_GRAPH` / `CALLER_GRAPH` を最初から有効にしている|

-----

## 12. Git 管理の方針

### 管理対象

- `docs/doxygen/Doxyfile`
- `tools/generate_doxygen.bat`

### 管理対象外

- `docs/doxygen/html/`
- `docs/doxygen/latex/`

`.gitignore` に以下を追加する。

```gitignore
docs/doxygen/html/
docs/doxygen/latex/
```

-----

## 13. チェックリスト

### 初回セットアップ

- [ ] Doxygen をインストールした
- [ ] Graphviz をインストールした
- [ ] `docs\doxygen\` を作成した
- [ ] `tools\generate_doxygen.bat` を作成した
- [ ] `docs\doxygen\Doxyfile` を生成した
- [ ] `INPUT` を自プロジェクト向けに修正した
- [ ] バッチを実行した
- [ ] `index.html` が開いた

### 初回探索

- [ ] Classes を確認した
- [ ] Class Hierarchy を確認した
- [ ] 基底クラスをいくつか特定した
- [ ] Factory / Manager / Controller クラスを特定した
- [ ] 担当ユースケースを1本追った

-----

## 14. この運用の位置づけ

この手順の目的は、完璧な設計文書を作ることではない。  
巨大 C++ プロジェクトへの新規参画時に、構造把握の初速を上げることが目的。

Doxygen は万能ではないが、クラス図が無い現場・コメントが少ない現場では有効な探索ツールとして機能する。
