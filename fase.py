"""Classe Fase: transforma um mapa de texto nos objetos do jogo."""
import random

import pygame

from config import ALTURA, AMARELO, BRANCO, LARGURA, TAMANHO_BLOCO
from sprites import Bateria, Bloco, Espinho, Inimigo, Porta


class Fase:
    """Guarda todos os objetos de uma fase e o desenho do fundo."""

    def __init__(self, dados):
        """Lê o mapa (lista de textos) e cria um objeto para cada letra.

        dados: um dicionário da lista FASES (arquivo fases.py).
        """
        self.nome = dados["nome"]
        self.blocos = pygame.sprite.Group()
        self.espinhos = pygame.sprite.Group()
        self.baterias = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.porta = None
        self.inicio_jogador = (0, 0)

        mapa = dados["mapa"]
        # enumerate devolve o número da linha/coluna junto com o conteúdo
        for linha, texto in enumerate(mapa):
            for coluna, letra in enumerate(texto):
                x = coluna * TAMANHO_BLOCO
                y = linha * TAMANHO_BLOCO
                if letra == "#":
                    # tem grama se a letra de cima não for bloco
                    tem_grama = linha == 0 or mapa[linha - 1][coluna] != "#"
                    self.blocos.add(Bloco(x, y, dados["cor_bloco"], tem_grama))
                elif letra == "^":
                    self.espinhos.add(Espinho(x, y))
                elif letra == "B":
                    self.baterias.add(Bateria(x, y))
                elif letra == "I":
                    self.inimigos.add(Inimigo(x, y, dados["velocidade_inimigo"]))
                elif letra == "P":
                    self.porta = Porta(x, y)
                elif letra == "J":
                    self.inicio_jogador = (x, y)

        self.total_baterias = len(self.baterias)
        self.fundo = self.desenhar_fundo(dados)

    def desenhar_fundo(self, dados):
        """Desenha uma vez só o céu em degradê, as montanhas e o sol ou as estrelas."""
        fundo = pygame.Surface((LARGURA, ALTURA))
        cima = dados["ceu_cima"]
        baixo = dados["ceu_baixo"]
        # degradê: cada linha horizontal tem uma cor entre "cima" e "baixo"
        for y in range(ALTURA):
            t = y / ALTURA
            cor = (int(cima[0] + (baixo[0] - cima[0]) * t),
                   int(cima[1] + (baixo[1] - cima[1]) * t),
                   int(cima[2] + (baixo[2] - cima[2]) * t))
            pygame.draw.line(fundo, cor, (0, y), (LARGURA, y))

        if dados["noite"]:
            for _ in range(80):
                pygame.draw.circle(fundo, BRANCO, (random.randint(0, LARGURA), random.randint(0, 350)), 1)
            pygame.draw.circle(fundo, (240, 240, 210), (650, 110), 35)   # lua
        else:
            pygame.draw.circle(fundo, AMARELO, (650, 110), 45)            # sol

        # montanhas: um polígono com picos em alturas aleatórias
        pontos = [(0, ALTURA)]
        for x in range(0, LARGURA + 100, 100):
            pontos.append((x, random.randint(300, 420)))
            pontos.append((x + 50, random.randint(380, 470)))
        pontos.append((LARGURA, ALTURA))
        pygame.draw.polygon(fundo, dados["cor_montanha"], pontos)
        return fundo

    def atualizar(self):
        """Atualiza as animações e o movimento dos objetos da fase."""
        self.baterias.update()
        self.inimigos.update(self.blocos)
        self.porta.update()

    def desenhar(self, janela):
        """Desenha o fundo e todos os objetos da fase."""
        janela.blit(self.fundo, (0, 0))
        self.blocos.draw(janela)
        janela.blit(self.porta.image, self.porta.rect)
        self.espinhos.draw(janela)
        self.baterias.draw(janela)
        self.inimigos.draw(janela)
