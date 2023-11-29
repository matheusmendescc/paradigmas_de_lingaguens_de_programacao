import os

import requests
from flask import Flask, render_template

from src.modulos.persistencia import Persistencia

app = Flask(__name__)
persistencia = Persistencia(f"{os.getcwd()}/../../data/usuarios.json")


@app.route("/", methods=["GET"])
def get_feed():

    try:
        requests.get(f"http://127.0.0.1:5001/usuarios").json()
        usuarios = True
    except Exception:
        usuarios = False

    try:
        requests.get(f"http://127.0.0.1:5002/postagens").json()
        postagens = True
    except Exception:
        postagens = False

    try:
        requests.get(f"http://127.0.0.1:5003/comentarios").json()
        comentarios = True
    except Exception:
        comentarios = False

    return render_template('index.html', application=True, usuarios=usuarios, postagens=postagens, comentarios=comentarios)


@app.route("/feed", methods=["GET"])
def get_sobre():
    posts = []

    try:
        posts = requests.get(f"http://127.0.0.1:5002/postagens").json()

        for key in posts:
            posts[key]["usuario"] = requests.get(f"http://127.0.0.1:5001/usuarios/{posts[key]['uid']}").json()
            posts[key]["num_comentarios"] = len(posts[key]["comentarios"])
    except Exception:
        pass

    return render_template('feed.html', posts=posts)


@app.route("/perfil/<string:uid>", methods=["GET"])
def get_perfil(uid):
    perfil = {}
    postagens = []

    try:
        perfil = requests.get(f"http://127.0.0.1:5001/usuarios/{uid}").json()
        perfil["num_comentarios"] = len(perfil["postagens"])

    except Exception:
        pass

    try:
        postagens = requests.get(f"http://127.0.0.1:5002/postagens/usuario/{uid}").json()

        for key in postagens:
            postagens[key]["num_comentarios"] = len(postagens[key]["comentarios"])
    except Exception:
        pass

    return render_template('profile.html', perfil=perfil, postagens=postagens)


@app.route("/postagem/<string:pid>", methods=["GET"])
def get_postagem(pid):
    postagem = {}
    comentarios = {}

    try:
        postagem = requests.get(f"http://127.0.0.1:5002/postagens/{pid}").json()
        postagem["usuario"] = requests.get(f"http://127.0.0.1:5001/usuarios/{postagem['uid']}").json()

    except Exception:
        pass

    try:
        comentarios = requests.get(f"http://127.0.0.1:5003/comentarios/postagem/{pid}").json()
    except Exception:
        pass

    for key in comentarios:
        try:
            comentarios[key]["usuario"] = requests.get(
                f"http://127.0.0.1:5001/usuarios/{comentarios[key]['uid']}").json()
        except Exception:
            pass

    return render_template('postagem.html', postagem=postagem, comentarios=comentarios,
                           num_comentarios=len(comentarios))


if __name__ == "__main__":
    app.run(port=5000)
