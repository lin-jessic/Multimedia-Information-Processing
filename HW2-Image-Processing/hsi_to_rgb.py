# step 6:將 H, S, I 轉回 R, G, B
# 公式來自課堂 HSI 轉 RGB 定義(老師 PPT)
import numpy as np

def hsi_to_rgb(H, S, I):
    # 把角度轉回弧度(公式要使用弧度)
    H = H * np.pi / 180.0
    R = np.zeros_like(H)
    G = np.zeros_like(H)
    B = np.zeros_like(H)
    # 三段 H 區間(因為 RGB 分段定義)
    # 0 ~ 120度
    idx1 = (H >= 0) & (H < 2*np.pi/3)
    # 120 ~ 240度
    idx2 = (H >= 2*np.pi/3) & (H < 4*np.pi/3)
    # 240° ~ 360°
    idx3 = (H >= 4*np.pi/3) & (H < 2*np.pi)
    # 第一段：0~120度
    H1 = H[idx1]
    S1 = S[idx1]
    I1 = I[idx1]
    B[idx1] = I1 * (1 - S1)
    R[idx1] = I1 * (1 + (S1 * np.cos(H1) / np.cos(np.pi/3 - H1)))
    G[idx1] = 3*I1 - (R[idx1] + B[idx1])
    # 第二段：120~240度
    H2 = H[idx2] - 2*np.pi/3
    S2 = S[idx2]
    I2 = I[idx2]
    R[idx2] = I2 * (1 - S2)
    G[idx2] = I2 * (1 + (S2 * np.cos(H2) / np.cos(np.pi/3 - H2)))
    B[idx2] = 3*I2 - (R[idx2] + G[idx2])
    # 第三段：240~360度
    H3 = H[idx3] - 4*np.pi/3
    S3 = S[idx3]
    I3 = I[idx3]
    G[idx3] = I3 * (1 - S3)
    B[idx3] = I3 * (1 + (S3 * np.cos(H3) / np.cos(np.pi/3 - H3)))
    R[idx3] = 3*I3 - (G[idx3] + B[idx3])
    # 裁切到合法範圍
    R = np.clip(R, 0, 255).astype(np.uint8)
    G = np.clip(G, 0, 255).astype(np.uint8)
    B = np.clip(B, 0, 255).astype(np.uint8)
    return R, G, B
