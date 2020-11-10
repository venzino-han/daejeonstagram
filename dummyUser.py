import requests
URL = 'http://127.0.0.1:8000/login/regist_user'

response = requests.get(URL)
print(response.status_code )
print(response.text)

def addUser(URL, name, email, pw, gender, birth):
    param = "?userName=%s&userEmail=%s&pw=%s&gender=%s&birth=%s" % (name, email, pw, gender, birth)
    URL += param
    print(URL)
    response = requests.post(URL)
    print(response.text)


# addUser(URL, 'Han', 'han@gmail.com', '321321', '0', '19910808')

names = ['kim2','park2','lee2', 'james2', 'joon2', 'bin2', 'kyli2']
pw, gender, birth = '321321', '1', '20000808'

userData = [ [n, n+'@gmail.com', pw, gender, birth] for n in names]

for d in userData:
    addUser(URL, *d)