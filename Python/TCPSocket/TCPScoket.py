import socket
import sys
import _thread as thread
import json

class TCPSocket:
    def __init__(self):
        print("Programa feito por Luiz Henrique\n\n")
        
    def servidor(self, ip="localhost", porta=9999, fn=False, log=False): # Instância de servidor
        entrada = {}
        
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        endereco_servidor = (ip, porta)
        
        if (log): print ('Iniciando servidor em %s na porta %s' % endereco_servidor)
        
        tcp.bind(endereco_servidor)
        tcp.listen(1)
        
        def conexao(con, cliente): # Objeto de conexão para multi-thread
            try:
                entrada[cliente[1]] = ""
                if (log): print ('\nConexao recebida de: ' + str(cliente))
                while True:
                    dados = con.recv(4096)
                    entrada[cliente[1]] += str(dados.decode('utf-8'))
                    if not dados:
                        if (log): print ('Fim do recebimento')
                        break
                entrada[cliente[1]] = json.loads(entrada[cliente[1]])
                if (log): print ('Recebido:', entrada[cliente[1]])
                if (fn != False):
                    fn(entrada[cliente[1]])
            except:
                e = sys.exc_info()[0]
                if (log): print ('Ocorreu um erro: %s' % e)

            finally:
                con.close()
                del entrada[cliente[1]]
                if (log): print ('Conexão encerrada')

            return 0
        
        while True:
            if (log): print ('\nAguardando conexão')
            con, cliente = tcp.accept()
            thread.start_new_thread(conexao, tuple([con, cliente]))
            
    def cliente(self, ip="localhost", porta=9999, obj={}, log=False):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        endereco_servidor = ('localhost', 9999)
        
        if (log): print ('Conectando em %s porta %s' % endereco_servidor)
        try:
            tcp.connect(endereco_servidor)
            
            if (log): print ('Enviando dados...')
            tcp.sendall(json.dumps(obj).encode('utf-8'))
        except:
            e = sys.exc_info()[0]
            print ('Ocorreu um erro: %s' % e)
        
        return 0