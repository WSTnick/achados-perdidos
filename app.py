from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "chave-local-achados-perdidos"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "achados.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def conectar_banco():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco():
    conexao = conectar_banco()
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL CHECK(tipo IN ('perdido', 'encontrado')),
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            local TEXT NOT NULL,
            contato TEXT NOT NULL,
            imagem TEXT,
            resolvido INTEGER NOT NULL DEFAULT 0,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conexao.commit()
    conexao.close()


def extensao_permitida(nome):
    return "." in nome and nome.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    filtro = request.args.get("filtro", "todos")
    busca = request.args.get("busca", "").strip()

    consulta = "SELECT * FROM itens WHERE 1=1"
    parametros = []

    if filtro in ("perdido", "encontrado"):
        consulta += " AND tipo = ?"
        parametros.append(filtro)

    if busca:
        consulta += """
            AND (
                nome LIKE ? OR
                descricao LIKE ? OR
                local LIKE ?
            )
        """
        termo = f"%{busca}%"
        parametros.extend([termo, termo, termo])

    consulta += " ORDER BY resolvido ASC, criado_em DESC"

    conexao = conectar_banco()
    itens = conexao.execute(consulta, parametros).fetchall()
    conexao.close()

    return render_template(
        "index.html",
        itens=itens,
        filtro=filtro,
        busca=busca
    )


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip()
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        local = request.form.get("local", "").strip()
        contato = request.form.get("contato", "").strip()
        arquivo = request.files.get("imagem")

        if not all([tipo, nome, descricao, local, contato]):
            flash("Preencha todos os campos obrigatórios.", "erro")
            return render_template("cadastrar.html")

        if tipo not in ("perdido", "encontrado"):
            flash("Tipo de item inválido.", "erro")
            return render_template("cadastrar.html")

        nome_imagem = None

        if arquivo and arquivo.filename:
            if not extensao_permitida(arquivo.filename):
                flash("Formato de imagem não permitido.", "erro")
                return render_template("cadastrar.html")

            nome_seguro = secure_filename(arquivo.filename)
            nome_imagem = f"{os.urandom(8).hex()}_{nome_seguro}"
            arquivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nome_imagem))

        conexao = conectar_banco()
        conexao.execute("""
            INSERT INTO itens (tipo, nome, descricao, local, contato, imagem)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tipo, nome, descricao, local, contato, nome_imagem))
        conexao.commit()
        conexao.close()

        flash("Item cadastrado com sucesso!", "sucesso")
        return redirect(url_for("index"))

    return render_template("cadastrar.html")


@app.route("/resolver/<int:item_id>", methods=["POST"])
def resolver(item_id):
    conexao = conectar_banco()
    item = conexao.execute(
        "SELECT resolvido FROM itens WHERE id = ?", (item_id,)
    ).fetchone()

    if item:
        novo_status = 0 if item["resolvido"] else 1
        conexao.execute(
            "UPDATE itens SET resolvido = ? WHERE id = ?",
            (novo_status, item_id)
        )
        conexao.commit()
        flash(
            "Item marcado como resolvido." if novo_status
            else "Item voltou para o mural.",
            "sucesso"
        )

    conexao.close()
    return redirect(request.referrer or url_for("index"))


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)
