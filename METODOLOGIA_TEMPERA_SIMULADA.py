from calendar import different_locale
from re import I
from unicodedata import bidirectional
import pygame
import os
import random
import time

ia_joganodo = True
geracao = 0

colisao = False

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_FOGO = pygame.transform.scale2x(pygame.image.load('fogo.png'))
IMAGENS_BLOCO = [
    pygame.transform.scale2x(pygame.image.load('ia1.png')),
    pygame.transform.scale2x(pygame.image.load('ia4.png')),
    pygame.transform.scale2x(pygame.image.load( 'ia5.png')),
]

pygame.font.init()
FONTE = pygame.font.SysFont('arial', 30)

class bloco:
    IMGS = IMAGENS_BLOCO
    # animações da rotação
    TEMPO_ANIMACAO = 5
    colisao = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]
  
        

    def pular(self):
        self.velocidade = -10
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento e controla a gravidade do jogo
        if deslocamento > 10:
            deslocamento = 10
        elif deslocamento < 0:
            deslocamento += 5

        self.y += deslocamento


    def desenhar(self, tela, colisao ):
        # definir qual imagem do bloco_pos vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = 0

        # desenhar a imagem
        imagem_atualizada = self.imagem
        tela.blit(imagem_atualizada , (self.x, self.y))
         
        #fica com a cor vermelha em caso de colisao com o fogo
        if colisao == 1 :
         self.contagem_imagem += 1

         if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
         elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[0]
         elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[0]
         elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0


         # desenhar a imagem
         imagem_atualizada = self.imagem
         tela.blit(imagem_atualizada , (self.x, self.y))



    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class fogo:
    DISTANCIA = 300
    VELOCIDADE = 20

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_fogo_de_cima = 0
        self.pos_fogo_de_baixo = 0
        self.fogo_de_cima = pygame.transform.flip(IMAGEM_FOGO, False, True)
        self.fogo_de_baixo = IMAGEM_FOGO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(60, 600)
        self.pos_fogo_de_cima = self.altura - self.fogo_de_cima.get_height()
        self.pos_fogo_de_baixo = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.fogo_de_cima, (self.x, self.pos_fogo_de_cima))
        tela.blit(self.fogo_de_baixo, (self.x, self.pos_fogo_de_baixo))

    def colidir(self, bloco_pos):
        bloco_mask = bloco_pos.get_mask()
        topo_mask = pygame.mask.from_surface(self.fogo_de_cima)
        base_mask = pygame.mask.from_surface(self.fogo_de_baixo)

        distan_figo_cima = (self.x - bloco_pos.x, self.pos_fogo_de_cima - round(bloco_pos.y))
        distan_fogo_baixo = (self.x - bloco_pos.x, self.pos_fogo_de_baixo - round(bloco_pos.y))

        ponto_fogo_cima = bloco_mask.overlap(topo_mask, distan_figo_cima)
        ponto_fogo_baixo = bloco_mask.overlap(base_mask, distan_fogo_baixo)

        if ponto_fogo_baixo or ponto_fogo_cima:
            return True
        else:
            return False

def desenhar_tela(tela, blocos , fogo_repeticao, pontos,colisao):
   
    for bloco_pos in blocos:
        if colisao == False :
         bloco_pos.desenhar(tela,colisao)
        else: 
            bloco_pos.desenhar(tela, colisao)


    for fogo_pos in fogo_repeticao:
        fogo_pos.desenhar(tela)

    texto = FONTE.render(f"Pontuação: {pontos}", 1, (255, 0, 0))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))


    texto = FONTE.render(f"geração: {geracao}", 1, (255, 0, 0))
    tela.blit(texto, (10, 10))   

    

    pygame.display.update() 

def main():
    global geracao , colisao  
    colisao = False


    blocos = [bloco(230, 350)]
    fogo_repeticao = [fogo(700)]
    pontos = 0
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    relogio = pygame.time.Clock()
    
    
    rodando = True
    while rodando:
        relogio.tick(30)
        tela.fill((255,255,255))
        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            #se o jogador estiver controlando utilizar espaço:    
            if evento.type == pygame.KEYDOWN:
                  if evento.key == pygame.K_SPACE:
                     for bloco_pos in blocos:
                        bloco_pos.pular()
        
        indice_fogo = 0
        if len(blocos) > 0:
          if len(fogo_repeticao) > 1 and blocos[0].x > (fogo_repeticao[0].x + fogo_repeticao[0].fogo_de_cima.get_width()):
            indice_fogo = 1

      
        # ia utilizando o metodo de hill cilmb 
        for i, bloco_pos in enumerate(blocos):
            bloco_pos.mover()
            movendo = True
            diferenca_de_altura = abs(bloco_pos.y - fogo_repeticao[indice_fogo].altura) 
            if movendo == True: 
              if bloco_pos.y - diferenca_de_altura > 1 :
                 if indice_fogo == 1:
                  bloco_pos.pular()
                  bloco_pos.pular()
                  bloco_pos.pular()
                  bloco_pos.pular()
                  bloco_pos.pular()
                  bloco_pos.pular()


        
        #cria o grupo para o fogo     
        adicionar_fogo = False
        remover_fogo = []
        for fogo_pos in fogo_repeticao:
            for i, bloco_pos in enumerate(blocos):
                if fogo_pos.colidir(bloco_pos):
                     geracao+=1
                     colisao = True
                     altura = random.randrange(50, 600)
                     #adicona novo bloco ao colidir
                     blocos.append(bloco(230,altura))
                     #remove os bloco que morreram 
                     blocos.pop(i)

                if not fogo_pos.passou and bloco_pos.x > fogo_pos.x:
                    fogo_pos.passou = True
                    adicionar_fogo = True
            fogo_pos.mover()
            if fogo_pos.x + fogo_pos.fogo_de_cima.get_width() < 0:
                remover_fogo.append(fogo_pos)

        if adicionar_fogo:
            if colisao != True:
              pontos += 2
            else:
                pontos = 0  
            fogo_repeticao.append(fogo(600))
        for fogo_pos in remover_fogo:
            fogo_repeticao.remove(fogo_pos)


        #nâo permite o bloco suba
        if bloco_pos.y > TELA_ALTURA:
         for i in range(10):
                  bloco_pos.pular()
        if pontos == 20 :
            break

        desenhar_tela(tela, blocos, fogo_repeticao, pontos, colisao)
        colisao= False
       
 
if __name__ == '__main__':
    main()
