# Roteiro do projeto: Robô Coletor

Checklist diário para o grupo construir o jogo do zero. Marque `[x]` em cada item pronto e faça commit **no mesmo dia**, cada um na sua conta.

**Legenda:** 🅰 Arthur · 🅱 Bernardo · 🅶 Gabriel · 👥 todos juntos

> Este roteiro foi planejado com ajuda de IA (Claude). Ele explica **o que** fazer e **quais conceitos** usar, mas não traz o código pronto: o código é escrito pelo grupo.

## Regras de cada dia

1. Antes de começar: **Pull** no GitHub Desktop.
2. Terminou um item: rode o jogo, faça **commit** com a mensagem sugerida e **push**.
3. Ficou travado? Leia a documentação (pyga.me/docs), pergunte ao grupo, ao professor ou peça à IA uma **explicação** (por exemplo: "explique como funciona spritecollide"). Não peça "faça o código". Tudo o que a IA ajudar, anote em `docs/uso_de_ia.md`.
4. No fim do dia, cada um explica para os outros, em 2 minutos, o que fez. Esse é o treino para a prova individual de 25/11.

## Dia 1: quarta, 11/11 (preparação)

- [ ] 👥 Criar o repositório no GitHub e convidar os três e o professor
- [ ] 👥 Cada um clona o repositório e adiciona o próprio nome no README
  - commit: `Adiciona meu nome ao README`
- [ ] 🅶 Desenhar no papel (quadriculado, 20 colunas × 15 linhas) a fase 1, fotografar e salvar em `docs/rascunhos/`
- [ ] 🅰 Criar `main.py`, que abre uma janela 800×600 com fundo azul e fecha no X
  - conceitos: `pygame.init`, `pygame.display.set_mode`, laço `while`, `pygame.event.get`, `pygame.QUIT`, `pygame.display.flip`
  - **pronto quando:** a janela abre e fecha sem erro
  - commit: `Cria janela do jogo`
- [ ] 🅱 Criar `config.py` com as constantes: `LARGURA`, `ALTURA`, `FPS`, `TAMANHO_BLOCO = 40` e as cores
  - por que existe: assim nenhum número fica "solto" no meio do código
  - commit: `Adiciona arquivo de configurações`

## Dia 2: quinta, 12/11 (o mapa)

- [ ] 🅶 Criar `fases.py` com a fase 1 como uma **lista de 15 textos de 20 letras**
  - letras: `#` bloco, `.` vazio, `J` jogador, `B` bateria, `I` inimigo, `^` espinho, `P` porta
  - commit: `Adiciona mapa da fase 1`
- [ ] 🅰 Criar `sprites.py` com a classe `Bloco(pygame.sprite.Sprite)`: um quadrado 40×40 colorido
  - conceitos: herança, `super().__init__()`, `self.image`, `self.rect`
  - commit: `Cria classe Bloco`
- [ ] 🅱 Criar `fase.py` com a classe `Fase`, que percorre o mapa e cria um `Bloco` para cada `#`
  - conceitos: dois `for` com `enumerate` (linha e coluna). A posição na tela é `x = coluna * 40` e `y = linha * 40`. Guarde os blocos num `pygame.sprite.Group`.
  - **pronto quando:** o mapa da fase 1 aparece desenhado na janela
  - commit: `Desenha a fase a partir do mapa`

## Dia 3: sexta, 13/11 (o robô se mexe)

- [ ] 🅰 Classe `Jogador`, desenhada como um retângulo por enquanto, que nasce na letra `J`
  - commit: `Cria jogador`
- [ ] 🅱 Andar para os lados com as setas
  - conceitos: `pygame.key.get_pressed()` (tecla **segurada**) e diferença para o evento `KEYDOWN`
  - commit: `Jogador anda para os lados`
- [ ] 👥 **Gravidade, pulo e colisão com blocos.** É a parte mais difícil: façam os três juntos, numa tela só, revezando quem digita.
  - ideia 1: `vel_y` aumenta um pouco a cada quadro (gravidade). Pular é colocar `vel_y` negativo.
  - ideia 2: mova **primeiro no x** e resolva as colisões, **depois no y** e resolva as colisões. Pensem: por que separar?
  - ideia 3: caindo e bateu num bloco, então pousou (`rect.bottom = bloco.rect.top`). Subindo e bateu, então bateu a cabeça.
  - ideia 4: só pode pular se estiver no chão (`no_chao`)
  - **pronto quando:** o robô pula nas plataformas, não atravessa paredes e não pula no ar
  - commit: `Adiciona gravidade, pulo e colisão`

## Dia 4: sábado, 14/11 (objetivo do jogo)

- [ ] 🅶 Classe `Bateria`, colocada nas letras `B`. Encostar nela faz a bateria sumir e dá +10 pontos.
  - conceitos: `pygame.sprite.spritecollide(jogador, grupo, True)`
  - commit: `Coleta de baterias e pontos`
- [ ] 🅱 Classe `Porta` na letra `P`, que abre (muda de cor) quando acabam as baterias
  - conceitos: `len(grupo) == 0`
  - commit: `Porta abre ao coletar todas as baterias`
- [ ] 🅰 Função `escrever(janela, texto, tamanho, cor, centro)` e placar com pontos e baterias coletadas
  - conceitos: `pygame.font.Font`, `render`, `blit`
  - commit: `Adiciona placar`

## Dia 5: domingo, 15/11 (perigos)

- [ ] 🅰 Classe `Espinho` e vidas: encostar tira 1 vida e faz o robô voltar ao início
  - commit: `Espinhos e sistema de vidas`
- [ ] 🅱 Classe `Inimigo` que anda de um lado para o outro e vira ao bater numa parede **ou quando o chão acaba**
  - dica: teste se existe bloco no ponto logo abaixo e à frente do pé do inimigo (`rect.collidepoint`)
  - commit: `Inimigo que patrulha a plataforma`
- [ ] 🅶 Pisar no inimigo derrota ele (+50); encostar de lado tira vida
  - pensem: o que significa "pisar"? O robô está caindo e o pé está perto do topo do inimigo.
  - commit: `Pisar no inimigo`
- [ ] 👥 Invencibilidade de 1,5 s depois de levar dano, com o robô piscando

## Dia 6: segunda, 16/11 (várias fases)

- [ ] 🅶 Desenhar no papel e escrever no código as fases 2 e 3, mais difíceis, e testar se dá para passar
  - commit: `Adiciona fases 2 e 3`
- [ ] 🅰 Entrar na porta aberta carrega a próxima fase. Depois da última, vitória.
  - commit: `Troca de fase`
- [ ] 🅱 Cronômetro de 90 s por fase, com os segundos que sobram virando bônus. Cair num buraco tira vida.
  - dica: contem o tempo em **quadros** (60 por segundo)
  - commit: `Cronômetro e bônus de tempo`
- [ ] 👥 Organizar as regras numa classe `Partida` (`partida.py`), separada da `Fase` e dos sprites

## Dia 7: terça, 17/11 (telas)

- [ ] 🅰 Tela de menu com Jogar / Instruções / Sair, navegando com as setas
  - dica: uma variável `tela` com o nome da tela atual; cada tela devolve o nome da próxima
  - commit: `Tela de menu`
- [ ] 🅱 Tela de instruções e pausa (tecla P)
  - commit: `Tela de instruções e pausa`
- [ ] 🅶 Tela de vitória/derrota e recorde salvo em `recorde.txt`
  - conceitos: `open`, `read`, `write`, `os.path.exists`
  - commit: `Tela final e recorde`

## Dia 8: quarta, 18/11 (som e animação)

- [ ] 🅱 Sons: música em loop e efeitos (pulo, coletar, dano, porta, vitória, derrota)
  - onde conseguir: crie os seus no **jsfxr** (sfxr.me) ou baixe do **freesound.org** e cite a fonte no README
  - conceitos: `pygame.mixer.Sound`, `pygame.mixer.music.play(-1)`
  - commit: `Adiciona música e efeitos sonoros`
- [ ] 🅰 Animação do robô: parado, andando (2 ou mais quadros) e pulando, virando para o lado em que anda
  - dica: um contador de quadros escolhe a figura; `pygame.transform.flip`
  - commit: `Animação do jogador`
- [ ] 🅶 Animações da bateria (gira e flutua) e do inimigo
  - commit: `Animações da bateria e do inimigo`

## Dia 9: quinta, 19/11 (cenário e acabamento)

- [ ] 🅶 Fundo de cada fase com céu em degradê, montanhas e sol ou estrelas, desenhado **uma vez só** (por quê?)
  - commit: `Cenários das fases`
- [ ] 🅰 Partículas ao coletar e ao pisar num inimigo
  - commit: `Efeito de partículas`
- [ ] 🅱 Imagens PNG no lugar dos retângulos, por exemplo do **kenney.nl** (gratuito; citem a fonte)
  - conceitos: `pygame.image.load(...).convert_alpha()`
  - commit: `Troca desenhos por imagens`

## Dia 10: sexta, 20/11 (extras para o conceito A)

- [ ] 🅱 Suporte a controle de videogame (`pygame.joystick`). A rubrica valoriza dispositivos externos.
  - commit: `Suporte a controle`
- [ ] 🅶 Fase 4 ou plataforma que se move
  - commit: `Adiciona fase 4`
- [ ] 🅰 Transição com escurecimento (fade) entre as fases
  - commit: `Transição entre fases`

## Dia 11: sábado, 21/11 (qualidade do código)

- [ ] 👥 Docstring em **toda** classe e função (a rubrica exige para o A)
- [ ] 👥 Procurar código repetido ou sem uso e apagar
- [ ] 👥 Jogar as fases inteiras, anotar os bugs e corrigir
- [ ] 🅰 README: descrição, como rodar, controles e organização dos arquivos
- [ ] 🅶 README: fotos dos rascunhos e a tabela "quem fez o quê"
- [ ] 🅱 Gravar um vídeo curto (Win+Alt+R grava a tela) e colocar o link no README

## Dia 12: domingo, 22/11 (revisão)

- [ ] 👥 Clonar o repositório numa pasta nova e testar se roda do zero, só com `pip install pygame-ce`
- [ ] 👥 Completar `docs/uso_de_ia.md` e a seção de IA no README
- [ ] 👥 **Treino para a prova:** cada um explica um arquivo que **não** escreveu

## Dia 13: segunda, 23/11 (entrega e Feira)

- [ ] 👥 Último commit **antes das 12h00**
- [ ] 👥 Feira de Jogos, das 12h às 14h, com os três presentes

## Dias 24 e 25/11: prova individual

- [ ] Reler todo o código e saber responder:
  - como funciona o pulo?
  - como a porta sabe que pode abrir?
  - como se cria uma fase nova?
