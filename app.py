import os
from flask import Flask, send_file

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def home():
    # Busca index.html en templates/ o en la raiz del repositorio
    for ruta in ("templates/index.html", "index.html"):
        archivo = os.path.join(BASE, ruta)
        if os.path.exists(archivo):
            return send_file(archivo)
    return "No encuentro index.html en el repositorio", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
