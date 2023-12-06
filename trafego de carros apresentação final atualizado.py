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
velocidade_minvoltando = -0.1
velocidade_maxvoltando = -0.25
aceleracao_min = 0.001
aceleracao_max = 0.005
aceleracao_minima_voltando = -0.001
aceleracao_maxima_voltando = -0.005

# Solicitando informações do usuário
quantidade_max_carros = int(input("Digite a quantidade máxima de carros: "))
velocidade_max = None
while velocidade_max is None:
    try:
        velocidade_max = float(input("Digite a velocidade máxima dos carros (escolha de 0.1 a 1): "))
        # Verificar se a velocidade está dentro da faixa desejada
        if not 0.1 <= velocidade_max <= 1:
            raise ValueError("A velocidade máxima deve estar entre 0.1 e 1.")
    except ValueError as e:
        print(f"Erro: {e}")
        velocidade_max = None


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

class Semaforo:
    def __init__(self, raio, tverde, tvermelho, pos_x, pos_y):
        self.x, self.y, self.tempo_verde, self.tempo_vermelho = pos_x, pos_y, tverde, tvermelho
        self.raio = raio
        self.cor = random.choice([(0, 255, 0), (255, 0, 0)])

    def atualizar(self, frame):
        if frame % (self.tempo_verde + self.tempo_vermelho) < self.tempo_verde:
            self.cor = (0, 255, 0)  # Verde
        else:
            self.cor = (255, 0, 0)  # Vermelho

    def verificar_semaforo(self, carro):
        # Verifica se o carro está próximo ao semáforo e se o semáforo está vermelho
        distancia = ((self.x - carro.x) ** 2 + (self.y - carro.y) ** 2) ** 0.5
        return distancia <= (self.raio + 3) and self.cor == (255, 0, 0)

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)

# Inicializando os semáforos
semaforos = [
    Semaforo(3, 1500, 1500, 250, 110),
    Semaforo(3, 1500, 1000, 500, 330),
    Semaforo(3, 2000, 1500, 500, 180),
    Semaforo(3, 1500, 1000, 250, 270),
    Semaforo(3, 1500, 1000, 220, 150),
    Semaforo(3, 1000, 1500, 530, 300),
    Semaforo(3, 1500, 1000, 470, 150),
    Semaforo(3, 1000, 1500, 280, 300)
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
        # Verifica o estado do semáforo na estrada do carro
        semaforo = None
        for s in semaforos:
            if s.verificar_semaforo(self):
                semaforo = s
                break

        if semaforo:
            # Semáforo vermelho, carro para
            return

        # Atualiza a posição do carro apenas se não estiver próximo a um semáforo vermelho
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
frame = 0
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
#desenha e atualiza os semafaros
    for semaforo in semaforos:
        semaforo.atualizar(frame)
        semaforo.desenhar(tela)

    # Adiciona novos carros aleatoriamente
    if random.randint(0, 80) < 5 and len(carros) < quantidade_max_carros:
        estrada = random.choice(estradas)
        novo_carro = Carro(estrada)
        carros.append(novo_carro)

    for carro in carros:
        # Atualiza a posição do carro apenas se não estiver próximo a um semáforo vermelho
        carro.atualizar_posicao()
        carro.desenhar()

    # Atualiza a tela
    pygame.display.update()

    #atualiza os frames
    frame += 1

