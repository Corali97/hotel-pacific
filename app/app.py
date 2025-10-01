from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, Tuple
from urllib.parse import parse_qs

from wsgiref.simple_server import make_server

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "reservations.db"
STYLE_PATH = BASE_DIR / "static" / "style.css"

HTML_HEAD = """<!DOCTYPE html>
<html lang=\"es\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>Hotel Pacific</title>
    <link rel=\"stylesheet\" href=\"/static/style.css\" />
  </head>
  <body>
    <header>
      <h1>Hotel Pacific</h1>
      <nav>
        <a href=\"/\">Nueva reserva</a>
        <a href=\"/reservas\">Listado de reservas</a>
      </nav>
    </header>
    <main>
      <section class=\"card\">
"""

HTML_FOOT = """
      </section>
    </main>
    <footer>
      <p>&copy; 2024 Hotel Pacific. Todos los derechos reservados.</p>
    </footer>
  </body>
</html>
"""


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_name TEXT NOT NULL,
                email TEXT NOT NULL,
                check_in DATE NOT NULL,
                check_out DATE NOT NULL,
                guests INTEGER NOT NULL,
                room_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def get_reservations() -> Tuple[Tuple]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT guest_name, email, check_in, check_out, guests, room_type, created_at FROM reservations ORDER BY created_at DESC"
        ).fetchall()
        return tuple(tuple(row[col] for col in row.keys()) for row in rows)


def render_messages(message: str | None, category: str | None) -> str:
    if not message or not category:
        return ""
    return f"<ul class=\"messages\"><li class=\"{category}\">{message}</li></ul>"


def render_form(message: str | None = None, category: str | None = None, data: Dict[str, str] | None = None) -> bytes:
    data = data or {}
    room_type_options = [
        ('estándar', 'Estándar'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
    ]
    room_type_select = '<label for="room_type">Tipo de habitación</label><select id="room_type" name="room_type" required>'
    selected_type = data.get('room_type', '')
    for value, label in room_type_options:
        selected_attr = ' selected="selected"' if selected_type == value else ''
        room_type_select += f'<option value="{value}"{selected_attr}>{label}</option>'
    room_type_select += '</select>'

    content = f"""
        <h2>Formulario de reserva</h2>
        {render_messages(message, category)}
        <form method=\"post\" action=\"/guardar\" class=\"form-grid\">
            <label for=\"guest_name\">Nombre completo</label>
            <input type=\"text\" id=\"guest_name\" name=\"guest_name\" value=\"{data.get('guest_name', '')}\" required />

            <label for=\"email\">Correo electrónico</label>
            <input type=\"email\" id=\"email\" name=\"email\" value=\"{data.get('email', '')}\" required />

            <label for=\"check_in\">Fecha de llegada</label>
            <input type=\"date\" id=\"check_in\" name=\"check_in\" value=\"{data.get('check_in', '')}\" required />

            <label for=\"check_out\">Fecha de salida</label>
            <input type=\"date\" id=\"check_out\" name=\"check_out\" value=\"{data.get('check_out', '')}\" required />

            <label for=\"guests\">Número de huéspedes</label>
            <input type=\"number\" id=\"guests\" name=\"guests\" min=\"1\" value=\"{data.get('guests', '1')}\" required />

            {room_type_select}

            <button type=\"submit\" class=\"primary\">Guardar reserva</button>
        </form>
    """
    print(content)  # Debug: mostrar el HTML generado en la consola
    return (HTML_HEAD + content + HTML_FOOT).encode("utf-8")


def render_reservations() -> bytes:
    reservations = get_reservations()
    if reservations:
        rows_html = "".join(
            f"<tr><td>{name}</td><td>{email}</td><td>{check_in}</td><td>{check_out}</td><td>{guests}</td><td>{room_type}</td><td>{created_at}</td></tr>"
            for name, email, check_in, check_out, guests, room_type, created_at in reservations
        )
        table = f"""
        <h2>Reservas registradas</h2>
        <table>
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Correo</th>
                    <th>Llegada</th>
                    <th>Salida</th>
                    <th>Huéspedes</th>
                    <th>Tipo de habitación</th>
                    <th>Creado</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """
    else:
        table = """
        <h2>Reservas registradas</h2>
        <p>No hay reservas registradas aún. Crea la primera desde el formulario.</p>
        """
    return (HTML_HEAD + table + HTML_FOOT).encode("utf-8")


def parse_post_data(environ) -> Dict[str, str]:
    try:
        size = int(environ.get("CONTENT_LENGTH") or "0")
    except ValueError:
        size = 0
    body = environ["wsgi.input"].read(size).decode("utf-8")
    parsed = parse_qs(body)
    return {k: v[0] for k, v in parsed.items()}


def application(environ, start_response):
    if path == "/dashboard" and method == "GET":
        with open(BASE_DIR / "templates" / "dashboard.html", encoding="utf-8") as f:
            html = f.read()
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]
    if path == "/pagos" and method == "GET":
        with open(BASE_DIR / "templates" / "pagos.html", encoding="utf-8") as f:
            html = f.read()
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]
    init_db()
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET").upper()
    if path == "/reservar" and method == "GET":
        # Obtener el tipo de habitación desde la query string
        query = environ.get("QUERY_STRING", "")
        params = parse_qs(query)
        room_type = params.get("tipo", [""])[0]
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [render_form(data={"room_type": room_type})]

    if path == "/" and method == "GET":
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [render_form()]

    if path == "/reservas" and method == "GET":
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [render_reservations()]

    if path == "/habitaciones" and method == "GET":
        with open(BASE_DIR / "templates" / "rooms.html", encoding="utf-8") as f:
            html = f.read()
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

    if path == "/guardar" and method == "POST":
        data = parse_post_data(environ)
        required = ["guest_name", "email", "check_in", "check_out", "guests", "room_type"]
        if not all(data.get(field, "").strip() for field in required):
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
            return [render_form("Todos los campos son obligatorios.", "error", data)]

        try:
            guests = int(data.get("guests", "1"))
            if guests <= 0:
                raise ValueError
        except ValueError:
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
            return [render_form("El número de huéspedes debe ser un entero positivo.", "error", data)]

        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                INSERT INTO reservations (guest_name, email, check_in, check_out, guests, room_type)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    data["guest_name"].strip(),
                    data["email"].strip(),
                    data["check_in"].strip(),
                    data["check_out"].strip(),
                    guests,
                    data["room_type"].strip(),
                ),
            )

        start_response("303 See Other", [("Location", "/reservas")])
        return [b""]

    if path == "/static/style.css" and method == "GET":
        start_response("200 OK", [("Content-Type", "text/css; charset=utf-8")])
        return [STYLE_PATH.read_bytes()]

    start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Ruta no encontrada"]


def run_server(host: str = "0.0.0.0", port: int = 5000) -> None:
    with make_server(host, port, application) as server:
        print(f"Servidor ejecutándose en http://{host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    run_server()
