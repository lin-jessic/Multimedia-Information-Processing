# Homework 1:前導練習_讀取Nello.wav並寫出b.wav
import os
# 原始檔名與目標檔名
input_file = "Nello.wav"
output_file = "result/b0.wav"
# 開啟原始檔(rb = read binary)
with open(input_file, "rb") as f_in:
    data = f_in.read() # 讀取整個音檔內容(bytes)
# 開啟輸出檔(wb = write binary)
with open(output_file, "wb") as f_out:
    f_out.write(data) # 把剛剛讀進來的內容原封不動地寫出
print("已輸出result/b0.wav(內容與Nello.wav相同)")