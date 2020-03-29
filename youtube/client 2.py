# Echo client program
import socket

sample = """
[
{
    "domain": ".youtube.com",
    "expirationDate": 1567013678,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.1208356791.1499835948",
    "id": 1
},
{
    "domain": ".youtube.com",
    "expirationDate": 1505875939,
    "hostOnly": false,
    "httpOnly": false,
    "name": "8y6X_.resume",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "fqGSJVmX9Jw:3331,m1Hf6YNMehM:2218,nCzHni0UaOo:2072,DIKaPpFeAAE:1068",
    "id": 2
},
{
    "domain": ".youtube.com",
    "expirationDate": 1567438861.209828,
    "hostOnly": false,
    "httpOnly": false,
    "name": "APISID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "alCne3KsZBCuHSVi/Ai_CUr93Su7pRiqIJ",
    "id": 3
},
{
    "domain": ".youtube.com",
    "expirationDate": 1567438861.209737,
    "hostOnly": false,
    "httpOnly": true,
    "name": "HSID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "AHmwI7H_xajaWiTtm",
    "id": 4
},
{
    "domain": ".youtube.com",
    "expirationDate": 1567438862.50215,
    "hostOnly": false,
    "httpOnly": true,
    "name": "LOGIN_INFO",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "AFpGGQUwRgIhAIYBo0-PGHeWsw2jSA_qoB3YuQOCa6c6U9Bm_XIOel7SAiEAqJkcBG32uF294iF5lGRR506rv-SXl0tShoLQtNtqd-8:QUVrbWRPYmJTZ2drMVQ2N0lFa0x3STJZRm5CcUlPXzBKRmpvZWMzR3lGQWJUTGJSbG1qY1ZMQ1daLWNLeTllMm8xX1NLVVJuSS1mdFE1OWM1VEJZSXR3NDI1ZGZpcnd1c243bUtfRXVsSjhrb0NPTEZzSlRISHRQaGlSSnpPdURhZjZLZzFDdVZiVFVlc1FBdTF5R0NMUmw4dThDMm1tMzVNTnRhSElDbkZwV01pUnZhek12QkNN",
    "id": 5
},
{
    "domain": ".youtube.com",
    "expirationDate": 1567179106,
    "hostOnly": false,
    "httpOnly": false,
    "name": "PREF",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "f1=50000000&f5=30&f4=4000000",
    "id": 6
},
{
    "domain": ".youtube.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "s_gl",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "b49ac3bed2c9f40af89303115dbee38ccwIAAABLUg==",
    "id": 7
},
{
    "domain": ".youtube.com",
    "expirationDate": 1567438861.209869,
    "hostOnly": false,
    "httpOnly": false,
    "name": "SAPISID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "vaOmqTz5E-iSnPGt/AInsvrPN-pwX2d1El",
    "id": 8
},
{
    "domain": ".youtube.com",
    "expirationDate": 1567438861.209637,
    "hostOnly": false,
    "httpOnly": false,
    "name": "SID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "HgUVTCIxr7tFLg1W66quSara6iTQECSanJ_yjWVzQ264aDnMchO7C78qbW1tFhEX3s46jQ.",
    "id": 9
},
{
    "domain": ".youtube.com",
    "expirationDate": 1567438861.209784,
    "hostOnly": false,
    "httpOnly": true,
    "name": "SSID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "A6RIXQG-Q0ac518aU",
    "id": 10
},
{
    "domain": ".youtube.com",
    "expirationDate": 1525398103.702833,
    "hostOnly": false,
    "httpOnly": true,
    "name": "VISITOR_INFO1_LIVE",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "6YYnvnllhS8",
    "id": 11
},
{
    "domain": ".youtube.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "YSC",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "9fMWNxRlyHo",
    "id": 12
},
{
    "domain": "www.youtube.com",
    "hostOnly": true,
    "httpOnly": false,
    "name": "llbcs",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "2",
    "id": 13
}
]
"""
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("./_cookie")
s.send(sample)
data = s.recv(1024)
s.close()
print('Received ' + data)