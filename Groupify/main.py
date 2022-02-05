import flask
import requests
from flask import Flask


app = Flask(__name__)


@app.route("/", methods=["GET"])
def route():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
