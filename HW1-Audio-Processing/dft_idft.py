# ============================================================
# HW1 離散傅立葉正逆轉換 (20%)
# 題目：對 Nello.wav 做 DFT -> IDFT，不改變內容再輸出 b.wav
# 限制：不得使用 numpy.fft，只能自行撰寫 DFT / IDFT
# 作者：你的名字或學號
# ============================================================

import wave          # 讀寫 wav 檔案
import numpy as np   # 處理陣列與數學運算
import os
import matplotlib.pyplot as plt  # 畫頻譜圖

# ------------------------------------------------------------
# 離散傅立葉轉換 DFT（最基本的 for 迴圈版本）
# ------------------------------------------------------------
def DFT(x):
    N = len(x)             # 資料長度
    X = []                 # 建立空陣列
    for k in range(N):     # 逐一計算每個頻率分量
        real = 0.0
        imag = 0.0
        for n in range(N):
            angle = 2 * np.pi * k * n / N
            real += x[n] * np.cos(-angle)  # 實部
            imag += x[n] * np.sin(-angle)  # 虛部
        X.append(complex(real, imag))      # 寫入複數
    return np.array(X)

# ------------------------------------------------------------
# 離散傅立葉逆轉換 IDFT
# ------------------------------------------------------------
def IDFT(X):
    N = len(X)
    x = []
    for n in range(N):     # 對時間點 n 逐一計算
        s = 0
        for k in range(N): # 對所有頻率分量加總
            angle = 2 * np.pi * k * n / N
            s += X[k] * complex(np.cos(angle), np.sin(angle))
        x.append((s / N).real)             # 取實部
    return np.array(x)

# ------------------------------------------------------------
# 主程式開始
# ------------------------------------------------------------

# Step 1. 建立輸出資料夾
if not os.path.exists("result"):
    os.makedirs("result")

# Step 2. 讀取原始音檔
wav_in = wave.open("Nello.wav", "rb")
params = wav_in.getparams()
frames = wav_in.readframes(wav_in.getnframes())
wav_in.close()

# Step 3. 將 8bit unsigned 轉成 -128~127
data = np.frombuffer(frames, dtype=np.uint8)
data = data.astype(np.int16) - 128

# Step 4. 設定分段長度（可改 128 / 256 / 512）
N = 128
if len(data) % N != 0:
    pad = N - (len(data) % N)
    data = np.append(data, np.zeros(pad))
segments = len(data) // N

result = np.zeros_like(data, dtype=float)

print("總長度:", len(data), "分段長度:", N, "共", segments, "段")

# Step 5. 分段做 DFT -> IDFT
for s in range(segments):
    start = s * N
    end = start + N
    segment = data[start:end]

    # 顯示進度
    if s % 20 == 0:
        print("處理第", s, "段 / 共", segments, "段")

    # --- DFT ---
    X = DFT(segment)

    # 第一段畫頻譜
    if s == 0:
        mag = np.sqrt(np.real(X)**2 + np.imag(X)**2)
        plt.plot(mag)
        plt.title("Magnitude Spectrum (第一段)")
        plt.xlabel("Frequency Bin (k)")
        plt.ylabel("|X[k]|")
        plt.grid(True)
        plt.savefig("result/spectrum_segment1.png")
        plt.close()
        print("已輸出頻譜圖 result/spectrum_segment1.png")

    # --- 不進行濾波（原封不動）---
    Y = X

    # --- IDFT ---
    y = IDFT(Y)
    result[start:end] = y

# Step 6. 轉回 8bit unsigned (0~255)
result = np.clip(result + 128, 0, 255).astype(np.uint8)

# Step 7. 寫出音檔 b.wav
wav_out = wave.open("result/b.wav", "wb")
wav_out.setparams(params)
wav_out.writeframes(result.tobytes())
wav_out.close()

print("完成輸出 result/b.wav")
