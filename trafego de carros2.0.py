# Importando as bibliotecas necessárias
import pygame
from pygame.locals import *
import random
from sys import exit

# Inicializando o Pygame
pygame.init()

# Variáveis da tela
largura = 640
altura = 480
corfundo = (255, 255, 255)
fonte = pygame.font.SysFont(None, 25)  # Fonte para exibição de informações

# Movimentação dos carros
velocidade_min = 0.1
velocidade_max = 0.25
velocidade_minvoltando = -0.1
velocidade_maxvoltando = -0.25
aceleracao_min = 0.001
aceleracao_max = 0.005
aceleracao_minima_voltando = -0.001
aceleracao_maxima_voltando = -0.005

# Solicitando informações do usuário
quantidade_min_carros = int(input("Digite a quantidade mínima de carros: "))
quantidade_max_carros = int(input("Digite a quantidade máxima de carros: "))
velocidade_maxima = float(input("Digite a velocidade máxima dos carros: "))

# Configurando a tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Simulação de Tráfego')

# Inicializando as estradas
estradas = [
    {'x1': 0, 'y1': 150, 'x2': largura, 'y2': 150, 'sentido': 'horizontal_indo'},
    {'x1': 0, 'y1': 300, 'x2': largura, 'y2': 300, 'sentido': 'horizontal_voltando'},
    {'x1': 250, 'y1': 0, 'x2': 250, 'y2': altura, 'sentido': 'vertical_indo'},
    {'x1': 500, 'y1': 0, 'x2': 500, 'y2': altura, 'sentido': 'vertical_voltando'}
]

# Definindo a classe Carro
class Carro:
    def __init__(self, estrada):
        self.x, self.y, self.velocidade_x, self.velocidade_y, self.aceleracao = self.criar_carro(estrada)
        self.cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.sentido = estrada['sentido']

    def criar_carro(self, estrada):
        # Lógica para criar um carro com posição, velocidade e aceleração iniciais
        if estrada['sentido'] == 'horizontal_indo':
            x = random.choice([0, largura])
            y = estrada['y1']
            velocidade_x = random.uniform(velocidade_min, velocidade_max)
            velocidade_y = 0
            aceleracao = random.uniform(aceleracao_min, aceleracao_max)
        elif estrada['sentido'] == 'vertical_indo':
            x = estrada['x1']
            y = random.choice([0, altura])
            velocidade_x = 0
            velocidade_y = random.uniform(velocidade_min, velocidade_max)
            aceleracao = random.uniform(aceleracao_min, aceleracao_max)
        else:
            x = estrada['x2'] if estrada['sentido'] == 'horizontal_voltando' else estrada['x2']
            y = estrada['y2'] if estrada['sentido'] == 'horizontal_voltando' else estrada['y2']
            velocidade_x = 0
            velocidade_y = 0
            aceleracao = random.uniform(aceleracao_minima_voltando, aceleracao_maxima_voltando)

        return x, y, velocidade_x, velocidade_y, aceleracao

    def atualizar_velocidade(self):
        # Atualiza a velocidade do carro baseado na aceleração
        if abs(self.velocidade_x) < velocidade_max:
            self.velocidade_x += self.aceleracao
        if abs(self.velocidade_y) < velocidade_max:
            self.velocidade_y += self.aceleracao

    def atualizar_posicao(self):
        # Atualiza a posição do carro com base na velocidade
        self.atualizar_velocidade()
        if self.sentido == 'horizontal_indo' or self.sentido == 'horizontal_voltando':
            self.x += self.velocidade_x
        else:
            self.y += self.velocidade_y

    def desenhar(self):
        # Desenha o carro na tela
        pygame.draw.rect(tela, self.cor, (self.x, self.y, 8, 15))

# Lista de carros na simulação
carros = []

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Preenche a tela com a cor de fundo
    tela.fill(corfundo)

    # Exibe o número de carros na tela
    texto_info = fonte.render(f'Número de Carros: {len(carros)}', True, (0, 0, 0))
    tela.blit(texto_info, (10, 10))

    # Desenha as estradas na tela
    for estrada in estradas:
        pygame.draw.line(tela, (0, 0, 0), (estrada['x1'], estrada['y1']), (estrada['x2'], estrada['y2']), 30)

    # Adiciona novos carros aleatoriamente
    if random.randint(0, 80) < 5 and len(carros) < quantidade_max_carros:
        estrada = random.choice(estradas)
        novo_carro = Carro(estrada)
        carros.append(novo_carro)

    # Atualiza e desenha cada carro na tela
    for carro in carros:
        carro.atualizar_posicao()
        carro.desenhar()

    # Atualiza a tela
    pygame.display.update()
