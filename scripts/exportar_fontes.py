#!/usr/bin/env fontforge -lang=py -script
"""Exporta as fontes OTF a partir dos projetos FontForge (.sfd).

Uso (FontForge instalado, ex.: `brew install fontforge`):

    fontforge -lang=py -script scripts/exportar_fontes.py [diretorio_saida]

O diretório de saída padrão é `dist/`. O nome do arquivo gerado é o `FontName`
do projeto (ex.: `CPRMGeologyRegular.otf`). Retorna erro se algum projeto não
puder ser aberto ou se algum glifo do OTF gerado diferir do .sfd.
"""
import os
import sys

import fontforge

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJETOS = [
    "fonts/cprm_geology.sfd",
    "fonts/cprm_stratigraphy_paleontology.sfd",
]


def exportar(sfd, saida):
    fonte = fontforge.open(os.path.join(RAIZ, sfd))
    destino = os.path.join(saida, fonte.fontname + ".otf")
    fonte.generate(destino)

    # Reprodutibilidade: compara os glifos (não os bytes do arquivo, que variam
    # com a versão do FontForge). Por glifo: largura, caixa delimitadora (tolerância
    # de 1 unidade, por arredondamento) e número de contornos.
    gerada = fontforge.open(destino)

    def resumo(f):
        return {
            g.unicode: (g.width, tuple(round(v) for v in g.boundingBox()), len(g.foreground))
            for g in f.glyphs() if g.unicode >= 0
        }

    esperados, obtidos = resumo(fonte), resumo(gerada)
    erros = [f"U+{u:04X}: sem glifo no OTF" for u in esperados.keys() - obtidos.keys()]
    erros += [f"U+{u:04X}: glifo extra no OTF" for u in obtidos.keys() - esperados.keys()]
    for u in sorted(esperados.keys() & obtidos.keys()):
        (w1, b1, c1), (w2, b2, c2) = esperados[u], obtidos[u]
        if w1 != w2 or c1 != c2 or any(abs(x - y) > 1 for x, y in zip(b1, b2)):
            erros.append(f"U+{u:04X}: projeto {w1}/{b1}/{c1} contornos, OTF {w2}/{b2}/{c2}")
    if erros:
        raise SystemExit(f"ERRO: {destino} difere do projeto {sfd}:\n  " + "\n  ".join(erros))
    print(f"OK {destino}: {len(esperados)} glifos")


def main():
    saida = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(RAIZ, "dist")
    os.makedirs(saida, exist_ok=True)
    for sfd in PROJETOS:
        exportar(sfd, saida)


main()
