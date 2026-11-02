from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "stock.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            min_stock INTEGER NOT NULL DEFAULT 0,
            unit_price REAL NOT NULL DEFAULT 0,
            supplier TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('entry','exit')),
            quantity INTEGER NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
        """
    )
    conn.commit()
    conn.close()


def serialize_product(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "quantity": row["quantity"],
        "min_stock": row["min_stock"],
        "unit_price": row["unit_price"],
        "supplier": row["supplier"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def serialize_movement(row):
    return {
        "id": row["id"],
        "product_id": row["product_id"],
        "product_name": row["product_name"],
        "type": row["type"],
        "quantity": row["quantity"],
        "notes": row["notes"],
        "created_at": row["created_at"],
    }


def create_app():
    app = Flask(__name__)

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "database": str(DB_PATH)})

    @app.route("/api/products")
    def list_products():
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
        conn.close()
        return jsonify([serialize_product(row) for row in rows])

    @app.route("/api/products", methods=["POST"])
    def create_product():
        payload = request.get_json(silent=True) or {}
        required = ["name", "category", "quantity", "min_stock", "unit_price", "supplier"]
        missing = [field for field in required if field not in payload]
        if missing:
            return jsonify({"error": f"Campos obrigatórios ausentes: {', '.join(missing)}"}), 400

        try:
            name = str(payload["name"]).strip()
            category = str(payload["category"]).strip()
            supplier = str(payload["supplier"]).strip()
            quantity = int(payload["quantity"])
            min_stock = int(payload["min_stock"])
            unit_price = float(payload["unit_price"])
        except (TypeError, ValueError):
            return jsonify({"error": "Valores numéricos inválidos."}), 400

        if not name or not category or not supplier:
            return jsonify({"error": "Nome, categoria e fornecedor são obrigatórios."}), 400

        conn = get_db_connection()
        cursor = conn.execute(
            """
            INSERT INTO products (name, category, quantity, min_stock, unit_price, supplier)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, category, quantity, min_stock, unit_price, supplier),
        )
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({"id": product_id, "message": "Produto criado com sucesso"}), 201

    @app.route("/api/products/<int:product_id>", methods=["PUT"])
    def update_product(product_id):
        payload = request.get_json(silent=True) or {}
        if not payload:
            return jsonify({"error": "Corpo da requisição inválido."}), 400

        conn = get_db_connection()
        existing = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if existing is None:
            conn.close()
            return jsonify({"error": "Produto não encontrado."}), 404

        name = str(payload.get("name", existing["name"])).strip()
        category = str(payload.get("category", existing["category"])).strip()
        supplier = str(payload.get("supplier", existing["supplier"])).strip()
        quantity = int(payload.get("quantity", existing["quantity"]))
        min_stock = int(payload.get("min_stock", existing["min_stock"]))
        unit_price = float(payload.get("unit_price", existing["unit_price"]))

        conn.execute(
            """
            UPDATE products
            SET name = ?, category = ?, quantity = ?, min_stock = ?, unit_price = ?, supplier = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (name, category, quantity, min_stock, unit_price, supplier, product_id),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Produto atualizado com sucesso."})

    @app.route("/api/products/<int:product_id>", methods=["DELETE"])
    def delete_product(product_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM movements WHERE product_id = ?", (product_id,))
        cursor = conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({"error": "Produto não encontrado."}), 404
        return jsonify({"message": "Produto excluído."})

    @app.route("/api/products/<int:product_id>/movement", methods=["POST"])
    def movement(product_id):
        payload = request.get_json(silent=True) or {}
        movement_type = str(payload.get("type", "")).strip().lower()
        quantity = payload.get("quantity")
        notes = payload.get("notes", "")

        if movement_type not in {"entry", "exit"}:
            return jsonify({"error": "Tipo da movimentação deve ser 'entry' ou 'exit'."}), 400

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return jsonify({"error": "Quantidade inválida."}), 400

        if quantity <= 0:
            return jsonify({"error": "Quantidade deve ser maior que zero."}), 400

        conn = get_db_connection()
        product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if product is None:
            conn.close()
            return jsonify({"error": "Produto não encontrado."}), 404

        current_quantity = int(product["quantity"])
        next_quantity = current_quantity + quantity if movement_type == "entry" else current_quantity - quantity
        if next_quantity < 0:
            conn.close()
            return jsonify({"error": "Quantidade final negativa não permitida."}), 400

        conn.execute(
            "INSERT INTO movements (product_id, type, quantity, notes) VALUES (?, ?, ?, ?)",
            (product_id, movement_type, quantity, notes),
        )
        conn.execute(
            "UPDATE products SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (next_quantity, product_id),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Movimentação registrada com sucesso."})

    @app.route("/api/movements")
    def list_movements():
        conn = get_db_connection()
        rows = conn.execute(
            """
            SELECT m.*, p.name AS product_name
            FROM movements m
            INNER JOIN products p ON p.id = m.product_id
            ORDER BY m.created_at DESC
            """
        ).fetchall()
        conn.close()
        return jsonify([serialize_movement(row) for row in rows])

    @app.route("/api/summary")
    def summary():
        conn = get_db_connection()
        total_products = conn.execute("SELECT COUNT(*) AS total FROM products").fetchone()["total"]
        total_quantity = conn.execute("SELECT COALESCE(SUM(quantity), 0) AS total FROM products").fetchone()["total"]
        low_stock = conn.execute("SELECT COUNT(*) AS total FROM products WHERE quantity <= min_stock").fetchone()["total"]
        inventory_value = conn.execute(
            "SELECT COALESCE(SUM(quantity * unit_price), 0) AS total FROM products"
        ).fetchone()["total"]
        conn.close()

        return jsonify({
            "total_products": total_products,
            "total_quantity": total_quantity,
            "low_stock": low_stock,
            "total_value": float(inventory_value),
        })

    @app.route("/api/products/reset", methods=["POST"])
    def reset_products():
        conn = get_db_connection()
        conn.execute("DELETE FROM movements")
        conn.execute("DELETE FROM products")
        conn.commit()
        conn.close()
        return jsonify({"message": "Dados resetados com sucesso."})

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_static(path):
        if path and not path.startswith("api"):
            file_path = BASE_DIR / path
            if file_path.is_file():
                return send_from_directory(BASE_DIR, path)
        return send_from_directory(BASE_DIR, "index.html")

    return app


app = create_app()

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
