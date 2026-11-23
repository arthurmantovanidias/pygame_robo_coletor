"""Classe Partida: as regras do jogo enquanto se está jogando."""
import pygame

from config import (ALTURA, AMARELO, BRANCO, FPS, LARGURA, PONTOS_BATERIA, PONTOS_INIMIGO,
                    PONTOS_POR_SEGUNDO_RESTANTE, ROXO, TEMPO_INVENCIVEL, TEMPO_POR_FASE, VERDE,
                    VERMELHO, VIDAS_INICIAIS)
from fase import Fase
from fases import FASES
from sprites import Jogador, Particula
from texto import escrever


class Partida:
    """Uma partida inteira: da fase 1 até vencer ou perder todas as vidas."""

    def __init__(self, sons):
        """Começa a partida na primeira fase."""
        self.sons = sons
        self.pontos = 0
        self.vidas = VIDAS_INICIAIS
        self.numero_fase = 0          # índice na lista FASES (0 = primeira)
        self.resultado = None         # vira "vitoria" ou "derrota" no final
        self.pausado = False
        self.particulas = pygame.sprite.Group()
        self.carregar_fase()

    def carregar_fase(self):
        """Monta a fase atual, coloca o robô no início e zera o cronômetro."""
        self.fase = Fase(FASES[self.numero_fase])
        x, y = self.fase.inicio_jogador
        self.jogador = Jogador(x, y)
        self.tempo_restante = TEMPO_POR_FASE * FPS   # contado em quadros
        self.tempo_aviso = 120        # mostra o nome da fase por 2 segundos
        self.tempo_fim = 0            # pausa curta antes da tela final
        self.particulas.empty()
        self.sons["fase"].play()

    # ------------------------------------------------------------------
    def tratar_evento(self, evento):
        """Pular (seta para cima, W ou espaço) e pausar (P ou ESC)."""
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key in (pygame.K_p, pygame.K_ESCAPE):
            self.pausado = not self.pausado
        elif evento.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE) and not self.pausado:
            if self.jogador.pular():
                self.sons["pulo"].play()

    def atualizar(self):
        """Um quadro do jogo: movimento, colisões, tempo e troca de fase."""
        if self.pausado:
            return
        if self.tempo_aviso > 0:      # jogo congelado enquanto mostra o nome da fase
            self.tempo_aviso -= 1
            return
        if self.tempo_fim > 0:        # perdeu: espera um pouco e termina
            self.tempo_fim -= 1
            self.particulas.update()
            if self.tempo_fim == 0:
                self.resultado = "derrota"
            return

        teclas = pygame.key.get_pressed()
        self.jogador.update(teclas, self.fase.blocos)
        self.fase.atualizar()
        self.particulas.update()

        self.verificar_baterias()
        self.verificar_inimigos()
        self.verificar_perigos()
        self.verificar_porta()

    def soltar_particulas(self, centro, cor, quantidade):
        """Cria várias partículas no ponto `centro`."""
        for _ in range(quantidade):
            self.particulas.add(Particula(centro, cor))

    def verificar_baterias(self):
        """Coleta as baterias tocadas. Se acabarem, abre a porta."""
        coletadas = pygame.sprite.spritecollide(self.jogador, self.fase.baterias, True)
        for bateria in coletadas:
            self.pontos += PONTOS_BATERIA
            self.sons["bateria"].play()
            self.soltar_particulas(bateria.rect.center, VERDE, 10)
        if coletadas and len(self.fase.baterias) == 0:
            self.fase.porta.abrir()
            self.sons["porta"].play()

    def verificar_inimigos(self):
        """Pisar em cima do inimigo derrota ele; encostar de lado tira vida."""
        tocados = pygame.sprite.spritecollide(self.jogador, self.fase.inimigos, False)
        for inimigo in tocados:
            caindo = self.jogador.vel_y > 0
            por_cima = self.jogador.rect.bottom - inimigo.rect.top < 20
            if caindo and por_cima:
                inimigo.kill()
                self.jogador.quicar()
                self.pontos += PONTOS_INIMIGO
                self.sons["pisar"].play()
                self.soltar_particulas(inimigo.rect.center, ROXO, 15)
            else:
                self.perder_vida()
                return

    def verificar_perigos(self):
        """Espinhos, buraco e fim do tempo tiram uma vida."""
        if pygame.sprite.spritecollideany(self.jogador, self.fase.espinhos):
            self.perder_vida()
        elif self.jogador.caiu_da_tela():
            self.perder_vida()
        self.tempo_restante -= 1
        if self.tempo_restante <= 0:
            self.tempo_restante = TEMPO_POR_FASE * FPS
            self.perder_vida()

    def perder_vida(self):
        """Tira uma vida (se não estiver invencível) e volta ao início da fase."""
        if self.jogador.invencivel > 0 or self.tempo_fim > 0:
            return
        self.vidas -= 1
        self.sons["dano"].play()
        self.soltar_particulas(self.jogador.rect.center, VERMELHO, 25)
        if self.vidas <= 0:
            self.tempo_fim = 90           # 1,5 s vendo a explosão antes do fim
            self.jogador.kill()
        else:
            self.jogador.voltar_ao_inicio(TEMPO_INVENCIVEL)

    def verificar_porta(self):
        """Entrar na porta aberta: ganha bônus de tempo e vai para a próxima fase."""
        porta = self.fase.porta
        if not porta.aberta or not self.jogador.rect.colliderect(porta.rect):
            return
        segundos = self.tempo_restante // FPS
        self.pontos += segundos * PONTOS_POR_SEGUNDO_RESTANTE
        self.numero_fase += 1
        if self.numero_fase >= len(FASES):
            self.resultado = "vitoria"
        else:
            self.carregar_fase()

    # ------------------------------------------------------------------
    def desenhar(self, janela):
        """Desenha a fase, o robô, as partículas, o placar e os avisos."""
        self.fase.desenhar(janela)
        if self.tempo_fim == 0:
            janela.blit(self.jogador.image, self.jogador.rect)
        self.particulas.draw(janela)
        self.desenhar_placar(janela)

        if self.tempo_aviso > 0:
            escrever(janela, f"FASE {self.numero_fase + 1}", 90, AMARELO, (LARGURA // 2, ALTURA // 2 - 30))
            escrever(janela, self.fase.nome, 50, BRANCO, (LARGURA // 2, ALTURA // 2 + 30))
        if self.pausado:
            veu = pygame.Surface((LARGURA, ALTURA))
            veu.set_alpha(150)                 # 150 de 255: semitransparente
            janela.blit(veu, (0, 0))
            escrever(janela, "PAUSADO", 90, BRANCO, (LARGURA // 2, ALTURA // 2 - 20))
            escrever(janela, "Aperte P para continuar", 36, BRANCO, (LARGURA // 2, ALTURA // 2 + 40))

    def desenhar_placar(self, janela):
        """Barra no topo: pontos, baterias, fase, tempo e vidas."""
        barra = pygame.Surface((LARGURA, 40))
        barra.set_alpha(170)
        janela.blit(barra, (0, 0))

        escrever(janela, f"Pontos: {self.pontos}", 30, BRANCO, (90, 20))
        coletadas = self.fase.total_baterias - len(self.fase.baterias)
        escrever(janela, f"Baterias: {coletadas}/{self.fase.total_baterias}", 30, VERDE, (260, 20))
        escrever(janela, f"Fase {self.numero_fase + 1}", 30, BRANCO, (420, 20))
        segundos = self.tempo_restante // FPS
        cor_tempo = VERMELHO if segundos <= 10 else BRANCO
        escrever(janela, f"Tempo: {segundos}", 30, cor_tempo, (550, 20))
        for i in range(self.vidas):
            pygame.draw.circle(janela, VERMELHO, (LARGURA - 25 - i * 30, 20), 10)
