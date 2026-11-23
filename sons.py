"""Carregamento da música e dos efeitos sonoros (arquivos .wav em assets/sons)."""
import os

import pygame

from config import PASTA_SONS

NOMES_DOS_SONS = ["pulo", "bateria", "pisar", "dano", "porta", "fase", "menu", "vitoria", "derrota"]


def carregar_sons():
    """Devolve um dicionário nome -> som. Exemplo: sons["pulo"].play()"""
    sons = {}
    for nome in NOMES_DOS_SONS:
        caminho = os.path.join(PASTA_SONS, nome + ".wav")
        sons[nome] = pygame.mixer.Sound(caminho)
    return sons


def tocar_musica():
    """Começa a música de fundo, repetindo para sempre (-1)."""
    pygame.mixer.music.load(os.path.join(PASTA_SONS, "musica.wav"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
