"""Configurações do jogo: tela, cores, física e regras.

Todos os números importantes ficam aqui. Para deixar o jogo mais fácil
ou mais difícil, basta mudar os valores deste arquivo.
"""
import os

# ---------- Janela ----------
TITULO = "Robô Coletor"
TAMANHO_BLOCO = 40          # cada letra do mapa vira um quadrado de 40x40
COLUNAS = 20
LINHAS = 15
LARGURA = COLUNAS * TAMANHO_BLOCO   # 800
ALTURA = LINHAS * TAMANHO_BLOCO     # 600
FPS = 60

# ---------- Arquivos ----------
PASTA_DO_JOGO = os.path.dirname(__file__)
PASTA_SONS = os.path.join(PASTA_DO_JOGO, "assets", "sons")
ARQUIVO_RECORDE = os.path.join(PASTA_DO_JOGO, "recorde.txt")

# ---------- Cores (vermelho, verde, azul) ----------
PRETO = (0, 0, 0)            # usada como cor transparente (colorkey)
BRANCO = (255, 255, 255)
CINZA_ESCURO = (40, 40, 50)
CINZA = (120, 120, 130)
CINZA_CLARO = (190, 195, 205)
AZUL = (60, 140, 255)
AZUL_CLARO = (120, 200, 255)
VERMELHO = (230, 50, 50)
VERDE = (60, 200, 80)
VERDE_ESCURO = (30, 120, 50)
AMARELO = (255, 220, 40)
LARANJA = (255, 140, 30)
ROXO = (150, 70, 200)

# ---------- Física do jogador ----------
GRAVIDADE = 0.7             # quanto a velocidade de queda aumenta por quadro
FORCA_PULO = 15             # velocidade para cima no início do pulo
VELOCIDADE_MAXIMA_QUEDA = 15
VELOCIDADE_JOGADOR = 5
QUIQUE_AO_PISAR = 10        # pulinho ao pisar num inimigo

# ---------- Regras ----------
VIDAS_INICIAIS = 3
TEMPO_POR_FASE = 90         # segundos
TEMPO_INVENCIVEL = 90       # quadros piscando depois de levar dano (1,5 s)
PONTOS_BATERIA = 10
PONTOS_INIMIGO = 50
PONTOS_POR_SEGUNDO_RESTANTE = 5
