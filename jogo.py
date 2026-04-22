# Mini RPG em Python com POO - Inspirado em Undertale
# Vinícius Alves Machado de Araújo - RA: 824127157

import random
import time
import sys
import os
import threading

# ─────────────────────────────────────────────
#  MÚSICA DE FUNDO
# ─────────────────────────────────────────────
ARQUIVO_MUSICA = "tema.mp3"

def iniciar_musica():
    """Toca a música em loop usando pygame, se disponível."""
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(ARQUIVO_MUSICA)
        pygame.mixer.music.play(-1)  # -1 = loop infinito
    except FileNotFoundError:
        pass  
    except Exception:
        pass  

def parar_musica():
    try:
        import pygame
        pygame.mixer.music.stop()
    except Exception:
        pass


# ─────────────────────────────────────────────
#  CORES ANSI
# ─────────────────────────────────────────────
class C:
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    DIM      = "\033[2m"
    BRANCO   = "\033[97m"
    CINZA    = "\033[97m" #teste 90 cinz
    AMARELO  = "\033[93m"
    CIANO    = "\033[96m"
    VERDE    = "\033[92m"
    VERMELHO = "\033[91m"
    MAGENTA  = "\033[95m"
    AZUL     = "\033[94m"
    LARANJA  = "\033[33m"

def ativar_cores_windows():
    if sys.platform == "win32":
        try:
            import ctypes
            kernel = ctypes.windll.kernel32
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
        except Exception:
            pass

ativar_cores_windows()


# ─────────────────────────────────────────────
#  UTILITÁRIOS VISUAIS
# ─────────────────────────────────────────────
LARGURA = 60

def limpar():
    os.system("cls" if sys.platform == "win32" else "clear")

def linha(char="═", cor=C.CINZA):
    print(cor + (char * LARGURA) + C.RESET)

def separador(cor=C.CINZA):
    """Linha simples sem laterais, para menus."""
    print(cor + ("─" * LARGURA) + C.RESET)

def digitar(texto, delay=0.028, cor="", som=False):
    """Efeito typewriter sem centralização."""
    print(cor, end="", flush=True)
    for ch in texto:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print(C.RESET)

def pausa(msg="  Pressione ENTER para continuar...", cor=C.CINZA):
    print()
    print(cor + msg + C.RESET)
    input()

def barra_hp(hp_atual, hp_max, tamanho=18):
    hp_atual = max(0, hp_atual)
    pct = hp_atual / hp_max
    preenchido = int(pct * tamanho)
    cor = C.AMARELO
    barra = cor + "█" * preenchido + C.DIM + "░" * (tamanho - preenchido) + C.RESET
    return f"[{barra}{C.RESET}] {C.AMARELO}{C.BOLD}{hp_atual}/{hp_max}{C.RESET}"

def menu_opcoes(opcoes):
    print()
    separador()
    for op in opcoes:
        print(op)
    separador()
    print()


# ─────────────────────────────────────────────
#  ALMAS
# ─────────────────────────────────────────────
ALMAS = {
    "1": {"nome": "Determinação", "emoji": "* ",  "cor": C.VERMELHO,  "vida": 100, "forca": 12, "defesa": 2},
    "2": {"nome": "Integridade",  "emoji": "* ",  "cor": C.AZUL,      "vida":  90, "forca": 11, "defesa": 4},
    "3": {"nome": "Bravura",      "emoji": "* ",  "cor": C.LARANJA,   "vida":  80, "forca": 16, "defesa": 1},
    "4": {"nome": "Perseverança", "emoji": "* ",  "cor": C.MAGENTA,   "vida": 130, "forca":  9, "defesa": 5},
    "5": {"nome": "Bondade",      "emoji": "* ",  "cor": C.VERDE,     "vida":  95, "forca": 10, "defesa": 3},
    "6": {"nome": "Justiça",      "emoji": "* ",  "cor": C.AMARELO,   "vida":  80, "forca": 15, "defesa": 2},
    "7": {"nome": "Paciência",    "emoji": "* ",  "cor": C.CIANO,     "vida": 110, "forca":  8, "defesa": 6},
}

def exibir_almas():
    print()
    print(C.AMARELO + C.BOLD + "  ✦  ESCOLHA SUA ALMA  ✦" + C.RESET)
    separador(C.AMARELO)
    for k, v in ALMAS.items():
        print(
            f"  {C.BOLD}[{k}]{C.RESET}  {v['cor']}{v['nome']:14s}{C.RESET}"
            f"  HP:{C.AMARELO}{v['vida']:3d}{C.RESET}"
            f"  Forca:{C.VERMELHO}{v['forca']:2d}{C.RESET}"
            f"  Defesa:{C.AZUL}{v['defesa']}{C.RESET}"
        )
    separador(C.AMARELO)
    print()


# ─────────────────────────────────────────────
#  ARMAS
# ─────────────────────────────────────────────
ARMAS = {
    "1": {"nome": "Varinha de Manteiga", "emoji": "~", "bonus": 5,  "crit": 0.40, "desc": "+5 dano  40% critico"},
    "2": {"nome": "Faca de Chef",        "emoji": "/", "bonus": 8,  "crit": 0.20, "desc": "+8 dano  20% critico"},
    "3": {"nome": "Osso Magico",         "emoji": "-", "bonus": 6,  "crit": 0.30, "desc": "+6 dano  30% critico"},
    "4": {"nome": "Frigideira de Ouro",  "emoji": "O", "bonus": 10, "crit": 0.10, "desc": "+10 dano 10% critico"},
    "5": {"nome": "Espada de Papelao",   "emoji": "|", "bonus": 3,  "crit": 0.60, "desc": "+3 dano  60% critico"},
}

def exibir_armas():
    print()
    print(C.CIANO + C.BOLD + "  ⚔  ESCOLHA SUA ARMA  ⚔" + C.RESET)
    separador(C.CIANO)
    for k, v in ARMAS.items():
        print(
            f"  {C.BOLD}[{k}]{C.RESET}  {C.BRANCO}{v['nome']:22s}{C.RESET}"
            f"  {C.CINZA}{v['desc']}{C.RESET}"
        )
    separador(C.CIANO)
    print()


# ─────────────────────────────────────────────
#  CLASSE ARMA
# ─────────────────────────────────────────────
class Arma:
    def __init__(self, dados):
        self.nome        = dados["nome"]
        self.emoji       = dados["emoji"]
        self.bonus_dano  = dados["bonus"]
        self.chance_crit = dados["crit"]

    def calcular_dano(self, forca):
        dano = forca + self.bonus_dano
        critico = random.random() < self.chance_crit
        if critico:
            dano = int(dano * 2.2)
        return dano, critico


# ─────────────────────────────────────────────
#  CLASSE PERSONAGEM
# ─────────────────────────────────────────────
class Personagem:
    def __init__(self, nome, alma, arma):
        self.nome     = nome
        self.alma     = alma["nome"]
        self.emoji    = alma["emoji"]
        self.cor      = alma["cor"]
        self.vida     = alma["vida"]
        self.vida_max = alma["vida"]
        self.forca    = alma["forca"]
        self.defesa   = alma["defesa"]
        self.arma     = arma
        self.itens    = 5
        self.nivel    = 1
        self.xp       = 0
        self.xp_prox  = 15   

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        subiu = False
        while self.xp >= self.xp_prox:
            self.xp      -= self.xp_prox
            self.nivel   += 1
            self.xp_prox  = int(self.xp_prox * 1.5)
            ganho_hp      = 15
            ganho_forca   = 2
            ganho_defesa  = 1
            self.vida_max += ganho_hp
            self.vida      = min(self.vida + ganho_hp, self.vida_max)
            self.forca    += ganho_forca
            self.defesa   += ganho_defesa
            subiu = True
            print()
            digitar(f"  ★ LEVEL UP! Agora voce e nivel {self.nivel}!", cor=C.AMARELO + C.BOLD)
            digitar(f"  + {ganho_hp} HP maximo  + {ganho_forca} Forca  + {ganho_defesa} Defesa", cor=C.VERDE)
            print(f"  HP: {barra_hp(self.vida, self.vida_max)}")
            time.sleep(0.5)
        return subiu

    def atacar(self, alvo):
        dano, critico = self.arma.calcular_dano(self.forca)
        if critico:
            digitar(f"  ✦ GOLPE CRITICO com {self.arma.nome}!", cor=C.AMARELO + C.BOLD)
            digitar(f"  {alvo.nome} recebeu {dano} de dano!", cor=C.AMARELO)
        else:
            digitar(f"  {self.nome} atacou com {self.arma.nome}.")
            digitar(f"  {alvo.nome} recebeu {dano} de dano.", cor=C.CINZA)
        alvo.receber_dano(dano)

    def receber_dano(self, dano_bruto):
        dano = max(1, dano_bruto - self.defesa)
        self.vida -= dano
        print()
        print(f"  {self.cor}{self.nome}{C.RESET}  HP: {barra_hp(self.vida, self.vida_max)}")

    def curar(self, valor=25):
        self.vida = min(self.vida + valor, self.vida_max)
        digitar(f"  ✨ {self.nome} usou um Biscoito Dourado e recuperou {valor} HP!", cor=C.VERDE)
        print(f"  HP atual: {barra_hp(self.vida, self.vida_max)}")
        self.itens -= 1

    def esta_vivo(self):
        return self.vida > 0


# ─────────────────────────────────────────────
#  CLASSE INIMIGO
# ─────────────────────────────────────────────
class Inimigo:
    def __init__(self, cfg):
        self.nome             = cfg["nome"]
        self.vida             = cfg["vida"]
        self.vida_max         = cfg["vida"]
        self.forca            = cfg["forca"]
        self.bonus_dano       = cfg["bonus_dano"]
        self.chance_crit      = cfg["chance_crit"]
        self.defesa           = cfg.get("defesa", 0)
        self.manso            = False
        self.atos             = 0
        self.atos_necessarios = cfg["atos_necessarios"]
        self.frases_ato       = cfg["frases_ato"]
        self.frase_manso      = cfg["frase_manso"]
        self.frase_derrota    = cfg["frase_derrota"]
        self.habilidade_especial = cfg.get("habilidade_especial", None)
        self.cor_ascii        = cfg.get("cor_ascii", C.BRANCO)
        self.xp               = cfg.get("xp", 20)
        self._turno           = 0

    def atacar(self, alvo):
        self._turno += 1
        if self.habilidade_especial and self._turno % 3 == 0:
            self.habilidade_especial(alvo)
            return
        dano_base = self.forca + self.bonus_dano
        critico   = random.random() < self.chance_crit
        dano      = int(dano_base * 2) if critico else dano_base
        if critico:
            digitar(f"  ⚠ {self.nome} desferiu um golpe critico!", cor=C.VERMELHO + C.BOLD)
        else:
            digitar(f"  {self.nome} atacou causando {dano} de dano!", cor=C.CINZA)
        alvo.receber_dano(dano)

    def receber_dano(self, dano_bruto):
        dano = max(1, dano_bruto - self.defesa)
        self.vida -= dano
        print()
        print(f"  {C.BRANCO}{self.nome}{C.RESET}  HP: {barra_hp(self.vida, self.vida_max)}")

    def reagir_ao_ato(self):
        self.atos += 1
        idx = min(self.atos - 1, len(self.frases_ato) - 1)
        digitar(f'  {self.nome}: "{self.frases_ato[idx]}"', cor=C.CIANO, delay=0.035)
        if self.atos >= self.atos_necessarios:
            self.manso = True
            print()
            digitar(f"  * {self.nome} parece ter se acalmado...", cor=C.VERDE)

    def esta_vivo(self):
        return self.vida > 0


# ─────────────────────────────────────────────
#  ASCII ART DOS INIMIGOS
# ─────────────────────────────────────────────
def ascii_flowey():
    print(r"""
            ⣠⠖⠺⣍⣉⣓⣲⣚⣉⣉⡗⠲⣄
        ⢀⣠⠤⢷⣤⣶⠟⠋⢉⠉⠉⠛⠛⣷⣤⡾⠤⣄⡀
        ⡏⠀⠶⢶⣿⠁⠀⠀⣿⢀⣀⡀⠀⠈⣿⡶⠶⠀⢹
        ⠉⢷⣀⣈⣻⣆⠈⢲⠻⢲⠒⠒⠁⣰⣿⡤⠤⠾⠉
        ⠀⠀⢰⠋⢉⠿⣧⣌⣉⣁⣀⣀⣴⡿⡉⠙⢦⠀⠀
        ⠀⠀⢸⡀⠃⠀⣀⣉⡭⠽⢭⣉⣀⠀⠘⢀⣸⠀⠀
        ⠀⠀⠀⠉⠉⠉⠁⢰⠋⢹⠀⠀⠈⠉⠉⠉⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠸⣆⡈⣧⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⡖⣦⠞⠁⠈⣷⢲⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠙⢮⣓⣒⣚⡵⠋⠀⠀⠀⠀⠀⠀
        """)

def ascii_toriel():
    print(r"""
              ⢰⢱⠤⠤⠾⢱⠀
        ⠀⠀⠀⠀⠀⡔⢡⢵⢆⢐⢾⠁⢱⠀
        ⠀⠀⠀⠀⠀⡇⠸⡈⢁⢀⠉⡆⠀⡇⠀
        ⠀⠀⠀⢀⠔⣧⠀⣷⣔⣒⣼⡁⣸⡢⢄
        ⠀⠀⢠⠃⢸⣿⡿⢯⣿⣿⡿⠿⡟⣷⠀⢇
        ⠀⠀⡞⠀⣾⢫⣿⣦⣵⣼⣴⣾⣳⣿⠀⢸
        ⠀⡰⠁⠀⣿⣸⣟⣿⣾⢿⣾⣿⣿⣿⡆⠀⢣
        ⢰⠃⠀⢠⡿⣿⣿⣿⣟⣻⣵⣿⣿⣼⡇⠀⠀⢇
        ⡸⠳⡀⢸⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⡐⢱
        ⢧⣰⠧⢼⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⠔⢵⡠
        ⠀⠀⠀⣧⣿⣿⣿⣿⣿⣿⣿⣿⡟⡄
        ⠀⠀⠀⠀⣈⡲⠿⠿⢗⢺⠿⠿⢶⣉
        ⠀⠀⠀⢎⣄⣄⣤⠤⠜⠑⠤⢤⣀⣀⣱
        """)

def ascii_papyrus():
    print(r"""
              ⣠⡂⠒⠂⠠⡀
        ⠀⠀⠀⠀⠀⡇⣸⠂⢲⡀⠸⠀
        ⠀⠀⠀⠀⠀⠻⣀⣓⣀⣼⠁
        ⠀⠀⠀⢐⢰⡢⣽⢴⣶⢿⣶⡿⠓⣢⣀⠀⣀⡀
        ⠀⠔⢨⠞⢆⠙⠫⡿⠷⢚⠞⠀⠀⠘⠃⠒⠁⠛
        ⠘⡄⠘⡄⠈⢻⡖⠔⢮⠀⠈⣦⠤⡜
        ⢠⡿⠉⠉⠂⠄⡀⠀⡫⠠⠊⢹⡟
        ⠙⠻⠿⠟⠛⣑⣷⡖⠁⠀⠀⢸⡇
        ⠀⠀⠳⡹⠎⣜⠸⠇⠀⡀⠀⢸⡇
        ⠀⠀⠀⠈⢹⣷⠄⢉⣴⠁⠀⢸⠃⡤⠤⠂⢂⠅
        ⠀⠀⠀⠀⣸⣇⣀⠀⢻⣧⡀⠀⠪⠄⠐⠂
        ⠀⠀⠀⠛⢻⡿⢻⢣⣾⢟⣉⠆
        ⠀⠀⠀⢈⣊⠭⠘⡄⠑⢀⠚⡸⣀⣀
        ⠀⠀⢎⣀⣀⡀⠤⠄⠀⠘⠄⢀⣀⣀⡨
        """)

def ascii_sans():
    print(r"""
              ⣠⠖⠀⠉⠉⠉⠉⠀
        ⠀⠀⠀⢠⠁⣀⣀⣀⠀⠀⣀⣀⣀⠈⡄
        ⠀⠀⠀⠘⡜⠿⣯⡟⢠⡄⢻⣽⡿⢣⠃
        ⠀⠀⠀⣀⣎⠤⡨⣀⣙⣋⣀⣩⡦⢰⣀⡀
        ⠀⠀⢼⣍⣙⠤⣉⠚⠘⠀⠓⣋⣴⢊⣴⡯⡀
        ⢠⣾⣾⡏⣿⣿⢨⢱⠤⢤⣯⢩⣶⣿⢹⣿⣮⢄
        ⢎⣿⣿⣧⣽⣿⣗⣺⠀⠈⢰⢸⣭⣷⣸⣿⣿⣾
        ⠀⠳⢿⠿⢿⣿⡇⠿⣤⣴⡀⠿⠿⠿⢻⢿⠯⠊
        ⠀⠀⠀⠁⣶⢒⣾⣿⣿⣿⣿⡏⣿⣯⠂
        ⠀⠀⠀⣤⡗⣼⣿⣿⢿⡜⣿⡇⣿⣿⣶
        ⠀⠀⠀⣫⡥⣿⣿⣿⠟⠣⣿⣧⣽⡯⢝⡀
        ⠀⠀⢎⣀⣉⣢⡄⠀⠀⠀⢨⣤⣴⣊⣁⣉⠢""")

def ascii_asgore():
    print(r"""
    ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠗⣪⣵⣶⠞⣃⣄⡻⠇⣿⣿⣿⣿⣿⣶⣿⡇⣿⣿ 
⢸⣿⣿⣿⣿⣿⣿⣿⣿⡿⢡⣾⣿⣿⠁⠚⠧⠿⠛⠜⢸⣿⣿⣿⣿⡏⣿⡇⣿⣿
 ⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡿⣛⣋⢅⣤⣷⡯⣥⣒⠎⣙⡛⠿⠿⠿⢋⡇⣿⣿
 ⢨⣭⣭⣭⣭⣭⣭⣭⣭⢡⣴⣾⠏⣴⣯⣍⠻⣿⣮⠻⢷⣌⢻⣧⢰⣶⡟⡅⣿⣿ 
⢸⣿⣿⣿⣿⣿⣿⡿⣥⣾⣿⠇⣾⢿⣧⣤⣤⣌⡟⢳⠿⠛⠀⣿⠸⢋⣼⣧⣛⣻ 
⢈⣉⣉⣉⣉⣉⢉⠁⣿⣿⠏⣾⢟⣨⣛⠻⣛⣻⡻⣿⣶⣮⢐⢡⣾⡈⣿⣿⣿⣿ 
⢀⣠⣤⣶⣶⡶⢒⠀⠿⡿⢸⡏⠼⢢⡩⣅⠈⢹⣿⢿⡛⢗⢸⢘⣟⣣⣛⣛⣛⣛ 
⢸⣿⣿⣿⡿⣣⣿⢿⡷⣭⠘⡀⠐⣻⣷⠪⣛⠦⣤⣤⣬⡤⢠⡈⢼⣇⣿⣿⣿⣿ 
⢸⣿⣿⡟⣰⣿⣿⣦⡛⢷⣾⣿⠡⣿⣿⣿⣶⣿⣷⣶⠶⣶⣆⢩⢸⣿⣿⣿⣿⣿ 
⢸⣿⣿⢱⣿⣿⣿⣿⣿⡦⠙⣿⣟⠹⣿⣿⣿⣿⣯⣷⣿⣿⢣⣿⡇⢿⣿⣿⣿⣿ 
⢸⣿⡏⣿⣿⣿⣿⣿⠟⣵⣷⠹⣿⣷⣤⣉⣥⣛⠘⣋⠛⢣⣿⣿⡇⣠⡹⣿⣿⣿ 
⢸⣿⣧⠻⣿⣿⡿⢋⣾⣿⣿⣧⠹⠿⡿⠿⢿⣿⠿⢋⣔⣻⠿⣫⣾⣿⣿⡌⢿⣿""")

_ASCII_FUNCS = {
    "Flowey":  ascii_flowey,
    "Toriel":  ascii_toriel,
    "Papyrus": ascii_papyrus,
    "Sans":    ascii_sans,
    "Asgore":  ascii_asgore,
}

def mostrar_ascii(nome):
    fn = _ASCII_FUNCS.get(nome)
    if fn:
        fn()


# ─────────────────────────────────────────────
#  HABILIDADES ESPECIAIS DOS INIMIGOS
# ─────────────────────────────────────────────
def habilidade_flowey(alvo):
    hits = random.randint(3, 5)
    dano_total = 0
    digitar(f"  Flowey dispara PETALAS EM LEQUE! ({hits} acertos)", cor=C.AMARELO)
    for _ in range(hits):
        d = random.randint(3, 7)
        dano_total += d
    alvo.receber_dano(dano_total)
    digitar(f"  Total: {dano_total} de dano!", cor=C.CINZA)

def habilidade_toriel(alvo):
    dano = 18
    digitar(f"  Toriel invoca MAGIA DE FOGO! {dano} de dano!", cor=C.LARANJA)
    alvo.receber_dano(dano)

def habilidade_papyrus(alvo):
    dano = 15
    digitar(f"  NYEH! Papyrus lanca CHUVA DE OSSOS! {dano} de dano!", cor=C.BRANCO)
    alvo.receber_dano(dano)

def habilidade_sans(alvo):
    if random.random() < 0.35:
        digitar("  Sans mirou... mas voce conseguiu desviar!", cor=C.VERDE)
    else:
        dano = 30
        digitar(f"  GASTER BLASTER! {dano} de dano!", cor=C.VERMELHO + C.BOLD)
        alvo.receber_dano(dano)

def habilidade_asgore(alvo):
    dano = 22
    digitar(f"  Asgore ergue o TRIDENTE REAL! {dano} de dano!", cor=C.AMARELO + C.BOLD)
    alvo.receber_dano(dano)


# ─────────────────────────────────────────────
#  CONFIGURAÇÃO DOS INIMIGOS
# ─────────────────────────────────────────────
INIMIGOS_CFG = [
    {
        "nome": "Flowey", "vida": 70, "forca": 6, "bonus_dano": 3, "chance_crit": 0.05, "defesa": 0,
        "xp": 20,
        "atos_necessarios": 2,
        "habilidade_especial": habilidade_flowey,
        "frases_ato": [
            "Heh. Voce realmente acha que pode me ajudar?",
            "...Tudo bem. Eu me lembro de voce.",
        ],
        "frase_manso":   "Tudo bem. So desta vez... desapareco.",
        "frase_derrota": "Isso... nao foi o esperado. Ate logo, idiota!",
        "intro": [
            "  * O Underground parece silencioso demais.",
            "  * Uma flor amarela surge do chao. Ela sorri.",
            "  * Algo nesse sorriso nao parece certo...",
        ],
        "cor_ascii": C.BRANCO,
    },
    {
        "nome": "Toriel", "vida": 110, "forca": 8, "bonus_dano": 5, "chance_crit": 0.10, "defesa": 2,
        "xp": 30,
        "atos_necessarios": 3,
        "habilidade_especial": habilidade_toriel,
        "frases_ato": [
            "Minha crianca... por favor, desista de sair.",
            "Eu nao quero te machucar. So quero te proteger.",
            "...Voce realmente quer partir, nao e?",
        ],
        "frase_manso":   "Esta bem. Vou te deixar ir. Mas tome cuidado la fora.",
        "frase_derrota": "Eu... entendo. Boa sorte, minha crianca.",
        "intro": [
            "  * Uma figura imponente bloqueia o caminho.",
            "  * E uma cabra enorme, de olhos gentis e maos quentes.",
            "  * Ela diz que quer te proteger. Mas a que custo?",
        ],
        "cor_ascii": C.BRANCO,
    },
    {
        "nome": "Papyrus", "vida": 130, "forca": 10, "bonus_dano": 7, "chance_crit": 0.10, "defesa": 1,
        "xp": 40,
        "atos_necessarios": 3,
        "habilidade_especial": habilidade_papyrus,
        "frases_ato": [
            "NYEH HEH HEH! O Grande Papyrus vai te capturar!",
            "Hmm... voce e persistente. Talvez nao seja tao ruim assim.",
            "D-desculpe! Eu so queria amigos. Voce pode ser meu amigo?",
        ],
        "frase_manso":   "NYEH... esta bem! Voce passou no teste do Grande Papyrus!",
        "frase_derrota": "NYEH HEH... eu perdi... mas ainda sou o Grande Papyrus!",
        "intro": [
            "  * Uma armadura branca surge da neve.",
            "  * Ele grita o proprio nome com muito orgulho.",
            "  * Debaixo de toda aquela arrogancia... parece so querer um amigo.",
        ],
        "cor_ascii": C.BRANCO,
    },
    {
        "nome": "Sans", "vida": 160, "forca": 12, "bonus_dano": 10, "chance_crit": 0.20, "defesa": 0,
        "xp": 55,
        "atos_necessarios": 4,
        "habilidade_especial": habilidade_sans,
        "frases_ato": [
            "heh. voce realmente veio ate aqui.",
            "...olha. eu odeio lutar. mas uma promessa e uma promessa.",
            "...por que voce continua tentando?",
            "...heh. tudo bem. voce e do tipo que nao desiste.",
        ],
        "frase_manso":   "...tudo bem. voce passou. cuide bem deles, ta bom?",
        "frase_derrota": "heh... parece que voce ganhou. cuide bem deles.",
        "intro": [
            "  * A temperatura cai de repente.",
            "  * Um esqueleto de jaleco azul bloqueia a ponte.",
            "  * Ele nao parece com raiva. Parece... cansado.",
            "  * 'eu prometi que cuidaria deles. desculpe.'",
        ],
        "cor_ascii": C.BRANCO,
    },
    {
        "nome": "Asgore", "vida": 200, "forca": 15, "bonus_dano": 12, "chance_crit": 0.15, "defesa": 4,
        "xp": 70,
        "atos_necessarios": 5,
        "habilidade_especial": habilidade_asgore,
        "frases_ato": [
            "...Desculpe. Eu devo fazer isso.",
            "Eu nao quero lutar. Mas... nao tenho escolha.",
            "Voce poderia... simplesmente ir embora?",
            "...Voce lembra meus filhos.",
            "...Por favor. Nao me force a continuar.",
        ],
        "frase_manso":   "...Obrigado. Eu estava... cansado disso tudo.",
        "frase_derrota": "...Esta bem. Voce merece sair daqui.",
        "intro": [
            "  * Voce chega ao trono do Underground.",
            "  * Um monstro imenso se levanta lentamente.",
            "  * A coroa pesa. Os olhos, cheios de culpa.",
            "  * 'Eu me arrependo de tudo.' — ele sussurra.",
            "  * Mas ele avanca mesmo assim.",
        ],
        "cor_ascii": C.BRANCO,
    },
]


# ─────────────────────────────────────────────
#  LOOP DE COMBATE
# ─────────────────────────────────────────────
def combate(jogador, inimigo):
    linha()
    digitar(f"  * {C.BOLD}{inimigo.nome}{C.RESET} apareceu!", cor=C.BRANCO)
    time.sleep(0.5)

    while jogador.esta_vivo() and inimigo.esta_vivo():
        linha()
        mostrar_ascii(inimigo.nome)

        # Status
        print(f"  {jogador.cor}{jogador.nome}{C.RESET}  HP: {barra_hp(jogador.vida, jogador.vida_max)}  {C.AMARELO}LV {jogador.nivel}{C.RESET}  {C.CINZA}XP: {jogador.xp}/{jogador.xp_prox}{C.RESET}")
        print(f"  {C.BRANCO}{inimigo.nome}{C.RESET}   HP: {barra_hp(inimigo.vida, inimigo.vida_max)}")
        print(f"  {C.CINZA}Itens: {jogador.itens}  Arma: {jogador.arma.nome}{C.RESET}")

        if inimigo.manso:
            print()
            print(f"  {C.VERDE}[{inimigo.nome} esta manso... use MERCY!]{C.RESET}")

        menu_opcoes([
            f"  {C.VERMELHO}[1] FIGHT{C.RESET}    Atacar o inimigo",
            f"  {C.AZUL}[2] ACT{C.RESET}      Interagir com o inimigo",
            f"  {C.VERDE}[3] ITEM{C.RESET}     Usar Biscoito Dourado ({jogador.itens} restantes)",
            f"  {C.AMARELO}[4] MERCY{C.RESET}    Poupar o inimigo"
            + (f"  {C.VERDE}<<< DISPONIVEL{C.RESET}" if inimigo.manso else ""),
        ])

        try:
            acao = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        esquivou = False

        if acao == "1":
            print()
            jogador.atacar(inimigo)
            if not inimigo.esta_vivo():
                print()
                digitar(f'  {inimigo.nome}: "{inimigo.frase_derrota}"', cor=C.CIANO, delay=0.04)
                time.sleep(0.5)
                digitar(f"  + {inimigo.xp} XP", cor=C.AMARELO)
                jogador.ganhar_xp(inimigo.xp)
                time.sleep(0.5)
                return "venceu"

        elif acao == "2":
            print()
            digitar(f"  * Voce tenta interagir com {inimigo.nome}...", delay=0.03)
            time.sleep(0.4)
            inimigo.reagir_ao_ato()
            esquivou = random.random() < 0.45

        elif acao == "3":
            if jogador.itens > 0:
                print()
                jogador.curar(25)
            else:
                digitar("  * Voce nao tem mais itens!", cor=C.CINZA)
            continue

        elif acao == "4":
            if inimigo.manso:
                print()
                digitar(f"  * Voce poupou {inimigo.nome}!", cor=C.VERDE + C.BOLD)
                time.sleep(0.4)
                digitar(f'  {inimigo.nome}: "{inimigo.frase_manso}"', cor=C.CIANO, delay=0.04)
                time.sleep(1)
                return "poupou"
            else:
                digitar(f"  * {inimigo.nome} nao vai aceitar misericordia assim...", cor=C.CINZA)

        else:
            digitar("  * Opcao invalida!", cor=C.CINZA)
            continue

        # Turno do inimigo
        if inimigo.esta_vivo():
            print()
            separador(C.CINZA)
            digitar(f"  — Turno de {inimigo.nome} —", cor=C.CINZA, delay=0.02)
            if esquivou:
                digitar(f"  * {inimigo.nome} hesitou e errou o ataque!", cor=C.VERDE)
            else:
                time.sleep(0.3)
                inimigo.atacar(jogador)

        if not jogador.esta_vivo():
            return "derrotado"

        print()

    return "derrotado"


# ─────────────────────────────────────────────
#  INTRODUÇÃO NARRATIVA DE CADA INIMIGO
# ─────────────────────────────────────────────
def mostrar_intro_inimigo(cfg):
    limpar()
    linha()
    mostrar_ascii(cfg["nome"])
    linha()
    print()
    for frase in cfg["intro"]:
        digitar(frase, delay=0.04, cor=C.CINZA)
        time.sleep(0.35)
    print()
    pausa()


# ─────────────────────────────────────────────
#  TELA TÍTULO
# ─────────────────────────────────────────────
LOGO = r"""
 _   _ _   _ ____  _____ ____  _____  _    _     _____
| | | | \ | |  _ \| ____|  _ \|_   _|/ \  | |   | ____|
| | | |  \| | | | |  _| | |_) | | | / _ \ | |   |  _|
| |_| | |\  | |_| | |___|  _ <  | |/ ___ \| |___| |___
 \___/|_| \_|____/|_____|_| \_\ |_/_/   \_\_____|_____|
"""

def tela_titulo():
    limpar()
    print(C.AMARELO + C.BOLD)
    for l in LOGO.strip("\n").split("\n"):
        print(l)
    print(C.RESET)
    print(C.CINZA + "* uma historia sobre escolhas, no Underground *" + C.RESET)
    print()

def menu_principal():
    while True:
        tela_titulo()
        menu_opcoes([
            f"  {C.VERDE}[1]{C.RESET}  INICIAR JOGO",
            f"  {C.CIANO}[2]{C.RESET}  COMO JOGAR",
            f"  {C.AMARELO}[3]{C.RESET}  CREDITOS",
            f"  {C.VERMELHO}[4]{C.RESET}  SAIR",
        ])
        try:
            op = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            op = "4"

        if   op == "1": return
        elif op == "2": tela_como_jogar()
        elif op == "3": tela_creditos()
        elif op == "4": sair()
        else:
            digitar("  * Opcao invalida.", cor=C.CINZA)
            time.sleep(0.6)

def sair():
    limpar()
    linha()
    digitar("  * Ate a proxima...", cor=C.CINZA)
    digitar("  * Tenha determinacao.", cor=C.AMARELO)
    linha()
    parar_musica()
    sys.exit()

def tela_como_jogar():
    limpar()
    linha()
    print()
    print(C.AMARELO + C.BOLD + "  COMO JOGAR" + C.RESET)
    print()
    print(f"  {C.BOLD}FIGHT{C.RESET}  -> Ataca o inimigo diretamente.")
    print(f"           Pode causar golpe critico!")
    print()
    print(f"  {C.BOLD}ACT{C.RESET}    -> Interaja com o inimigo.")
    print(f"           Faca ACTs suficientes para")
    print(f"           acalma-lo e liberar o MERCY.")
    print()
    print(f"  {C.BOLD}ITEM{C.RESET}   -> Usa um Biscoito Dourado. (5 usos)")
    print(f"           Recupera 25 HP.")
    print()
    print(f"  {C.BOLD}MERCY{C.RESET}  -> Poupa o inimigo. So funciona")
    print(f"           se ele estiver manso via ACT.")
    print()
    print(f"  {C.CINZA}Habilidades especiais do inimigo")
    print(f"  aparecem a cada 3 turnos!{C.RESET}")
    print()
    print(f"  {C.VERDE}PACIFISTA{C.RESET}  -> Poupe todos.")
    print(f"  {C.VERMELHO}GENOCIDIO{C.RESET}  -> Derrote todos.")
    print(f"  {C.AMARELO}NEUTRO{C.RESET}     -> Uma mistura.")
    print()
    linha()
    pausa()

def tela_creditos():
    limpar()
    linha()
    print()
    print(C.AMARELO + C.BOLD + "  CREDITOS" + C.RESET)
    print()
    print(f"  {C.CIANO}Desenvolvedor:{C.RESET}")
    print(f"    Vinicius Alves Machado de Araujo")
    print()
    print(f"  {C.CIANO}RA:{C.RESET} 824127157")
    print(f"  {C.CIANO}Professora:{C.RESET} Erica Silva")
    print()
    print(f"  Inspirado em UNDERTALE, de Toby Fox (2015)")
    print()
    print(f"  {C.CINZA}\"Mesmo os monstros tem historias para contar.\"{C.RESET}")
    print()
    linha()
    pausa()


# ─────────────────────────────────────────────
#  TELA DE FIM — melhorada por rota
# ─────────────────────────────────────────────
def tela_fim(jogador, resultados, alma_dados):
    limpar()
    linha("═", C.AMARELO)
    print()

    if not jogador.esta_vivo():
        # GAME OVER
        print(C.VERMELHO + C.BOLD + "  GAME OVER" + C.RESET)
        print()
        print(f"  {jogador.nome} foi derrotado no Underground.")
        print()
        digitar("  * ...", cor=C.CINZA, delay=0.08)
        time.sleep(0.4)
        digitar("  * Mas no fundo do seu peito,", cor=C.CINZA, delay=0.05)
        digitar(f"  * a alma de {alma_dados['cor']}{jogador.alma}{C.RESET} ainda pulsa.", delay=0.05)
        digitar("  * Nao desista.", cor=C.AMARELO, delay=0.05)
        print()
        linha("─", C.VERMELHO)
        print(f"  {C.CINZA}Inimigos enfrentados: {len(resultados)}{C.RESET}")
        return

    poupados   = [n for n, r in resultados if r == "poupou"]
    derrotados = [n for n, r in resultados if r == "venceu"]

    if derrotados and not poupados:
        # ROTA GENOCÍDIO
        print(C.VERMELHO + C.BOLD + "  ROTA GENOCIDIO" + C.RESET)
        print()
        digitar("  * O Underground ficou em silencio.", cor=C.CINZA, delay=0.05)
        digitar("  * Nenhuma voz. Nenhum passo. Nenhum sorriso.", cor=C.CINZA, delay=0.05)
        print()
        digitar(f"  * {jogador.nome} cruzou o Underground sem olhar para tras.", delay=0.05)
        digitar("  * Poder absoluto. Mas a que preco?", cor=C.CINZA, delay=0.05)
        print()
        digitar("  * Em algum lugar, uma crianca pergunta:", cor=C.CINZA, delay=0.05)
        digitar("  * 'Por que voce fez isso?'", cor=C.VERMELHO, delay=0.06)
        print()
        digitar("  * Voce nao responde.", cor=C.CINZA, delay=0.05)
        print()
        linha("─", C.VERMELHO)
        print(f"  {C.CINZA}Derrotados: {', '.join(derrotados)}{C.RESET}")

    elif poupados and not derrotados:
        # ROTA PACIFISTA
        print(C.VERDE + C.BOLD + "  ROTA PACIFISTA" + C.RESET)
        print()
        digitar("  * O Underground nunca foi tao luminoso.", cor=C.VERDE, delay=0.05)
        digitar("  * Cada monstro que voce poupou olha para o ceu", delay=0.05)
        digitar("  * e ve algo que nunca viu antes: esperanca.", cor=C.AMARELO, delay=0.05)
        print()
        digitar(f"  * {jogador.nome} mostrou que nao precisa de violencia", delay=0.05)
        digitar("  * para ser forte. Precisa de coragem para se importar.", delay=0.05)
        print()
        digitar("  * Flowey observa de longe, confuso.", cor=C.CINZA, delay=0.05)
        digitar("  * Pela primeira vez em muito tempo,", cor=C.CINZA, delay=0.05)
        digitar("  * ele sente algo que havia esquecido.", cor=C.CINZA, delay=0.05)
        print()
        digitar("  * Talvez isso seja o que chamam de alma.", cor=C.AMARELO, delay=0.06)
        print()
        linha("─", C.VERDE)
        print(f"  {C.CINZA}Poupados: {', '.join(poupados)}{C.RESET}")

    else:
        # ROTA NEUTRA
        print(C.AMARELO + C.BOLD + "  ROTA NEUTRA" + C.RESET)
        print()
        digitar("  * O Underground guarda suas memorias.", cor=C.CINZA, delay=0.05)
        digitar("  * Algumas bondosas. Outras, pesadas.", cor=C.CINZA, delay=0.05)
        print()
        digitar(f"  * {jogador.nome} nao foi um heroi nem um vilao.", delay=0.05)
        digitar("  * Foi apenas alguem tentando sobreviver.", delay=0.05)
        print()
        digitar("  * Os que foram poupados te lembram com carinho.", cor=C.VERDE, delay=0.05)
        digitar("  * Os que foram derrotados... nao te lembram mais.", cor=C.CINZA, delay=0.05)
        print()
        digitar("  * O que voce faria diferente?", cor=C.AMARELO, delay=0.06)
        print()
        linha("─", C.AMARELO)
        if poupados:
            print(f"  {C.VERDE}Poupados: {', '.join(poupados)}{C.RESET}")
        if derrotados:
            print(f"  {C.VERMELHO}Derrotados: {', '.join(derrotados)}{C.RESET}")

    print()
    time.sleep(0.5)
    digitar("  * Obrigado por jogar.", cor=C.CINZA, delay=0.04)
    linha("═", C.AMARELO)


# ─────────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────
def main():
    limpar()
    linha()
    print()
    for frase in [
        "  * Muito tempo atras, humanos e monstros viviam juntos.",
        "  * Depois de uma grande guerra, os monstros foram selados",
        "  * sob a terra, atras de uma barreira magica.",
        "  * Diz a lenda que quem cai na Montanha Ebott... nunca volta.",
        "  * Voce caiu no Underground.",
    ]:
        digitar(frase, cor=C.CINZA, delay=0.04)
        time.sleep(0.3)
    linha()
    time.sleep(0.4)

    # Nome
    print()
    print(C.AMARELO + "  Nomeie a crianca caida" + C.RESET)
    print()
    try:
        nome = input("  > ").strip() or "Frisk"
    except EOFError:
        nome = "Frisk"

# Easter egg
    
    if nome.strip().lower() == "elza":
        limpar()
        linha()
        time.sleep(0.4)
        for frase, cor in [
            ("  * ...", C.CINZA),
            ("  * Ei...", C.BRANCO),
            ("  * Esse nome não é qualquer nome.", C.BRANCO),
            ("  * É um nome que carrega cuidado, força e amor.", C.CINZA),
            ("  * Um amor daqueles que acolhe, protege e nunca vai embora.", C.CINZA),
            ("  * Vinicius nao sabe muito bem falar essas coisas.", C.BRANCO),
            ("  * No jeito que ele fala de você.", C.BRANCO),
            ("  * Ele te ama muito, Elza. <3", C.VERMELHO + C.BOLD),
            ("  * Agora vai. Tem um Underground pra atravessar.", C.AMARELO),
        ]:
            digitar(frase, cor=cor, delay=0.05)
            time.sleep(0.5)
        linha()
        time.sleep(1.2)

    # Alma
    limpar()
    exibir_almas()
    try:
        op_alma = input("  > ").strip()
    except EOFError:
        op_alma = "1"
    if op_alma not in ALMAS:
        op_alma = "1"
    alma_dados = ALMAS[op_alma]
    print()
    digitar(f"  * Alma de {alma_dados['cor']}{alma_dados['nome']}{C.RESET} escolhida!", cor=C.BRANCO)
    time.sleep(0.6)

    # Arma
    limpar()
    exibir_armas()
    try:
        op_arma = input("  > ").strip()
    except EOFError:
        op_arma = "1"
    if op_arma not in ARMAS:
        op_arma = "1"
    arma_dados = ARMAS[op_arma]
    arma = Arma(arma_dados)
    print()
    digitar(f"  * {C.BOLD}{arma.nome}{C.RESET} equipada!", cor=C.BRANCO)
    time.sleep(0.6)

    # Criar personagem
    jogador = Personagem(nome, alma_dados, arma)
    limpar()
    linha()
    print()
    digitar(f"  * {jogador.cor}{jogador.nome}{C.RESET} ({jogador.alma}) entrou no Underground.", cor=C.BRANCO)
    digitar(f"  * Arma: {arma.nome}  HP: {jogador.vida_max}  Forca: {jogador.forca}  Defesa: {jogador.defesa}  LV: {jogador.nivel}", cor=C.CINZA)
    time.sleep(0.5)
    pausa()

    # Loop de batalhas
    resultados = []
    for cfg in INIMIGOS_CFG:
        if not jogador.esta_vivo():
            break

        mostrar_intro_inimigo(cfg)

        inimigo = Inimigo(cfg)
        resultado = combate(jogador, inimigo)
        resultados.append((cfg["nome"], resultado))

        limpar()
        linha()
        print()
        if resultado == "poupou":
            digitar(f"  * Voce poupou {C.VERDE}{cfg['nome']}{C.RESET}.", cor=C.BRANCO)
        elif resultado == "venceu":
            digitar(f"  * {C.BOLD}{cfg['nome']}{C.RESET} foi derrotado.", cor=C.CINZA)
        elif resultado == "derrotado":
            break
        time.sleep(1)

    # Fim de jogo
    tela_fim(jogador, resultados, alma_dados)


# ─────────────────────────────────────────────
#  PONTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    iniciar_musica()
    menu_principal()
    while True:
        main()
        print()
        linha()
        digitar("  * O Underground ainda existe...", cor=C.CINZA)
        time.sleep(0.5)
        try:
            jogar_de_novo = input("\n  Deseja jogar novamente? (s/n)\n  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            jogar_de_novo = "n"
        if jogar_de_novo != "s":
            sair()
        limpar()