"""
ColaPrint · um utilitário Clésio Artes
Print de qualquer parte da tela, colado direto onde você quiser.

  F9             menu: Tela inteira ou Selecionar área
                 (Esc ou clique fora dos botões cancela)
  depois         clique esquerdo livre (trocar aba, achar o campo)
                 clique DIREITO no campo certo cola ali
                 Esc deixa só copiado
  Ctrl+Alt+F9    fecha o ColaPrint

Linha de comando (usada pelos .bat):
  colaprint.pyw --instalar      atalhos + versão nos documentos
  colaprint.pyw --desinstalar   fecha o app, tira atalhos e início automático
  colaprint.pyw --versao        copia o número do VERSION para README e LEIA-ME

Este arquivo segue o Padrão Clésio Artes Miniapps v1.0:
  [PADRÃO]      partes iguais em todo miniapp (copiar sem mudar a lógica)
  [ESPECÍFICO]  partes só do ColaPrint (não copiar para outro app)
"""
import ctypes
import io
import os
import queue
import re
import sys
import threading
import time
import traceback
import winreg

import win32api
import win32clipboard
import win32con
import win32event
import win32gui
import winerror


# =====================================================================
# [ESPECÍFICO] Identidade e configurações do ColaPrint
# =====================================================================
NOME = "ColaPrint"
DESCRICAO = "ColaPrint: print rápido, colado onde você quiser"
ARQ_PRINCIPAL = "colaprint.pyw"
ARQ_ICONE_NOME = "colaprint.ico"
ARQ_LOG_NOME = "colaprint_erros.txt"

ATALHO = "f9"                # tecla que abre o menu de captura
ATALHO_SAIR = "ctrl+alt+f9"  # fecha o programa
ESCURECER = 0.45             # escurecimento da tela (0 = preto, 1 = nada)
TEMPO_MENU = 10              # segundos até o menu do F9 sumir sozinho
TEMPO_PARA_COLAR = 90        # segundos esperando o clique direito
COR = "#4da3ff"              # cor do app
FUNDO = "#1e1e1e"
BOTAO = "#2d2d2d"
TEXTO = "#f0f0f0"


# =====================================================================
# [PADRÃO] Caminhos, versão e log
# =====================================================================
PASTA = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(PASTA, ARQ_PRINCIPAL)
ARQ_ICONE = os.path.join(PASTA, ARQ_ICONE_NOME)
ARQ_LOG = os.path.join(PASTA, ARQ_LOG_NOME)
TAMANHO_MAX_LOG = 512_000    # bytes; acima disso o log recomeça
CHAVE_RUN = r"Software\Microsoft\Windows\CurrentVersion\Run"
DOCUMENTOS = ("README.md", "LEIA-ME.html")
MARCA_VERSAO = re.compile(r"(<!--versao-->)(.*?)(<!--/versao-->)")


def ler_versao():
    """A versão vem só do arquivo VERSION."""
    try:
        with open(os.path.join(PASTA, "VERSION"), encoding="utf-8") as f:
            return f.read().strip() or "?"
    except OSError:
        return "?"


VERSAO = ler_versao()


def registrar_erro(contexto=""):
    """Anota o erro no log do app, que nunca passa de TAMANHO_MAX_LOG."""
    try:
        if os.path.exists(ARQ_LOG) and os.path.getsize(ARQ_LOG) > TAMANHO_MAX_LOG:
            os.remove(ARQ_LOG)
        with open(ARQ_LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime(f"\n--- %d/%m/%Y %H:%M:%S · {NOME} {VERSAO}"))
            f.write(f" · {contexto} ---\n" if contexto else " ---\n")
            f.write(traceback.format_exc())
    except OSError:
        pass


def sincronizar_versao():
    """Copia o número do VERSION para README e LEIA-ME,
    entre as marcas <!--versao--> e <!--/versao-->."""
    for nome in DOCUMENTOS:
        caminho = os.path.join(PASTA, nome)
        try:
            with open(caminho, encoding="utf-8", newline="") as f:
                texto = f.read()
        except OSError:
            continue
        novo = MARCA_VERSAO.sub(lambda m: m.group(1) + VERSAO + m.group(3), texto)
        if novo != texto:
            with open(caminho, "w", encoding="utf-8", newline="") as f:
                f.write(novo)


# =====================================================================
# [PADRÃO] Instalar / desinstalar / iniciar com o Windows
# (só precisa de pywin32, então funciona mesmo sem as outras peças)
# =====================================================================
def caminhos_atalho():
    from win32com.client import Dispatch
    shell = Dispatch("WScript.Shell")
    menu = os.path.join(os.environ["APPDATA"],
                        r"Microsoft\Windows\Start Menu\Programs", f"{NOME}.lnk")
    mesa = os.path.join(shell.SpecialFolders("Desktop"), f"{NOME}.lnk")
    return shell, [menu, mesa]


def pythonw():
    return os.path.join(os.path.dirname(sys.executable), "pythonw.exe")


def inicia_com_windows():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, CHAVE_RUN) as k:
            winreg.QueryValueEx(k, NOME)
            return True
    except OSError:
        return False


def definir_inicio(ligar):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, CHAVE_RUN, 0,
                            winreg.KEY_SET_VALUE) as k:
            if ligar:
                winreg.SetValueEx(k, NOME, 0, winreg.REG_SZ,
                                  f'"{pythonw()}" "{SCRIPT}"')
            else:
                winreg.DeleteValue(k, NOME)
    except OSError:
        pass


def instalar():
    """Cria os atalhos com ícone e acerta a versão nos documentos."""
    if not os.path.exists(ARQ_ICONE):
        gerar_icone(ARQ_ICONE)
    shell, destinos = caminhos_atalho()
    for destino in destinos:
        a = shell.CreateShortCut(destino)
        a.TargetPath = pythonw()
        a.Arguments = f'"{SCRIPT}"'
        a.WorkingDirectory = PASTA
        a.IconLocation = ARQ_ICONE
        a.Description = DESCRICAO
        a.save()
    if inicia_com_windows():      # se já iniciava, aponta para esta pasta
        definir_inicio(True)
    sincronizar_versao()


def fechar_app_aberto():
    """Fecha só este app (nenhum outro programa Python)."""
    from win32com.client import GetObject
    eu = os.getpid()
    alvo = ARQ_PRINCIPAL.lower()
    consulta = ("SELECT ProcessId, CommandLine FROM Win32_Process "
                "WHERE Name='pythonw.exe' OR Name='python.exe'")
    for proc in GetObject("winmgmts:").ExecQuery(consulta):
        linha = (proc.CommandLine or "").lower()
        if (proc.ProcessId != eu and alvo in linha
                and "--instalar" not in linha and "--desinstalar" not in linha):
            try:
                proc.Terminate()
            except Exception:
                pass


def desinstalar():
    """Fecha o app e tira atalhos e início automático.
    Não mexe no Python, nas dependências nem nos arquivos da pasta."""
    fechar_app_aberto()
    _, destinos = caminhos_atalho()
    for destino in destinos:
        if os.path.exists(destino):
            os.remove(destino)
    definir_inicio(False)


def gerar_icone(caminho):
    """[ESPECÍFICO] Desenha o ícone do ColaPrint, caso o .ico falte na pasta."""
    from PIL import Image, ImageDraw
    S = 1024
    grad = Image.new("RGBA", (S, S))
    gd = ImageDraw.Draw(grad)
    topo, baixo = (92, 176, 255), (40, 104, 224)
    for y in range(S):
        t = y / (S - 1)
        gd.line((0, y, S, y), fill=tuple(
            int(topo[i] + (baixo[i] - topo[i]) * t) for i in range(3)) + (255,))
    mascara = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mascara).rounded_rectangle(
        (48, 48, S - 48, S - 48), radius=220, fill=255)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    img.paste(grad, (0, 0), mascara)
    d = ImageDraw.Draw(img)
    branco, w, L, a, b = (255, 255, 255, 255), 70, 190, 250, S - 250
    for x, y, dx, dy in ((a, a, 1, 1), (b, a, -1, 1), (a, b, 1, -1), (b, b, -1, -1)):
        d.rounded_rectangle((min(x, x + L * dx) - w // 2, y - w // 2,
                             max(x, x + L * dx) + w // 2, y + w // 2),
                            radius=w // 2, fill=branco)
        d.rounded_rectangle((x - w // 2, min(y, y + L * dy) - w // 2,
                             x + w // 2, max(y, y + L * dy) + w // 2),
                            radius=w // 2, fill=branco)
    c = S // 2
    d.rounded_rectangle((c - 40, c - 150, c + 40, c + 40), radius=40, fill=branco)
    d.polygon([(c - 130, c + 10), (c + 130, c + 10), (c, c + 150)], fill=branco)
    img.save(caminho, sizes=[(16, 16), (24, 24), (32, 32), (48, 48),
                             (64, 64), (128, 128), (256, 256)])


ACOES = {"--instalar": instalar, "--desinstalar": desinstalar,
         "--versao": sincronizar_versao}
if len(sys.argv) > 1 and sys.argv[1] in ACOES:
    try:
        ACOES[sys.argv[1]]()
    except Exception:
        registrar_erro(sys.argv[1])
        traceback.print_exc()     # aparece na janela do .bat
        sys.exit(1)
    sys.exit(0)


# =====================================================================
# [PADRÃO] Peças do app (só carregadas quando ele roda de verdade)
# =====================================================================
import tkinter as tk  # noqa: E402

import keyboard  # noqa: E402
import pystray  # noqa: E402
from pynput import mouse  # noqa: E402
from PIL import Image, ImageEnhance, ImageGrab, ImageTk  # noqa: E402

# Só uma cópia por vez
_trava = win32event.CreateMutex(None, False, f"{NOME}_unico")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    sys.exit(0)

# Pixels reais (alinhado mesmo com zoom de 125%/150% e vários monitores)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

comandos = queue.Queue()


def tela_virtual():
    """Área de todos os monitores juntos: x, y, largura, altura."""
    u = ctypes.windll.user32
    return (u.GetSystemMetrics(76), u.GetSystemMetrics(77),
            u.GetSystemMetrics(78), u.GetSystemMetrics(79))


def janela_flutuante():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    return root


def ao_clicar(acao):
    """Protege as opções do menu do ícone: erro vira log, não queda."""
    def executar(icon, item):
        try:
            acao()
        except Exception:
            registrar_erro("menu do ícone")
    return executar


def carregar_icone():
    try:
        return Image.open(ARQ_ICONE)
    except OSError:
        return Image.new("RGBA", (64, 64), COR)


# =====================================================================
# [ESPECÍFICO] O que o ColaPrint faz
# =====================================================================
config = {"colar": True}


def perguntar():
    """Menu discreto perto do mouse. Devolve 'tela', 'area' ou None."""
    mx, my = win32api.GetCursorPos()
    root = janela_flutuante()
    root.configure(bg=FUNDO)
    escolha = {"v": None}

    def escolher(v):
        escolha["v"] = v
        root.destroy()

    caixa = tk.Frame(root, bg=FUNDO, padx=6, pady=6)
    caixa.pack()
    for texto, valor in (("Tela inteira", "tela"), ("Selecionar área", "area")):
        tk.Button(caixa, text=texto, command=lambda v=valor: escolher(v),
                  bg=BOTAO, fg=TEXTO, activebackground=COR,
                  activeforeground="white", relief="flat", borderwidth=0,
                  padx=18, pady=8, font=("Segoe UI", 10),
                  cursor="hand2").pack(fill="x", pady=2)

    root.update_idletasks()
    vx, vy, vw, vh = tela_virtual()
    w, h = root.winfo_width(), root.winfo_height()
    root.geometry(f"+{min(mx + 12, vx + vw - w - 4)}+{min(my + 12, vy + vh - h - 4)}")

    def vigiar():
        """Esc ou clique fora dos botões cancela."""
        if keyboard.is_pressed("esc"):
            root.destroy()
            return
        if (win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000 or
                win32api.GetAsyncKeyState(win32con.VK_RBUTTON) & 0x8000):
            cx, cy = win32api.GetCursorPos()
            x1, y1 = root.winfo_rootx(), root.winfo_rooty()
            if not (x1 <= cx < x1 + root.winfo_width() and
                    y1 <= cy < y1 + root.winfo_height()):
                root.destroy()
                return
        root.after(30, vigiar)

    root.after(30, vigiar)
    root.after(TEMPO_MENU * 1000, root.destroy)
    root.focus_force()
    root.mainloop()
    return escolha["v"]


def capturar_tela_inteira():
    """Print do monitor onde o mouse está."""
    monitor = win32api.MonitorFromPoint(win32api.GetCursorPos(), 2)  # 2 = mais próximo
    return ImageGrab.grab(bbox=win32api.GetMonitorInfo(monitor)["Monitor"],
                          all_screens=True)


def selecionar_area():
    """Congela a tela, escurece e deixa selecionar. Devolve o recorte ou None."""
    x0, y0, w, h = tela_virtual()
    foto = ImageGrab.grab(all_screens=True)
    escura = ImageEnhance.Brightness(foto).enhance(ESCURECER)

    root = janela_flutuante()
    root.geometry(f"{w}x{h}+{x0}+{y0}")
    canvas = tk.Canvas(root, width=w, height=h, highlightthickness=0,
                       cursor="crosshair")
    canvas.pack()
    fundo = ImageTk.PhotoImage(escura, master=root)
    canvas.create_image(0, 0, anchor="nw", image=fundo)

    estado = {"ini": None, "ret": None, "resultado": None}

    def apertou(e):
        estado["ini"] = (e.x, e.y)
        estado["ret"] = canvas.create_rectangle(
            e.x, e.y, e.x, e.y, outline=COR, width=2)

    def arrastou(e):
        if estado["ret"]:
            x, y = estado["ini"]
            canvas.coords(estado["ret"], x, y, e.x, e.y)

    def soltou(e):
        if not estado["ini"]:
            return
        x, y = estado["ini"]
        l, t, r, b = min(x, e.x), min(y, e.y), max(x, e.x), max(y, e.y)
        if r - l > 5 and b - t > 5:
            estado["resultado"] = foto.crop((l, t, r, b))
        root.destroy()

    def checar_esc():
        if keyboard.is_pressed("esc"):
            root.destroy()
        else:
            root.after(40, checar_esc)

    canvas.bind("<ButtonPress-1>", apertou)
    canvas.bind("<B1-Motion>", arrastou)
    canvas.bind("<ButtonRelease-1>", soltou)
    canvas.bind("<ButtonPress-3>", lambda e: root.destroy())
    root.after(40, checar_esc)
    root.focus_force()
    root.mainloop()
    return estado["resultado"]


def copiar(imagem):
    """Coloca a imagem na área de transferência (igual Ctrl+C)."""
    buf = io.BytesIO()
    imagem.convert("RGB").save(buf, "BMP")
    dados = buf.getvalue()[14:]   # sem o cabeçalho do BMP
    for tentativa in range(10):   # outro programa pode estar usando
        try:
            win32clipboard.OpenClipboard()
            break
        except Exception:
            if tentativa == 9:
                raise
            time.sleep(0.05)
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, dados)
    finally:
        win32clipboard.CloseClipboard()


def esperar_clique_e_colar():
    """Clique esquerdo fica livre; o clique DIREITO cola ali
    (sem abrir o menu do botão direito)."""
    estado = {"colar": False, "ini": time.time()}

    def filtro(msg, data):
        if msg in (0x0204, 0x0205):      # botão direito: aperta / solta
            if msg == 0x0205:
                estado["colar"] = True
            ouvinte.suppress_event()    # engole o clique direito

    ouvinte = mouse.Listener(win32_event_filter=filtro)
    ouvinte.start()
    try:
        root = janela_flutuante()
        root.attributes("-alpha", 0.92)
        tk.Label(root, text="Clique direito onde quer colar   ·   Esc = só copiar",
                 bg=FUNDO, fg=TEXTO, font=("Segoe UI", 9),
                 padx=10, pady=5).pack()
        root.update_idletasks()

        # etiqueta não recebe clique nem rouba o foco
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        estilo = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(
            hwnd, win32con.GWL_EXSTYLE,
            estilo | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOOLWINDOW
            | 0x08000000)  # WS_EX_NOACTIVATE

        def seguir():
            x, y = win32api.GetCursorPos()
            root.geometry(f"+{x + 18}+{y + 20}")
            if (estado["colar"] or keyboard.is_pressed("esc") or
                    time.time() - estado["ini"] > TEMPO_PARA_COLAR):
                root.destroy()
                return
            root.after(30, seguir)

        root.after(30, seguir)
        root.mainloop()
    finally:
        ouvinte.stop()

    if estado["colar"]:
        time.sleep(0.2)
        keyboard.send("ctrl+v")


def executar(cmd):
    """Um ciclo completo: menu, captura, copiar, colar."""
    if cmd == "perguntar":
        time.sleep(0.15)          # espera soltar a tecla
        cmd = perguntar()
        if not cmd:
            return
    time.sleep(0.3)               # espera o menu sumir antes do print
    imagem = capturar_tela_inteira() if cmd == "tela" else selecionar_area()
    if imagem is None:
        return
    copiar(imagem)
    if config["colar"]:
        esperar_clique_e_colar()


def alternar_colar():
    config["colar"] = not config["colar"]


MENU = pystray.Menu(
    pystray.MenuItem("Tirar print (F9)",
                     ao_clicar(lambda: comandos.put("perguntar")), default=True),
    pystray.MenuItem("Tela inteira", ao_clicar(lambda: comandos.put("tela"))),
    pystray.MenuItem("Selecionar área", ao_clicar(lambda: comandos.put("area"))),
    pystray.Menu.SEPARATOR,
    pystray.MenuItem("Colar com clique direito", ao_clicar(alternar_colar),
                     checked=lambda it: config["colar"]),
    # [PADRÃO] as duas opções abaixo existem em todo miniapp
    pystray.MenuItem("Iniciar com o Windows",
                     ao_clicar(lambda: definir_inicio(not inicia_com_windows())),
                     checked=lambda it: inicia_com_windows()),
    pystray.Menu.SEPARATOR,
    pystray.MenuItem("Sair", ao_clicar(lambda: comandos.put("sair"))),
)


# =====================================================================
# [PADRÃO] Laço principal: ícone, atalhos, fila de comandos, saída limpa
# =====================================================================
def main():
    if inicia_com_windows():      # se a pasta mudou, o início acompanha
        definir_inicio(True)

    icone = pystray.Icon(NOME, carregar_icone(), f"{NOME} {VERSAO} · F9", MENU)
    threading.Thread(target=icone.run, daemon=True).start()

    keyboard.add_hotkey(ATALHO, lambda: comandos.put("perguntar"), suppress=True)
    keyboard.add_hotkey(ATALHO_SAIR, lambda: comandos.put("sair"))

    try:
        while True:
            cmd = comandos.get()
            if cmd == "sair":
                break
            try:
                executar(cmd)
            except Exception:
                registrar_erro(cmd)
    finally:
        keyboard.unhook_all()
        icone.stop()
        win32api.CloseHandle(_trava)


if __name__ == "__main__":
    main()
