import os

from flask import Flask, jsonify, request

from src.modulos.persistencia import Persistencia

app = Flask(__name__)
persistencia = Persistencia(f"{os.getcwd()}/../../data/comentarios.json")


@app.route("/comentarios", methods=["GET"])
def get_itens():
    return jsonify(persistencia.carregar_itens())


@app.route("/comentarios/<string:cid>", methods=["GET"])
def get_item(cid):
    comentario = persistencia.carregar_item_id(cid)
    if not comentario:
        return jsonify({"message": "Comentario not found"}), 404

    return jsonify(comentario)


@app.route("/comentarios/postagem/<string:pid>", methods=["GET"])
def get_item_pid(pid):
    comentarios = persistencia.carregar_itens()

    comentarios_pid = {}
    for key in comentarios:
        if comentarios[key]["pid"] == pid:
            comentarios_pid[key] = comentarios[key]

    return jsonify(comentarios_pid)


# POST ENDPOINT
@app.route("/comentarios/", methods=["POST"])
def adicionar_item():
    data = request.get_json()

    if "uid" not in data or "pid" not in data or "conteudo" not in data:
        return jsonify({"message": "Campos obrigatórios: uid:str, pid:str, conteudo:str"}), 400

    persistencia.adicionar_item(data)
    return jsonify(data), 201


# PUT ENDPOINT
@app.route("/comentarios/<string:cid>", methods=["PUT"])
def atualizar_item(cid):
    comentario = persistencia.carregar_item_id(cid)

    if not comentario:
        return jsonify({"message": "Comentário não encontrado"}), 404

    data = request.get_json()

    if "conteudo" in data:
        comentario["conteudo"] = data["conteudo"]

    persistencia.alterar_item(cid, comentario)

    return jsonify(comentario), 200


# DELETE ENDPOINT
@app.route("/comentarios/<string:cid>", methods=["DELETE"])
def remover_item(cid):
    erro = persistencia.remover_item(cid)

    if erro:
        return jsonify({"message": "Comentario não encontrado"}), 404
    else:
        return jsonify({"message": "Comentario removido com sucesso"}), 200


if __name__ == "__main__":
    app.run(port=5003)
