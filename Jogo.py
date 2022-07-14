from operator import ge
from pickle import TRUE
import pygame, random , sys
from pygame.locals import *

LARGURA = 300
ALTURA = 800
SPEED = 10
GRAVIDADE = 1
VELOCIDADE = 15

GROUND_WIDTH = 2 * LARGURA
GROUND_HEIGHT = 100

PIPE_WIDTH = 100
PIPE_HEIGHT = 500

PIPE_GAP = 200



#fonte utilizada e o tamanho 
pygame.font.init()
FONTE = pygame.font.SysFont('arial', 20)

#crição da classe do bloco
class bloquinho(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('ia4.png').convert_alpha(),
                       pygame.image.load('ia5.png').convert_alpha(),
                       pygame.image.load('ia1.png').convert_alpha()]

        self.speed = SPEED
        self.current_image = 0
        self.image = pygame.image.load('ia5.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        #onde ele vai iniciar 
        self.rect[0] = LARGURA / 2
        self.rect[1] = ALTURA / 2

    #fisica do jogo para alterar a gravidade
    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]
        self.speed += GRAVIDADE
        self.rect[1] += self.speed
    #ele pula de acordo com a velociadade
    def pulo(self):
        self.speed = - SPEED


class FOGUINHO (pygame.sprite.Sprite):

    def __init__(self, fogo_dois, xpos, ysize ):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('fogo.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect[0] = xpos 

        size_aleatorio = random.randint(50,750)
        #nasce dois fogos por vez no jogo e lugar e alturas diferentes e aleatorias
        if fogo_dois:
            self.rect[1] = - (self.rect[1] - ysize)
            self.rect[1] = ALTURA - size_aleatorio
        else:
            self.rect[1] = ALTURA - ysize
            self.rect[1] = - (self.rect[1] - ysize)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= VELOCIDADE 

#faz com que a lava passe dando impressão de velocidades 
class chao(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('chao.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = ALTURA - GROUND_HEIGHT
    
    def update(self):
        self.rect[0] -= VELOCIDADE + 1 




#VERIFICA SE A TELA ESTA FORA DA TELA, PARA FAZER A REPETIÇÃO
def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

#gera fogo aleatorio
def get_random_fogo(xpos):
    size = random.randint(50,750)
    fogo_um = FOGUINHO (False, xpos, size)
    fogo_duplicado = FOGUINHO (True, xpos, ALTURA - size - PIPE_GAP)
    return (fogo_um, fogo_duplicado)


def get_random_bloco(xpos):
    size = random.randint(50,750)
    bloco_aleatorio = FOGUINHO (False, xpos, size)
    return bloco_aleatorio



#inicio do pygame
pygame.init()
screen = pygame.display.set_mode((LARGURA, ALTURA))

#definindo a imagem de tras
BACKGROUD = pygame.image.load('branco.png')
BACKGROUD = pygame.transform.scale( BACKGROUD, (LARGURA, ALTURA))

#grupo do bloco para implementação da IA 
bloquinho_group = pygame.sprite.Group()
for i in range(1):
    bloco = bloquinho()
    bloquinho_group.add(bloco)


#faz o chao andar 
chao_group = pygame.sprite.Group()
for i in range(3):
    ground = chao(GROUND_WIDTH * i)
    chao_group.add(ground)

#O FOGO APARECE DE FORMA ALEATORIA E ADICONA NOVAMENTE AO GRUPO 
fogo_group = pygame.sprite.Group()
for i in range(4):
    fogo = get_random_fogo(LARGURA * i + 600)
    fogo_group.add(fogo[0])
    fogo_group.add(fogo[1])



clock = pygame.time.Clock()  



geracao = 0
ponto = 0 
nova_geracao = 1

while True:

        clock.tick(20)
        for event in pygame.event.get():
            if event.type == QUIT:
                 pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                     bloco.pulo()

        screen.blit(BACKGROUD, (0, 0))
    
        if is_off_screen(chao_group.sprites()[0]):
             chao_group.remove(chao_group.sprites()[0])
             novo_chao = chao(GROUND_WIDTH - 20)
             chao_group.add(novo_chao)

        if is_off_screen(fogo_group.sprites()[0]):
             fogo_group.remove(fogo_group.sprites()[0])
             fogo_group.remove(fogo_group.sprites()[0])
             fogo = get_random_fogo(LARGURA * 2)
             fogo_group.add(fogo[0])
             fogo_group.add(fogo[1])
             ponto = ponto + 1

        #escreve a pontuação na tela     
        screen.blit((FONTE.render(f"pontuacao : {ponto}  ", True, (255,0,0))), (150,0))
        screen.blit((FONTE.render(f" geração : {geracao}  ", True, (255,0,0))), (20,0))

        bloquinho_group.update()
        chao_group.update()
        fogo_group.update()

        bloquinho_group.draw(screen)
        fogo_group.draw(screen)
        chao_group.draw(screen)

        pygame.display.update()

        if (pygame.sprite.groupcollide(bloquinho_group, chao_group, False, False, pygame.sprite.collide_mask) or
             pygame.sprite.groupcollide(bloquinho_group, fogo_group, False, False, pygame.sprite.collide_mask)):
             # game over
             break
            
