import json
import uuid


class Persistencia:
    def __init__(self, caminho: str) -> None:
        super().__init__()
        self.__caminho = caminho

    def __carregar_json(self) -> json:
        with open(self.__caminho, encoding='utf-8') as file:
            data = json.load(file)
        return data

    def __salvar_json(self, dados: json):
        with open(self.__caminho, 'w', encoding='utf-8') as outfile:
            json.dump(dados, outfile, sort_keys=True, indent=2, ensure_ascii=False)

    def carregar_itens(self) -> json:
        return self.__carregar_json()

    def carregar_item_id(self, key: str) -> json:
        dados = self.__carregar_json()
        return dados[key] if key in dados else {}

    def adicionar_item(self, item: json):
        dados = self.__carregar_json()

        key = str(uuid.uuid4())
        while key in dados:
            key = str(uuid.uuid4())

        dados[key] = item

        self.__salvar_json(dados)

    def alterar_item(self, key: str, novo_item: json) -> bool:
        dados = self.__carregar_json()

        if key not in dados:
            return False

        dados[key] = novo_item

        self.__salvar_json(dados)

        return True

    def remover_item(self, key: str) -> bool:
        dados = self.__carregar_json()

        if key in dados:
            del dados[key]

            self.__salvar_json(dados)

            return False

        return True
