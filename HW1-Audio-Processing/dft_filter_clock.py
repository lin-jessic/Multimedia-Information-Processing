# HW1 頻域的變音處理 (20%)
# 題目：對 Clocks Striking.wav 進行 DFT → Filtering → IDFT
# 實作理想低通(ILPF)、理想高通(IHPF)、
#      Butterworth 低通(BLPF)、Butterworth 高通(BHPF)、
#      自創加分項目：Butterworth 帶通(BPF)
# 限制：不得使用 numpy.fft，只能自行撰寫 DFT / IDFT
import wave
import numpy as np
import os
import matplotlib.pyplot as plt
# 離散傅立葉轉換 DFT
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
# 離散傅立葉逆轉換 IDFT
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
# 濾波器設計（理想 & Butterworth）
def ideal_lowpass(X, cutoff):
    N = len(X)
    H = np.zeros(N)
    H[:cutoff] = 1
    H[-cutoff:] = 1
    return X * H
def ideal_highpass(X, cutoff):
    N = len(X)
    H = np.ones(N)
    H[:cutoff] = 0
    H[-cutoff:] = 0
    return X * H
def butterworth_lowpass(X, cutoff, n=2):
    N = len(X)
    H = np.zeros(N)
    for k in range(N):
        D = abs(k - N / 2)
        H[k] = 1 / (1 + (D / cutoff) ** (2 * n))
    return X * H
def butterworth_highpass(X, cutoff, n=2):
    N = len(X)
    H = np.zeros(N)
    for k in range(N):
        D = abs(k - N / 2)
        if D == 0:
            H[k] = 0
        else:
            H[k] = 1 / (1 + (cutoff / D) ** (2 * n))
    return X * H
# 自創加分項目：Butterworth 帶通濾波器 (BPF)
def butterworth_bandpass(X, low_cut, high_cut, n=2):
    N = len(X)
    H = np.zeros(N)
    for k in range(N):
        D = abs(k - N / 2)
        if D == 0:
            H[k] = 0
        else:
            # 低通 × 高通 = 帶通
            H_low = 1 / (1 + (D / high_cut) ** (2 * n))
            H_high = 1 / (1 + (low_cut / D) ** (2 * n))
            H[k] = H_low * H_high
    return X * H
# 主程式開始
if not os.path.exists("result"):
    os.makedirs("result")
# Step 1. 讀取 Clocks Striking.wav
wav_in = wave.open("Clocks Striking.wav", "rb")
params = wav_in.getparams()
frames = wav_in.readframes(wav_in.getnframes())
wav_in.close()
# Step 2. 轉成 -128~127
data = np.frombuffer(frames, dtype=np.uint8)
data = data.astype(np.int16) - 128
# Step 3. 設定分段長度與截止頻率
N = 256
cutoff = 40
low_cut = 30
high_cut = 100
if len(data) % N != 0:
    pad = N - (len(data) % N)
    data = np.append(data, np.zeros(pad))
segments = len(data) // N
print("資料長度:", len(data), "每段 N =", N, "共", segments, "段")
# Step 4. 建立五個輸出空間
out_low = np.zeros_like(data, dtype=float)
out_high = np.zeros_like(data, dtype=float)
out_butter_low = np.zeros_like(data, dtype=float)
out_butter_high = np.zeros_like(data, dtype=float)
out_band = np.zeros_like(data, dtype=float)
# Step 5. 分段處理
for s in range(segments):
    start = s * N
    end = start + N
    seg = data[start:end]
    if s % 100 == 0:
        print("進度:", s, "/", segments)
    X = DFT(seg)
    # 各種濾波器
    Y_low = ideal_lowpass(X, cutoff)
    Y_high = ideal_highpass(X, cutoff)
    Y_butter_low = butterworth_lowpass(X, cutoff)
    Y_butter_high = butterworth_highpass(X, cutoff)
    Y_band = butterworth_bandpass(X, low_cut, high_cut)
    # IDFT 還原
    out_low[start:end] = IDFT(Y_low)
    out_high[start:end] = IDFT(Y_high)
    out_butter_low[start:end] = IDFT(Y_butter_low)
    out_butter_high[start:end] = IDFT(Y_butter_high)
    out_band[start:end] = IDFT(Y_band)
# Step 6. 轉回 8bit unsigned (0~255)
def to_uint8(x):
    return np.clip(x + 128, 0, 255).astype(np.uint8)
out_low = to_uint8(out_low)
out_high = to_uint8(out_high)
out_butter_low = to_uint8(out_butter_low)
out_butter_high = to_uint8(out_butter_high)
out_band = to_uint8(out_band)
# Step 7. 寫出音檔
def save_wav(name, data):
    wav_out = wave.open(f"result/{name}", "wb")
    wav_out.setparams(params)
    wav_out.writeframes(data.tobytes())
    wav_out.close()
save_wav("clock_low.wav", out_low)
save_wav("clock_high.wav", out_high)
save_wav("clock_butter_low.wav", out_butter_low)
save_wav("clock_butter_high.wav", out_butter_high)
save_wav("clock_butter_band.wav", out_band)
print("✅ Clocks Striking.wav 濾波完成！")
print("輸出五個音檔：")
print("result/clock_low.wav          -> 理想低通")
print("result/clock_high.wav         -> 理想高通")
print("result/clock_butter_low.wav   -> Butterworth 低通")
print("result/clock_butter_high.wav  -> Butterworth 高通")
print("result/clock_butter_band.wav  -> 自創加分：Butterworth 帶通 (BPF)")
