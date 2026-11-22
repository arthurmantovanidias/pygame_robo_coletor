"""Função para escrever textos na tela."""
import pygame

# guarda as fontes já criadas: criar fonte toda hora deixaria o jogo lento
fontes = {}


def escrever(janela, texto, tamanho, cor, centro):
    """Escreve `texto` na janela, centralizado no ponto `centro` (x, y)."""
    if tamanho not in fontes:
        fontes[tamanho] = pygame.font.Font(None, tamanho)
    imagem = fontes[tamanho].render(texto, True, cor)
    janela.blit(imagem, imagem.get_rect(center=centro))
