"""Classes dos objetos do jogo.

Todas herdam de pygame.sprite.Sprite e têm:
  - self.image: a figura (Surface)
  - self.rect:  o retângulo com a posição e o tamanho na tela

As figuras são desenhadas com pygame.draw. A cor PRETO é usada como
transparente (set_colorkey), por isso os desenhos nunca usam preto puro.
"""
import math
import random

import pygame

from config import (ALTURA, AMARELO, AZUL, AZUL_CLARO, BRANCO, CINZA, CINZA_CLARO, CINZA_ESCURO,
                    FORCA_PULO, GRAVIDADE, LARANJA, PRETO, QUIQUE_AO_PISAR, ROXO, TAMANHO_BLOCO, VELOCIDADE_JOGADOR,
                    VELOCIDADE_MAXIMA_QUEDA, VERDE, VERMELHO)


def nova_figura(largura, altura):
    """Cria uma Surface vazia com o preto transparente."""
    figura = pygame.Surface((largura, altura))
    figura.fill(PRETO)
    figura.set_colorkey(PRETO)
    return figura


def escurecer(cor, quanto):
    """Devolve a cor um pouco mais escura (usado nas bordas dos blocos)."""
    return (max(0, cor[0] - quanto), max(0, cor[1] - quanto), max(0, cor[2] - quanto))


# =====================================================================
class Bloco(pygame.sprite.Sprite):
    """Um quadrado sólido do cenário (chão, parede ou plataforma)."""

    def __init__(self, x, y, cor, tem_grama):
        """Cria o bloco na posição (x, y) da tela.

        tem_grama: True se não há bloco em cima (desenha a grama no topo).
        """
        super().__init__()
        self.image = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO))
        self.image.fill(cor)
        pygame.draw.rect(self.image, escurecer(cor, 40), (0, 0, TAMANHO_BLOCO, TAMANHO_BLOCO), 3)
        # pedrinhas decorativas em lugares aleatórios
        for _ in range(3):
            px = random.randint(6, TAMANHO_BLOCO - 6)
            py = random.randint(12, TAMANHO_BLOCO - 6)
            pygame.draw.circle(self.image, escurecer(cor, 25), (px, py), 3)
        if tem_grama:
            pygame.draw.rect(self.image, VERDE, (0, 0, TAMANHO_BLOCO, 8))
        self.rect = self.image.get_rect(topleft=(x, y))


class Espinho(pygame.sprite.Sprite):
    """Espinhos no chão: encostar tira uma vida."""

    def __init__(self, x, y):
        """Desenha três triângulos na metade de baixo do quadrado (x, y)."""
        super().__init__()
        self.image = nova_figura(TAMANHO_BLOCO, 20)
        for i in range(3):
            esquerda = i * 13 + 1
            pontas = [(esquerda, 20), (esquerda + 6, 2), (esquerda + 12, 20)]
            pygame.draw.polygon(self.image, CINZA_CLARO, pontas)
            pygame.draw.polygon(self.image, CINZA, pontas, 2)
        self.rect = self.image.get_rect(bottomleft=(x, y + TAMANHO_BLOCO))


class Bateria(pygame.sprite.Sprite):
    """Bateria que gira e flutua. Coletar todas abre a porta."""

    def __init__(self, x, y):
        """Cria a bateria no centro do quadrado (x, y)."""
        super().__init__()
        self.figura_original = nova_figura(20, 30)
        pygame.draw.rect(self.figura_original, VERDE, (0, 4, 20, 26), border_radius=4)
        pygame.draw.rect(self.figura_original, CINZA_CLARO, (6, 0, 8, 5))
        pygame.draw.rect(self.figura_original, AMARELO, (8, 10, 4, 14))   # raio
        pygame.draw.rect(self.figura_original, AMARELO, (4, 15, 12, 4))
        self.image = self.figura_original
        self.centro_x = x + TAMANHO_BLOCO // 2
        self.centro_y = y + TAMANHO_BLOCO // 2
        self.rect = self.image.get_rect(center=(self.centro_x, self.centro_y))
        self.tempo = random.randint(0, 100)   # cada bateria começa num ponto da animação

    def update(self):
        """Animação: a largura muda (parece girar) e a bateria sobe e desce."""
        self.tempo += 1
        largura = max(2, int(20 * abs(math.cos(self.tempo * 0.06))))
        self.image = pygame.transform.scale(self.figura_original, (largura, 30))
        flutuar = int(4 * math.sin(self.tempo * 0.08))
        self.rect = self.image.get_rect(center=(self.centro_x, self.centro_y + flutuar))


class Porta(pygame.sprite.Sprite):
    """Porta de saída da fase. Começa trancada (luz vermelha)."""

    def __init__(self, x, y):
        """Cria a porta em pé sobre o quadrado (x, y)."""
        super().__init__()
        self.aberta = False
        self.tempo = 0
        self.image = self.desenhar()
        self.rect = self.image.get_rect(midbottom=(x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO))

    def desenhar(self):
        """Desenha a porta fechada ou aberta (com brilho pulsando)."""
        figura = nova_figura(36, 56)
        pygame.draw.rect(figura, CINZA, (0, 0, 36, 56), border_radius=6)
        if self.aberta:
            brilho = 150 + int(100 * abs(math.sin(self.tempo * 0.05)))
            pygame.draw.rect(figura, (brilho, brilho, 80), (5, 8, 26, 48))
            cor_luz = VERDE
        else:
            pygame.draw.rect(figura, CINZA_ESCURO, (5, 8, 26, 48))
            cor_luz = VERMELHO
        pygame.draw.circle(figura, cor_luz, (18, 4), 3)
        return figura

    def abrir(self):
        """Destranca a porta."""
        self.aberta = True

    def update(self):
        """Redesenha a porta (só muda quando está aberta, por causa do brilho)."""
        if self.aberta:
            self.tempo += 1
            self.image = self.desenhar()


class Inimigo(pygame.sprite.Sprite):
    """Gosma que anda de um lado para o outro numa plataforma.

    Ela vira quando bate numa parede ou quando o chão acaba.
    """

    def __init__(self, x, y, velocidade):
        """Cria o inimigo em pé sobre o quadrado (x, y)."""
        super().__init__()
        self.velocidade = velocidade
        self.figuras = [self.desenhar(0), self.desenhar(1)]
        self.indice_figura = 0
        self.contador = 0
        self.image = self.figuras[0]
        self.rect = self.image.get_rect(midbottom=(x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO))

    def desenhar(self, quadro):
        """Desenha a gosma. Quadro 0 = achatada, quadro 1 = esticada."""
        figura = nova_figura(32, 28)
        if quadro == 0:
            pygame.draw.ellipse(figura, ROXO, (0, 6, 32, 22))
        else:
            pygame.draw.ellipse(figura, ROXO, (3, 0, 26, 28))
        pygame.draw.circle(figura, BRANCO, (11, 14), 5)
        pygame.draw.circle(figura, BRANCO, (21, 14), 5)
        pygame.draw.circle(figura, CINZA_ESCURO, (13, 14), 2)
        pygame.draw.circle(figura, CINZA_ESCURO, (23, 14), 2)
        return figura

    def tem_chao_na_frente(self, blocos):
        """Verifica se existe bloco logo abaixo e à frente do inimigo."""
        if self.velocidade > 0:
            ponto = (self.rect.right + 1, self.rect.bottom + 1)
        else:
            ponto = (self.rect.left - 1, self.rect.bottom + 1)
        for bloco in blocos:
            if bloco.rect.collidepoint(ponto):
                return True
        return False

    def update(self, blocos):
        """Anda; se bater numa parede ou o chão acabar, volta e vira."""
        self.rect.x += self.velocidade
        bateu = pygame.sprite.spritecollideany(self, blocos)
        if bateu or not self.tem_chao_na_frente(blocos):
            self.rect.x -= self.velocidade
            self.velocidade = -self.velocidade

        # animação: troca de figura a cada 12 quadros
        self.contador += 1
        if self.contador >= 12:
            self.contador = 0
            self.indice_figura = 1 - self.indice_figura
            figura = self.figuras[self.indice_figura]
            # olhos para o lado em que está andando
            if self.velocidade < 0:
                figura = pygame.transform.flip(figura, True, False)
            base = self.rect.midbottom
            self.image = figura
            self.rect = self.image.get_rect(midbottom=base)


class Jogador(pygame.sprite.Sprite):
    """O robô controlado pelo jogador."""

    def __init__(self, x, y):
        """Cria o robô em pé sobre o quadrado (x, y)."""
        super().__init__()
        self.figura_parado = self.desenhar(0)
        self.figuras_andando = [self.desenhar(1), self.desenhar(2)]
        self.figura_pulando = self.desenhar(3)
        self.image = self.figura_parado
        self.rect = self.image.get_rect(midbottom=(x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO))
        self.inicio = self.rect.midbottom   # para onde volta ao perder vida

        # o rect só guarda números inteiros; guardamos a altura "exata" aqui
        self.y_exato = float(self.rect.y)
        self.vel_x = 0
        self.vel_y = 0.0
        self.no_chao = False
        self.olhando_direita = True
        self.invencivel = 0
        self.contador_passos = 0

    def desenhar(self, pose):
        """Desenha o robô. Pose 0: parado, 1 e 2: andando, 3: pulando."""
        figura = nova_figura(28, 36)
        # pernas (mudam conforme a pose)
        if pose == 1:
            pernas = [(5, 27, 6, 9), (17, 27, 6, 7)]
        elif pose == 2:
            pernas = [(5, 27, 6, 7), (17, 27, 6, 9)]
        elif pose == 3:
            pernas = [(3, 26, 6, 7), (19, 26, 6, 7)]
        else:
            pernas = [(6, 27, 6, 9), (16, 27, 6, 9)]
        for perna in pernas:
            pygame.draw.rect(figura, CINZA, perna)
        pygame.draw.rect(figura, CINZA_CLARO, (3, 12, 22, 16), border_radius=3)   # corpo
        pygame.draw.rect(figura, LARANJA, (10, 16, 8, 6))                         # painel
        pygame.draw.rect(figura, AZUL, (5, 2, 18, 11), border_radius=3)           # cabeça
        pygame.draw.rect(figura, AZUL_CLARO, (14, 5, 7, 5))                       # olho
        pygame.draw.line(figura, CINZA, (10, 2), (10, 0), 2)                      # antena
        return figura

    def pular(self):
        """Pula, mas só se estiver no chão. Devolve True se pulou."""
        if self.no_chao:
            self.vel_y = -FORCA_PULO
            self.no_chao = False
            return True
        return False

    def quicar(self):
        """Pulinho automático depois de pisar num inimigo."""
        self.vel_y = -QUIQUE_AO_PISAR

    def voltar_ao_inicio(self, tempo_invencivel):
        """Volta para o começo da fase e fica invencível por um tempo."""
        self.rect.midbottom = self.inicio
        self.y_exato = float(self.rect.y)
        self.vel_y = 0.0
        self.invencivel = tempo_invencivel

    def update(self, teclas, blocos):
        """Lê as setas, aplica a gravidade, trata colisões e anima."""
        # ----- movimento horizontal -----
        self.vel_x = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.vel_x = -VELOCIDADE_JOGADOR
            self.olhando_direita = False
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vel_x = VELOCIDADE_JOGADOR
            self.olhando_direita = True

        self.rect.x += self.vel_x
        # se entrou num bloco, empurra de volta para a borda do bloco
        for bloco in pygame.sprite.spritecollide(self, blocos, False):
            if self.vel_x > 0:
                self.rect.right = bloco.rect.left
            elif self.vel_x < 0:
                self.rect.left = bloco.rect.right

        # ----- movimento vertical (gravidade) -----
        self.vel_y = min(self.vel_y + GRAVIDADE, VELOCIDADE_MAXIMA_QUEDA)
        self.y_exato += self.vel_y
        self.rect.y = round(self.y_exato)
        self.no_chao = False
        for bloco in pygame.sprite.spritecollide(self, blocos, False):
            if self.vel_y > 0:        # caindo: pousou em cima do bloco
                self.rect.bottom = bloco.rect.top
                self.no_chao = True
            elif self.vel_y < 0:      # subindo: bateu a cabeça
                self.rect.top = bloco.rect.bottom
            self.vel_y = 0.0
            self.y_exato = float(self.rect.y)

        if self.invencivel > 0:
            self.invencivel -= 1
        self.animar()

    def animar(self):
        """Escolhe a figura certa (parado, andando ou pulando) e pisca se invencível."""
        if not self.no_chao:
            figura = self.figura_pulando
        elif self.vel_x != 0:
            self.contador_passos += 1
            figura = self.figuras_andando[(self.contador_passos // 8) % 2]
        else:
            figura = self.figura_parado
        if not self.olhando_direita:
            figura = pygame.transform.flip(figura, True, False)
        # piscar: fica invisível em alguns quadros enquanto está invencível
        if self.invencivel > 0 and (self.invencivel // 5) % 2 == 0:
            figura = nova_figura(28, 36)
        self.image = figura

    def caiu_da_tela(self):
        """True se o robô caiu num buraco e saiu por baixo da tela."""
        return self.rect.top > ALTURA


class Particula(pygame.sprite.Sprite):
    """Pedacinho colorido que voa e cai (efeito ao coletar ou pisar)."""

    def __init__(self, centro, cor):
        """Cria a partícula em `centro` com uma velocidade aleatória."""
        super().__init__()
        self.image = nova_figura(6, 6)
        pygame.draw.circle(self.image, cor, (3, 3), 3)
        self.rect = self.image.get_rect(center=centro)
        self.vel_x = random.randint(-4, 4)
        self.vel_y = random.randint(-8, -2)
        self.vida = 30   # quadros até sumir

    def update(self):
        """Move a partícula com gravidade; some quando a vida acaba."""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += 1
        self.vida -= 1
        if self.vida <= 0:
            self.kill()
