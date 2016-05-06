#!usr/bin/Python
# -*- coding:utf-8 -*-
"""为了应付时不时出现的Too many redirects异常，使用此类打开链接。
此类会自动处理redirect和cookie，同时增加了失败自动重试功能"""
import urllib, urllib2, Cookie, urlparse, time
# from google.appengine.api import urlfetch
# from google.appengine.runtime.apiproxy_errors import OverQuotaError
from config import CONNECTION_TIMEOUT

class MyResp:
    def __init__(self, a, b):
        self.status_code = a
        self.content = b
        self.headers= {}



class URLOpener:
    _codeMapDict = {
        200 : 'Ok',
        201 : 'Created',
        202 : 'Accepted',
        203 : 'Non-Authoritative Information',
        204 : 'No Content',
        205 : 'Reset Content',
        206 : 'Partial Content',
        300 : 'Multiple Choices',
        301 : 'Moved Permanently',
        302 : 'Found',
        303 : 'See Other',
        304 : 'Not Modified',
        305 : 'Use Proxy',
        307 : 'Temporary Redirect',
        400 : 'Bad Request',
        401 : 'Unauthorized',
        402 : 'Payment Required',
        403 : 'Forbidden',
        404 : 'Not Found',
        405 : 'Method Not Allowed',
        406 : 'Not Acceptable',
        407 : 'Proxy Authentication Required',
        408 : 'Request Timeout',
        409 : 'Conflict',
        410 : 'Gone',
        411 : 'Length Required',
        412 : 'Precondition Failed',
        413 : 'Request Entity Too Large',
        414 : 'Request-URI Too Long',
        415 : 'Unsupported Media Type',
        416 : 'Requested Range Not Satisfiable',
        417 : 'Expectation Failed',
        500 : 'Internal Server Error',
        501 : 'Not Implemented',
        502 : 'Bad Gateway',
        503 : 'Service Unavailable',
        504 : 'Gateway Timeout',
        505 : 'HTTP Version Not Supported',
        
        #------- Custom Code -----------------
        529 : 'OverQuotaError',
        530 : 'Timeout',
        531 : 'ResponseTooLargeError',
        532 : 'SSLCertificateError',
        533 : 'UnAuthorizedError',
        534 : 'DownloadError',
        535 : 'GeneralDownloadError',
    }
    
    @classmethod
    def CodeMap(cls, errCode):
        des = cls._codeMapDict.get(errCode, None)
        return '%d %s' % (errCode, des) if des else str(errCode)
    
    def __init__(self, host=None, maxfetchcount=2, maxredirect=5, 
              timeout=CONNECTION_TIMEOUT, addreferer=True, headers=None):
        self.cookie = Cookie.SimpleCookie()
        self.maxFetchCount = maxfetchcount
        self.maxRedirect = maxredirect
        self.host = host
        self.addReferer = addreferer
        self.timeout = timeout
        self.realurl = ''
        self.initHeaders = headers
    
    def open(self, url, data=None, headers=None):
        print url
        self.realurl = url
        maxRedirect = self.maxRedirect
        
        class resp: #出现异常时response不是合法的对象，使用一个模拟的
            code=555
            content=''
            headers={}
        
        response = resp()
        if url.startswith('data:'):
            import base64, re
            rxDataUri = re.compile("^data:(?P<mime>[a-z]+/[a-z]+);base64,(?P<data>.*)$", re.I | re.M | re.DOTALL)
            m = rxDataUri.match(url)
            try:
                response.content = base64.decodestring(m.group("data"))
                response.code = 200
            except Exception as e:
                response.code = 404
        else:
            while url and (maxRedirect > 0):
                cnt = 0
                while cnt < self.maxFetchCount:
                    try:
                        if data and isinstance(data, dict):
                            data = urllib.urlencode(data)
                        request = urllib2.Request(url)
                        h = self._getHeaders(url)
                        for k in h:
                            request.add_header(k, h[k])
                        response = urllib2.urlopen(request)
                        print response
                        #break
                    except Exception as e:
                        if response.code == 555:
                            response.code = 535
                            default_log.warn('url [%s] failed [%s].' % (url, str(e)))
                        break
                    else:
                        break
                
                data = None
                try:
                    self.SaveCookies(response.header_msg.getheaders('Set-Cookie'))
                except:
                    pass
                
                if response.code not in [300, 301, 302, 303, 307]: #只处理重定向信息
                    break
                
                urlnew = response.headers.get('Location')
                if urlnew and not urlnew.startswith("http"):
                    url = urlparse.urljoin(url, urlnew)
                else:
                    url = urlnew
                maxRedirect -= 1
        
        if maxRedirect <= 0:
            default_log.warn('Too many redirections:%s'%url)
        
        self.realurl = url
        # return response
        return MyResp(response.code, response.read())
        
    def _getHeaders(self, url=None, extheaders=None):
        headers = {
             'User-Agent':"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  }
        cookie = '; '.join(["%s=%s" % (v.key, v.value) for v in self.cookie.values()])
        if cookie:
            headers['Cookie'] = cookie
        if self.addReferer and (self.host or url):
            headers['Referer'] = self.host if self.host else url
        
        if self.initHeaders:
            headers.update(self.initHeaders)
        if extheaders:
            headers.update(extheaders)
        return headers
        
    def SaveCookies(self, cookies):
        if not cookies:
            return
        self.cookie.load(cookies[0])
        for cookie in cookies[1:]:
            obj = Cookie.SimpleCookie()
            obj.load(cookie)
            for v in obj.values():
                self.cookie[v.key] = v.value
            
