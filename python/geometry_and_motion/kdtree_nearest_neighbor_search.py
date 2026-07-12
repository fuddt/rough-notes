import numpy as np
from scipy.spatial import cKDTree

# 例：座標配列 A（探索対象）と B（探索先）
A = np.array([[1, 2], [3, 4], [5, 6]])
B = np.array([[0, 0], [2, 2], [6, 7]])

# B に対して KDTree を構築（1回で済む）
tree = cKDTree(B)

# A の各点に対して、最近傍点のインデックスと距離を取得
distances, indices = tree.query(A, k=1)  # k=1 → 最も近い点だけ

# 最近傍の座標を取得
nearest_points = B[indices]

# 結果を表示
print("Aの各点に対するB内の最も近い点（高速版）:")
for i in range(len(A)):
    print(f"A[{i}] = {A[i]} → 最近傍 B = {nearest_points[i]} (距離 = {distances[i]:.2f})")