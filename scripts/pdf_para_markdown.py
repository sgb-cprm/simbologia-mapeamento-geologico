#!/usr/bin/env python3
"""Converte o PDF da biblioteca de símbolos (Bibl_Geologia_SGB_2019.pdf) em Markdown,
com todas as colunas e com o desenho de cada símbolo recortado do próprio PDF.

Uso (na raiz do repositório; requer poppler: pdftotext e pdftoppm):
    python scripts/pdf_para_markdown.py docs/bibl_geologia_sgb_2019/Bibl_Geologia_SGB_2019.pdf docs/bibl_geologia_sgb_2019/Bibl_Geologia_SGB_2019.md

Como funciona:
  1. Renderiza cada página em tons de cinza e detecta a grade das tabelas
     (linhas horizontais de largura total e linhas verticais contínuas).
  2. Lê as palavras com posição (pdftotext -bbox) e atribui cada uma à célula onde está.
  3. Recorta a célula do desenho (300 dpi) para a pasta img/, ao lado do .md de saída, e a referencia na tabela,
     na escala do PDF a 96 dpi.
Só biblioteca padrão do Python; nenhum pacote extra.
"""
import html
import os
import re
import subprocess
import sys

DPI_GRADE = 150
DPI_RECORTE = 300
LIMIAR = 235

# Correções ortográficas do texto do PDF (a edição de 2019 tem erros de digitação).
# Cada item é (expressão, substituição); o script conta quantas vezes cada uma foi aplicada.
CORRECOES = [
    (r"\bboundins\b", "boudins"),
    (r"\bCoprólitoss\b", "Coprólitos"),
    (r"\bestiollítica\b", "estilolítica"),
    (r"\bhitrotermal\b", "hidrotermal"),
    (r"\bLineção\b", "Lineação"),
    (r"\bmovimetno\b", "movimento"),
    (r"\bparasitica\b", "parasítica"),
    (r"\bStorckwork\b", "Stockwork"),
    (r"\bdetritico\b", "detrítico"),
    (r"\bSimbol\b", "Símbolo"),
    (r"\bslinckenlines\b", "slickenlines"),
    (r"\bTMD\b", "TDM"),
    (r"\bU-TH-Pb\b", "U-Th-Pb"),
    # PENDENTE (decisão do autor: manter o texto do PDF por enquanto; ver PENDENCIAS.md):
    # (r"\bfluxo magnético\b", "fluxo magmático"),
    (r"\bdeverão fica\b", "deverão ficar"),
    # "Rb-Sr rocha total": o PDF diz "C255%" (impossível em CMYK). A cor real é o vermelho RGB (255, 0, 0),
    # confirmado no .stylx e no PDF; em CMYK, como as demais cores da tabela, fica M100% Y100%.
    (r"\bC255%", "M100% Y100%"),
    # ortografia atual (Acordo de 1990), como em "Amonoides" e "Equinoides" já presentes no PDF
    (r"\bCrinóides\b", "Crinoides"),
    (r"\bNautilóides\b", "Nautiloides"),
]
APLICADAS = {}


def corrigir(texto):
    for padrao, novo in CORRECOES:
        texto, n = re.subn(padrao, novo, texto)
        if n:
            APLICADAS[padrao] = APLICADAS.get(padrao, 0) + n
    return texto


# ---------- grade das tabelas (a partir da imagem da página) ----------
def render_cinza(pdf, pagina):
    dados = subprocess.run(
        ["pdftoppm", "-gray", "-r", str(DPI_GRADE), "-f", str(pagina), "-l", str(pagina), pdf],
        capture_output=True, check=True).stdout
    partes = dados.split(b"\n", 3)
    w, h = map(int, partes[1].split())
    return w, h, partes[3]


def agrupar(indices, folga=2):
    grupos = []
    for i in indices:
        if grupos and i - grupos[-1][-1] <= folga:
            grupos[-1].append(i)
        else:
            grupos.append([i])
    return [(g[0] + g[-1]) / 2 for g in grupos]


def tabelas_da_pagina(pdf, pagina, cabecalhos_pt):
    """Devolve lista de tabelas: {'y': [linhas horizontais], 'x': [linhas verticais]} em px.

    `cabecalhos_pt`: posição vertical (pt) de cada palavra NOMENCLATURA; cada uma marca uma tabela.
    """
    w, h, px = render_cinza(pdf, pagina)
    cont = [sum(1 for b in px[y * w:(y + 1) * w] if b < LIMIAR) for y in range(h)]
    horiz = agrupar([y for y in range(h) if cont[y] > 0.80 * w])
    inicios = sorted({max((y for y in horiz if y <= hy * DPI_GRADE / 72.0), default=None)
                      for hy in cabecalhos_pt} - {None})
    tabelas = []
    for k, ini in enumerate(inicios):
        fim = inicios[k + 1] if k + 1 < len(inicios) else float("inf")
        b = [y for y in horiz if ini <= y < fim]
        if len(b) < 3:
            continue
        y0, y1 = int(b[0]), int(b[-1])
        passo = range(y0, y1 + 1, 2)
        vert = [x for x in range(w) if sum(1 for y in passo if px[y * w + x] < LIMIAR) > 0.9 * len(passo)]
        tabelas.append({"y": b, "x": agrupar(vert)})
    return tabelas


# ---------- palavras com posição ----------
def palavras_por_pagina(pdf):
    xml = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True, check=True).stdout
    paginas = []
    for pg in xml.split("<page ")[1:]:
        ws = [(float(a), float(b), float(c), float(d), html.unescape(t)) for a, b, c, d, t in
              re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', pg)]
        paginas.append(ws)
    return paginas


def texto_da_celula(palavras, x0, x1, y0, y1):
    """Palavras cujo centro cai na célula (em pt), agrupadas por linha."""
    dentro = [w for w in palavras if x0 <= (w[0] + w[2]) / 2 <= x1 and y0 <= (w[1] + w[3]) / 2 <= y1]
    dentro.sort(key=lambda w: (round((w[1] + w[3]) / 2 / 3), w[0]))
    linhas, ult = [], None
    for w in dentro:
        yc = (w[1] + w[3]) / 2
        if ult is not None and abs(yc - ult) <= 3:
            linhas[-1].append(w[4])
        else:
            linhas.append([w[4]])
        ult = yc
    partes = [" ".join(l) for l in linhas]
    saida = ""
    for p in partes:
        saida = p if not saida else (saida + p if saida.endswith("_") else saida + " " + p)
    return corrigir(saida.strip())


CAMPOS = [("NOMENCLATURA", "nome"), ("TRAÇO", "traco"), ("TAMANHO", "mm"), ("SELECTOR", "pt"),
          ("SYMBOL", "pt"), ("BIBLIOTECA", "bib"), ("COR", "cor")]


def campo_do_cabecalho(texto, primeira):
    up = texto.upper()
    for chave, campo in CAMPOS:
        if re.search(r"\b%s\b" % chave, up):
            return campo
    return "desenho" if primeira else "?"


def esc(t):
    return t.replace("|", "\\|")


def unir(linhas):
    """Junta as linhas de um parágrafo; "Ex." e "Nas ..." (exemplo) começam em nova linha, sem novo parágrafo."""
    texto = ""
    for l in linhas:
        if not texto:
            texto = l
        elif re.match(r"Ex\.|Nas ", l):
            texto += "  \n" + l
        else:
            texto += " " + l
    return texto


# ---------- principal ----------
def main(pdf, md):
    os.makedirs(os.path.dirname(os.path.abspath(md)), exist_ok=True)
    pasta_img = os.path.join(os.path.dirname(os.path.abspath(md)), "img")
    os.makedirs(pasta_img, exist_ok=True)
    nome_pasta = os.path.basename(pasta_img)
    paginas = palavras_por_pagina(pdf)
    pt_px = 72.0 / DPI_GRADE
    saida, total, avisos = [], 0, []

    # capa
    capa = {}
    for w in paginas[0]:
        capa.setdefault(round((w[1] + w[3]) / 2 / 4), []).append(w)
    linhas_capa = [" ".join(x[4] for x in sorted(v, key=lambda w: w[0])) for _, v in sorted(capa.items())]
    saida.append("# " + " ".join(l for l in linhas_capa if l.startswith(("BIBLIOTECA", "CARTOGRAFIA"))).title()
                 if False else "# Biblioteca de símbolos: cartografia geológica (Bibl_Geologia_SGB_2019)")
    saida.append("")
    saida.append("> Conversão automática de `%s` para Markdown, com os desenhos recortados do próprio PDF. "
                 "Edição 2019. Gerado por `scripts/pdf_para_markdown.py`." % os.path.basename(pdf))
    saida.append("> Serviço Geológico do Brasil – CPRM · Diretoria de Geologia e Recursos Minerais · "
                 "Departamento de Geologia · Divisão de Geologia Básica.")
    saida.append("")

    assinatura_atual = None
    for pagina in range(2, len(paginas) + 1):
        palavras = paginas[pagina - 1]
        tabelas = tabelas_da_pagina(pdf, pagina, [(w[1] + w[3]) / 2 for w in palavras if w[4] == "NOMENCLATURA"])
        fim_tabelas, n_tab = 0, 0
        for tab in tabelas:
            ys = [y * pt_px for y in tab["y"]]
            xs = [x * pt_px for x in tab["x"]]
            if len(xs) < 3:
                avisos.append("pág. %d: grade de colunas não detectada" % pagina)
                continue
            fim_anterior = fim_tabelas
            fim_tabelas = max(fim_tabelas, ys[-1])
            n_tab += 1
            colunas = list(zip(xs[:-1], xs[1:]))
            # cabeçalho: o intervalo horizontal que contém a palavra NOMENCLATURA
            idx_cab = next((i for i in range(len(ys) - 1) if any(
                w[4] == "NOMENCLATURA" and ys[i] <= (w[1] + w[3]) / 2 <= ys[i + 1] for w in palavras)), None)
            if idx_cab is None:
                avisos.append("pág. %d: cabeçalho não encontrado" % pagina)
                continue
            cab = [texto_da_celula(palavras, x0, x1, ys[idx_cab], ys[idx_cab + 1]) for x0, x1 in colunas]
            campos = [campo_do_cabecalho(t, i == 0) for i, t in enumerate(cab)]
            # título acima da tabela (ex.: "SÍMBOLOS DE GEOCRONOLOGIA")
            titulo = texto_da_celula(palavras, 0, 600, max(ys[0] - 45, fim_anterior, 0), ys[0] - 1)
            titulo = re.sub(r"^\d+\s*$", "", titulo).strip()
            if titulo or assinatura_atual is None or (tuple(campos), cab[0]) != assinatura_atual:
                if titulo:
                    saida += ["", "## " + titulo.capitalize(), ""]
                if campos[0] == "desenho" and cab[0].upper().startswith("FEI"):
                    saida += ["", "### " + cab[0].capitalize(), ""]
                saida.append("| " + " | ".join(esc(c.replace("\n", " ")) or " " for c in cab) + " |")
                saida.append("| " + " | ".join("---" for _ in cab) + " |")
                assinatura_atual = (tuple(campos), cab[0])
            for i in range(idx_cab + 1, len(ys) - 1):
                y0, y1 = ys[i], ys[i + 1]
                if y1 - y0 < 8:
                    continue
                celulas = []
                for (x0, x1), campo in zip(colunas, campos):
                    if campo == "desenho":
                        total += 1
                        arq = "p%02d_%02d.png" % (pagina, i - idx_cab) if n_tab == 1 else "p%02d_t%d_%02d.png" % (pagina, n_tab, i - idx_cab)
                        px = lambda v: int(round(v * DPI_RECORTE / 72.0))
                        xa, ya = px(x0) + 5, px(y0) + 5
                        wa, ha = px(x1) - px(x0) - 10, px(y1) - px(y0) - 10
                        subprocess.run(["pdftoppm", "-r", str(DPI_RECORTE), "-f", str(pagina), "-l", str(pagina),
                                        "-x", str(xa), "-y", str(ya), "-W", str(wa), "-H", str(ha),
                                        "-png", "-singlefile", pdf, os.path.join(pasta_img, arq[:-4])], check=True)
                        largura_96 = round(wa * 96 / DPI_RECORTE)
                        celulas.append('<img src="%s/%s" width="%d" alt="símbolo">' % (nome_pasta, arq, largura_96))
                    else:
                        celulas.append(esc(texto_da_celula(palavras, x0, x1, y0, y1)) or " ")
                saida.append("| " + " | ".join(celulas) + " |")
        # notas abaixo das tabelas (ex.: "ORIENTAÇÕES")
        notas = [w for w in palavras if fim_tabelas and fim_tabelas + 5 < w[1] and not re.fullmatch(r"\d+", w[4])]
        if notas:
            linhas = {}
            for w in notas:
                linhas.setdefault(round((w[1] + w[3]) / 2 / 3), []).append(w)
            paragrafo, anterior = [], None
            saida.append("")
            for k in sorted(linhas):
                txt = " ".join(x[4] for x in sorted(linhas[k], key=lambda w: w[0]))
                if anterior is not None and (k - anterior > 6 or re.match(r"\d+\)", txt)):
                    saida += [corrigir(unir(paragrafo)), ""]
                    paragrafo = []
                paragrafo.append(txt)
                anterior = k
            saida += [corrigir(unir(paragrafo)), ""]
            assinatura_atual = None

    saida.append("")
    open(md, "w", encoding="utf-8").write("\n".join(saida) + "\n")
    print("%s: %d recortes de desenho em %s" % (md, total, pasta_img))
    for padrao, n in APLICADAS.items():
        print("correção %-28s %d" % (padrao, n))
    for a in avisos:
        print("AVISO:", a)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
