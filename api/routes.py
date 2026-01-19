from datetime import datetime

from flask import (
    Flask, request, render_template, redirect, url_for,
    make_response, jsonify
)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from .services import *  # mantém como tens (idealmente importar só o que usas)
from configs.settings import API_KEY  # se precisares no middleware


api = Flask(__name__)
CORS(api, supports_credentials=True)

# Necessário para sessões (Flask-Login usa session cookie)
api.config["SECRET_KEY"] = "troca-isto-por-uma-chave-segura"

api.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(api)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(api)
login_manager.login_view = "login"  # endpoint name da rota /login


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)

    password_hash = db.Column(db.String(255), nullable=False)

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=True)

    # Flask-Login verifica .is_active; evitamos conflito com coluna "is_active"
    @property
    def is_active_func(self):
        return self.is_active

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.id} - {self.username}>"


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))


# Swagger UI setup
SWAGGER_URL = "/swagger"
API_SPEC_URL = "/static/swagger.yaml"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_SPEC_URL,
    config={"app_name": "PYXL - API"},
)
api.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@api.get("/token")
def token():
    return jsonify(access_token="abc123")


# (Opcional) Middleware API key – está comentado no teu original
"""
@api.before_request
def check_authentication():
    token = request.headers.get("Authorization")
    if token != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401
"""

# endpoints que NÃO exigem login
PUBLIC_ENDPOINTS = {
    "login",          # /login
    "static",         # /static/...
    # "token",        # se quiseres deixar /token público, descomenta e adiciona aqui
}

@api.before_request
def require_login_globally():
    # Se não houver endpoint (ex.: 404), deixa passar
    if request.endpoint is None:
        return

    # Permite endpoints públicos
    if request.endpoint in PUBLIC_ENDPOINTS:
        return

    # Permite ficheiros estáticos por path (mais robusto)
    if request.path.startswith("/static/"):
        return

    # Se quiseres deixar Swagger público, mantém isto; se quiseres proteger Swagger, remove.
    if request.path.startswith("/swagger") or request.path.startswith("/static/swagger"):
        return

    # Bloqueia tudo o resto se não estiver autenticado
    if not current_user.is_authenticated:
        # Para rotas tipo API, normalmente é melhor devolver 401 em vez de redirect
        if request.path.startswith("/pyxl/") or request.is_json:
            return jsonify({"error": "Unauthorized"}), 401

        # Para páginas HTML, redireciona para o login
        return redirect(url_for("login", next=request.url))


@api.route("/pyxl/write", methods=["PATCH"])
def write():
    data = write_file(request.json)
    return make_response(data, 200)


@api.route("/pyxl/read", methods=["POST"])
def read():
    data = read_file(request.json)
    return make_response(data, 200)


@api.route("/")
def home():
    return redirect("/api")


@api.route("/api")
def index():
    return render_template("options.html")


@api.route("/api/read")
def read_front():
    return render_template("read.html")


@api.route("/api/write")
def write_front():
    return render_template("write.html")


@api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # Garante que o template suporta {{ error }}
        return render_template("login.html", error=None)

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    remember = request.form.get("remember") == "1"

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return render_template("login.html", error="Credenciais inválidas"), 401

    if not user.is_active_func:
        return render_template("login.html", error="Conta desativada"), 403

    login_user(user, remember=remember)
    user.last_login_at = datetime.utcnow()
    db.session.commit()

    return redirect(url_for("protected"))


@api.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@api.route("/protected")
@login_required
def protected():
    return f"Olá, {current_user.username}!"


with api.app_context():
    db.create_all()


if __name__ == "__main__":
    api.run(debug=True)