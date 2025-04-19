import asyncio
import sys
import time
from datetime import datetime,timedelta
import orjson
import aiohttp
import requests
import psutil
import socket
import os
import jwt
import ssl
import multiprocessing as mp
from aiohttp import web
from db_info import *
from mysql_query_builder import *
from read_creds import read
CREDS=read()
HUBDBI=getDbInstance(user=CREDS['localhost']['user'],
                     password=CREDS['localhost']['password'])
HOSTNAME=socket.gethostname()
HOST=socket.gethostbyname(HOSTNAME)
PID=os.getpid()
PPID=os.getppid()
with open('./key_private') as fl:
    PRIVATE_KEY=fl.read()
with open('./key_public') as fl:
    PUBLIC_KEY=fl.read()
def get_user_info(USER_INFO):
    t1=HUBDBI.hub.users
    t2=HUBDBI.hub.user_perms
    sq1=Select(t1.uid,t1.name,t1.ip,t1.expiry).str()
    sq2=Select(t2.uid,t2.perm).str()
    while True:
        user_perms={}
        try:
            crs=HUBDBI.query(sq2,cursor='dict')
        except Exception:
            traceback.print_exc()
            time.sleep(2)
            continue
        for d in crs:
            uid=d['uid']
            user_perms[uid]=user_perms.get(uid) or set()
            user_perms[uid].add(d['perm'])
        try:
            crs=HUBDBI.query(sq1,cursor='dict')
        except Exception:
            traceback.print_exc()
            time.sleep(2)
            continue
        known=set()
        for d in crs:
            d['perms']=user_perms.get(d['uid']) or set()
            known.add(d['ip'])
            known.add(d['uid'])
            USER_INFO[d['ip']]=d
            USER_INFO[d['uid']]=d
        for k in list(USER_INFO.keys()):
            if not k in known:
                del USER_INFO[k]
        time.sleep(2)
def get_routing_info(ROUTING_INFO,ROUTING_COUNTS,USER_ROUTING_INFO):
    t1=HUBDBI.web_ms.ms
    t2=HUBDBI.web_ms.routing
    t3=HUBDBI.web_ms.user_routing
    sq2=Select(t2.ms,t2.host,t2.port,t1.requiredPerm).str()
    sq3=Select(t3.uid,t3.ms,t3.host,t3.port,t3.time)\
        .where(t3.time.ge(datetime.now()-timedelta(minutes=60))).str()
    while True:
        try:
            crs=HUBDBI.query(sq2,cursor='dict')
        except Exception:
            traceback.print_exc()
            time.sleep(2)
            continue
        routing={}
        for d in crs:
            url=d['ms']
            routing[url]=routing.get(url) or {'requiredPerm':d['requiredPerm'],'addresses':[]}
            hp=(d['host'],d['port'])
            routing[url]['addresses'].append(hp)
            ROUTING_COUNTS[hp]=0
        for url in routing:
            ROUTING_INFO[url]=routing[url]
        try:
            crs=HUBDBI.query(sq3,cursor='dict')
        except Exception:
            traceback.print_exc()
            time.sleep(2)
            continue
        for d in crs:
            hp=(d['host'],d['port'])
            ROUTING_COUNTS[hp]+=1
            USER_ROUTING_INFO[(d['uid'],d['ms'])]=d
        time.sleep(2)
def get_idlest(ROUTING_INFO,ROUTING_COUNTS,url):
    mn=10e10
    mnHp=None
    for hp in ROUTING_INFO[url]['addresses']:
        if hp=='meta':continue
        if ROUTING_COUNTS[hp]<mn:
            mn=ROUTING_COUNTS[hp]
            mnHp=hp
    return {'host':mnHp[0],'port':mnHp[1]}
def logger(qu):
    t1=HUBDBI.usage_log.t
    t2=HUBDBI.web_ms.user_routing
    while True:
        kwa=qu.get()
        now=datetime.now()
        ym=(now.year,now.month)
        if kwa['type']=='user_routing':
            sq=Insert(t2.uid,t2.ms,t2.host,t2.port,t2.time).values([
                kwa['uid'],kwa['url'],kwa['host'],kwa['port'],SQL.now(),
            ]).on_duplicate_update(t2.host,t2.port,t2.time).str()
        elif kwa['type']=='request_error':
            sq=Insert(t1.uid,t1.url,t1.fullUrl,t1.time,t1.host,t1.port,
                      t1.responseTime,t1.body,t1.error).values([
                kwa['uid'],kwa['baseUrl'],kwa['url'],SQL.now(),
                kwa['host'],kwa['port'],kwa['responseTime'],kwa['body'],kwa['error']
            ]).str(ym)
        elif kwa['type']=='request_result':
            sq=Insert(t1.uid,t1.url,t1.fullUrl,t1.time,t1.host,t1.port,t1.
                      responseSize,t1.responseTime,t1.body).values([
                kwa['uid'],kwa['baseUrl'],kwa['url'],SQL.now(),
                kwa['host'],kwa['port'],kwa['responseSize'],
                kwa['responseTime'],kwa['body'],
            ]).str(ym)
        else:
            print(f"unknown logger type {kwa['type']}")
            continue
        try:
            HUBDBI.query(sq)
        except Exception as e:
            print(e)
def get_network_usage(PORT):
    UPDATE_DELAY=2
    io=psutil.net_io_counters()
    bytes_sent,bytes_recv=io.bytes_sent,io.bytes_recv
    t1=HUBDBI.network_traffic.t
    while True:
        now=datetime.now()
        ym=(now.year,now.month)
        time.sleep(UPDATE_DELAY)
        io_2=psutil.net_io_counters()
        sent=io_2.bytes_sent-bytes_sent
        recv=io_2.bytes_recv-bytes_recv
        # print(f"Upload: {sent}, Download: {recv}")
        bytes_sent,bytes_recv=io_2.bytes_sent,io_2.bytes_recv
        sq=Insert(t1.hostname,t1.host,t1.port,t1.time,t1.pid,t1.upload,t1.download).values([
            HOSTNAME,HOST,PORT,SQL.now(),PPID,sent,recv
        ]).str(ym)
        HUBDBI.query(sq)
def set_token_cookie(resp:web.Response,token):
    resp.set_cookie(
        'access_token',
        token,
        httponly=True,
        secure=True
    )
async def handler(req:web.Request,MANAGER):
    timer=time.time()
    aip=req.remote
    print('[+]',aip)
    url=str(req.rel_url)
    print('[+]',aip,url)
    if url=='/': url='/home'
    baseUrl=url.lstrip('/').split('/')[0]
    logger=lambda e:LOGGING_QU.put({
            'type':'request_error',
            'uid':'unknown',
            'url':url,
            'baseUrl':baseUrl,
            'host':None,
            'port':None,
            'body':None,
            'error':e,
            'responseTime':time.time()-timer,
        })

    if aip in {
        '92.255.57.58',
        '81.229.41.66',
        '216.10.250.218',
    }:
        m='hello, bye'
        logger('blocked user')
        return web.Response(status=401,reason=m,body=m)
    user_info=MANAGER['USER_INFO'].get(aip) or {}
    uid=user_info.get('uid')
    if not user_info:
        user_info={
            'expiry':(datetime.now()+timedelta(hours=1)),
            'perms':set()
        }
        uid='unknown|'+aip
    print('[+]',uid)

    ROUTING_INFO=MANAGER['ROUTING_INFO']
    if not uid and False:
        m='unauthorized user'
        logger(m)
        return web.Response(status=401,reason=m,body=m)
    if baseUrl=='/favicon.ico':
        m='no favicon'
        logger(m)
        return web.Response(status=400,reason=m,body=m)
    elif user_info is None:
        m='no user found'
        logger(m)
        return web.Response(status=401,reason=m,body=m)
    elif datetime.now()>user_info['expiry']:
        m='user authorization expired'
        logger(m)
        return web.Response(status=401,reason=m,body=m)
    elif url not in ROUTING_INFO:
        m=f'no routing info for {url}'
        logger(m)
        return web.Response(status=400,reason=m,body=m)
    elif ROUTING_INFO[url]['requiredPerm']\
            and ROUTING_INFO[url]['requiredPerm'] not in user_info['perms']:
        m='user does not have required permissions'
        logger(m)
        return web.Response(status=401,reason=m,body=m)
    else:
        ri=MANAGER['USER_ROUTING_INFO'].get((uid,url))
        if not ri: ri=get_idlest(ROUTING_INFO,MANAGER['ROUTING_COUNTS'],url)
        MANAGER['USER_ROUTING_INFO'][(uid,url)]=ri
        LOGGING_QU.put({
            'type':'user_routing',
            'uid':uid,
            'url':url,
            'baseUrl':baseUrl,
            'host':ri['host'],
            'port':ri['port'],
        })
        newToken=jwt.encode({
            'uid':uid,
            'iat':datetime.now().timestamp(),
            'exp':(datetime.now()+timedelta(hours=1)).timestamp(),
        },PRIVATE_KEY,algorithm='RS256')
        # oldToken=req.cookies.get('access_token')
        # decodedOldToken=jwt.decode(oldToken,key=PUBLIC_KEY,algorithms=['RS256'])
        # print(decodedOldToken)
        # if decodedOldToken['uid']!=uid:
        #     LOGGING_QU.put({
        #         'type':'request_error',
        #         'uid':uid,
        #         'url':url,
        #         'baseUrl':baseUrl,
        #         'host':ri['host'],
        #         'port':ri['port'],
        #         'body':None,
        #         'error':'invalid token',
        #         'responseTime':time.time()-timer,
        #     })
        #     m='invalid token'
        #     return web.Response(status=401,reason=m,body=m)
        rl=f"http://{ri['host']}:{ri['port']}{url}"
        print('[+]',aip,rl,)
        async with aiohttp.ClientSession() as session:
            if baseUrl=='home':
                resp:web.Response=await session.get(rl)
                reqBody={}
            else:
                reqBody=await req.json()
                resp:web.Response=await session.post(rl,body=reqBody)
            if resp.status!=200:
                LOGGING_QU.put({
                    'type':'request_error',
                    'uid':uid,
                    'url':url,
                    'baseUrl':baseUrl,
                    'host':ri['host'],
                    'port':ri['port'],
                    'body':reqBody,
                    'error':resp.reason,
                    'responseTime':time.time()-timer,
                })
                reqResp=web.Response(status=resp.status,reason=resp.reason,body=resp.reason)
                set_token_cookie(reqResp,newToken)
                return reqResp
            else:
                mimeType=resp.content_type
                if mimeType=='application/json':
                    respBody=await resp.json()
                    respBody=orjson.dumps(respBody)
                else:
                    respBody=await resp.text()
                LOGGING_QU.put({
                    'type':'request_result',
                    'uid':uid,
                    'url':url,
                    'baseUrl':baseUrl,
                    'host':ri['host'],
                    'port':ri['port'],
                    'body':reqBody,
                    'mimeType':mimeType,
                    'responseTime':time.time()-timer,
                    'responseSize':len(respBody),
                })
                reqResp=web.Response(body=respBody,content_type=mimeType)
                set_token_cookie(reqResp,newToken)
                return reqResp
async def start_server():
    global LOGGING_QU
    if len(sys.argv)>1:
        bind_port=int(sys.argv[1])
    else:
        bind_port=443
        # bind_port=80
    bind_ip="0.0.0.0"
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    except AttributeError:
        traceback.print_exc()
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    sock.bind((bind_ip,bind_port))
    print(f"[+] Listening on port {bind_ip} : {bind_port}")

    manager=mp.Manager()
    MANAGER=manager.dict()
    USER_INFO=MANAGER['USER_INFO']=manager.dict()
    ROUTING_INFO=MANAGER['ROUTING_INFO']=manager.dict()
    ROUTING_COUNTS=MANAGER['ROUTING_COUNTS']=manager.dict()
    USER_ROUTING_INFO=MANAGER['USER_ROUTING_INFO']=manager.dict()
    LOGGING_QU=mp.Queue()

    user_info_thread=mp.Process(target=get_user_info,args=(USER_INFO,))
    user_info_thread.start()
    logger_thread=mp.Process(target=logger,args=(LOGGING_QU,))
    logger_thread.start()
    network_usage_thread=mp.Process(target=get_network_usage,args=(bind_port,))
    network_usage_thread.start()
    routing_info_thread=mp.Process(target=get_routing_info,
               args=(ROUTING_INFO,ROUTING_COUNTS,USER_ROUTING_INFO))
    routing_info_thread.start()


    app=web.Application()
    app.router.add_route('GET','/{tail:.*}',lambda req:handler(req,MANAGER))
    app.router.add_route('POST','/{tail:.*}',lambda req:handler(req,MANAGER))
    runner=web.AppRunner(app)
    await runner.setup()
    ctx=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain(certfile='origin.pem',keyfile='private.pem')
    # web.run_app(sock=sock,ssl_context=ctx)
    srv=web.SockSite(runner,sock,ssl_context=ctx)
    await srv.start()
if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(start_server())
    loop.run_forever()