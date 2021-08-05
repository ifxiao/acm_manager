from urllib import request, parse
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup
import json

#post方法
def post(url, form, headers=None):
    return url_requests(url, form,headers=headers)
#get方法
def get(url, headers=None):
    return url_requests(url, headers=headers)

def url_requests(url, form=None, headers=None):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    if headers == None:
        headers = {
            'User-Agent': user_agent
        }
    html_bytes = b''
    try:
        if form:
            #转换为str
            form_str = parse.urlencode(form)
            form_bytes = form_str.encode('utf-8')
            req = request.Request(url, data=form_bytes,headers=headers)

        else:
            req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        html_bytes = response.read()
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    return html_bytes

