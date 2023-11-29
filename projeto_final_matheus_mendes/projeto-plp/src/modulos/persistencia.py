import json
import os
import uuid


class Persistencia:
    __caminho = f"{os.getcwd()}/modulos/../../dados/dados.json"

    def __init__(self) -> None:
        super().__init__()

    def __carregar_json(self) -> json:
        with open(self.__caminho, encoding='utf-8') as file:
            data = json.load(file)
        return data

    def __salvar_json(self, dados: json):
        with open(self.__caminho, 'w', encoding='utf-8') as outfile:
            json.dump(dados, outfile, sort_keys=True, indent=2, ensure_ascii=False)

    def carregar_itens(self, key: str) -> json:
        return self.__carregar_json()[key]

    def carregar_item_id(self, key: str, item_id: str) -> json:
        dados = self.__carregar_json()[key]
        return dados[item_id] if item_id in dados else {}

    def adicionar_item(self, key: str, item: json) -> str:
        dados = self.__carregar_json()

        item_key = str(uuid.uuid4())
        while item_key in dados:
            item_key = str(uuid.uuid4())

        dados[key][item_key] = item

        self.__salvar_json(dados)

        return item_key

    def alterar_item(self, key: str, item_id: str, novo_item: json) -> bool:
        dados = self.__carregar_json()

        if item_id not in dados[key]:
            return False

        dados[key][item_id] = novo_item

        self.__salvar_json(dados)

        return True

    def remover_item(self, key: str, item_id: str) -> bool:
        dados = self.__carregar_json()

        if item_id in dados[key]:
            del dados[key][item_id]

            self.__salvar_json(dados)

            return False

        return True
