import os

from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory, jsonify
from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import HTTPException

from backend.config import get_config
from backend.extensions import db, jwt


def create_app() -> Flask:
    load_dotenv()

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.config.update(get_config())

    db.init_app(app)
    jwt.init_app(app)

    # Register REST blueprints
    from backend.routes.auth_routes import auth_bp
    from backend.routes.item_routes import item_bp
    from backend.routes.status_routes import status_bp
    from backend.routes.admin_routes import admin_bp
    from backend.routes.me_routes import me_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(me_bp)

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename: str):
        # Uploads are stored inside backend/uploads by config
        upload_dir = app.config["UPLOAD_FOLDER"]
        return send_from_directory(upload_dir, filename)

    # -------- Frontend routes (minimal pages) --------
    @app.route("/")
    def index_page():
        return render_template("index.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/register")
    def register_page():
        return render_template("register.html")

    @app.route("/report/lost")
    def report_lost_page():
        return render_template("report_lost.html")

    @app.route("/report/found")
    def report_found_page():
        return render_template("report_found.html")

    @app.route("/dashboard")
    def dashboard_page():
        # Dashboard relies on JWT stored in localStorage
        return render_template("dashboard.html")

    @app.route("/admin")
    def admin_page():
        return render_template("admin.html")

    # Helpful default error shape for the frontend
    @app.errorhandler(404)
    def not_found(_err):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(HTTPException)
    def handle_http_exception(err: HTTPException):
        # Keep a consistent JSON error shape for the REST API.
        # Frontend pages that are served from templates can still show their own errors.
        return jsonify({"error": err.description or "Request failed"}), err.code or 400

    with app.app_context():
        # Creates tables on startup (works for SQLite dev; for production use migrations).
        # Import models first so SQLAlchemy registers them.
        import backend.models  # noqa: F401
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=app.config.get("DEBUG", True))

