import numpy as np

def angle_between(v1: np.ndarray, v2: np.ndarray) -> float:
    n1 = np.linalg.norm(v1) + 1e-12
    n2 = np.linalg.norm(v2) + 1e-12
    u1 = v1 / n1
    u2 = v2 / n2
    c = float(np.clip(np.dot(u1, u2), -1.0, 1.0))
    return float(np.arccos(c))

def local_theta(points: np.ndarray) -> np.ndarray:
    """
    局所点列（順序あり）に対して曲がり角θを返す。
    端は定義できないのでnan。
    """
    p = np.asarray(points, dtype=float)
    n = len(p)
    theta = np.full(n, np.nan)
    for i in range(1, n - 1):
        v1 = p[i] - p[i - 1]
        v2 = p[i + 1] - p[i]
        theta[i] = angle_between(v1, v2)
    return theta

def mad(x: np.ndarray) -> float:
    """Median Absolute Deviation (外れ値に強いばらつき指標)"""
    x = x[~np.isnan(x)]
    if len(x) == 0:
        return 0.0
    m = np.median(x)
    return float(np.median(np.abs(x - m)))

def judge_break_local(points: np.ndarray, center_idx: int, window: int = 5):
    """
    断線候補点center_idxの前後window点（計2*window+1点）だけで判定する。
    距離は使わない（角度とその滑らかさのみ）。
    """
    p = np.asarray(points, dtype=float)
    n = len(p)

    lo = max(0, center_idx - window)
    hi = min(n, center_idx + window + 1)  # pythonスライスはhiが排他的
    seg = p[lo:hi]

    # seg内での中心位置
    c = center_idx - lo

    # 角度系列
    theta = local_theta(seg)

    # 2階差分（滑らかさ破れ）
    jerk = np.full_like(theta, np.nan)
    for i in range(1, len(seg) - 1):
        if i - 1 < 0 or i + 1 >= len(seg):
            continue
        if np.isnan(theta[i-1]) or np.isnan(theta[i]) or np.isnan(theta[i+1]):
            continue
        jerk[i] = abs(theta[i+1] - 2*theta[i] + theta[i-1])

    # 自動閾値（局所内の分布から決める：固定値より現場で安定しやすい）
    th_med = np.nanmedian(theta)
    th_mad = mad(theta)
    jk_med = np.nanmedian(jerk)
    jk_mad = mad(jerk)

    # 「突出」の判定（kは調整パラメータ）
    k_theta = 3.0
    k_jerk = 3.0
    theta_thr = th_med + k_theta * th_mad
    jerk_thr = jk_med + k_jerk * jk_mad

    # 判定：中心の角度が突出 or 中心のjerkが突出
    is_break = False
    reasons = []

    if 0 <= c < len(seg):
        if not np.isnan(theta[c]) and theta[c] > theta_thr:
            is_break = True
            reasons.append("theta_outlier")
        if not np.isnan(jerk[c]) and jerk[c] > jerk_thr:
            is_break = True
            reasons.append("jerk_outlier")

    return {
        "is_break": is_break,
        "reasons": reasons,
        "segment_range": (lo, hi - 1),
        "theta_center_deg": None if np.isnan(theta[c]) else float(np.rad2deg(theta[c])),
        "jerk_center_deg": None if np.isnan(jerk[c]) else float(np.rad2deg(jerk[c])),
        "theta_thr_deg": float(np.rad2deg(theta_thr)) if not np.isnan(theta_thr) else None,
        "jerk_thr_deg": float(np.rad2deg(jerk_thr)) if not np.isnan(jerk_thr) else None,
    }

# 使い方例:
# points = np.array([(x0,y0),(x1,y1),...])  # 順序あり
# i = 10  # 断線候補点のインデックス
# result = judge_break_local(points, i, window=5)
# print(result)