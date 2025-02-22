from datetime import datetime
import matplotlib
from matplotlib import pyplot as plt
import pandas

"""
__atributosLog__

time="2025-02-10T12:00:05+00:00"
ip="128.201.57.52"
req="GET/j/eyJhbGciOiJSUzUxMiIsImtpZCI6IjEiLCJ0eXAiOiJKV1QifQ.eyJjb3VudHJ5X2NvZGUiOiJCUiIsImRvbWFpbiI6ImxpdmUtY20tYWgtMTEtMDMudmlkZW8uZ2xvYm8uY29tIiwiZXhwIjoxNzM5MjY3NzQ4LCJpYXQiOjE3MzkxODEzNDgsImlzcyI6InBsYXliYWNrLWFwaS1wcm9kLWdjcCIsIm93bmVyIjoiZDc0MzJlZjAtYmI4NS00NjllLThkZDMtZGE5NGExMGE3MjY5IiwicGF0aCI6Ii9udS9mKGE9YXVkaW9fMSxkdnI9MTIwLGhscz0zLGk9Mix2PXZpZGVvKS9nbG9iby1yai9wbGF5bGlzdC5tM3U4In0.nqg4OPvuS_TjGYUxQS25dpQRA34dhbLRXDSnk7ypZgi1RkXzfBdKUfx_ADKG8tisIFho81Y5Xs8RaO8hKzoJpWwbG0WnoDFystKbsYNbqfZS2_zBG6r21W9xYILIdz9BhwoJhoY6u3M2nQBrDe1K_4Rc-eSItEggYowiYuG9xXR652iaUA_8pLCvgtexw-ZUBm5b6wHiSQQa7H0T5BNsSOjwqCl3HqClg3T9Yh6SezLVQK-V1rOLRk5CCnzSYgIYR8neISaw3l09zrqxgEGoo6SskdVM8fYdAM7jmsVXXCgGRAci3Kufhl11Hcj3P3fP_rEieTC0kHmTur9qVrwilA/nu/f(a=audio_1,dvr=120,hls=3,i=2,v=video)/globo-rj/globo-rj-audio1=128000-video=5512000.m3u8?hls_client_manifest_version=3&dvr_window_length=120 HTTP/1.1"
status="200"
req_time="0.000"
bytes_sent="3420"
up_cache_status="HIT"
up_status="-"
up_addr="-"
up_server="cmah11lb34.globoi.com,cmah07lb35.globoi.com,cmad06lb25.globoi.com"
up_resp_time="-"
up_servers=""
ref="-"
ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.77.34.5 Safari/537.36 QJY/2.0 PHILCO_PTV42G10N5SKF_DRM DID/F4Ed5f7f17c9 PTK5.1 NETRANGEMMH"
fwd_for="-"
req_id="9c965e6f33c0603687779c665c62b8c1"
scheme="http" host="live-cm-ah-11-03.video.globo.com"
fe_host="-"
port="80"
cache_key=""
cc="BR"
user="d7432ef0-bb85-469e-8dd3-da94a10a7269"
media="globo-rj"
transaction_id="-"

"""

class logG():
    def __init__(self, time:str, ip:str,req_time:str,rq_id,user:str,port:int,media:str,transaction_id:str):
        self.time = datetime.fromisoformat(time)
        self.ip = ip
        self.rq_time = req_time
        self.rq_id = rq_id
        self.user = user
        self.port = port
        self.media = media
        self.transaction_id = transaction_id

    def toString(self)->str:
        s = f"user : {self.user}\nip : {self.ip}\ntime : {self.time}\nrq_time : {self.rq_time}\nrq_id : {self.rq_id}\nport : {self.port}\nmedia : {self.media}\ntransaction_id : {self.transaction_id}"
        return s


def lerLogs(arq:str)->list[logG]:
    tmp = {}
    logs:list[logG] = []
    with open(arq, 'r') as arquivo:
        for l in arquivo:
            elm = l.split("\" ")
            for i in elm:
                k = i.split('=\"')
                tmp[k[0]] = k[1]
            print(tmp['time'])
            logs.append(logG(tmp['time'],tmp['ip'],tmp['req_time'],tmp['req_id'],tmp['user'],int(tmp['port']),tmp['media'],tmp['transaction_id']))
            tmp = {}
    return logs

def countReq(logs:list[logG]):
    users = {}
    for i in logs:
        try:   
            users[i.user][0] += 1
            users[i.user][1].append(i.rq_id)
        except:
            users[i.user] = (1,[i.rq_id])
    return users

def plotTotalTime(logs:list[logG])->None:
    map = {}
    for log in logs:
        try:
            map[log.user][1] = log.time
        except:
            map[log.user] = (log.time, log.time)
    users = list(map.keys())
    time = [(map[i][1] - map[i][0]).total_seconds() for i in users]
    
    plt.figure()
    plt.bar(users, time)
    plt.xlabel("Users")
    plt.ylabel("Tempo total")
    plt.title("Data")
    plt.suptitle('Tempo total por usuário')
    plt.show()

if __name__== '__main__':
    logs = lerLogs('teste.log')
    #for log in logs:
    #    print(log.toString())
    #us = countReq(logs)
    #for i in us.keys():
    #    print(f"user_id = ({i}), total = ({us[i][0]}), rq_ids = ({us[i][1]})")
    plotTotalTime(logs)