import requests

headers = {
    'Authorization': 'eff6b9db75af19556d695435d94c3384f1a0548263fbb67ce717209cfaabf141d417b2b4b542e4dd0d8e85339a2b4ee8',
}

url = 'https://api.switch-bot.com/v1.1/devices'
response = requests.get(url, headers=headers)
print(response.json())
