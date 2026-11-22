# Robô Coletor

Jogo de plataforma 2D em Python com PyGame. Projeto Final de Design de Software (Insper).

## Integrantes

- Arthur Mantovani Dias
- Bernardo Kobayashi
- Gabriel Batista

## Vídeo

Link do vídeo: PREENCHER

## Descrição

Você controla um robô que precisa coletar todas as baterias de cada fase. Quando a última bateria é coletada, a porta de saída se abre. Pelo caminho existem:

- **Gosmas**, que andam de um lado para o outro. Pular em cima delas derrota a gosma (+50 pontos). Encostar de lado tira uma vida.
- **Espinhos** e **buracos**, que tiram uma vida.
- **Tempo:** cada fase tem 90 segundos. Os segundos que sobram viram pontos extras.

São 3 fases com cenários diferentes (Floresta, Deserto e Cidade à Noite). A cada fase os inimigos ficam mais rápidos e o caminho fica mais difícil. O jogador começa com 3 vidas, e o recorde fica salvo em `recorde.txt`.

**Telas:** menu (navegação com as setas), instruções, partida (com pausa), vitória e derrota.

**Sons:** música de fundo e efeitos (pulo, bateria, pisar, dano, porta, fase, menu, vitória e derrota).

## Como rodar

```bash
pip install pygame-ce
```

```bash
python main.py
```

No Windows, também dá para clicar duas vezes em `jogar.bat`.

## Controles

| Tecla | Ação |
|-------|------|
| Setas ou A/D | Andar |
| Seta para cima, W ou Espaço | Pular |
| P ou ESC | Pausar |
| Setas + ENTER | Escolher no menu |

## Organização do código

| Arquivo | Responsabilidade |
|---------|------------------|
| `main.py` | Ponto de entrada: cria o `Jogo` e chama `executar()` |
| `jogo.py` | Classe `Jogo`: janela e telas (menu, instruções, partida e fim) |
| `partida.py` | Classe `Partida`: regras (vidas, pontos, tempo, colisões e troca de fase) |
| `fase.py` | Classe `Fase`: lê o mapa de texto e cria os objetos da fase e o fundo |
| `fases.py` | Os mapas das 3 fases, desenhados com letras (`#` bloco, `B` bateria...) |
| `sprites.py` | Classes `Jogador`, `Inimigo`, `Bloco`, `Bateria`, `Porta`, `Espinho` e `Particula` |
| `sons.py` | Carrega a música e os efeitos sonoros |
| `recorde.py` | Lê e salva o recorde num arquivo |
| `texto.py` | Função `escrever`, que escreve textos na tela |
| `config.py` | Todas as constantes (tamanhos, cores, física e regras) |
| `assets/sons/` | Arquivos `.wav` |

## Andamento

- **Quadro de tarefas (A fazer / Fazendo / Feito):** https://github.com/users/arthurmantovanidias/projects/1
- **Lista de tarefas por dia:** aba **Issues → Milestones** deste repositório
- Roteiro completo explicado: [ROTEIRO.md](ROTEIRO.md)

## Quem fez o quê

| Integrante | Arquivos que enviou |
|------------|---------------------|
| Arthur Mantovani Dias | `main.py`, `jogo.py`, `sprites.py`, `texto.py`, `jogar.bat`, README |
| Bernardo Kobayashi | `config.py`, `fase.py`, `partida.py` |
| Gabriel Batista | `fases.py`, `recorde.py`, `sons.py`, `assets/sons/` |

O código foi gerado com ajuda de IA (Claude); veja a seção abaixo.

## Design (rascunhos)

Fotos em [docs/rascunhos](docs/rascunhos).

## Uso de IA generativa

O código do jogo foi gerado com o Claude (Anthropic) e revisado e enviado pelo grupo. Os commits feitos com a IA têm a linha `Co-Authored-By: Claude`. O registro completo está em [docs/uso_de_ia.md](docs/uso_de_ia.md).
