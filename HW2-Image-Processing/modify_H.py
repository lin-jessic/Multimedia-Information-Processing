# Step 5:自行定義 H 通道的變化（Hue shift）
# 我選用直觀的方法:把 H 整體加上一個角度
# 例如 shift_degree = 20，表示把色調整體往紅色方向偏移 20 度
# H 的範圍是 0~360，所以加完後記得用 %360 包回合法範圍
import numpy as np

def modify_H(H, shift_degree):
    # 把 H + shift_degree
    H_new = H + shift_degree
    # H 是角度，要確保在 0~360 範圍，所以用取模
    H_new = H_new % 360
    # 轉成 float32（HSI→RGB 時需要）
    return H_new.astype(np.float32)
