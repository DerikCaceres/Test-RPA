# Template - V 8.1.0

## V 8.1.0 do template de projeto de RPA em python

### Modificações:

- Adição do script configure.ps1 para facilitação na configuração de ambiente de execução;
- Melhoria no formato das entradas: 
  - Parâmetros de entrada e credenciais deixam de ser recebidos como argumentos do script e devem ser passados como variáveis de ambiente (Jenkins) ou pelo arquivo de inputs (Json).
  - Implementação de funções de obtenção de credenciais e parâmetros de entrada no arquivo Assets\Libraries\RPA\inputs.py.

## Objetivo
O projeto tem como objetivo seguir de Template para o início do desenvolvimento RPA em Python.

## Fluxo
O projeto se inicia com a configuração geral e em seguida realiza a extração de Issues do tipo Bug e Epic no Board RPA no Jira finalizando com um print das Issues.

## Contatos
- Contato da área: desenvolvedores do RPA CoE
- Business Analyst: NA