URL = 'http://127.0.0.1:8000/place/review/'
import requests
import random

pids = [27312998,
        14575281,
        27398546,
        9648677,
        ]


def addReview(URL):
    params = dict(  kakaoId=random.choice(pids),
                    userId=random.randint(1,15),
                    star=random.randint(4,5),
                    body = "what a place!"
                    )
    response = requests.post(URL, params=params)
    print(response.status_code)

for i in range(300):
    addReview(URL)