# データフロー調査 PlantUML テンプレート集

## 1. 全体処理フロー図

### 図の名称

全体処理フロー図

### 何を表すか

- 元構造体
- 中間構造体
- 最終構造体
- 関数ポインタ / 条件コンパイル分岐
- DLL / ローカル処理
- 最終利用箇所

### PlantUML テンプレコード

```plantuml
@startuml
left to right direction

rectangle "元構造体\nSourceStruct" as SRC
rectangle "中間構造体A\nWorkStruct" as MID1
rectangle "中間構造体B\nDispatchStruct" as MID2
rectangle "分岐関数\nDispatch()" as DISP

rectangle "DLL経路\nFunction Pointer Call" as DLLPATH
rectangle "ローカル経路\nLocal Function Call" as LOCALPATH

rectangle "最終利用箇所\nCalculation / Judge / Output" as FINAL

SRC --> MID1 : 値を設定
MID1 --> MID2 : 値を詰め替え
MID2 --> DISP : 最終入力
DISP --> DLLPATH : #ifdef 有効時
DISP --> LOCALPATH : #ifdef 無効時
DLLPATH --> FINAL
LOCALPATH --> FINAL

@enduml
```

---

## 2. パラメータ影響フロー図

### 図の名称

パラメータ影響フロー図（個別）

### 何を表すか

- 1つのパラメータが
- どのメンバーに移り
- どの関数を通って
- 最終的にどこへ効くか

### PlantUML テンプレコード

```plantuml
@startuml
top to bottom direction

rectangle "元構造体\nSourceStruct.paramA" as P1
rectangle "関数\nbuild_work_param()" as F1
rectangle "中間構造体\nWorkStruct.limit" as P2
rectangle "関数\nbuild_dispatch_input()" as F2
rectangle "最終構造体\nDispatchStruct.limit" as P3
rectangle "関数\nexecute_calc()" as F3
rectangle "最終利用箇所\njudge_result()" as P4

P1 --> F1
F1 --> P2
P2 --> F2
F2 --> P3
P3 --> F3
F3 --> P4 : 比較条件に使用

@enduml
```

---

## 3. 関数経路図

### 図の名称

関数経路図

### 何を表すか

- 値がどの関数を経由して運ばれるか
- 中間構造体よりも「関数の流れ」を見せたいとき用

### PlantUML テンプレコード

```plantuml
@startuml
top to bottom direction

rectangle "load_config()" as F1
rectangle "build_work_param()" as F2
rectangle "build_dispatch_input()" as F3
rectangle "dispatch_execute()" as F4
rectangle "execute_local() / execute_dll()" as F5
rectangle "judge_result()" as F6

F1 --> F2 : 元構造体を受け取る
F2 --> F3 : 中間構造体を生成
F3 --> F4 : 最終構造体を渡す
F4 --> F5 : 経路分岐
F5 --> F6 : 計算結果を利用

@enduml
```

---

## 4. 条件コンパイル分岐図

### 図の名称

条件コンパイル分岐図

### 何を表すか

- `#ifdef` によって処理経路がどう変わるか
- DLL 経路とローカル経路の違い

### PlantUML テンプレコード

```plantuml
@startuml
top to bottom direction

rectangle "dispatch_execute()" as D

if "#ifdef USE_DLL" then (true)
  rectangle "関数ポインタ呼び出し\nfp_handler(&input)" as DLLCALL
  rectangle "DLL側処理" as DLLPROC
  D --> DLLCALL
  DLLCALL --> DLLPROC
else (false)
  rectangle "ローカル関数呼び出し\nlocal_handler(&input)" as LOCALCALL
  rectangle "ローカル処理" as LOCALPROC
  D --> LOCALCALL
  LOCALCALL --> LOCALPROC
endif

rectangle "最終計算 / 判定 / 出力" as FINAL
DLLPROC --> FINAL
LOCALPROC --> FINAL

@enduml
```

---

## 5. 構造体変換図

### 図の名称

構造体変換図

### 何を表すか

- 構造体Aのどのメンバーが
- 構造体B/Cのどこへ入るか
- 名前変更が多いときに有効

### PlantUML テンプレコード

```plantuml
@startuml
left to right direction

rectangle "元構造体\nSourceStruct" as S {
  rectangle "paramA" as S1
  rectangle "paramB" as S2
  rectangle "paramC" as S3
}

rectangle "中間構造体\nWorkStruct" as W {
  rectangle "limit" as W1
  rectangle "mode" as W2
  rectangle "unusedX" as W3
}

rectangle "最終構造体\nDispatchStruct" as D {
  rectangle "threshold" as D1
  rectangle "execMode" as D2
}

S1 --> W1
S2 --> W2
W1 --> D1
W2 --> D2

@enduml
```

---

## 6. 確認状況マップ

### 図の名称

確認状況マップ

### 何を表すか

- どこまで確認済みか
- DLL 内部未確認などを可視化

### PlantUML テンプレコード

```plantuml
@startuml
left to right direction

rectangle "元構造体\n確認済み" as A
rectangle "中間構造体\n確認済み" as B
rectangle "最終構造体\n確認済み" as C
rectangle "関数ポインタ呼び出し\n確認済み" as D
rectangle "DLL内部\n未確認" as E

A --> B
B --> C
C --> D
D --> E

note bottom of E
DLLソースなし / 内部利用未確認
end note

@enduml
```

---

## どの図を使うべきか

最低限ならこの3つでいい。

1. 全体処理フロー図
2. パラメータ影響フロー図（重要パラメータだけ）
3. 条件コンパイル分岐図

余裕があれば追加。

4. 構造体変換図
5. 確認状況マップ

---

## 使い分け

**全体を見せたい**
- 全体処理フロー図

**このパラメータがどう効くか見せたい**
- パラメータ影響フロー図

**関数を通る流れを見せたい**
- 関数経路図

**`#ifdef` がややこしい**
- 条件コンパイル分岐図

**名前変更が多くてしんどい**
- 構造体変換図

**どこまで確認したか示したい**
- 確認状況マップ
