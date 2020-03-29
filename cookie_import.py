import subprocess
import sys
import os
a = os.chdir("history")
cookie_info = sys.argv[1]
# {
#   "8y6X_.resume": "fqGSJVmX9Jw:3331,m1Hf6YNMehM:2218,nCzHni0UaOo:2072,DIKaPpFeAAE:1068",
#   "APISID": "alCne3KsZBCuHSVi/Ai_CUr93Su7pRiqIJ",
#   "HSID": "AHmwI7H_xajaWiTtm",
#   "LOGIN_INFO": "AFpGGQUwRgIhAIYBo0-PGHeWsw2jSA_qoB3YuQOCa6c6U9Bm_XIOel7SAiEAqJkcBG32uF294iF5lGRR506rv-SXl0tShoLQtNtqd-8:QUVrbWRPYmJTZ2drMVQ2N0lFa0x3STJZRm5CcUlPXzBKRmpvZWMzR3lGQWJUTGJSbG1qY1ZMQ1daLWNLeTllMm8xX1NLVVJuSS1mdFE1OWM1VEJZSXR3NDI1ZGZpcnd1c243bUtfRXVsSjhrb0NPTEZzSlRISHRQaGlSSnpPdURhZjZLZzFDdVZiVFVlc1FBdTF5R0NMUmw4dThDMm1tMzVNTnRhSElDbkZwV01pUnZhek12QkNN",
#   "PREF": "f1=50000000&f5=30&f4=4000000",
#   "SAPISID": "vaOmqTz5E-iSnPGt/AInsvrPN-pwX2d1El",
#   "SID": "HgUVTCIxr7tFLg1W66quSara6iTQECSanJ_yjWVzQ264aDnMchO7C78qbW1tFhEX3s46jQ.",
#   "SSID": "A6RIXQG-Q0ac518aU",
#   "VISITOR_INFO1_LIVE": "6YYnvnllhS8",
#   "YSC": "9fMWNxRlyHo",
#   "_ga": "GA1.2.1208356791.1499835948",
#   "llbcs": "2",
#   "s_gl": "b49ac3bed2c9f40af89303115dbee38ccwIAAABLUg=="
# }

command = "/home/byeon/anaconda3/envs/tf/bin/scrapy crawl yth_spider -a input_cookies='%s'" % (cookie_info)


p = subprocess.call(command, shell=True)
# p = subprocess.call(command, shell=True)