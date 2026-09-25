# step 2: RGB 轉 HSI
# 這部份程式是依照老師 PPT 上的公式，把 R/G/B 轉成 H/S/I 三個通道
# 因為之後 Step 3、Step 4、Step 5 都會用到 H/S/I
import numpy as np

def rgb_to_hsi(R, G, B):
    # 1. 先把 R, G, B 轉成浮點數，避免後面公式計算被整數截斷
    R = R.astype(np.float32)
    G = G.astype(np.float32)
    B = B.astype(np.float32)
    # 2. 計算 I（Intensity）
    # I = (R + G + B) / 3
    I = (R + G + B) / 3.0
    # 3. 計算 S（Saturation）
    # 如果 R、G、B 三個最小值加起來為 0，S 會變成 0，避免除以 0 錯誤
    min_rgb = np.minimum(np.minimum(R, G), B)
    sum_rgb = R + G + B
    # 4. S = 1 - 3 * min(R,G,B) / (R+G+B)
    # 如果 sum = 0，就直接設成 0
    S = np.where(sum_rgb == 0, 0, 1 - (3 * min_rgb / sum_rgb))
    # 5. 計算 H (Hue)
    # 老師 PPT 的公式:
    # θ = arccos{[(R-G)+(R-B)]/[2*sqrt((R-G)^2+(R-B)(G-B))]}
    # 若 B <= G，H = θ
    # 若 B > G，H = 360° - θ

    # 分子 numerator
    numerator = ( (R - G) + (R - B) ) / 2.0
    # 分母 denominator
    denominator = np.sqrt( (R - G)**2 + (R - B)*(G - B) )
    # 避免除以零
    denominator = np.where(denominator == 0, 1e-6, denominator)
    # acos 的輸入要介於 [-1, 1]
    cos_theta = numerator / denominator
    cos_theta = np.clip(cos_theta, -1, 1)
    # 計算 θ(單位是弧度 rad)
    theta = np.arccos(cos_theta)
    # H 根據 B <= G 或 B > G 分成兩種情況
    H = np.where(B <= G, theta, 2*np.pi - theta)
    # 把 H 從弧度轉成角度
    H = H * 180 / np.pi
    return H, S, I
