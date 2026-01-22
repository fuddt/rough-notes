"""
ロングテールな正のデータに対して
1) 明らかな入力ミス（物理的/業務的にあり得ない値）を除去
2) log1p 空間で MAD による robust z-score を計算
3) 異常値(anomaly) / 極端値(extreme) をフラグ付け
4) サマリを出す

使い方：
    x: 1次元の配列（list / numpy array / pandas Series）
    result = analyze_long_tail(x, upper_physical_limit=1e6, z_thresh=4.0, extreme_q=99.9)

注意：
- upper_physical_limit は統計ではなく「現実世界の制約」で決める
- z_thresh は 4.0 前後が扱いやすい（ロングテールで 3.5 は過敏になりがち）
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import numpy as np


@dataclass
class LongTailAnalysisResult:
    """分析結果をまとめて返すコンテナ"""
    cleaned_values: np.ndarray          # 入力ミス除去後の値
    cleaned_indices: np.ndarray         # 元配列に対するインデックス（cleaned_values の位置対応）
    flags: np.ndarray                   # "normal" / "anomaly" / "extreme"（cleaned_values と同長）
    robust_z_log: np.ndarray            # log1p 空間での robust z-score（cleaned_values と同長）
    thresholds: Dict[str, float]        # 使った閾値など
    summary: Dict[str, Any]             # サマリ統計


def _as_1d_float_array(x) -> np.ndarray:
    """入力を 1次元 float ndarray に正規化（NaN/infは除外対象）"""
    arr = np.asarray(x, dtype=float).reshape(-1)
    return arr


def analyze_long_tail(
    x,
    *,
    upper_physical_limit: float,
    z_thresh: float = 4.0,
    extreme_q: float = 99.9,
    treat_extreme_as: str = "extreme",
) -> LongTailAnalysisResult:
    """
    ロングテール分布（非負）向けの異常値分析。

    Parameters
    ----------
    x : array-like
        非負の数値データ（負値がある場合は例外にする）
    upper_physical_limit : float
        「現実的にあり得ない入力ミス」を判定する上限（ここだけは統計ではなくドメインで決める）
    z_thresh : float
        log1p 空間での robust z-score 閾値（例：4.0）
    extreme_q : float
        極端値フラグ用の上側分位（例：99.9）
    treat_extreme_as : str
        extreme を flags にどう表現するか（デフォルト "extreme"）

    Returns
    -------
    LongTailAnalysisResult
    """
    arr = _as_1d_float_array(x)

    # --- 入力の健全性チェック ---
    # NaN/inf は後で落とす（異常値以前にデータ品質問題）
    finite_mask = np.isfinite(arr)

    # 負値は「今回ない前提」なので、入ってたら設計崩壊として止める
    if np.any(arr[finite_mask] < 0):
        raise ValueError("負の値が含まれています。今回の前提（非負）と矛盾するため停止します。")

    # --- ステップ1：明らかな入力ミス除去（統計を使わない） ---
    # 0以上かつ有限かつ upper_physical_limit 以下だけ残す
    valid_mask = finite_mask & (arr >= 0) & (arr <= upper_physical_limit)

    cleaned_indices = np.flatnonzero(valid_mask)
    x_clean = arr[valid_mask]

    # ここでデータが空/極端に少ないなら分析不可能
    if x_clean.size < 10:
        raise ValueError(f"有効データが少なすぎます: {x_clean.size}件。upper_physical_limit を見直してください。")

    # --- ステップ2：log1p 変換 ---
    x_log = np.log1p(x_clean)

    # --- ステップ3：MAD による robust z-score（log空間） ---
    med = float(np.median(x_log))
    abs_dev = np.abs(x_log - med)
    mad = float(np.median(abs_dev))

    # MAD=0 だと全て同値に近いケースなので z-score が作れない
    if mad == 0.0:
        # ほぼ同じ値しかない（または離散が荒すぎる）状態
        robust_z = np.zeros_like(x_log)
    else:
        # 1.4826 は MAD を正規分布の標準偏差スケールに合わせる補正（≈ 1/0.6745）
        robust_z = (x_log - med) / (1.4826 * mad)

    # --- ステップ4：極端値（分位）と異常値（z）をフラグ付け ---
    # 「極端値」は異常値とは別概念（ただし運用上は別扱いにしたいことが多い）
    extreme_cut = float(np.percentile(x_clean, extreme_q))

    flags = np.full(x_clean.shape, "normal", dtype=object)

    # まず extreme を付与（上側分位）
    flags[x_clean >= extreme_cut] = treat_extreme_as

    # 次に anomaly を付与（優先度は anomaly を強くしたいので上書き）
    flags[np.abs(robust_z) > z_thresh] = "anomaly"

    # --- サマリ統計 ---
    def pct(v: float) -> float:
        return float(np.percentile(x_clean, v))

    summary = {
        "n_total": int(arr.size),
        "n_finite": int(np.sum(finite_mask)),
        "n_valid_after_physical_filter": int(x_clean.size),
        "n_removed_as_invalid_physical": int(np.sum(finite_mask) - np.sum(valid_mask)),
        "min": float(np.min(x_clean)),
        "p50": pct(50),
        "p90": pct(90),
        "p99": pct(99),
        "p999": pct(99.9) if x_clean.size >= 1000 else float("nan"),
        "max": float(np.max(x_clean)),
        "log_median": med,
        "log_mad": mad,
        "anomaly_count": int(np.sum(flags == "anomaly")),
        "extreme_count": int(np.sum(flags == treat_extreme_as)),
        "normal_count": int(np.sum(flags == "normal")),
        "extreme_cut_value": extreme_cut,
    }

    thresholds = {
        "upper_physical_limit": float(upper_physical_limit),
        "z_thresh": float(z_thresh),
        "extreme_q": float(extreme_q),
    }

    return LongTailAnalysisResult(
        cleaned_values=x_clean,
        cleaned_indices=cleaned_indices,
        flags=flags,
        robust_z_log=robust_z,
        thresholds=thresholds,
        summary=summary,
    )


# --- （任意）実行例 ---
if __name__ == "__main__":
    # ダミーデータ例：ロングテール + 入力ミス
    rng = np.random.default_rng(0)
    base = rng.lognormal(mean=4.5, sigma=1.2, size=40000)  # ロングテールっぽい
    base = np.clip(base, 0, None)
    base[0] = 10_000_000  # 入力ミス（地球が壊れる）

    result = analyze_long_tail(
        base,
        upper_physical_limit=1e6,  # ここはドメインで決める
        z_thresh=4.0,
        extreme_q=99.9,
    )

    print("=== SUMMARY ===")
    for k, v in result.summary.items():
        print(f"{k}: {v}")

    # 異常っぽい上位を少し見る
    idx_anom = np.where(result.flags == "anomaly")[0]
    if idx_anom.size > 0:
        top = idx_anom[np.argsort(result.cleaned_values[idx_anom])[-10:]]
        print("\n=== TOP ANOMALIES (cleaned space) ===")
        for i in top:
            print(f"value={result.cleaned_values[i]:.3f}, z_log={result.robust_z_log[i]:.2f}, flag={result.flags[i]}")