# 移動平均を計算
window_size = 10  # 移動平均の窓幅
moving_avg = widths.rolling(window=window_size).mean()

# 差分を計算
diffs = np.abs(widths - moving_avg)

# しきい値を設定
threshold_diff = np.mean(diffs) + 2 * np.std(diffs)

# 異常検知
anomalies = diffs > threshold_diff

# 異常フレームを出力
anomalous= np.where(anomalies)[0]
print(f"異常: {anomalous}")


# 異常の連続性を確認
anomalous_diff = np.diff(anomalous)
continuous_anomalies = anomalous[anomalous_diff == 1]  # 連続した異常のみ
print(f"連続した異常: {continuous_anomalies}")