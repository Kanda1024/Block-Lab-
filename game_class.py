### インポート
import sys
import time
import copy
import pygame
from pygame.locals import *
from const import *


#スクリーンクラス
class Screen(pygame.sprite.Sprite):
    #初期化メソッド
    def __init__(self, image_name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_name).convert()
        self.image = pygame.transform.scale(self.image, (WINDOW_SIZE_X, WINDOW_SIZE_Y))
        self.rect = self.image.get_rect()
    #スクリーンの描画
    def draw(self, surface):
        surface.blit(self.image, self.rect)

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
    
        self.vx = 0                 #ボール横速度
        self.vy = 0                  #ボール縦速度
        self.bar = bar              #バーを参照
        self.block  = block         #ブロックを参照
        self.update = self.setup    #初期状態

    def setup(self, surface):
        #ボール初期位置
        self.rect.centerx = WINDOW_SIZE_X/2 + 1
        self.rect.centery = WINDOW_SIZE_Y/3
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
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx *= -1
        #右壁の反射
        if self.rect.right >= WINDOW_SIZE_X:
            self.rect.right = WINDOW_SIZE_X
            self.vx *= -1
        #上壁の反射
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy *= -1
        #ボールとバーの当たり判定
        if self.rect.colliderect(self.bar.rect):
            self.sound_bar.play(0)
            self.rect.bottom = self.bar.rect.top
            self.vy *= -1
        
        #ゲーム失敗判定
        if self.rect.bottom >= WINDOW_SIZE_Y:
            ### GAME OVERを表示
            font = pygame.font.Font(None, 60)
            text = font.render("GAME OVER", True, (255,31,31))
            surface.blit(text, [73,299])
            #time.sleep(5)

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

    def ballSpeed(self):
        self.vx += 1

#ブロッククラス
class Block(pygame.sprite.Sprite):
    #初期化メソッド
    def __init__(self, image_name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_name).convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE_X, BLOCK_SIZE_Y))
        self.rect = self.image.get_rect()
        #ブロック位置の取得
        self.rect.left = x * (self.rect.width + BLOCK_BLANK) + BLOCK_BLANK_LEFT
        self.rect.top  = y * (self.rect.height + BLOCK_BLANK) + BLOCK_BLANK_TOP
    
    #ブロックの描画
    def draw(self, surface):
        surface.blit(self.image, self.rect)