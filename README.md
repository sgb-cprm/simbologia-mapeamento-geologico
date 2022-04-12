# Biblioteca de Estilos para Mapas Temáticos da CPRM/SGB para ArcGIS 10.x e QGIS 3.x: Geologia, Estratigrafia e Paleontologia

- Flavia Renata Ferreira <flavia.ferreira@cprm.gov.br>
- Elias Bernard S. do Espirito Santo <elias.bernard@cprm.gov.br>
- Carlos Eduardo Miranda Mota <carlos.mota@cprm.gov.br>
- Francisca de Paula da Silva e Lima Abreu <paula.lima@cprm.gov.br>

## Apresentação

Este produto consiste em disponibilizar as paletas de cores correspondente a biblioteca de Geologia, Estratigrafia e Paleontologia da SGB/CPRM, em versões compatíveis com os softwares ArcGIS 10.x e QGIS 3.x. Originalmente esta biblioteca foi construída sob o formato ESRI Style (.style), com posterior conversão paa QGIS Style (.xml). 

A biblioteca foi originalmente produzida pela CPRM para compor portifólio de estilos dos mapeamentos geológicos. Os glifos, em formato bitmap, foram substituídos por formatos vetoriais W3C SVG 1.1 e empacotados em arquivos de fonte OTF, disponibilizados junto das bibliotecas de estilos.

Os arquivos de fonte CPRM_Geology.otf e CPRM_StratigraphyPaleontology.otf precisam estar instalados no sistema operacional, para as bibliotecas de estilos buscarem os glifos corretamente.

O processo de conversão para QGIS Style foi realizado através do plugin SLYR v4.0.1 Community Edition (https://north-road.com/slyr/), em uma instalação de QGIS 3.22.5 para Windows. Este produto foi testado em ambientes Windows 10 e Debian Linux 11 (bullseye). Alguns ajustes de compatibilidade na renderização dos símbolos foram realizados.

Caso seja encontrado algum erro ou inconsistência na biblioteca, pedimos a gentileza que nos reporte o problema a partir dos canais oficiais da SGB/CPRM ou via contato direto com os autores.

## Organização do Conteúdo

### Diretório `fonts`

Este diretório contém os itens necessários para a composição de arquivos de fonte a partir de tabelas de caracteres. Os arquivos .sfd correspondem a projetos de fontes OTF, que são abertos a partir do software [FontForge](https://fontforge.org/). 

Além dos arquivos de projeto, existe um diretório `glyphs` (glifos), que contém as figuras em formato W3C SVG 1.1, editáveis em softwares, tais como o [LibreOffice Draw](https://pt-br.libreoffice.org/descubra/draw/) e o [Inkscape](https://inkscape.org/).

O diretório `export` contém as versões de fontes geradas pelo FontForge. Estas fontes podem ser instaladas diretamente no sistema operacional

### Diretório `esri-style`

Este diretório contém o arquivo de estilos para o ESRI ArcGIS Desktop (.style). Originalmente, e por questões de legado, as tabelas de cores e símbolos são confeccionadas nesta plataforma.

### Diretório `qgis-xml`

Este diretório contém o arquivo de estilos para o QGIS (.xml). Como este arquivo, por enquanto, é obtido a partir de conversão dos originais em .style, também é disponibilizado o log de execução da conversão da biblioteca para o formato do QGIS.

## Instalação da Biblioteca de Estilos

Veja no arquivo README.md dos diretórios `esri-style` e `qgis-xml` as páginas de documentação para instalação das bibliotecas.

Se as bibliotecas dependerem de arquivos de fontes para renderizar os símbolos corretamente, é necessário fazer a instalação dos arquivos de fonte .OTF antes de iniciar o software de GIS/SIG. Os arquivos de fontes estão disponíveis no diretório `fonts >> export`.

Para instalação de fontes no Windows, [veja este link](https://support.microsoft.com/pt-br/office/adicionar-uma-fonte-b7c5f17c-4426-4b53-967f-455339c564c1).

## Produção Científica

- [II SBIDE 2020 - II Simpósio Brasileiro de Infraestruturas de Dados Espaciais](https://inde.gov.br/images/inde/sessao8/Portabilidade-de-biblioteca-de-simbolos-cartograficos-para-padroes-abertos.pdf)
- [FOSS4G 2021 Buenos Aires](https://callforpapers.2021.foss4g.org/foss4g2021/talk/DCMXLW/)
- [ISPRS Archives 2021](https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLVI-4-W2-2021/51/2021/isprs-archives-XLVI-4-W2-2021-51-2021.html)

## Disclaimer

Copyright © 2022, Serviço Geológico do Brasil/CPRM

"Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, su
subject to the following conditions"

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION

## License/Licença

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg