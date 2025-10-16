import pygame
import numpy as np
import sounddevice as sd
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

samplerate = 44100
blocksize = 1024

circles = []  # 水玉リスト

def audio_callback(indata, frames, time, status):
    global fft_data
    audio = indata[:, 0]
    fft_result = np.fft.rfft(audio)  
    fft_data = np.abs(fft_result)

fft_data = np.zeros(blocksize // 2 + 1)

with sd.InputStream(channels=1, callback=audio_callback,
                    blocksize=blocksize, samplerate=samplerate):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # 200Hz〜800Hzの範囲でFFTを分割
        start_bin = int(200 / (samplerate / blocksize))  # ≈5
        end_bin = int(800 / (samplerate / blocksize))    # ≈18
        fft_segment = fft_data[start_bin:end_bin]

        # 範囲を3つに分割
        low = np.mean(fft_segment[0:5])    # 200-400Hz
        mid = np.mean(fft_segment[5:10])   # 400-600Hz
        high = np.mean(fft_segment[10:18]) # 600-800Hz

        # デバッグ表示
        #print(f"Low:{low:.2f}, Mid:{mid:.2f}, High:{high:.2f}")

        # 一番強い帯域を色に対応
        threshold = 1  # 音を検知する閾値
        if low > mid and low > high and low > threshold:
            color = (0, 0, 255)   # 青 = 低音
        elif mid > high and mid > threshold:
            color = (0, 255, 0)   # 緑 = 中音
        elif high > threshold:
            color = (255, 0, 0)   # 赤 = 高音
        else:
            color = None

        # 新しい水玉を追加
        if color:
            x, y = random.randint(100, 700), random.randint(100, 500)
            circles.append({"pos": (x, y), "radius": 10, "color": color, "alpha": 255})

        # 水玉を描画 & 更新
        new_circles = []
        for c in circles:
            c["radius"] += 3
            c["alpha"] -= 5
            if c["alpha"] > 0:
                s = pygame.Surface((800, 600), pygame.SRCALPHA)
                col = (*c["color"], c["alpha"])
                pygame.draw.circle(s, col, c["pos"], c["radius"], 0)
                screen.blit(s, (0, 0))
                new_circles.append(c)

        circles = new_circles

        pygame.display.flip()
        clock.tick(60)

pygame.quit()

