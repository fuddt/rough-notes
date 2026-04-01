# Doxygen 運用手順書（Visual Studio 版 / C++ プロジェクト向け）

## 目的

Windows に導入した Doxygen を Visual Studio から使いやすくし、C++ プロジェクトの構造把握を効率化する。

**重要：** Doxygen は Visual Studio の標準機能ではなく、外部ツールとして連携する。

対象範囲：

- Visual Studio から Doxygen を実行する
- Visual Studio から生成結果を開きやすくする
- プロジェクト内に最小限の運用ファイルを置く

-----

## 1. 前提

以下が完了していること。

- Doxygen が Windows にインストールされている
- Graphviz がインストールされている
- `docs/doxygen/Doxyfile` が作成済み
- `tools/generate_doxygen.bat` が作成済み

未完了の場合は先に <DOXYGEN_SETUP_WINDOWS.md> を実施すること。

-----

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
```

Visual Studio のソリューションファイルと同じルートに置くことが望ましい。

理由：

- パスが分かりやすい
- チームメンバーも使いやすい
- External Tools の設定が説明しやすい

-----

## 3. バッチ単体での動作確認

Visual Studio に組み込む前に、バッチが単体で動くことを確認する。

```cmd
tools\generate_doxygen.bat
```

`docs\doxygen\html\index.html` が生成されることを確認する。

> ここで失敗する場合、Visual Studio 連携に進んでも解決しない。先にバッチ単体を通すこと。

-----

## 4. Visual Studio から外部ツールとして実行する

### 4-1. 外部ツールの設定画面を開く

```
Tools → External Tools...
```

### 4-2. 新しい外部ツールを追加する

`Add` を押して以下のように設定する。

|項目               |設定値                                                   |
|-----------------|------------------------------------------------------|
|Title            |`Generate Doxygen`                                    |
|Command          |`C:\your-project\tools\generate_doxygen.bat`（バッチのフルパス）|
|Arguments        |空欄                                                    |
|Initial directory|`C:\your-project`（プロジェクトルート）                          |

### 4-3. 動作の流れ

`Tools → Generate Doxygen` を実行すると：

1. 登録したバッチが呼ばれる
1. Doxygen が実行される
1. HTML が生成される
1. `index.html` がブラウザで開く

-----

## 5. バッチファイルの推奨版

Visual Studio から呼ばれる前提では、以下の構成にすると安定する。

`tools\generate_doxygen.bat`

```bat
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
```

### 各処理の意図

|処理           |意図                                     |
|-------------|---------------------------------------|
|`cd /d %~dp0`|bat ファイル自身の場所へ移動。呼び出し元のカレントディレクトリに依存しない|
|`cd ..`      |`tools\` から1つ上のプロジェクトルートへ移動            |
|`exit /b 0`  |Visual Studio 側に正常終了を返す                |

-----

## 6. Visual Studio からの実行方法

```
Tools → Generate Doxygen
```

-----

## 7. よくある詰まりどころ

### 7-1. Command に `doxygen.exe` を直接指定している

動作する場合もあるが、パスやカレントディレクトリの問題で詰まりやすい。  
`generate_doxygen.bat` を経由する構成が安定する。

### 7-2. Initial directory を適切に設定していない

今回のバッチは自分で `cd` しているため依存を減らしているが、設定は正確に行うこと。

### 7-3. ソリューションの場所とプロジェクトルートがズレている

例：

```text
repo/
├── solution/
│   └── YourSolution.sln
└── product/
    ├── src/
    ├── include/
    ├── docs/
    └── tools/
```

この場合は `Command` と `Initial directory` をその構造に合わせて設定し直す。

-----

## 8. ソリューションエクスプローラに補助ファイルを表示する

`Doxyfile` や `bat` をソリューションエクスプローラ上で見えるようにしたい場合、「既存項目として追加」で以下を追加する。

- `docs\doxygen\Doxyfile`
- `tools\generate_doxygen.bat`

効果：

- チームメンバーが場所を把握しやすくなる
- 右クリックで直接開ける
- 「どこに設定があるか」の質問が減る

> ビルド対象にするわけではない。Visual Studio 上で見せるだけ。

-----

## 9. 個人用途 vs チーム用途

### 個人用途

`Tools → Generate Doxygen` で十分。

### チーム用途

- `tools\generate_doxygen.bat` をリポジトリ管理する
- `docs\doxygen\Doxyfile` をリポジトリ管理する
- README に実行方法を記載する

最初から MSBuild に組み込む必要はない。

-----

## 10. MSBuild / ビルドイベントに組み込むべきか

**最初は組み込まない。**

理由：

- 毎ビルド時に Doxygen が走り、ビルドが重くなる
- 開発者全員に同じ負荷がかかる
- エラー原因の切り分けが難しくなる

推奨する順序：

1. まず手動実行で運用する
1. チームで使えると確認できたら共有する
1. 本当に必要な場合は CI 側での生成を検討する

-----

## 11. どうしてもビルドイベントに組み込む場合

推奨しないが、やるなら以下の手順で設定する。

### 11-1. 設定画面を開く

```
Project → Properties → Build Events → Post-Build Event
```

### 11-2. コマンド例

```
call "$(SolutionDir)tools\generate_doxygen.bat"
```

### 11-3. この方法の問題点

- ビルドのたびに Doxygen が走る
- 生成処理が重い
- Doxygen エラーと C++ ビルドエラーが混在する
- 開発者全員に強制される

常用には向かない。

-----

## 12. Visual Studio と Doxygen の役割分担

### 効率的な使い方の流れ

1. Visual Studio で気になる基底クラス名を見つける
1. `Tools → Generate Doxygen` を実行する
1. ブラウザでそのクラスのページを開く
1. 継承関係を確認する
1. Visual Studio に戻って実装クラスを開く

### 役割分担

|ツール          |用途                    |
|-------------|----------------------|
|Visual Studio|実コード編集・定義ジャンプ・デバッグ    |
|Doxygen      |全体構造の俯瞰・継承関係の可視化・クラス索引|

-----

## 13. README への最低限の記載内容

チームへ共有するとき、README に以下を記載する。

```markdown
# Doxygen の使い方

## 目的
C++ プロジェクトのクラス構造・継承関係を把握するために使う。

## 必要なもの
- Doxygen
- Graphviz

## 設定ファイル
- docs/doxygen/Doxyfile

## 実行方法
- tools/generate_doxygen.bat を実行する
- または Visual Studio の Tools → Generate Doxygen

## 出力先
- docs/doxygen/html/index.html
```

-----

## 14. 運用上の結論

Visual Studio 連携の本質は、Doxygen を IDE の一部に見せることではない。  
巨大 C++ コードベースの構造把握を、普段の開発導線の中に差し込むことが目的。

最初の現実解：

- `Doxyfile` を置く
- `bat` を置く
- Visual Studio の External Tools に登録する

これで十分。  
最初からビルドイベントや CI に組み込むのは過剰。まず自分が速くなることを優先する。
