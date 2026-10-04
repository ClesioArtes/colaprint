<!-- Padrão Clésio Artes Miniapps v1.0 · README
     Espaço da logo Clésio Artes: quando existir, salve como clesioartes-logo.png
     e troque esta linha por <p align="center"><img src="clesioartes-logo.png" alt="Clésio Artes" height="40"></p> -->

<p align="center"><img src="colaprint.ico" alt="" width="72"></p>

<h1 align="center">ColaPrint</h1>

<p align="center">
Print de qualquer parte da tela, colado direto onde você quiser.<br>
<sub>um utilitário Clésio Artes · versão <!--versao-->1.0.0<!--/versao--> · Windows</sub>
</p>

---

## O que faz

- Tira print da **tela inteira** ou de uma **área** que você seleciona.
- **Não salva arquivo**: vai direto para a área de transferência.
- Cola **onde você clicar com o botão direito**: conversa com IA, e-mail, WhatsApp Web, documento.
- Fica num **ícone perto do relógio** e pode **iniciar com o Windows**.
- Funciona com **vários monitores** e telas com zoom.

## Instalar

1. Tenha o [Python 3.9+](https://www.python.org/downloads/) com **Add python.exe to PATH** marcado.
2. Baixe (**Code → Download ZIP**) e extraia numa pasta, por exemplo `C:\dev\colaprint`.
3. Dois cliques em **`Instalar ColaPrint.bat`**.

## Usar

1. Aperte <kbd>F9</kbd> e escolha **Tela inteira** ou **Selecionar área**.
2. Na seleção, a tela escurece: arraste em cima do que quer mostrar.
3. O clique esquerdo fica livre: troque de aba, abra a janela, clique no campo.
4. **Clique com o botão direito** onde quer colar.

## Atalhos

| Tecla | O que faz |
|---|---|
| <kbd>F9</kbd> | Abre o menu de captura |
| <kbd>Esc</kbd> | Cancela (no menu, na seleção ou antes de colar) |
| Clique direito | Cola o print no lugar apontado |
| <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>F9</kbd> | Fecha o ColaPrint |

## Requisitos

- Windows 10 ou 11
- Python 3.9 ou mais novo
- Dependências em [`requirements.txt`](requirements.txt), instaladas pelo instalador

## Desinstalar

Dois cliques em **`Desinstalar ColaPrint.bat`**. Ele fecha o ColaPrint e tira atalhos e início automático. Python, dependências e arquivos da pasta ficam onde estão.

## Problemas

- **F9 não faz nada**: veja se o ícone azul está perto do relógio (ou na setinha **^**).
- **A instalação parou**: o motivo fica em `colaprint_instalacao.txt`, na pasta.
- **Erro durante o uso**: o motivo fica em `colaprint_erros.txt`, na pasta.
- **Trocar a tecla F9**: mude `ATALHO = "f9"` no começo do `colaprint.pyw`.

O guia completo, com demonstração, está em **`LEIA-ME.html`**.

---

<sub>ColaPrint <!--versao-->1.0.0<!--/versao--> · Clésio Artes · © 2026 · uso livre, redistribuição e venda só com autorização ([LICENSE](LICENSE))</sub>
