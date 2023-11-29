from xmlrpc.server import SimpleXMLRPCServer

from src.modulos.persistencia import Persistencia


class Servidor:

    def __init__(self, porta: int) -> None:
        super().__init__()
        # Determina a porta
        self.__porta = porta

        # Cria um objeto que será compartilhado entre os clientes
        self.__persistencia = Persistencia()

        # Cria um servidor RPC com a porta pre determinada e registra a instância do objeto
        self.__server = SimpleXMLRPCServer(("localhost", self.__porta), allow_none=True)
        self.__server.register_instance(self.__persistencia)

    def run(self):
        # Inicia o servidor
        print(f"Servidor rodando em http://localhost:{self.__porta}")
        self.__server.serve_forever()


if __name__ == '__main__':
    Servidor(5004).run()
