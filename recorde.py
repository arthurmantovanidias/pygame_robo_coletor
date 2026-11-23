"""Funções para ler e salvar o recorde num arquivo de texto."""
import os

from config import ARQUIVO_RECORDE


def ler_recorde():
    """Devolve o recorde salvo, ou 0 se o arquivo ainda não existe."""
    if not os.path.exists(ARQUIVO_RECORDE):
        return 0
    with open(ARQUIVO_RECORDE, "r") as arquivo:
        texto = arquivo.read().strip()
    if texto.isdigit():
        return int(texto)
    return 0


def salvar_recorde(pontos):
    """Grava `pontos` como o novo recorde."""
    with open(ARQUIVO_RECORDE, "w") as arquivo:
        arquivo.write(str(pontos))
