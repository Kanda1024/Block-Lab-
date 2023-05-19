### インポート
import sys
import time
import copy
import pygame
from pygame.locals import *

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

#バークラス
class Bar(pygame.sprite.Sprite):
    #初期化メソッド
    def __init__(self, image_name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_name).convert()
        self.image = pygame.transform.scale(self.image, (BAR_SIZE_X, BAR_SIZE_Y))
        self.rect = self.image.get_rect()
    
    #バーの位置更新
    def update(self, bar_x):
        #バーの位置
        self.rect.centerx = bar_x
        self.rect.centery = BAR_Y

        #画面内に収める
        #self.rect.clamp_ip(SURFACE)
    #バーの描画
    def draw(self, surface):
        surface.blit(self.image, self.rect)


#ボールクラス
class Ball(pygame.sprite.Sprite):
    #初期化メソッド
    def __init__(self, image_name, bar, block):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect()
        self.sound_bar = pygame.mixer.Sound("./sound/maou_se_system41.wav")
        self.sound_block = pygame.mixer.Sound("./sound/maou_se_system35.wav")
    
        self.vx = 0               #ボール横速度
        self.vy = 0               #ボール縦速度
        self.bar = bar              #バーを参照
        self.block  = block         #ブロックを参照
        self.update = self.setup    #初期状態

    def setup(self, surface):
        #ボール初期位置
        self.rect.centerx = int(SURFACE.width/2) + 1
        self.rect.centery = int(SURFACE.height/3)
        #ボール初期速度
        self.vx = BALL_SPEED
        self.vy = BALL_SPEED

        self.update = self.moveBall

    #ボールの挙動
    def moveBall(self, surface):
        #ボールの位置更新
        self.rect.centerx += int(self.vx)
        self.rect.centery += int(self.vy)
        #左壁の反射
        if self.rect.left <= SURFACE.left:
            self.rect.left = SURFACE.left
            self.vx *= -1
        #右壁の反射
        if self.rect.right >= SURFACE.right:
            self.rect.right = SURFACE.right
            self.vx *= -1
        #上壁の反射
        if self.rect.top <= SURFACE.top:
            self.rect.top = SURFACE.top
            self.vy *= -1
        #ボールとバーの当たり判定
        if self.rect.colliderect(self.bar.rect):
            self.sound_bar.play(0)
            self.rect.centery = self.bar.rect.top
            self.vy *= -1
        
        #ゲーム失敗判定
        if self.rect.bottom >= SURFACE.bottom:
            ### GAME OVERを表示
            font = pygame.font.Font(None, 60)
            text = font.render("GAME OVER", True, (255,31,31))
            surface.blit(text, [73,299])

        ### ブロック接触リスト取得(接触したブロックは削除)
        block_list = pygame.sprite.spritecollide(self, self.block, True)

        #ブロックに接触した場合
        if len(block_list) >= 1:
            ball_rect = copy.copy(self.rect)

            for block in block_list:
                    #ブロック上に接触
                    if block.rect.top > ball_rect.top and block.rect.bottom > ball_rect.bottom and self.vy > 0:
                        self.rect.bottom = block.rect.top
                        self.vy *= -1
                        self.sound_block.play(0)
                    #ブロック下に接触
                    if block.rect.top < ball_rect.top and block.rect.bottom < ball_rect.bottom and self.vy < 0:
                        self.rect.top = block.rect.bottom
                        self.vy *= -1
                        self.sound_block.play(0)
                    #ブロック左に接触
                    if block.rect.left > ball_rect.left and block.rect.right > ball_rect.right and self.vx > 0:
                        self.rect.right = block.rect.left
                        self.vx *= -1
                        self.sound_block.play(0)
                    #ブロック右に接触
                    if block.rect.left < ball_rect.left and block.rect.right < ball_rect.right and self.vx < 0:
                        self.rect.left = block.rect.right
                        self.vx *= -1
                        self.sound_block.play(0)
        
            #ゲームクリア判定
            if len(self.block) == 0:
                ### GAME CLEARを表示
                font = pygame.font.Font(None, 60)
                text = font.render("GAME CLEAR", True, (63,255,63))
                surface.blit(text, [59,299])
                pygame.display.update()

                ### CLEAR画面時間
                time.sleep(20)
    #ボールの描画
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Block(pygame.sprite.Sprite):
    #初期化メソッド
    def __init__(self, image_name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_name).convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE_X, BLOCK_SIZE_Y))
        self.rect = self.image.get_rect()
        #ブロック位置の取得
        self.rect.left = x * (self.rect.width + BLOCK_BLANK)
        self.rect.top  = y * (self.rect.height + BLOCK_BLANK)
    
    #ブロックの描画
    def draw(self, surface):
        surface.blit(self.image, self.rect)


def main():
    #画面初期化
    pygame.init()
    pygame.display.set_caption("ブロック崩し")
    surface = pygame.display.set_mode(SURFACE.size)

    pygame.mixer.init()

    #ブロック生成
    blocks = pygame.sprite.Group()

    for y in range(BLOCK_NUM_Y):
        for x in range(BLOCK_NUM_X):
            blocks.add(Block("./image/block.png", x, y))
    
    bar = Bar("./image/bar.png")
    ball = Ball("./image/ball.png", bar, blocks)

    clock = pygame.time.Clock()
    bar_pos = int(SURFACE.width/2)
    pygame.key.set_repeat(KEY_REPEAT)

    ### STARTを表示
    font = pygame.font.Font(None, 60)
    text = font.render("START", True, (96,96,255))
    surface.fill((0,0,0))
    surface.blit(text, [133,299])
    pygame.display.update()

    time.sleep(2)

    while True:
        
        #フレームレート設定
        clock.tick(FRAME_RATE)

        #背景描画
        surface.fill((0,0,0))
    
        #更新
        bar.update(bar_pos)
        ball.update(surface)

        #描画
        bar.draw(surface)
        ball.draw(surface)
        blocks.draw(surface)
        pygame.display.update()

        for event in pygame.event.get():
            #エラー処理
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                #強制終了
                if event.key == K_ESCAPE:
                    exit()
                
                if event.key == K_LEFT:
                    #左に移動
                    bar_pos -= BAR_SPEED
                    #画面外処理(左端)
                    if bar_pos - BAR_SIZE_X/2 < 0:
                        bar_pos = 0 + BAR_SIZE_X/2
                if event.key == K_RIGHT:
                    #右に移動
                    bar_pos += BAR_SPEED
                    #画面外処理(右端)
                    if bar_pos + BAR_SIZE_X/2 > WINDOW_SIZE_X:
                        bar_pos = WINDOW_SIZE_X - BAR_SIZE_X/2
        
def exit():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()