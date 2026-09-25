# ============================================================
# HW1 頻域的變音處理 (30%)
# 題目：對 Nello.wav 做 DFT -> Filtering -> IDFT
# 實作理想低通(ILPF)、理想高通(IHPF)、
# Butterworth低通(BLPF)、Butterworth高通(BHPF)
# 並輸出四個音檔
# 限制：不得使用 numpy.fft，只能自行撰寫 DFT / IDFT

import wave
import numpy as np
import os
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 自訂：離散傅立葉轉換 DFT
# ------------------------------------------------------------
def DFT(x):
    N = len(x)
    X = []
    for k in range(N):
        real = 0.0
        imag = 0.0
        for n in range(N):
            angle = 2 * np.pi * k * n / N
            real += x[n] * np.cos(-angle)
            imag += x[n] * np.sin(-angle)
        X.append(complex(real, imag))
    return np.array(X)

# ------------------------------------------------------------
# 自訂：離散傅立葉逆轉換 IDFT
# ------------------------------------------------------------
def IDFT(X):
    N = len(X)
    x = []
    for n in range(N):
        s = 0
        for k in range(N):
            angle = 2 * np.pi * k * n / N
            s += X[k] * complex(np.cos(angle), np.sin(angle))
        x.append((s / N).real)
    return np.array(x)

# ------------------------------------------------------------
# 濾波器設計
# ------------------------------------------------------------
def ideal_lowpass(X, cutoff):
    """理想低通濾波器：保留低頻、去除高頻"""
    N = len(X)
    H = np.zeros(N)
    H[:cutoff] = 1
    H[-cutoff:] = 1
    return X * H

def ideal_highpass(X, cutoff):
    """理想高通濾波器：保留高頻、去除低頻"""
    N = len(X)
    H = np.ones(N)
    H[:cutoff] = 0
    H[-cutoff:] = 0
    return X * H

def butterworth_lowpass(X, cutoff, n=2):
    """Butterworth 低通濾波器 (BLPF)"""
    N = len(X)
    H = np.zeros(N)
    for k in range(N):
        D = abs(k - N / 2)                    # 距離中心頻率的距離
        H[k] = 1 / (1 + (D / cutoff) ** (2 * n))
    return X * H

def butterworth_highpass(X, cutoff, n=2):
    """Butterworth 高通濾波器 (BHPF)"""
    N = len(X)
    H = np.zeros(N)
    for k in range(N):
        D = abs(k - N / 2)
        # 高通濾波器公式為 1 / (1 + (cutoff / D)^(2n))
        if D == 0:     # 避免除以 0
            H[k] = 0
        else:
            H[k] = 1 / (1 + (cutoff / D) ** (2 * n))
    return X * H

# ------------------------------------------------------------
# 主程式開始
# ------------------------------------------------------------

# Step 1. 建立輸出資料夾
if not os.path.exists("result"):
    os.makedirs("result")

# Step 2. 讀取 Nello.wav 音檔
wav_in = wave.open("Nello.wav", "rb")
params = wav_in.getparams()
frames = wav_in.readframes(wav_in.getnframes())
wav_in.close()

# Step 3. 將 8bit unsigned 轉成 -128~127 的整數
data = np.frombuffer(frames, dtype=np.uint8)
data = data.astype(np.int16) - 128

# Step 4. 設定分段長度 N（可改 128 / 256 / 512）
N = 256
if len(data) % N != 0:
    pad = N - (len(data) % N)
    data = np.append(data, np.zeros(pad))
segments = len(data) // N
print("資料長度:", len(data), "每段 N =", N, "共", segments, "段")

# Step 5. 建立四個輸出陣列
out_low = np.zeros_like(data, dtype=float)
out_high = np.zeros_like(data, dtype=float)
out_butter_low = np.zeros_like(data, dtype=float)
out_butter_high = np.zeros_like(data, dtype=float)

# Step 6. 設定截止頻率 (cutoff)
cutoff = 40

# Step 7. 每段做 DFT -> 濾波 -> IDFT
for s in range(segments):
    start = s * N
    end = start + N
    seg = data[start:end]

    if s % 100 == 0:
        print("進度:", s, "/", segments)

    X = DFT(seg)

    # 第一段畫頻譜
    if s == 0:
        mag = np.sqrt(np.real(X)**2 + np.imag(X)**2)
        plt.figure()
        plt.plot(mag)
        plt.title("原始頻譜 (第一段)")
        plt.xlabel("k")
        plt.ylabel("|X[k]|")
        plt.grid(True)
        plt.savefig("result/spectrum_original.png")
        plt.close()
        print("已輸出頻譜圖 result/spectrum_original.png")

    # 四種濾波器
    Y_low = ideal_lowpass(X, cutoff)
    Y_high = ideal_highpass(X, cutoff)
    Y_butter_low = butterworth_lowpass(X, cutoff, n=2)
    Y_butter_high = butterworth_highpass(X, cutoff, n=2)

    # 逆轉換還原
    y_low = IDFT(Y_low)
    y_high = IDFT(Y_high)
    y_butter_low = IDFT(Y_butter_low)
    y_butter_high = IDFT(Y_butter_high)

    # 合併結果
    out_low[start:end] = y_low
    out_high[start:end] = y_high
    out_butter_low[start:end] = y_butter_low
    out_butter_high[start:end] = y_butter_high

# Step 8. 轉回 8bit unsigned (0~255)
def to_uint8(x):
    return np.clip(x + 128, 0, 255).astype(np.uint8)

out_low = to_uint8(out_low)
out_high = to_uint8(out_high)
out_butter_low = to_uint8(out_butter_low)
out_butter_high = to_uint8(out_butter_high)

# Step 9. 寫出音檔
def save_wav(name, data):
    wav_out = wave.open(f"result/{name}", "wb")
    wav_out.setparams(params)
    wav_out.writeframes(data.tobytes())
    wav_out.close()

save_wav("b_low.wav", out_low)
save_wav("b_high.wav", out_high)
save_wav("b_butter_low.wav", out_butter_low)
save_wav("b_butter_high.wav", out_butter_high)

print("已輸出四個音檔：")
print("result/b_low.wav         -> 理想低通")
print("result/b_high.wav        -> 理想高通")
print("result/b_butter_low.wav  -> Butterworth 低通")
print("result/b_butter_high.wav -> Butterworth 高通")
