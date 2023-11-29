import os

from flask import Flask, jsonify, request

from src.modulos.persistencia import Persistencia

app = Flask(__name__)
persistencia = Persistencia(f"{os.getcwd()}/../../data/postagens.json")


@app.route("/postagens", methods=["GET"])
def get_itens():
    return jsonify(persistencia.carregar_itens())


@app.route("/postagens/<string:pid>", methods=["GET"])
def get_item(pid):
    postagem = persistencia.carregar_item_id(pid)
    if not postagem:
        return jsonify({"message": "Post not found"}), 404

    return jsonify(postagem)


@app.route("/postagens/usuario/<string:uid>", methods=["GET"])
def get_item_id(uid):
    postagens = persistencia.carregar_itens()
    postagens_uid = {}
    for key in postagens:
        if postagens[key]["uid"] == uid:
            postagens_uid[key] = postagens[key]

    return jsonify(postagens_uid)


# POST ENDPOINT
@app.route("/postagens/", methods=["POST"])
def adicionar_item():
    data = request.get_json()

    if "uid" not in data or "conteudo" not in data:
        return jsonify({"message": "Campos obrigatórios: uid:str, conteudo:str"}), 400

    data["comentarios"] = []

    persistencia.adicionar_item(data)
    return jsonify(data), 201


# PUT ENDPOINT
@app.route("/postagens/<string:pid>", methods=["PUT"])
def atualizar_item(pid):
    postagem = persistencia.carregar_item_id(pid)

    if not postagem:
        return jsonify({"message": "Postagem não encontrada"}), 404

    data = request.get_json()

    if "conteudo" in data:
        postagem["conteudo"] = data["conteudo"]

    persistencia.alterar_item(pid, postagem)

    return jsonify(postagem), 200


# DELETE ENDPOINT
@app.route("/postagens/<string:pid>", methods=["DELETE"])
def remover_item(pid):
    erro = persistencia.remover_item(pid)

    if erro:
        return jsonify({"message": "Postagem não encontrada"}), 404
    else:
        return jsonify({"message": "Postagem removida com sucesso"}), 200


if __name__ == "__main__":
    app.run(port=5002)
