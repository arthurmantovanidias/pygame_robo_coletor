"""Classe Jogo: abre a janela e controla as telas (menu, instruções, partida e fim)."""
import math

import pygame

from config import (ALTURA, AMARELO, AZUL, BRANCO, CINZA_CLARO, FPS, LARGURA, TAMANHO_BLOCO,
                    TITULO, VERDE, VERMELHO)
from fase import Fase
from fases import FASES
from partida import Partida
from recorde import ler_recorde, salvar_recorde
from sons import carregar_sons, tocar_musica
from sprites import Bateria, Espinho, Inimigo, Jogador, Porta
from texto import escrever


class Jogo:
    """Guarda a janela, os sons e o recorde, e troca de uma tela para outra.

    Cada tela é um método que tem o seu próprio laço e devolve o nome da
    próxima tela: "menu", "instrucoes", "partida", "fim" ou "sair".
    """

    def __init__(self):
        """Inicia o pygame, abre a janela e carrega sons e recorde."""
        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.relogio = pygame.time.Clock()
        self.sons = carregar_sons()
        self.recorde = ler_recorde()
        self.ultima_partida = None
        # a fase 1 aparece de enfeite no fundo do menu
        self.fundo_menu = Fase(FASES[0]).fundo

    def executar(self):
        """Laço principal: chama a tela atual até alguém escolher sair."""
        tocar_musica()
        tela = "menu"
        while tela != "sair":
            if tela == "menu":
                tela = self.tela_menu()
            elif tela == "instrucoes":
                tela = self.tela_instrucoes()
            elif tela == "partida":
                tela = self.tela_partida()
            elif tela == "fim":
                tela = self.tela_fim()
        pygame.quit()

    def esperar_quadro(self):
        """Espera o tempo de um quadro, para o jogo rodar a 60 quadros por segundo."""
        self.relogio.tick(FPS)

    # ------------------------------------------------------------------
    def tela_menu(self):
        """Menu inicial com três opções escolhidas pelas setas e ENTER."""
        opcoes = ["Jogar", "Instruções", "Sair"]
        destinos = ["partida", "instrucoes", "sair"]
        escolhida = 0
        robo = Jogador(0, ALTURA - 2 * TAMANHO_BLOCO)   # robô decorativo andando
        quadro = 0

        while True:
            self.esperar_quadro()
            quadro += 1
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        escolhida = (escolhida - 1) % len(opcoes)   # % faz dar a volta
                        self.sons["menu"].play()
                    elif evento.key == pygame.K_DOWN:
                        escolhida = (escolhida + 1) % len(opcoes)
                        self.sons["menu"].play()
                    elif evento.key == pygame.K_RETURN:
                        self.sons["menu"].play()
                        return destinos[escolhida]

            # o robô anda da esquerda para a direita e volta ao começo
            robo.rect.x = (robo.rect.x + 2) % LARGURA
            robo.vel_x = 2
            robo.no_chao = True
            robo.animar()

            self.janela.blit(self.fundo_menu, (0, 0))
            titulo_y = 120 + int(10 * math.sin(quadro * 0.05))   # título balançando
            escrever(self.janela, "ROBÔ COLETOR", 100, AMARELO, (LARGURA // 2, titulo_y))
            for i, texto in enumerate(opcoes):
                if i == escolhida:
                    escrever(self.janela, f"> {texto} <", 56, BRANCO, (LARGURA // 2, 270 + i * 65))
                else:
                    escrever(self.janela, texto, 46, CINZA_CLARO, (LARGURA // 2, 270 + i * 65))
            escrever(self.janela, f"Recorde: {self.recorde}", 36, AMARELO, (LARGURA // 2, 480))
            self.janela.blit(robo.image, robo.rect)
            pygame.display.flip()

    def tela_instrucoes(self):
        """Explica o objetivo e os controles, com as figuras dos objetos."""
        exemplos = [
            (Bateria(0, 0).image, "Bateria: colete todas para abrir a porta (+10)"),
            (Porta(0, 0).image, "Porta: entre nela para ir para a próxima fase"),
            (Inimigo(0, 0, 1).image, "Gosma: pule em cima (+50), mas não encoste de lado!"),
            (Espinho(0, 0).image, "Espinho: tira uma vida"),
        ]
        while True:
            self.esperar_quadro()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self.sons["menu"].play()
                    return "menu"

            self.janela.fill((25, 30, 60))
            escrever(self.janela, "INSTRUÇÕES", 70, AMARELO, (LARGURA // 2, 50))
            escrever(self.janela, "Setas ou A/D: andar    Seta p/ cima, W ou Espaço: pular", 30, BRANCO,
                     (LARGURA // 2, 110))
            escrever(self.janela, "P ou ESC: pausar", 30, BRANCO, (LARGURA // 2, 145))
            y = 210
            for figura, texto in exemplos:
                self.janela.blit(figura, figura.get_rect(center=(110, y)))
                escrever(self.janela, texto, 30, BRANCO, (440, y))
                y += 75
            escrever(self.janela, "Termine as 3 fases antes do tempo acabar!", 34, VERDE, (LARGURA // 2, 510))
            escrever(self.janela, "O tempo que sobrar vira pontos extras.", 30, CINZA_CLARO, (LARGURA // 2, 545))
            escrever(self.janela, "ENTER para voltar", 28, AZUL, (LARGURA // 2, 580))
            pygame.display.flip()

    def tela_partida(self):
        """Roda a partida até ela terminar (vitória ou derrota)."""
        partida = Partida(self.sons)
        while partida.resultado is None:
            self.esperar_quadro()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                partida.tratar_evento(evento)
            partida.atualizar()
            partida.desenhar(self.janela)
            pygame.display.flip()
        self.ultima_partida = partida
        return "fim"

    def tela_fim(self):
        """Mostra o resultado, salva o recorde e pergunta se quer jogar de novo."""
        partida = self.ultima_partida
        venceu = partida.resultado == "vitoria"
        novo_recorde = partida.pontos > self.recorde
        if novo_recorde:
            self.recorde = partida.pontos
            salvar_recorde(self.recorde)
        if venceu:
            self.sons["vitoria"].play()
        else:
            self.sons["derrota"].play()

        quadro = 0
        while True:
            self.esperar_quadro()
            quadro += 1
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        return "partida"
                    if evento.key == pygame.K_ESCAPE:
                        return "menu"

            if venceu:
                self.janela.fill((20, 90, 40))
                escrever(self.janela, "VOCÊ VENCEU!", 100, AMARELO, (LARGURA // 2, 150))
                escrever(self.janela, "O robô coletou todas as baterias!", 36, BRANCO, (LARGURA // 2, 220))
            else:
                self.janela.fill((60, 10, 10))
                escrever(self.janela, "FIM DE JOGO", 100, VERMELHO, (LARGURA // 2, 150))
                escrever(self.janela, "Acabaram as vidas...", 36, BRANCO, (LARGURA // 2, 220))
            escrever(self.janela, f"Pontos: {partida.pontos}", 60, BRANCO, (LARGURA // 2, 300))
            if novo_recorde and (quadro // 20) % 2 == 0:      # pisca
                escrever(self.janela, "NOVO RECORDE!", 46, AMARELO, (LARGURA // 2, 360))
            elif not novo_recorde:
                escrever(self.janela, f"Recorde: {self.recorde}", 36, CINZA_CLARO, (LARGURA // 2, 360))
            escrever(self.janela, "ENTER: jogar de novo    ESC: menu", 34, BRANCO, (LARGURA // 2, 470))
            pygame.display.flip()
