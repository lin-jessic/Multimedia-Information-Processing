# step 1:正確讀取 RAW 彩色影像(Sequential 格式)
# 檔案格式：512x512，RGB，Sequential(Planar)
# 這支程式會讀 baboon.raw 和 lena.raw
# 然後把它們轉成 R、G、B 三個平面，再顯示出來
import numpy as np
import matplotlib.pyplot as plt
# step 2: RGB 轉 HSI 呼叫
from rgb_to_hsi import rgb_to_hsi
# step 3: 呼叫以 Histogram Equalization 進行 I channel 的加強
from hist_eq_I import hist_equalize_I
#step 4: 呼叫 S 通道做 Gamma Transformation
from gamma_S import gamma_transform_S
# step 5: H 通道做自行定義的色調變化
from modify_H import modify_H
#step 6: HSI 轉 RGB（顯示 HE、 S Gamma 、H channel 修改後的結果）
from hsi_to_rgb import hsi_to_rgb

# 影像的寬跟高(512x512)
width = 512
height = 512
# 一張彩色圖要的總 byte 數 = 寬 * 高 * 3(R,G,B 三個平面)
total_bytes = width * height * 3
# 然後讀一張 RAW 圖片的流程是:
# 1. 用 np.fromfile 把檔案整個讀進來(uint8，0~255)
# 2. 檢查檔案大小對不對
# 3. 切成 R、G、B 三段
# 4. 每段 reshape 成 (height, width)
# 5. 組回一張 RGB 圖片顯示

# 做成一個小函式，等等 baboon 跟 lena 都會用到
def read_raw_image(filename):
    print(f"開始讀取檔案：{filename}")

    # 1. 讀檔(binary)，dtype=uint8 代表每個 byte 是 0~255
    data = np.fromfile(filename, dtype=np.uint8)

    # 2. 檢查大小是否正確
    if data.size != total_bytes:
        print(f"檔案大小不對！讀到 {data.size} bytes，但正常應該是 {total_bytes} bytes")
        # 這邊先直接 return，避免後面 reshape 爆掉
        return None, None, None, None

    # 3. Sequential 排列：所有 R 在前面，接著所有 G，再來是 B
    # 前面 width*height 個是 R
    # 中間 width*height 個是 G
    # 後面 width*height 個是 B
    R_flat = data[0 : width * height]
    G_flat = data[width * height : 2 * width * height]
    B_flat = data[2 * width * height : 3 * width * height]

    # 4. 變成 2D 陣列(影像平面)，每個都是 512x512
    R = R_flat.reshape((height, width))
    G = G_flat.reshape((height, width))
    B = B_flat.reshape((height, width))

    # 5. 把三個平面疊在一起，變成一張 RGB 彩色圖（高,寬,3）
    img_rgb = np.dstack((R, G, B))

    print(f"讀取成功，R, G, B 的 shape 都是：{R.shape}")
    return R, G, B, img_rgb
# 讀取 baboon.raw
R_baboon, G_baboon, B_baboon, img_baboon = read_raw_image("baboon.raw")

if img_baboon is not None:
    plt.figure()
    plt.imshow(img_baboon)
    plt.title("Baboon (from baboon.raw)")
    plt.axis("off") # 不顯示座標
# 讀取 lena.raw
R_lena, G_lena, B_lena, img_lena = read_raw_image("lena.raw")

if img_lena is not None:
    plt.figure()
    plt.imshow(img_lena)
    plt.title("Lena (from lena.raw)")
    plt.axis("off")

# 讀取 add_1.raw
R_add1, G_add1, B_add1, img_add1 = read_raw_image("add_1.raw")

if img_add1 is not None:
    plt.figure()
    plt.imshow(img_add1)
    plt.title("add_1 (from add_1.raw)")
    plt.axis("off")

# 讀取 add_2.raw
R_add2, G_add2, B_add2, img_add2 = read_raw_image("add_2.raw")

if img_add2 is not None:
    plt.figure()
    plt.imshow(img_add2)
    plt.title("add_2 (from add_2.raw)")
    plt.axis("off")

# 顯示四張圖(如果上面都有讀成功)
plt.show()
# 到這裡為止:
# 已經拿到 R_baboon, G_baboon, B_baboon, R_lena, G_lena, B_lena
# 之後做 RGB -> HSI、HE、Gamma 都會用到它們

# step 2: RGB 轉 HSI 呼叫
# 把 baboon RAW 轉成 HSI
H_b, S_b, I_b = rgb_to_hsi(R_baboon, G_baboon, B_baboon)
print("baboon HSI 轉換完成")
# 把 lena RAW 轉成 HSI
H_l, S_l, I_l = rgb_to_hsi(R_lena, G_lena, B_lena)
print("lena HSI 轉換完成")
# add_1 HSI
H_a1, S_a1, I_a1 = rgb_to_hsi(R_add1, G_add1, B_add1)
print("add_1 HSI 轉換完成")
# add_2 HSI
H_a2, S_a2, I_a2 = rgb_to_hsi(R_add2, G_add2, B_add2)
print("add_2 HSI 轉換完成")

# step 3: 呼叫以 Histogram Equalization 進行 I channel 的加強
# 對 baboon 做 HE
# step 3-1: I 通道 HE
I_b_he = hist_equalize_I(I_b)
I_l_he = hist_equalize_I(I_l)

# step 3-2: 手動調整亮度（可調）
brightness_factor = 0.3 # >1 加亮； <1 變暗；1 不變

# baboon
I_b_new = np.clip(I_b_he * brightness_factor, 0, 255)
print("baboon I 通道直方圖均衡化完成！")
# lena
I_l_new = np.clip(I_l_he * brightness_factor, 0, 255)
print("lena I 通道直方圖均衡化完成！")

# add_1 I
I_a1_he = hist_equalize_I(I_a1)
I_a1_new = np.clip(I_a1_he * brightness_factor, 0, 255)
print("add_1 I 通道直方圖均衡化完成！")

# add_2 I
I_a2_he = hist_equalize_I(I_a2)
I_a2_new = np.clip(I_a2_he * brightness_factor, 0, 255)
print("add_2 I 通道直方圖均衡化完成！")


# step 6-1: HSI 轉 RGB（顯示 HE 成果）
# 把新的 I（I_b_new）與原本 H_b、S_b 組在一起轉回 RGB
R_b2, G_b2, B_b2 = hsi_to_rgb(H_b, S_b, I_b_new)
img_b2 = np.dstack((R_b2, G_b2, B_b2))

plt.figure()
plt.imshow(img_b2)
plt.title("Baboon - I channel Histogram Equalization")
plt.axis("off")

# lena 也做一次
R_l2, G_l2, B_l2 = hsi_to_rgb(H_l, S_l, I_l_new)
img_l2 = np.dstack((R_l2, G_l2, B_l2))

plt.figure()
plt.imshow(img_l2)
plt.title("Lena - I channel Histogram Equalization")
plt.axis("off")

# add_1：I channel Histogram Equalization
R_a1_6_1, G_a1_6_1, B_a1_6_1 = hsi_to_rgb(H_a1, S_a1, I_a1_new)
img_a1_6_1 = np.dstack((R_a1_6_1, G_a1_6_1, B_a1_6_1))

plt.figure()
plt.imshow(img_a1_6_1)
plt.title("add_1 - I channel Histogram Equalization")
plt.axis("off")

# add_2
R_a2_6_1, G_a2_6_1, B_a2_6_1 = hsi_to_rgb(H_a2, S_a2, I_a2_new)
img_a2_6_1 = np.dstack((R_a2_6_1, G_a2_6_1, B_a2_6_1))

plt.figure()
plt.imshow(img_a2_6_1)
plt.title("add_2 - I channel Histogram Equalization")
plt.axis("off")

plt.show()

#step 4: 呼叫 S 通道做 Gamma Transformation
gamma_value = 0.2 # 你可以自己調，<1 會更鮮豔
# baboon
S_b_new = gamma_transform_S(S_b, gamma_value)
print("baboon S 通道 Gamma 完成！")
# lena
S_l_new = gamma_transform_S(S_l, gamma_value)
print("lena S 通道 Gamma 完成！")
# add_1 S Gamma
S_a1_new = gamma_transform_S(S_a1, gamma_value)
print("add_1 S 通道 Gamma 完成！")
# add_2 S Gamma
S_a2_new = gamma_transform_S(S_a2, gamma_value)
print("add_2 S 通道 Gamma 完成！")

# step 6-2: HSI 轉 RGB (顯示 S Gamma 的結果)
# baboon，用 S_new + I（原始 I）
R_b3, G_b3, B_b3 = hsi_to_rgb(H_b, S_b_new, I_b)
img_b3 = np.dstack((R_b3, G_b3, B_b3))

plt.figure()
plt.imshow(img_b3)
plt.title("Baboon - S channel Gamma Transformation")
plt.axis("off")

# lena
R_l3, G_l3, B_l3 = hsi_to_rgb(H_l, S_l_new, I_l)
img_l3 = np.dstack((R_l3, G_l3, B_l3))

plt.figure()
plt.imshow(img_l3)
plt.title("Lena - S channel Gamma Transformation")
plt.axis("off")

# add_1 - S Gamma Transformation
R_a1_6_2, G_a1_6_2, B_a1_6_2 = hsi_to_rgb(H_a1, S_a1_new, I_a1)
img_a1_6_2 = np.dstack((R_a1_6_2, G_a1_6_2, B_a1_6_2))

plt.figure()
plt.imshow(img_a1_6_2)
plt.title("add_1 - S channel Gamma Transformation")
plt.axis("off")

# add_2
R_a2_6_2, G_a2_6_2, B_a2_6_2 = hsi_to_rgb(H_a2, S_a2_new, I_a2)
img_a2_6_2 = np.dstack((R_a2_6_2, G_a2_6_2, B_a2_6_2))

plt.figure()
plt.imshow(img_a2_6_2)
plt.title("add_2 - S channel Gamma Transformation")
plt.axis("off")

plt.show()

# step 5: H 通道做自行定義的色調變化
# 設定想偏移的角度，可自行調整
shift_deg = 90
# baboon
H_b_new = modify_H(H_b, shift_deg)
print("baboon H 通道色調變化完成！")
# lena
H_l_new = modify_H(H_l, shift_deg)
print("lena H 通道色調變化完成！")
# add_1 H shift
H_a1_new = modify_H(H_a1, shift_deg)
print("add_1 H 通道色調變化完成！")
# add_2 H shift
H_a2_new = modify_H(H_a2, shift_deg)
print("add_2 H 通道色調變化完成！")

# step 6-3:HSI 轉 RGB(顯示 H channel 修改後的結果)
# baboon（H_new + 原始 S + 原始 I）
R_b4, G_b4, B_b4 = hsi_to_rgb(H_b_new, S_b, I_b)
img_b4 = np.dstack((R_b4, G_b4, B_b4))

plt.figure()
plt.imshow(img_b4)
plt.title("Baboon - H Channel Modified (Hue Shift)")
plt.axis("off")

# lena（H_new + 原始 S + 原始 I）
R_l4, G_l4, B_l4 = hsi_to_rgb(H_l_new, S_l, I_l)
img_l4 = np.dstack((R_l4, G_l4, B_l4))

plt.figure()
plt.imshow(img_l4)
plt.title("Lena - H Channel Modified (Hue Shift)")
plt.axis("off")

# add_1 - H channel Hue Shift
R_a1_6_3, G_a1_6_3, B_a1_6_3 = hsi_to_rgb(H_a1_new, S_a1, I_a1)
img_a1_6_3 = np.dstack((R_a1_6_3, G_a1_6_3, B_a1_6_3))

plt.figure()
plt.imshow(img_a1_6_3)
plt.title("add_1 - H Channel Modified (Hue Shift)")
plt.axis("off")

# add_2
R_a2_6_3, G_a2_6_3, B_a2_6_3 = hsi_to_rgb(H_a2_new, S_a2, I_a2)
img_a2_6_3 = np.dstack((R_a2_6_3, G_a2_6_3, B_a2_6_3))

plt.figure()
plt.imshow(img_a2_6_3)
plt.title("add_2 - H Channel Modified (Hue Shift)")
plt.axis("off")

plt.show()

# step 6-4：最終結果（H、S、I 都做完變化後）
# baboon 最終結果
R_b_final, G_b_final, B_b_final = hsi_to_rgb(H_b_new, S_b_new, I_b_new)
img_b_final = np.dstack((R_b_final, G_b_final, B_b_final))

plt.figure()
plt.imshow(img_b_final)
plt.title("Baboon - Final Enhanced Result")
plt.axis("off")

# lena 最終結果
R_l_final, G_l_final, B_l_final = hsi_to_rgb(H_l_new, S_l_new, I_l_new)
img_l_final = np.dstack((R_l_final, G_l_final, B_l_final))

plt.figure()
plt.imshow(img_l_final)
plt.title("Lena - Final Enhanced Result")
plt.axis("off")

# add_1 最終結果
R_a1_final, G_a1_final, B_a1_final = hsi_to_rgb(H_a1_new, S_a1_new, I_a1_new)
img_a1_final = np.dstack((R_a1_final, G_a1_final, B_a1_final))

plt.figure()
plt.imshow(img_a1_final)
plt.title("add_1 - Final Enhanced Result")
plt.axis("off")
# add_2 最終結果
R_a2_final, G_a2_final, B_a2_final = hsi_to_rgb(H_a2_new, S_a2_new, I_a2_new)
img_a2_final = np.dstack((R_a2_final, G_a2_final, B_a2_final))

plt.figure()
plt.imshow(img_a2_final)
plt.title("add_2 - Final Enhanced Result")
plt.axis("off")

plt.show()