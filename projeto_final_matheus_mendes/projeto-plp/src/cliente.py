import xmlrpc.client


class Cliente:

    def __init__(self, porta: int) -> None:
        super().__init__()
        self.__porta = porta

    def run(self):
        # recebe o objeto via RPCe
        cliente = xmlrpc.client.ServerProxy(f"http://localhost:{self.__porta}")

        # faz as operações disponíveis para o objeto compartilhado

        # Adiciona um usuario
        key_usuario = cliente.adicionar_item("usuarios", {
            "bio": "❄",
            "nome": "Teste Testando",
            "postagens": [],
            "username": "@teste"
        })

        # Lista os usuarios
        usuarios = cliente.carregar_itens("usuarios")
        for key in usuarios:
            print(usuarios[key].__str__())
        print()

        # Remove o cliente
        cliente.remover_item("usuarios", key_usuario)

        # Lista os usuarios
        usuarios = cliente.carregar_itens("usuarios")
        for key in usuarios:
            print(usuarios[key].__str__())


if __name__ == '__main__':
    Cliente(5004).run()
