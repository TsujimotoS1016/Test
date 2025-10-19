import pygame
import numpy as np
import sounddevice as sd
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

samplerate = 44100
blocksize = 1024

def audio_callback(indata, frames, time, status):
    global volume
    volume = np.linalg.norm(indata) * 10

volume = 0
with sd.InputStream(channels=1, callback=audio_callback,
                    blocksize=blocksize, samplerate=samplerate):
    running = True
    x = 400 #中心
    y = 300
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        radius = int(volume)  # 音量に応じて半径変化
        pygame.draw.circle(screen, (100, 200, 255), (x, y), radius)
        x += random.randint(-15, 15)
        y += random.randint(-15, 15)

        # 画面外に出ないように制限
        x = max(0, min(800, x))
        y = max(0, min(600, y))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
