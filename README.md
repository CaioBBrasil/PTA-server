# PTA-server
Esse repositório contem uma implementação do protocólo de aplicação PTA. Ele permite execuar os comandos de CUMP, LIST, PEGA, TERM.
Essa aplicação funciona na porta 11550 e para o caso de clientes na mesma máquina que o servidor, o endereço será '127.0.0.1'. 

Para a execução do escript do servidor, executar o comando abaixo após baixar o repositório:

obs: é preciso entrar na pasta do repositório baixado
```
python3 pta-server/pta-server.py
```
obs2: só funciona em linux

Para execução do Cliente, troque "user" pelo usuário especifico:
```
python3 pta-client.py 127.0.0.1 11550 "user"
```
