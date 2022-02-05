import requests
import base64
from flask import Flask, request
from urllib.parse import urlencode
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)

cors = CORS(app) 


base_url_accounts = "https://accounts.spotify.com/"
base_url = "https://api.spotify.com/v1/"
redirect_uri = "http://99.235.37.139:3000/callback"
client_id = "73d6ad5ecca2451482fb1408eb34e231"
client_secret = "58a58b6409934e87a2d08fba82fa5019"



basic = client_id + ":" + client_secret
base64_byte = base64.urlsafe_b64encode(basic.encode("utf-8"))
basic_64 = str(base64_byte, "utf-8")


error_obj = {"error": True}
def refresh_access(refresh_token):
    url = base_url_accounts + "api/token"

    
    response = requests.post(url, headers={"Authorization": f"Basic {basic_64}"}, data={"grant_type": "refresh_token", "refresh_token": refresh_token})

    if (response.status_code != 200):
        return None
    
    return response.json()["access_token"] 


@app.route("/api/getAuthLink", methods=["GET"])
def getAuthLink():
    url = base_url_accounts + "authorize?"
    url += urlencode(
                {
               "response_type": 'code',
               "client_id": client_id,
               "scope": "user-read-playback-state user-modify-playback-state user-read-private user-read-email",
               "redirect_uri": redirect_uri,
               })
    return json.dumps({"url": url})

@app.route("/api/callback", methods=["POST"])
def callback():
    

    code = json.loads(request.data)
    code = code["code"]
    print(code)
    if (not code):
        return json.dumps(error_obj)

    url = base_url_accounts + "api/token"


    response = requests.post(url, data={"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri}, headers={"Authorization": f"Basic {basic_64}"})

    print(response.json())

    if (response.status_code != 200):
        return json.dumps(error_obj)
    
    refresh_token = response.json()["refresh_token"]


    access_token = refresh_access(refresh_token)
    if (not access_token):
        return json.dumps(error_obj)

    return json.dumps({"access_token": access_token, "refresh_token": refresh_token})



@app.route("/api/get_current_song", methods=["POST"])
def get_current_song():

    refresh_token = json.loads(request.data)["refresh_token"]
    access_token = refresh_access(refresh_token)
    if (not access_token):
        return json.dumps(error_obj)
    url = base_url + "me/player"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})


    print(url)
    print(response.json())

    return json.dumps(response.json())

    
if __name__ == "__main__":
    app.run(debug=True, port=8888, host="0.0.0.0")