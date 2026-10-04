# ColaPrint · História do projeto

*Documento interno da Clésio Artes. Não é manual de usuário e não vai para o GitHub.*

Escrito ao fechar a versão 1.0.0, em 04/10/2026.
Onde aparecer **[A COMPLETAR]**, é porque a informação não ficou registrada durante a construção e o Fernando pode completar depois.

---

## 1. Origem

O ColaPrint nasceu de uma necessidade interna, do próprio dia a dia do Fernando, e não de um cliente.

Naquela fase o Fernando estava usando muito o Claude para trabalhar. Toda hora ele queria mostrar alguma coisa da tela numa conversa: um erro, uma página, um pedaço de programa. E toda vez era a mesma volta.

O incômodo que disparou a ideia:

- abrir a Ferramenta de Captura do Windows;
- recortar;
- salvar a imagem;
- anexar na conversa.

O resultado era o computador cheio de prints salvos que só tinham servido uma vez.

A conversa toda que deu origem ao ColaPrint, da ideia até a 1.0.0, aconteceu no mesmo dia: 04/10/2026.

**[A COMPLETAR]** Há quanto tempo esse incômodo vinha acontecendo antes de virar ideia, e em quais projetos ele mais aparecia.

## 2. O problema

**Como era antes**

- Ferramenta de Captura do Windows, salvando arquivo a cada print.
- O atalho rápido do Windows (Win+Shift+S) estava abrindo uma ferramenta da Adobe no computador do Fernando, com muita coisa que ele não queria ver.

**O que incomodava**

- Passos demais para uma coisa que deveria ser instantânea.
- Pasta enchendo de imagens descartáveis.
- Interromper o raciocínio no meio de uma conversa para mexer em arquivo.

**Por que valeu fazer uma ferramenta própria**

- Antes de construir, pesquisamos o que já existia. Achamos servidores MCP que deixam o Claude Code tirar print sozinho e o atalho de print que o app do Claude tem no Mac. No Windows, para o uso que o Fernando queria (ele mesmo escolhendo a área e mandando direto), não havia nada simples e pronto.
- O Fernando quis explicitamente ter **o nosso**, bem simples, sem aplicativo pesado em volta.

## 3. A ideia

A imagem inicial do Fernando: apertar uma tecla, a tela escurece como na Ferramenta de Captura, ele seleciona a área e o print **já cai dentro da conversa**, sem salvar, sem Ctrl+C e Ctrl+V na mão.

A lógica central, que continua até hoje:

> uma tecla → escolher o que mostrar → o print já está pronto para ser colado → colar onde precisa.

O que ele deveria simplificar: tirar o "trabalho de arquivo" do meio de uma conversa.

## 4. O que o ColaPrint faz

Um utilitário pequeno para Windows que tira print de qualquer parte da tela e cola direto onde você quiser.

**Para quem foi criado**: para o próprio Fernando, no trabalho com IA. Depois ficou claro que serve para qualquer pessoa que mostra coisas da tela em conversas, e-mails ou documentos.

**Principais funções na 1.0.0**

- F9 abre um menu pequeno: *Tela inteira* ou *Selecionar área*.
- Na seleção, a tela congela e escurece; arrasta e solta.
- O print vai para a área de transferência, sem salvar arquivo.
- O clique esquerdo fica livre para achar o lugar certo; o **clique direito cola**.
- Esc ou clique fora cancela em qualquer etapa.
- Ícone perto do relógio, com opção de iniciar com o Windows.
- Funciona com vários monitores e com zoom de tela.

## 5. Como foi construído

**Tecnologia**

- Python, num único arquivo (`colaprint.pyw`), que roda sem janela.
- Peças usadas: Pillow (imagem), pywin32 (Windows e área de transferência), keyboard (tecla F9), pystray (ícone perto do relógio), pynput (segurar o clique direito).
- Tkinter (já vem com o Python) para o menu, a tela escurecida e a etiqueta que segue o mouse.

**Arquitetura, no geral**

- O programa fica parado esperando a tecla. Cada pedido vira um "comando" numa fila, e um laço principal executa um de cada vez: menu, captura, copiar, colar.
- Só uma cópia pode rodar por vez.
- O mesmo arquivo também sabe se instalar e se desinstalar (`--instalar`, `--desinstalar`, `--versao`).

**Peças criadas**

- `colaprint.pyw`: o programa.
- `colaprint.ico`: o ícone (quadrado azul com os cantos de seleção e uma seta de "colar"), desenhado por código. Se faltar, o instalador desenha de novo.
- `Instalar ColaPrint.bat` e `Desinstalar ColaPrint.bat`: dois cliques e pronto.
- Ícone na bandeja com menu: tirar print, tela inteira, área, colar com clique direito, iniciar com o Windows, sair.
- Atalhos com ícone na área de trabalho e no menu Iniciar.
- `LEIA-ME.html`: guia bonito, com uma demonstração que dá para testar na própria página.
- `README.md`: resumo para o GitHub.
- `VERSION`: fonte única da versão.
- `requirements.txt`: lista única de dependências.
- Logs: `colaprint_erros.txt` (uso) e `colaprint_instalacao.txt` (instalação).
- `LICENSE`: licença própria da Clésio Artes.

## 6. Evolução

Tudo isso aconteceu em rodadas curtas, testando no computador do Fernando entre uma e outra.

**Primeira versão: "cola no Claude"**
- F9, tela escurece, seleciona, e o programa procurava sozinho a janela com "Claude" no título, trazia ela para a frente e colava.
- Sem janela, sem menu.

**Segunda versão: pergunta, ícone e "cola onde eu clicar"**
- O Fernando pediu para escolher entre tela inteira e área.
- Percebemos que colar automaticamente na janela do Claude era arriscado: o print podia cair no lugar errado, e o ColaPrint servia para qualquer programa, não só para o Claude. Daí veio a ideia de esperar um clique e colar ali.
- Entrou o ícone perto do relógio, para ele não ficar invisível, e a opção de iniciar com o Windows.

**Terceira versão: clique direito cola**
- Com várias abas abertas, o clique esquerdo era necessário para navegar até o lugar certo. Então o clique esquerdo ficou livre e o **clique direito virou o "colar"**, sem abrir o menu de contexto do Windows.

**Ajustes de uso**
- Esc ou clique fora dos botões passou a cancelar o menu do F9.

**De script para produto**
- Nome, ícone, documentação, página LEIA-ME com demonstração, instalador e desinstalador.
- Depois, a rodada da 1.0.0: versão única, dependências numa lista, instalador que confere arquivos e mostra o erro, desinstalador que pergunta antes e fecha só o ColaPrint, licença, e a separação entre o que é padrão e o que é específico.

**Problemas que apareceram e como resolvemos**

- *"Está rodando a versão antiga"*: a versão antiga continuava aberta em segundo plano e a nova nem abria, porque faltava instalar uma peça. Resolvido com a trava de cópia única e com o instalador cuidando das dependências.
- *Ícone do Python no arquivo*: o Windows não deixa trocar o ícone de um `.pyw` sozinho. Resolvido com atalhos que carregam o ícone do ColaPrint.
- *Página não pode instalar nada*: navegador não roda programa por segurança. O "botão de instalar" virou o arquivo `.bat` dentro da pasta.
- *Mudar a pasta de lugar quebrava o início automático*: agora o programa se corrige sozinho ao abrir.
- *GitHub*: a conexão usada aqui não tinha permissão para criar repositórios, e o repositório `ClesioArtes/colaprint` estava numa conta diferente da conectada (astellumstudio). Isso expôs um problema maior: várias contas de e-mail logadas em lugares diferentes. O envio ficou para ser feito pelo próprio Fernando, com Git.

**O que foi descartado ou mudou**

- Procurar a janela do Claude e colar sozinho: trocado por "colar onde eu clicar", e depois por "clique direito cola".
- Iniciar com o Windows pela pasta `shell:startup`: trocado pela opção no menu do ícone.
- O primeiro `README.md` simples: trocado pelo `LEIA-ME.html` e, na 1.0.0, por um README curto próprio para o GitHub.

## 7. Decisões importantes

**Por que assim**

- **Python e não um `.exe`**: era o que já estava instalado e permitia ajustar rápido, testando na hora. O `.exe` ficou como passo futuro.
- **Não salvar arquivo**: era justamente o incômodo de origem.
- **Clique direito para colar**: deixa o clique esquerdo livre para navegar e confirma o lugar certo antes de colar.
- **Um arquivo só de programa**: fácil de entender, copiar e atualizar.
- **Licença "todos os direitos reservados"**: o código pode ficar público para ser visto e usado, mas o ColaPrint continua da Clésio Artes. Uma licença open source foi considerada e deixada de lado de propósito.

**O que deliberadamente NÃO entrou**

- Desenhar, marcar ou anotar no print.
- Histórico de prints.
- Pasta de prints salvos.
- Qualquer função "só para deixar o projeto maior".

**Limitações aceitas**

- Precisa do Python instalado.
- Só Windows.
- A tecla F9 só se troca editando o arquivo.
- A opção "Colar com clique direito" volta a ficar ligada sempre que o programa é aberto de novo (não é guardada).
- A página LEIA-ME usa uma fonte da internet; sem conexão, cai na fonte do Windows.
- O README e o LEIA-ME recebem o número da versão por meio do instalador ou do comando `--versao`; editados na mão, podem ficar desatualizados até o próximo comando.

## 8. Resultado

**O que a 1.0.0 resolveu**: mostrar algo da tela numa conversa virou F9, arrastar e clique direito. Sem arquivo, sem pasta, sem programa pesado.

**Como passou a ser usado**: no dia a dia do Fernando, principalmente para mostrar coisas da tela nas conversas com o Claude. **[A COMPLETAR]** Com que frequência e em quais outros programas ele passou a usar.

**O que consideramos pronto**

- Funciona do jeito que o Fernando pediu, testado no computador dele.
- Instala e desinstala com dois cliques.
- Tem documentação para usuário (LEIA-ME e README) e para nós (este arquivo).
- Tem versão, licença e estrutura limpa.

**Situação no GitHub ao fechar este documento**: o repositório `ClesioArtes/colaprint` existe e é público, mas a 1.0.0 ainda estava esperando o envio pelo Fernando. **[A COMPLETAR]** Data do envio e se o repositório ficou público ou privado.

## 9. Caminhos possíveis no futuro

*Possibilidades, não compromissos.*

- Virar um **ColaPrint.exe**, que funcione sem Python e carregue o próprio ícone.
- Desenhar uma seta ou um círculo no print antes de mandar (foi lembrado durante a construção, mas não entrou).
- Trocar a tecla pelo menu do ícone, sem editar o arquivo.
- Lembrar a escolha de "Colar com clique direito" entre uma vez e outra.
- Colocar a logo da Clésio Artes no LEIA-ME e no README quando ela existir (o espaço já está reservado).
- Observação: na pesquisa por nome no GitHub apareceu um repositório de outra pessoa chamado "ColaPrints-Downloads". Vale lembrar disso se um dia o nome for registrado ou divulgado.

## 10. Legado

O ColaPrint passou a ser a referência do **Padrão Clésio Artes Miniapps v1.0**. O próximo a nascer dele é o ELO. **[A COMPLETAR]** O que é o ELO.

O que pode ser reaproveitado nos próximos utilitários:

- A estrutura de pasta, com os mesmos arquivos e sem pastas extras.
- `VERSION` como fonte única e as marcas de versão nos documentos.
- `requirements.txt` como lista única de dependências.
- Os dois `.bat`, trocando só as variáveis do topo.
- No programa, todas as partes marcadas **[PADRÃO]**: versão, log, instalar/desinstalar, iniciar com o Windows, cópia única, ícone na bandeja com "Iniciar com o Windows" e "Sair", laço principal.
- A política de logs.
- A licença, trocando o nome do app.
- O LEIA-ME como modelo visual: assinatura "um utilitário Clésio Artes", espaço da logo, seções de instalar, perguntas, problemas e rodapé.

O que **não** deve ser copiado: tudo marcado **[ESPECÍFICO]** no código e no LEIA-ME (captura, colar com clique direito, F9, a demonstração, o ícone e a cor azul).
