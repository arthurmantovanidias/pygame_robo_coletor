# Guia de Git para o grupo (usando o GitHub Desktop)

Não precisa de linha de comando. Tudo se faz pelo programa **GitHub Desktop** (desktop.github.com).

## 1. Primeira vez (cada integrante faz uma vez)

1. Crie uma conta em github.com, se ainda não tiver.
2. Instale o GitHub Desktop e entre com a **sua** conta: **File → Options → Accounts → Sign in**.
3. Aceite o convite para o repositório. Ele chega por e-mail ou aparece em github.com/notifications.
4. No GitHub Desktop: **File → Clone repository**, escolha `robo_coletor` e clique em **Clone**.
5. Instale o PyGame:

   ```bash
   pip install pygame-ce
   ```

6. Abra a pasta no VS Code e rode `python main.py` para conferir que funciona.

## 2. Todo dia que for trabalhar

1. Abra o GitHub Desktop e clique em **Fetch origin**. Se aparecer, clique em **Pull origin** para baixar o que os colegas fizeram.
2. Faça as suas mudanças no VS Code e teste o jogo.
3. Volte ao GitHub Desktop. Os arquivos alterados aparecem na esquerda.
4. Embaixo, escreva um **resumo** do que fez (exemplo: "Adiciona música da fase 2") e clique em **Commit to main**.
5. Clique em **Push origin** para enviar ao GitHub.

Faça isso **várias vezes**, a cada pedaço que ficar pronto. O professor vê a quantidade e a data dos commits de cada um.

## 3. Se aparecer um "conflito"

Um conflito acontece quando duas pessoas mudaram a mesma linha. O GitHub Desktop avisa e abre o arquivo. Dentro dele vai aparecer algo assim:

```
<<<<<<< HEAD
a sua versão
=======
a versão do colega
>>>>>>> origin/main
```

Apague as linhas com `<<<<<<<`, `=======` e `>>>>>>>` e deixe o código certo, que pode juntar as duas versões. Salve, teste o jogo e faça commit. Na dúvida, chame o grupo antes de apagar qualquer coisa.

**Para evitar conflitos:** combinem quem mexe em qual arquivo (veja o `PLANO_DA_EQUIPE.md`) e sempre faça **Pull** antes de começar.

## 4. Dicas

- Não faça commit do `recorde.txt` nem da pasta `__pycache__`. O `.gitignore` já ignora os dois.
- Mensagem de commit boa diz **o que** mudou: "Adiciona plataforma móvel". Uma mensagem como "mudanças" não ajuda ninguém.
- Errou algo e não fez push ainda? Clique com o botão direito no commit, no histórico, e escolha **Undo commit**.
