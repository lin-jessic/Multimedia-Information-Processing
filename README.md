# Multimedia Information Processing

長庚大學資訊工程學系「多媒體資訊概論」課程實作整理。

本 Repository 收錄課程中的音訊與影像處理作業。HW1 以音訊頻域處理為主，自行實作 DFT / IDFT，並比較 Ideal 與 Butterworth Filter 對音訊訊號的影響；HW2 則以彩色影像處理為主，從 RAW RGB 影像讀取開始，實作 RGB / HSI 色彩空間轉換，以及 Histogram Equalization、Gamma Transformation 與 Hue Adjustment。

**Course:** 多媒體資訊概論  
**Institution:** 長庚大學 資訊工程學系  
**Language:** Python  
**Topics:** Digital Signal Processing / Audio Processing / Digital Image Processing

---

## Repository Structure

```text
多媒體資訊概論/
│
├── HW1-Audio-Processing/
│   ├── result/
│   ├── Clocks Striking.wav
│   ├── dft_filter_clock.py
│   ├── dft_filter_old.py
│   ├── dft_filter.py
│   ├── dft_idft.py
│   ├── Nello.wav
│   └── report.pdf
│
├── HW2-Image-Processing/
│   ├── add_1.raw
│   ├── add_2.raw
│   ├── baboon.raw
│   ├── gamma_S.py
│   ├── hist_eq_I.py
│   ├── hsi_to_rgb.py
│   ├── lena.raw
│   ├── main.py
│   ├── modify_H.py
│   ├── report.pdf
│   └── rgb_to_hsi.py
│
└── README.md
```

---

# HW1 — Audio Frequency-Domain Processing

第一份作業以 WAV 音訊訊號為處理對象，將時域訊號轉換至頻域後進行 Filtering，再透過 IDFT 還原為音訊。

本次作業的一項主要要求為：

> 不直接使用 `numpy.fft`，而是自行實作 DFT 與 IDFT。

因此從離散傅立葉轉換、頻域濾波到訊號還原皆由程式完成。

---

## Processing Flow

```text
WAV Audio
    │
    ▼
Read Samples
    │
    ▼
Segment Signal
    │
    ▼
Custom DFT
    │
    ▼
Frequency Spectrum
    │
    ├───────────────┬───────────────┬───────────────┐
    ▼               ▼               ▼               ▼
Ideal LPF       Ideal HPF     Butterworth LPF  Butterworth HPF
    │               │               │               │
    └───────────────┴───────────────┴───────────────┘
                            │
                            ▼
                         IDFT
                            │
                            ▼
                      Output WAV
```

---

## DFT / IDFT

### Discrete Fourier Transform

程式自行依照 DFT 定義計算每個 Frequency Bin：

```text
Time-domain Signal
        │
        ▼
       DFT
        │
        ▼
Frequency-domain Representation
```

將原始離散訊號轉換為複數頻譜後，即可進一步對不同頻率成分進行處理。

### Inverse DFT

Filter 完成後，再自行計算 IDFT：

```text
Filtered Spectrum
        │
        ▼
       IDFT
        │
        ▼
Reconstructed Signal
```

最後將訊號重新轉換成 WAV 格式輸出。

---

## Filters

HW1 實作四種 Frequency-domain Filter：

| Filter | Description |
| --- | --- |
| Ideal Low-pass Filter | 保留低頻、移除高頻 |
| Ideal High-pass Filter | 保留高頻、移除低頻 |
| Butterworth Low-pass Filter | 以較平滑的頻率響應抑制高頻 |
| Butterworth High-pass Filter | 以較平滑的頻率響應抑制低頻 |

程式將音訊切分成固定長度區段，再逐段執行：

```text
DFT → Filtering → IDFT
```

最後重新組合為完整音訊。

---

## HW1 Files
其中 `results/` 保留部分 Filter 後的 WAV 結果與 Frequency Spectrum 圖。

---

# HW2 — Color Image Processing

第二份作業以 512 × 512 RAW 彩色影像為處理對象。

程式首先自行讀取 Sequential / Planar RGB RAW Data，再將 RGB 轉換至 HSI Color Space，分別針對 Intensity、Saturation 與 Hue Channel 進行處理。

測試影像包含：

- `baboon.raw`
- `lena.raw`
- `add_1.raw`
- `add_2.raw`

---

## RAW Image Reading

原始影像採用 Sequential RGB 格式：

```text
┌──────────────┐
│   R Plane    │
├──────────────┤
│   G Plane    │
├──────────────┤
│   B Plane    │
└──────────────┘
```

每個 Channel 為：

```text
512 × 512
```

程式將 RAW Data 分割為 R、G、B 三個平面，再重新組合為 RGB Image。

---

## RGB ↔ HSI

影像處理流程並非直接修改 RGB Channel，而是先進行：

```text
RGB
 │
 ▼
HSI
```

將影像分成：

- **H — Hue**
- **S — Saturation**
- **I — Intensity**

處理完成後，再將：

```text
HSI
 │
 ▼
RGB
```

轉回可顯示的彩色影像。

RGB / HSI 轉換分別實作於：

```text
rgb_to_hsi.py
hsi_to_rgb.py
```

---

## Intensity — Histogram Equalization

Intensity Channel 使用 Histogram Equalization 進行增強。

```text
Original I
    │
    ▼
Histogram
    │
    ▼
CDF
    │
    ▼
Histogram Equalization
    │
    ▼
Enhanced I
```

完成後再與原始 H、S Channel 組合並轉回 RGB。

---

## Saturation — Gamma Transformation

Saturation Channel 使用 Gamma Transformation 調整影像的色彩飽和程度。

概念上：

```text
Original S
    │
    ▼
Gamma Transformation
    │
    ▼
Modified S
```

再與 H、I Channel 組合觀察色彩變化。

---

## Hue Modification

Hue Channel 則透過指定角度進行 Hue Shift。

```text
Original H
    │
    ▼
Hue Shift
    │
    ▼
Modified H
```

用來觀察 Hue 改變對整體影像色調造成的影響。

---

## Final Processing

最後將三個處理結果組合：

```text
Modified H
    +
Gamma-adjusted S
    +
Histogram-equalized I
    │
    ▼
HSI → RGB
    │
    ▼
Final Enhanced Image
```

藉此比較單獨修改 H、S、I Channel 與同時進行多種處理後的影像差異。

---

## HW2 Program Structure

| File | Function |
| --- | --- |
| `main.py` | 讀取 RAW Image 並控制完整影像處理流程 |
| `rgb_to_hsi.py` | RGB → HSI Color Space Conversion |
| `hsi_to_rgb.py` | HSI → RGB Color Space Conversion |
| `hist_eq_I.py` | Intensity Channel Histogram Equalization |
| `gamma_S.py` | Saturation Channel Gamma Transformation |
| `modify_H.py` | Hue Channel Modification |

---

## Processing Pipeline

```text
RAW RGB Image
      │
      ▼
Read R / G / B Planes
      │
      ▼
   RGB → HSI
      │
 ┌────┼─────────────┐
 ▼    ▼             ▼
 H    S             I
 │    │             │
Hue  Gamma       Histogram
Shift Transform  Equalization
 │    │             │
 └────┼─────────────┘
      ▼
 Modified HSI
      │
      ▼
   HSI → RGB
      │
      ▼
Processed Image
```

---

## Requirements

主要使用：

```text
Python
NumPy
Matplotlib
```

HW1 另外使用 Python 內建 `wave` module 處理 WAV 音訊。

---

## Documents

- [`HW1 Report`](./HW1-Audio-Processing/report.pdf) — 音訊頻域處理作業報告
- [`HW2 Report`](./HW2-Image-Processing/report.pdf) — 彩色影像處理作業報告

---

## What I Learned

這兩次作業讓我分別從音訊與影像兩種資料型態實際操作多媒體訊號處理。

HW1 從 DFT 的數學定義自行完成頻域轉換與 IDFT，而不是直接呼叫 FFT 函式，使我能更直接理解時域、頻域與 Filter 之間的關係；將處理後的訊號重新輸出為 WAV，也讓頻率處理的結果可以透過實際聲音進行比較。

HW2 則從 RAW Image 的資料排列開始，逐步完成 RGB / HSI 轉換，再分別處理 Hue、Saturation 與 Intensity。透過 Histogram Equalization、Gamma Transformation 與 Hue Shift，我更具體理解不同 Color Channel 對影像亮度、飽和度與色調的影響。

---

> 本 Repository 為大學課程作業成果整理，內容以課程期間實際完成之程式、實驗資料與報告為主。
