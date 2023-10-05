import pygame
from pygame.locals import *
import random
from sys import exit

pygame.init()
# Variáveis da tela

largura = 640
altura = 480
corfundo = (255, 255, 255)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Simulação de Tráfego')

# inicialização das estradas
estradas = [
    {'x1': 0, 'y1': 150, 'x2': largura, 'y2': 150, 'sentido': 'horizontal'},
    {'x1': 0, 'y1': 300, 'x2': largura, 'y2': 300, 'sentido': 'horizontal'},
    {'x1': 250, 'y1': 0, 'x2': 250, 'y2': altura, 'sentido': 'vertical'},
    {'x1': 500, 'y1': 0, 'x2': 500, 'y2': altura, 'sentido': 'vertical'}
]

carros = [] #lista de carros, todos os carros gerados serão contabilizados aqui

#função paracriar os carros
def criar_carro(estrada):
    if len(carros) >= 30:
        return None
#adiciona sentido aos carros spawnados
    if estrada['sentido'] == 'horizontal':
        x = random.choice([0, largura])
        y = estrada['y1']
        velocidade_x = (random.random() - 0.5) * 0.07  # Velocidade aleatória entre -0.035 e 0.035
        velocidade_y = 0
    else:
        x = estrada['x1']
        y = random.choice([0, altura])
        velocidade_x = 0
        velocidade_y = (random.random() - 0.5) * 0.07  # Velocidade aleatória entre -0.035 e 0.035

    cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    return {'x': x, 'y': y, 'velocidade_x': velocidade_x, 'velocidade_y': velocidade_y, 'cor': cor}

#serve para detectar o evento de fechar a tela (janela)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Preencha a tela com a cor de fundo
    tela.fill(corfundo)

    # Desenha as estradas
    for estrada in estradas:
        pygame.draw.line(tela, (0, 0, 0), (estrada['x1'], estrada['y1']), (estrada['x2'], estrada['y2']), 30)

    # cria e desenha carros aleatoriamente
    if random.randint(0, 100) < 5:  # Chance de criar um novo carro
        estrada = random.choice(estradas)
        novo_carro = criar_carro(estrada)
        if novo_carro:
            carros.append(novo_carro)

    # Atualiza e desenhe cada carro
    carros_a_remover = []
    for carro in carros:
        x, y, velocidade_x, velocidade_y, cor = carro['x'], carro['y'], carro['velocidade_x'], carro['velocidade_y'], \
        carro['cor']

        pygame.draw.rect(tela, cor, (x, y, 8, 15))  # Tamanho padrão: 8 de largura e 15 de altura

        x += velocidade_x
        y += velocidade_y

        # Remove carros que saíram da tela
        if (x < -8 or x > largura or y < -15 or y > altura):
            carros_a_remover.append(carro)

        carro['x'] = x
        carro['y'] = y

    # Remove carros que saíram da tela
    for carro in carros_a_remover:
        carros.remove(carro)

    # Atualiza a tela
    pygame.display.update()
