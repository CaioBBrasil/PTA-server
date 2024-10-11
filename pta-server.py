from socket import *
from signal import signal, SIGPIPE, SIG_DFL
import os
signal(SIGPIPE,SIG_DFL)

serverPort = 11550 # Porta da comunicação 
serverSocket = socket(AF_INET,SOCK_STREAM)  # Cria o Socket TCP (SOCK_STREAM) para rede IPv4 (AF_INET)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)  # Socket fica ouvindo conexoes. O valor 1 indica que uma conexao pode ficar na fila

print("Servidor pronto para receber mensagens. Digite Ctrl+C para terminar.")

while 1:
    
        cont_init = 0  # Varivel de verificação de inicio de comunicação
        connectionSocket, addr = serverSocket.accept()  # Cria um socket para tratar a conexao do cliente

        try:  # Trata excessão para parada do Servidor
            
            while True:  # Loop para respostas de mais de uma mensagem
               
               # Recebe a requisição do cliente e divide a mensagem
               sentence = connectionSocket.recv(1024)  
               sentence = sentence.decode('ascii')
               sentence = sentence.split(" ")
          
                
               if cont_init == 0:  # Verifica se é a primeira mensagem da conexão
                    try:
                         # Verifica se a mensagem segue o formato estabelecido pelo protocolo
                         SEQnum = int(sentence[0])
                         SEQnum = str(SEQnum)

                         if sentence[1] != "CUMP":
                              REPLY = "NOK"
                         else:

                              # Verificação se usuario é válido
                              user = sentence[2] + '\n'
                              validUsers = open("PTA-server/pta-server/users.txt", "r").readlines()

                              if user in validUsers:
                                   REPLY = "OK"
                              else:
                                   REPLY = "NOK"

                         # Monta a mensagem de resposta
                         BResp = SEQnum + " " + REPLY
                         connectionSocket.send(BResp.encode('ascii'))
                         cont_init += 1 # assegura que passou da primeira mensagem

                    except:
                         REPLY = "NOK"
                         connectionSocket.send(REPLY.encode('ascii'))
                    
                    # Fecha a conexão caso reposta NOK seja enviada
                    if REPLY == "NOK":
                         connectionSocket.close()
                         break
                   

               else:
                    try: # Assegura NOK para qualquer erro de requisição sem quebrar o servidor
                         SEQnum = int(sentence[0])
                         SEQnum = str(SEQnum)

                         # Comando LIST
                         if sentence[1] == "LIST":
                         
                                REPLY = "ARQS"
                                # Organiza a lista de arquivos presentes no servidor
                                ARGS = os.listdir("PTA-server/pta-server/files") #
                                text = str(len(ARGS)) + " " + str(ARGS[0])
                                for i in ARGS[1:]:
                                     text = text + "," + i 
                                ARGS = text

                                BResp = SEQnum + " " + REPLY + " " + ARGS # Monta a mensagem de resposta


                         # Comando PEGA
                         elif sentence[1] == "PEGA":
                                   REPLY = "ARQ"
                                   ARQ = open("PTA-server/pta-server/files/" + sentence[2], "rb").read() # Pega as informações em byte do arquivo
                                   SizeFile = os.stat("PTA-server/pta-server/files/" + sentence[2]).st_size # Pega as informações de tamanho do arquivo
                                   
                                   # Organiza a resposta de saída
                                   text = str(SizeFile) + " " + str(ARQ)[2:-1]
                                   ARGS = text
                                   BResp = SEQnum + " " + REPLY + " " + ARGS

                         # Comando TERM
                         elif sentence[1] == "TERM":
                              REPLY = "OK"
                              BResp = SEQnum + " " + REPLY
                              connectionSocket.send(BResp.encode('ascii'))
                              connectionSocket.close() # Assegura o fechamento da conexão aṕos o envio da mensagem
                              break
                         
                         # Envia as repostas para os comandos PEGA e LIST
                         BResp = BResp.encode('ascii')
                         connectionSocket.send(BResp)
                         
                         
                    except: # Trata as exeções como "arquivo não encontrado"
                         REPLY = "NOK"
                         BResp = SEQnum + " " + REPLY
                         connectionSocket.send(BResp.encode('ascii'))

              

        except(KeyboardInterrupt, SystemExit):
             connectionSocket.close()
             break


    
connectionSocket.close()
serverSocket.shutdown(SHUT_RDWR)
serverSocket.close()
