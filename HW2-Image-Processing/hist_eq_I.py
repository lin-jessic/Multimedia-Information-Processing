# Step 3:對 I 通道進行 Histogram Equalization(直方圖均衡化)
# 這支程式的目的：
# 把從 HSI 得到的 I（亮度）通道做對比度提升
# 讓暗的地方變亮、亮的地方變暗，使整體亮度分布更平均
# 直方圖均衡化主要流程：
# 1. 計算 I channel 每個亮度值(0~255)出現的次數 → histogram
# 2. 計算累積分布函數 CDF（每個亮度以下的累積機率）
# 3. 把舊 I 值映射到新的值： new_I = CDF[I] * 255
import numpy as np

def hist_equalize_I(I):
    # I 是 float 值（由 RGB→HSI 得來），但 HE 需要用 0~255 的整數亮度
    # 所以先做 clipping + 轉成 uint8
    I_uint8 = np.clip(I, 0, 255).astype(np.uint8)
    # 1. 計算 histogram (0~255 共 256 個 bin)
    hist, bins = np.histogram(I_uint8, bins=256, range=(0, 255))
    # 2. 計算累積分布函數 CDF
    cdf = hist.cumsum() # 累積到目前亮度為止的像素數量
    cdf_normalized = cdf / cdf[-1] # 除以最後一個累積值，正規化到 0~1
    # 3. 建立新的 mapping：把亮度值 0~255 映射到新亮度
    # new_value = CDF[value] * 255
    new_values = (cdf_normalized * 255).astype(np.uint8)
    # 4. 套用 mapping 取代舊 I 值
    I_equalized = new_values[I_uint8]
    # 轉回 float32（後面還會和 S、H 一起轉回 RGB）
    return I_equalized.astype(np.float32)
