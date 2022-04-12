# Manipulando glifos no FontForge

## Importar glifos SVG

TODO

## Exportar glifos para SVG, no formato `Unicode+FontName.svg`

No FontForge:

1. Ir em `File` >> `Execute Script`
2. Na janela de diálogo, copiar o código abaixo para a caixa de texto
3. Selecione `FF`, como o interpretador do script
```
SelectWorthOutputting(); 
foreach Export("U+%U-%f.svg"); 
endloop;
```
4. Pressione `OK`

Os arquivos exportados encontrarão-se no diretório de usuário logado (No Windows, em `%homedrive%%homepath%`, normalmente C:\Usuários\usuario, no Linux em `$HOME`, normalmente /home/usuario).