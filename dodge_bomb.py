import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, 5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (5, 0),
    }

kk_img_src = pg.image.load("fig/3.png")

kk_img_dict = { #方向転換辞書
        (0,0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (5, 0): pg.transform.rotozoom(pg.transform.flip(kk_img_src, True, False), 0, 0.9),
        (-5, 0): pg.transform.rotozoom(kk_img_src, 0, 0.9),
        (0, -5): pg.transform.rotozoom(pg.transform.flip(kk_img_src, False, True), -90, 0.9),
        (0, 5): pg.transform.rotozoom(pg.transform.flip(kk_img_src, False, True), -270, 0.9),
        (5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img_src, True, False), 45, 0.9),
        (5, 5): pg.transform.rotozoom(pg.transform.flip(kk_img_src, True, False), -45, 0.9),
        (-5, -5): pg.transform.rotozoom(kk_img_src, -45, 0.9),
        (-5, 5): pg.transform.rotozoom(kk_img_src, 45, 0.9),
    }


def make_accel_bomb() -> tuple[list[pg.Surface], list[int]]:
        """
        引数：なし
        戻り値：リスト(加速度と円の大きさ)
        時間に応じて爆弾画像と加速度を返す関数
        """
        bb_imgs = []
        bb_accs = [a for a in range(1, 11)]  # 加速度リスト（1〜10）
        for r in range(1, 11):
            img = pg.Surface((20*r, 20*r))  # サイズ20×rの正方形サーフェス
            pg.draw.circle(img, (255, 0, 0), (10*r, 10*r), 10*r)  # 赤い円
            img.set_colorkey((0, 0, 0))  
            bb_imgs.append(img)
        return bb_imgs, bb_accs


def gameover(screen: pg.Surface) -> None :
         """
         引数：screen
         戻り値：なし
         ゲームオーバーの画面の関数
         """
         #ブラックアウト
         black_out = pg.Surface((WIDTH, HEIGHT))
         black_out.fill((0,0,0))
         black_out.set_alpha(150)
         screen.blit(black_out, (0, 0))

         #泣き顔こうかとんの画像
         gameover_img = pg.image.load("fig/8.png")
         gameover_rct = gameover_img.get_rect()
         gameover_rct.center = WIDTH//2+200, HEIGHT//2
         screen.blit(gameover_img, gameover_rct)

         #泣き顔こうかとんの画像２
         gameover_img2 = pg.image.load("fig/8.png")
         gameover_rct2 = gameover_img2.get_rect()
         gameover_rct2.center = WIDTH//2-200, HEIGHT//2
         screen.blit(gameover_img2, gameover_rct2)

         # Game Over テキスト描画
         font = pg.font.SysFont(None, 80)
         txt = font.render("Game Over", True, (255, 255, 255))
         txt_rct = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
         screen.blit(txt, txt_rct)

         # 画面更新と表示維持
         pg.display.update()
         time.sleep(5)


def get_kk_img(mv: tuple[int, int]) -> pg.Surface:
        """
        引数：タプル
        戻り値：画像の方向転換
        タプルの値に応じて画像の向きを変える
        """
        return kk_img_dict[mv]


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
            """
            引数：こうかとんRectかばくだんRect
            戻り値：タプル（横方向判定結果，縦方向判定結果）
            画面内ならTrue，画面外ならFalse
            """
            yoko, tate = True, True
            if obj_rct.left < 0 or WIDTH < obj_rct.right: # 横方向判定
                yoko = False
            if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: # 縦方向判定
                tate = False
            return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    bb_imgs, bb_accs = make_accel_bomb()

    clock = pg.time.Clock()
    tmr = 0

    bg_img = pg.image.load("fig/pg_bg.jpg") #背景画像
    
    #爆弾サーフェイスの作成
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))

    #爆弾のランダム設定
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    vx,vy = 0,0 #爆弾の速度
    vx += 5
    vy += 5


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        for k, delta in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]
        kk_img = get_kk_img(tuple(sum_mv))
        kk_rct.move_ip(sum_mv)
        
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #移動をなかったことにする

        screen.blit(kk_img, kk_rct)

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        # 段階（0～9）を時間で決定
        stage = min(tmr // 500, 9)

        # 拡大・加速爆弾
        bb_img_now = bb_imgs[stage]
        acc = bb_accs[stage]
        avx = vx * acc
        avy = vy * acc

        bb_rct.move_ip(avx, avy)
        screen.blit(bb_img_now, bb_rct)

        if kk_rct.colliderect(bb_rct): #爆弾衝突判定
            gameover(screen)
            return

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
