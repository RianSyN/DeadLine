# -*- coding: utf-8 -*-
import json
import requests
import ssl

from thrift.protocol import TCompactProtocol
from thrift.transport import THttpClient
from . import saturday
from Trevor.saturday import TalkService
from Trevor.saturday import LineLoginService
from Trevor.saturday.ttypes import LoginRequest


host = 'https://gd2.line.naver.jp'
LINE_AUTH_QUERY_PATH = '/api/v4p/rs'
LINE_AUTH_QUERY_PATH_FIR = '/api/v4/TalkService.do'
LINE_CERTIFICATE_PATH = '/Q'
LINE_API_QUERY_PATH_FIR = '/S4'
UA, LA = ("DeadLine\6.0", 'CHROMEOS\t1.4.17\tDeadLine_Team\t1')
_session    = requests.session()



def getJson(url, headers=None):
    if headers is None:
        return json.loads(_session.get(url).text)
    else:
        return json.loads(_session.get(url, headers=headers).text)

def defaultCallback(str):
    print(str)

def createTransport(path=None, update_headers=None, service=None):
    Headers = {
        'User-Agent': UA,
        'X-Line-Application': LA,
        "x-lal": "ja-US_US",
    }
    Headers.update({"x-lpqs" : path})
    if(update_headers is not None):
        Headers.update(update_headers)
    transport = THttpClient.THttpClient(host + path)
    transport.setCustomHeaders(Headers)
    protocol = TCompactProtocol.TCompactProtocol(transport)
    client = service(protocol)
    return client

class LineCallback(object):

    def __init__(self, callback):
        self.callback = callback

    def QrUrl(self, url, showQr=True):
        self.callback(url)

    def default(self, str):
        self.callback(str)




class bmth():
    def spirit(self):
        client = createTransport(LINE_AUTH_QUERY_PATH_FIR, None, TalkService.Client)

        qr = client.getAuthQrcode(keepLoggedIn=1, systemName="DeadLine™")
        uri = "line://au/q/" + qr.verifier
        clb = LineCallback(defaultCallback)
        clb.QrUrl(uri, 1)
        header = {
                'User-Agent': UA,
                'X-Line-Application': LA,
                "x-lal" : "ja-US_US",
                "x-lpqs" : LINE_AUTH_QUERY_PATH_FIR,
                'X-Line-Access': qr.verifier
        }
        getAccessKey = getJson(host + LINE_CERTIFICATE_PATH, header)
        client = createTransport(LINE_AUTH_QUERY_PATH, None, LineLoginService.Client)
        req = LoginRequest()
        req.type = 1
        req.verifier = qr.verifier
        req.e2eeVersion = 1
        res = client.loginZ(req)
        client = createTransport(LINE_API_QUERY_PATH_FIR, {'X-Line-Access':res.authToken}, TalkService.Client)
        return res.authToken

if __name__ == '__main__':
    bmth().spirit()
