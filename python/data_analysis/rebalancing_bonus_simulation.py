import numpy as np, pandas as pd
np.random.seed(42)

# 仮定: A, B は月ごと ±15%／-5% を交互に出す
T = 120  # 月数10年
ret_a = np.where(np.arange(T) % 2 == 0, 1.15, 0.95)
ret_b = np.where(np.arange(T) % 2 == 1, 1.15, 0.95)

cap_a = cap_b = cap_pf = 1.0
pf = []

for ra, rb in zip(ret_a, ret_b):
    # 毎月50:50でリバランス
    w1, w2 = 0.5, 0.5
    cap_a *= ra
    cap_b *= rb
    total = cap_a + cap_b
    cap_a, cap_b = total * w1, total * w2   # 再均等化
    pf.append(total)

print("単体A累積:", cap_a)
print("単体B累積:", cap_b)
print("ポート累積:", pf[-1])        # > 1.0 になる