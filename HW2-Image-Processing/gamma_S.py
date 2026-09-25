# Step 4：對 S 通道做 Gamma Transformation（飽和度加強）
# Gamma 的公式:
# S_new = S^(gamma)
# 如果 gamma < 1，顏色會變得更飽和、更鮮豔
# 如果 gamma > 1，顏色會變淡、變灰
# S 在 HSI 是 0~1，所以用 S^(gamma) 就可以了
import numpy as np

def gamma_transform_S(S, gamma):
    # 保證 S 在 0~1 之間（避免超出範圍）
    S = np.clip(S, 0, 1)
    # 套用 Gamma 公式
    S_new = S ** gamma
    # 轉回 float32（後面 HSI 轉 RGB 要用）
    return S_new.astype(np.float32)
