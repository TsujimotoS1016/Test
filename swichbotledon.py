import requests # type: ignore
import time
import uuid
import hmac
import hashlib
import base64
import json

# トークンとシークレット
token = 'eff6b9db75af19556d695435d94c3384f1a0548263fbb67ce717209cfaabf141d417b2b4b542e4dd0d8e85339a2b4ee8'
secret = 'a31ca16a806b0112a2e52ee3491d5276'

# ヘッダー生成
nonce = str(uuid.uuid4())
t = str(int(round(time.time() * 1000)))
string_to_sign = (token + t + nonce).encode('utf-8')
secret_bytes = secret.encode('utf-8')
sign = base64.b64encode(hmac.new(secret_bytes, string_to_sign, hashlib.sha256).digest()).decode('utf-8')

headers = {
    'Authorization': token,
    't': t,
    'sign': sign,
    'nonce': nonce,
    'Content-Type': 'application/json; charset=utf8'
}

# 操作対象デバイスとコマンド
url = 'https://api.switch-bot.com/v1.1/devices/02-202404141055-53447619/commands'
payload = {
    "command": "turnOn",  # または open/close/press など
    "parameter": "default",
    "commandType": "command"
}

response = requests.post(url, headers=headers, json=payload)

# レスポンス確認
print(response.status_code)
print(response.json())
