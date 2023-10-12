import requests
import time
import json
import random


apikey = "cef019bc-7cf1-416a-b95d-6766ebe93695"
# apikey = "57999a7e-de5a-47ec-8e35-7eb7123f0705" # for debug
def getimage(url):
    payload={}
    files={}
    headers = {
    'Authorization': apikey
    }
    filename = str(time.time())+str(random.randrange(10, 1000))+".jpg"
    f = open("static/uploads/"+filename,'wb')
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    f.write(response.content)
    f.close()
    return filename

def callapi(path,type,q,apikey):
    # 理論上不會跑這裡！
    print("callapi:"+path)
    url = "https://saasv2.intemotech.com/saasapi/detect" # 目前打的 API 位置，後面是 detectv1 的是有加上驗證是否付費的 API 位置

    payload={'api_name': json.dumps(type)}
    files=[
    ('file',(str(time.time())+'.jpg',open(path,'rb'),'image/jpeg'))
    ]
    headers = {
    'Authorization': 'Bearer '+apikey
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    q.put({"type":"yolor","data":response.text,"path":path})
    print("callapi:"+path+"end")

def callxcreen(path,type,q,apikey):
    print("callapi:"+path)
    url = "https://saasxcreen.intemotech.com/ai/files"
    # url = 'http://xcreen_dev:54336/ai/files'#for debug
    payload={'api_name': json.dumps(type)}
    files=[
    ('file',(str(time.time())+'.jpg',open(path,'rb'),'image/jpeg'))
    ]
    headers = {
    'Authorization': 'Bearer '+apikey
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    q.put({"type":"xcreen","data":response.text,"path":path})
    print("callapi:"+path+"end")