### インポート
import sys
import time
import copy
import pygame
from pygame.locals import *
from game_class import *

#定数
WINDOW_SIZE_X = 480             #画面横サイズ
WINDOW_SIZE_Y = 640             #画面縦サイズ
BAR_SIZE_X = 150                #バー横サイズ
BAR_SIZE_Y = 10                 #バー縦サイズ
BAR_Y = WINDOW_SIZE_Y * 0.9     #バー縦位置
BAR_SPEED = 10                  #バーの横移動速度
BALL_SIZE = 18                  #ボールサイズ
BALL_SPEED = 10                 #ボール移動速度
BLOCK_SIZE_X = 60               #ブロック横サイズ
BLOCK_SIZE_Y = 30               #ブロック縦サイズ
BLOCK_NUM_X = 8                 #ブロック横列の数
BLOCK_NUM_Y = 5                 #ブロック縦列の数
BLOCK_BLANK = 0                 #ブロック間余白
FRAME_RATE = 50                 #フレームレート
KEY_REPEAT = 20                 #キーリピート間隔

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
ball = Ball("./image/ball.png", bar, blocks)

clock = pygame.time.Clock()
bar_pos = WINDOW_SIZE_X/2


#初期設定
def gameInit():
    pygame.init()
    pygame.display.set_caption("ブロック崩し")
    pygame.mixer.music.load("./sound/audio.mp3")
    pygame.mixer.music.play(1)
    pygame.key.set_repeat(KEY_REPEAT)


#描画関数
def Draw():
    surface.fill((0,0,0))
    bar.draw(surface)
    ball.draw(surface)
    blocks.draw(surface)
    pygame.display.update()

#キー入力
def keyInput(key):
    if key == K_ESCAPE:
        exit()     

def drawString(str):
    ### STARTを表示
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