### インポート
import sys
import time
import copy
import pygame
from pygame.locals import *
from game_class import *
from const import *

#画面定義
SURFACE = Rect(0, 0, WINDOW_SIZE_X, WINDOW_SIZE_Y)
surface = pygame.display.set_mode(SURFACE.size)

#ミキサー初期設定
pygame.mixer.init()

#インスタンス生成
blocks = pygame.sprite.Group()

for y in range(BLOCK_NUM_Y):
    for x in range(BLOCK_NUM_X):
        blocks.add(Block("./image/block.png", x, y))

bar = Bar("./image/bar.png")
ball = Ball("./image/ball01_red.png", bar, blocks)
screen = Screen("./image/bg_natural_sougen.jpg")

clock = pygame.time.Clock()
bar_pos = WINDOW_SIZE_X/2


#初期設定
def gameInit():
    pygame.init()
    pygame.display.set_caption("ブロック崩し")
    pygame.mixer.music.load("./sound/maou_bgm_8bit18.mp3")
    pygame.mixer.music.play(1)
    pygame.key.set_repeat(KEY_REPEAT)

#描画関数
def Draw():
    screen.draw(surface)
    bar.draw(surface)
    ball.draw(surface)
    blocks.draw(surface)
    pygame.display.update()

#キー入力
def keyInput(key):
    if key == K_ESCAPE:
        exit()     

#文字列表示
def drawString(str):
    font = pygame.font.Font(None, 60)
    text = font.render(str, True, (96,96,255))
    surface.fill((0,0,0))
    surface.blit(text, [133,299])
    pygame.display.update()

def main():
    
    global bar_pos

    #初期設定
    gameInit()

    drawString("START")
    time.sleep(2)

    while True: 
        #フレームレート設定
        clock.tick(FRAME_RATE)
    
        #更新
        bar.update(bar_pos)
        ball.update(surface)

        #画面描画
        Draw()

        #マウス入力
        mouseX, mouseY = pygame.mouse.get_pos()
        bar_pos = mouseX

        for event in pygame.event.get():
            #エラー処理
            if event.type == QUIT:
                exit()
            #キー入力
            if event.type == KEYDOWN:
                keyInput(event.key)
                
def exit():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()