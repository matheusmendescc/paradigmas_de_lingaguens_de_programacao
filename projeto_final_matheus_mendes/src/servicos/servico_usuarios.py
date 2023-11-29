import os

import requests
from flask import Flask, jsonify, request

from src.modulos.persistencia import Persistencia

app = Flask(__name__)
persistencia = Persistencia(f"{os.getcwd()}/../../data/usuarios.json")


# GET ENDPOINT
@app.route("/usuarios", methods=["GET"])
def get_all_users():
    return jsonify(persistencia.carregar_itens())


@app.route("/usuarios/<string:user_id>", methods=["GET"])
def get_user(user_id):
    usuario = persistencia.carregar_item_id(user_id)
    if not usuario:
        return jsonify({"message": "User not found"}), 404

    return jsonify(usuario)


@app.route("/usuarios/<string:user_id>/perfil")
def get_user_profile(user_id):
    usuario = persistencia.carregar_item_id(user_id)

    posts = {}
    try:
        for post_id in usuario['postagens']:
            request = requests.get(f"http://127.0.0.1:5002/postagens/{post_id}")
            posts[post_id] = request.json()

    except (Exception):
        pass

    usuario['postagens'] = posts

    return usuario


# POST ENDPOINT
@app.route("/usuarios/", methods=["POST"])
def adicionar_usuario():
    data = request.get_json()

    if "username" not in data or "nome" not in data or "bio" not in data:
        return jsonify({"message": "Campos obrigatórios: username:str, nome:str, bio:str"}), 400

    data["postagens"] = []

    persistencia.adicionar_item(data)
    return jsonify(data), 201


# PUT ENDPOINT
@app.route("/usuarios/<string:user_id>", methods=["PUT"])
def atualizar_usuario(user_id):
    usuario = persistencia.carregar_item_id(user_id)

    if not usuario:
        return jsonify({"message": "Usuario não encontrado"}), 404

    data = request.get_json()

    if "username" in data:
        usuario["username"] = data["username"]

    if "nome" in data:
        usuario["nome"] = data["nome"]

    if "bio" in data:
        usuario["bio"] = data["bio"]

    persistencia.alterar_item(user_id, usuario)

    return jsonify(usuario), 200


# DELETE ENDPOINT
@app.route("/usuarios/<string:user_id>", methods=["DELETE"])
def remover_usuario(user_id):
    erro = persistencia.remover_item(user_id)

    if erro:
        return jsonify({"message": "Usuario não encontrado"}), 404
    else:
        return jsonify({"message": "Usuário removido com sucesso"}), 200


if __name__ == "__main__":
    app.run(port=5001)
