#!/usr/bin/env fontforge -lang=py -script
"""Exporta as fontes OTF a partir dos projetos FontForge (.sfd).

Uso (FontForge instalado, ex.: `brew install fontforge`):

    fontforge -lang=py -script scripts/exportar_fontes.py [diretorio_saida]

O diretório de saída padrão é `dist/`. O nome do arquivo gerado é o `FontName`
do projeto (ex.: `CPRMGeologyRegular.otf`). Retorna erro se algum projeto não
puder ser aberto ou se o OTF gerado não tiver os mesmos glifos do .sfd.
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

    gerada = fontforge.open(destino)
    esperados = {g.unicode: g.width for g in fonte.glyphs() if g.unicode >= 0}
    obtidos = {g.unicode: g.width for g in gerada.glyphs() if g.unicode >= 0}
    if esperados != obtidos:
        raise SystemExit(f"ERRO: {destino} difere do projeto {sfd} (glifos/larguras)")
    print(f"OK {destino}: {len(esperados)} glifos")


def main():
    saida = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(RAIZ, "dist")
    os.makedirs(saida, exist_ok=True)
    for sfd in PROJETOS:
        exportar(sfd, saida)


main()
