import numpy as np

def polyfit_with_aic(x, y, max_deg=4):
    """
    NumPyのpolyfitで1〜max_degを順にあて、AIC最小の次数を選ぶ簡易版。
    外れ値耐性や汎化性能の見積りは弱いが、依存なく軽量。
    """
    x = np.asarray(x).ravel()
    y = np.asarray(y).ravel()
    n = len(x)
    if n < 3:
        raise ValueError("点が少なすぎます")

    records = []
    for deg in range(1, max_deg + 1):
        # polyfitは降べき係数を返す: [a_deg, a_deg-1, ..., a0]
        coef = np.polyfit(x, y, deg=deg)
        y_hat = np.polyval(coef, x)
        rss = np.sum((y - y_hat)**2)
        k = deg + 1  # パラメータ数（係数の数）
        # AIC（誤差分散未知・正規仮定なら単純化してOK）
        # AIC = n*log(RSS/n) + 2k
        aic = n * np.log(rss / n) + 2 * k
        records.append({"degree": deg, "coef": coef, "rss": rss, "aic": aic})

    best = min(records, key=lambda d: d["aic"])

    # “2次への移行”簡易判定: 1次→2次でRSSが一定割合以上減ったら2次を優先
    rec1 = next((r for r in records if r["degree"] == 1), None)
    rec2 = next((r for r in records if r["degree"] == 2), None)
    if rec1 and rec2 and rec1["rss"] > 0:
        improve = (rec1["rss"] - rec2["rss"]) / rec1["rss"]
        if improve >= 0.10:
            best = rec2

    coef = best["coef"]  # 降べき: [a, b, c]なら y = a x^2 + b x + c
    deg = best["degree"]

    # 可読式の生成
    terms = []
    for p, c in zip(range(deg, -1, -1), coef):
        if p == 0:
            terms.append(f"{c:.6g}")
        elif p == 1:
            terms.append(f"{c:.6g}x")
        else:
            terms.append(f"{c:.6g}x^{p}")
    equation = "y = " + " + ".join(terms)

    # R^2（説明力）
    y_hat = np.polyval(coef, x)
    ss_res = np.sum((y - y_hat)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    return {
        "best_degree": deg,
        "coef_descending": coef,
        "equation": equation,
        "r2": float(r2),
        "criteria_table": [{k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                            for k, v in rec.items()} for rec in records],
    }


# --- 使い方例 ---
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    x = np.linspace(-3, 3, 50)
    y = 1.5*x**2 + 0.3*x + 2.0 + rng.normal(0, 0.7, size=x.shape)

    res = polyfit_with_aic(x, y, max_deg=4)
    print("選ばれた次数:", res["best_degree"])
    print("式:", res["equation"])
    print("R^2:", res["r2"])