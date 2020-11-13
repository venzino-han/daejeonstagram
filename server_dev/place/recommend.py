import requests
import os

def getNearPlace(x,y,keyword):
    print(os.getcwd())
    with open('../kakaoKey.txt', 'r', encoding='utf-8') as f:
        rest_api_key = f.read().strip()
    header = {'Authorization': 'KakaoAK ' + rest_api_key}
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    params = dict(x=x, y=y,radius=500, query= keyword)
    r = requests.get(url, headers=header, params=params)

    items = []

    if r.status_code == 200:
        for item in r.json()['documents']:
            if '대전' in item['address_name']:
                items.append(item)
    else:
        return "ERROR[" + str(r.status_code) + "]"

    items = sorted(items, key=lambda x: int(x['distance']))

    if len(items) > 20 :
        items= items[:20]

    return items


# items = getNearPlace(127.3811,36.3542,"약국")
# for i in items:
#     print(i)