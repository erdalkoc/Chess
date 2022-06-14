'''
    *Eksikler:
    Bu Programdaki eksikler tek tek belirlenecek
    Hızla İlgili Ayarlar Yapılıyor

        -
'''

import sys,random
import pygame as pg
import time
from pygame.locals import *
from pygame.sprite import Sprite


# Global Constants
VERSION     = "0.01"
NAME        = "Chess " + VERSION
SCREEN_X    = 504
SCREEN_Y    = 504
FPS         = 30


# pygame başlıyor
pg.init()
screen  = pg.display.set_mode((SCREEN_X,SCREEN_Y))
caption = pg.display.set_caption(NAME)
clock   = pg.time.Clock()
letter  = ['a','b','c','d','e','f','g','h']
f0      = open("kaydet.txt", "w+")   # Kayıt yapmak için
f1      = open("kayıttan.txt", "r")  # Dosyada kayıtlı olan bilgileri tutan dosya tutacağı
moving  = f1.readlines()

     # Sahne Sınıfı
class SAHNE():
    def __init__(self):
        super().__init__()
        self.bDrop      = False  # Maus'un bir taşı tutup tutmadığını belirten bool değer
        self.DropObject = 3      # Maus'un tuttuğu taşın ne olduğunu kaydeden değer
        self.coord      = ''     # 'a1c7' gibi yer bilgisini tutan değişken
        self.h          = 0
        self.figures    = pg.image.load("images/figures.png").convert_alpha()
        self.board      = \
        [
        [-1, -2, -3, -4, -5, -3, -2, -1],     # Tabla bilgisini tutan dizi listesi
        [ -6, -6, -6, -6, -6, -6, -6, -6],    # 1-Kale  2-At 3-Fil 4-Vezir 5-Şah 6-Piyon
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [6, 6, 6, 6, 6, 6, 6, 6],
        [1, 2, 3, 4, 5, 3, 2, 1]
        ]

        #>---Mausun koordinatını alıp dizi koordinatına çevirir
    def GetMaus(self, x, y):
        if x > 26 and x < 26 + 8 * 56 and y > 26 and y < 26 + 8 * 56:
            PosX = int((x - 26) / 56)  # Hangi kutuya denk geldiği
            PosY = int((y - 26) / 56)
        else:
            PosX = -1
            PosY = -1
        return PosX,PosY

        #>-- Tablodaki şekil değerinin figures resminde hangi koordinatlara denk geldiğini bulur
    def GetİmajNo(self,deger):
        x = 0;y = 0
        if deger > 0: x = deger - 1     ; y = 0
        if deger < 0: x = abs(deger) - 1; y = 1
        return x,y

        #>-- Tabloyu ve sürüklenen şekli çizer
    def Show(self):
        for i in range(8):
            for r in range(8):
                A = self.board[r][i]
                if A != 0:
                    x, y = self.GetİmajNo(A)
                    pcs = self.figures.subsurface(x * 56, y * 56, 56, 56).convert_alpha()
                    screen.blit(pcs, (26 + i * 56, 26 + r * 56))

        if self.bDrop == True:
            x,y =self.GetİmajNo(self.DropObject)
            pcs = self.figures.subsurface(x * 56, y * 56, 56, 56).convert_alpha()
            mX,mY=pg.mouse.get_pos()
            screen.blit(pcs, (mX-26, mY-26))

        #>-- Verilen 'a1c4' gibi hareketi yerine getirir
    def Move(self,cord):
        x1 = letter.index(cord[0])
        y1 = 8-int(cord[1])
        x2 = letter.index(cord[2])
        y2 = 8-int(cord[3])

        g = self.board[y1][x1]
        if g != 0:
            self.board[y1][x1] = 0
            self.board[y2][x2] = g

        caption = pg.display.set_caption(str(x1)+str(y1)+str(x2)+str(y2))

    def GameOver(self):
        pass


Sahne = SAHNE()

# oyun döngüsünü çalıştırıyoruz
class main():
    def __init__(self):
        self.Background = pg.image.load("images/board.png").convert_alpha()
        self.game_loop()

    def game_loop(self):
        while True:
            clock.tick(FPS)

            for event in pg.event.get():
                if event.type == QUIT:
                    f0.close()
                    f1.close()
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:       #-Sağ Maus tuşuna basıldıysa
                        x, y = event.pos
                        x,y=Sahne.GetMaus(x,y)
                        if x>=0 and Sahne.board[y][x] != 0:       #-Tabla içinde ve bir taşın üzerine  basıldıysa
                            Sahne.bDrop = True
                            Sahne.coord =letter[x]+str(y+1)       #-Mausun konumunu 'a1' gibi bir değer haline getirir
                            Sahne.DropObject = Sahne.board[y][x]  #- Maus konumundaki şekil değerini alır
                            Sahne.board[y][x] = 0                 #- maus konumundaki şekili siler

                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1 and Sahne.bDrop == True:  #-Basılmış olan sağMaus tuşu bırakıldısa ve
                        x, y = event.pos                           # sürüklenen bir taş varsa
                        x, y = Sahne.GetMaus(x, y)
                        Sahne.board[y][x] = Sahne.DropObject       #-Maus konumuna sürüklenen şekli yaz
                        Sahne.coord += letter[x] + str(y + 1)      #-Hareketi 'a1c4' gibi halde değişkene ata
                        f0.write(Sahne.coord+"\n")                 #-Bu Değişkeni dosyaya kaydet
                        Sahne.bDrop = False                        #-Sürüklenme işlemini bitir


            # <-  KEYS   ->
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:             #-SPACE tuşuna basılırsa dosyadaki değerlerin tutulduğu moving dizisinden
                Sahne.Move(moving[Sahne.h])  #-bir hareketi okuyup yerine getir
                time.sleep(0.1)
                Sahne.h +=1
                if Sahne.h == len(moving):Sahne.h =0


            # <- SHOW ->
            screen.blit(self.Background, (0, 0))
            Sahne.Show()
            #caption = pg.display.set_caption(Sahne.coord)
            clock.tick(FPS)
            pg.display.flip()

if __name__ == '__main__':
    main()


