import urllib.request

url = "http://uta.pw/shodou/img/28/214.png"
savename = "test.png"

print("保存します")
urllib.request.urlretrieve(url,savename)
print("保存しました")