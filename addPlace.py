import requests

def getLatLng(params):
    result = ""
    # url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    #url = "https://dapi.kakao.com/v2/local/search/keyword.json?y=36.3542446&x=127.3754091&radius=10000&query=약국"
    with open('kakaoKey.txt', 'r') as f:
        rest_api_key = f.read().strip()
    header = {'Authorization': 'KakaoAK ' + rest_api_key}

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    r = requests.get(url, headers=header, params=params)

    items =[]

    if r.status_code == 200:
        print(r.json()['documents'][0].keys())
        for item in r.json()['documents']:
            if '대전' in item['address_name']:
                print(item['address_name']+" : "+ item['place_name'])
                print(item['id'])
                print(item['x'], item['y'])
                items.append(item)
    else:
        return "ERROR[" + str(r.status_code) + "]"

    return items



params = dict(y=36.3542446,
              x=127.3754091,
              radius=10000,
              query= "약국"
              )

# 카카오 REST API로 좌표 구하기
items = getLatLng(params)

URL = 'http://127.0.0.1:8000/place/'

def addPlace(URL, kakaoId, placeName, url, lat, lon, regUserId, body):
    # param = "?kakaoId=%s&placeName=%s&url=%s&lat=%s&lon=%s&regUserId=%s&body=%s" % (kakaoId, placeName, url, lat, lon, regUserId, body)
    params = dict(
                    kakaoId=kakaoId,
                    placeName=placeName,
                    url=url,
                    lat = lat,
                    lon = lon,
                    regUserId = regUserId,
                    body = body
                    )
    response = requests.post(URL, params=params)
    print(response.status_code)

import random

placeData = [[item['id'], item['place_name'], item['place_url'], round(float(item['y']),4), round(float(item['x']),4), random.randint(1,15), item['address_name'] ] for item in items]

for p in placeData:
    addPlace(URL, *p)