import requests
import datetime 
def sendMES(message,key='0f313-17b2-4e3d-84b8-3f9c290fa596',NN = None):
    webHookUrl = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={NN}{key}'
    if NN=="MT":
       webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8b7df0c1-bde0-4091-9e11-f77519439823"
    if NN=="MT1":
       webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=461a6eab-90e1-48d9-bb7e-ee91f6e16131"
    if NN=="WT":
        webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=de0c3cc5-d32b-4631-b807-9db3ae44c6df"
    try:
        url=webHookUrl
        headers = {"Content-Type":"application/json"}
        data = {'msgtype':'text','text':{"content":message}}
        res = requests.post(url,json=data,headers=headers)
    except Exception as e:
        print(e)
 