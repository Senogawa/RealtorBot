from email import header
import requests
from fake_useragent import UserAgent
import json

url = "https://smartagent.ru/auth/ajax"

if __name__ == "__main__":
    s = requests.Session()
    headers = {
        "user-agent":UserAgent().random
    }
    data = {
        "login":"79017480563",
        "password":"43182",
        "compid":"",
        "fingerprint":"264f832b6e6025c20a49616ad4f51712",
        "timezone":"Europe/Moscow"
        } 

    data1 = {
        "source[current]":"all",
        "source[all][type_status]":"1",
        "source[all][state_status]":"1",
        "section":"1",
        "price[type]":"all",
        "price[from]":"100000",
        "price[to]":"",
        "stage":"all",
        "mode":"list",
        "status":"active",
        "page":"1",
        "force":"1",
        "region":"1",
        "quantity":"40"
    }

    req = s.post(url,data=data, headers=headers)
    print(s.cookies)
    s.cookies.set("pushdealer_token","8pxry1kgfy")
    s.cookies.set("pushdealer_permission","denied")
    print(s.cookies)
    headers1 = {
        "user-agent":UserAgent().random,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        #"Content-Type": "multipart/form-data; boundary=---------------------------793856791064077589889787832688",
        #"Content-Length": "183",
        "Origin": "https://smartagent.ru",
        "Cookie": f"pushdealer_token=8pxry1kgfy; pushdealer_permission=denied; PHPSESSID={s.cookies['PHPSESSID']}",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cache-Control": "max-age=0",
        "Host": "smartagent.ru",
        "TE": "trailers"
        
    }
    # files = {
    #     "user_id":"293536"000000
    # }
    req = s.post("https://smartagent.ru/search2/search", headers=headers1, data = data1)
    with open("gg.json","w") as f:
        json.dump(req.json(), f, ensure_ascii=False)
    print(req.json())