import flask
import requests
import base64
from flask import Flask, request
from urllib.parse import urlencode

app = Flask(__name__)

base_url = "https://accounts.spotify.com/"
redirect_uri = "http://localhost:8000/callback"
client_id = "73d6ad5ecca2451482fb1408eb34e231"
@app.route("/", methods=["GET"])
def route():
    url = base_url + "authorize?"
    url += urlencode(
                {
               "response_type": 'code',
               "client_id": client_id,
               "scope": "user-read-playback-state user-modify-playback-state user-read-private",
               "redirect_uri": redirect_uri,
               })
    return f'<a href="{url}">Login to spotify</a>'


@app.route("/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    if (not code):
        return "Error"
    url = base_url + "api/token"


    client_id_b64 = client_id.encode('ascii')
    client_id_b64 = client_id_b64.b64encode(client_id_b64)


    response = requests.post(url, data={"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri}, headers={"Authorization": f"Authorization: Basic <{client_id_b64}:{'58a58b6409934e87a2d08fba82fa5019'}>"})
    return response.text









if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
