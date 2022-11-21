from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)


class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(240), unique=True, nullable=False)

    def __init__(self, titulo, descricao):
        self.titulo = titulo
        self.descricao = descricao


db.create_all()


@app.route("/anuncios/<id>", methods=["GET"])
def get_anuncio(id):
    item = Anuncio.query.get(id)
    del item.__dict__["_sa_instance_state"]
    return jsonify(item.__dict__)


@app.route("/anuncios", methods=["GET"])
def get_anuncios():
    anuncios = []
    for anuncio in db.session.query(Anuncio).all():
        del anuncio.__dict__["_sa_instance_state"]
        anuncios.append(anuncio.__dict__)
    return jsonify(anuncios)


@app.route("/anuncios", methods=["POST"])
def create_anuncio():
    body = request.get_json()
    db.session.add(Anuncio(body["titulo"], body["descricao"]))
    db.session.commit()
    return "Anúncio criado!"


@app.route("/anuncios/<id>", methods=["PUT"])
def update_anuncio(id):
    body = request.get_json()
    db.session.query(Anuncio).filter_by(id=id).update(
        dict(title=body["titulo"], content=body["descricao"])
    )
    db.session.commit()
    return "Anúncio atualizado!"


@app.route("/anuncios/<id>", methods=["DELETE"])
def delete_anuncio(id):
    db.session.query(Anuncio).filter_by(id=id).delete()
    db.session.commit()
    return "Anúncio deletado!"
