import requests
import base64


def post_login(session: requests.Session, open_cookie: str, username: str, password: str, repeat_time: int,
               url: str, referer: str):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Length": "53",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "e.zhbit.com",
        "Referer": "%s" % referer,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
    }
    username_base64 = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    password_base64 = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    index_cookie = {
        "JSESSIONID": "%s" % open_cookie
    }
    login_data = {
        "encoded": "%s%%%%%%%s" % (username_base64, password_base64)
    }

    repeat = 0
    while repeat < repeat_time:
        try:
            response = session.post(cookies=index_cookie, headers=headers, url=url, timeout=5,
                                    data=login_data, allow_redirects=False)
        except requests.exceptions.Timeout:
            repeat = repeat + 1
            if repeat == repeat_time:
                return -1
            continue
        break

    if int(response.status_code) >= 400:
        return -2

    if type(response.cookies) == 'str':
        return response.cookies['JSESSIONID']
    else:
        return open_cookie


def get_open_cookie(session: requests.Session, url: str, host: str, repeat_time: int):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "%s" % host,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
    }

    repeat = 0
    while repeat < repeat_time:
        try:
            response = session.get(url=url, headers=headers, timeout=3)
        except requests.exceptions.Timeout:
            repeat = repeat + 1
            if repeat == repeat_time:
                return -1
            continue
        break

    if int(response.status_code) >= 400:
        return -2

    return response.cookies['JSESSIONID']


def get_website(session: requests.Session, user_cookie: str, url: str, repeat_time: int, headers):
    cookies = {
        "JSESSIONID": "%s" % user_cookie
    }

    repeat = 0
    while repeat < repeat_time:
        try:
            response = session.get(url=url, cookies=cookies, headers=headers, allow_redirects=False, timeout=6)
        except requests.exceptions.Timeout:
            repeat = repeat + 1
            if repeat == repeat_time:
                return -1
            continue
        break

    if int(response.status_code) >= 400:
        return -2

    return response.text


class CourseList(object):
    def __init__(self):
        self.count = 1

    def post_class_list(self, session: requests.Session, user_cookie: str, url: str, startid: int,
                        repeat_time: int, host: str, referer_url):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "%s" % host,
            "Referer": "%s" % referer_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
            "X-Requested-With": "XMLHttpRequest"
        }
        cookies = {
            "JSESSIONID": "%s" % user_cookie
        }
        raw_data = 'sEcho=%s&'  \
                   'iColumns=11&' \
                   'sColumns=&' \
                   'iDisplayStart=%s&' \
                   'iDisplayLength=15&' \
                   'mDataProp_0=kch&' \
                   'mDataProp_1=kcmc&' \
                   'mDataProp_2=xf&' \
                   'mDataProp_3=skls&' \
                   'mDataProp_4=sksj&' \
                   'mDataProp_5=skdd&' \
                   'mDataProp_6=xkrs&' \
                   'mDataProp_7=syrs&' \
                   'mDataProp_8=xxrs&' \
                   'mDataProp_9=ctsm&' \
                   'mDataProp_10=czOper' % (str(self.count), str(startid))
        self.count = self.count + 1
        url_suffix = '?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false'
        url = url + url_suffix

        repeat = 0
        while repeat < repeat_time:
            try:
                response = session.post(cookies=cookies, headers=headers, url=url, timeout=8,
                                        data=raw_data, allow_redirects=False)
            except requests.exceptions.Timeout:
                repeat = repeat + 1
                if repeat == repeat_time:
                    return -1
                continue
            break

        if int(response.status_code) >= 400:
            return -2

        return response.text


def fuckClass(host: str, referer: str, user_cookie: str, class_id: str, repeat_time: int,
              session: requests.Session, url: str):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "%s" % host,
        "Referer": "%s" % referer,  # http://e.zhbit.com/jsxsd/xsxkkc/comeInGgxxkxk
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    cookies = {
        "JSESSIONID": "%s" % user_cookie
    }
    url_data = "jx0404id=%s&xkzy=&trjf=" % class_id  # 201820192001111
    url = url + url_data

    # request URL: http://e.zhbit.com/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=201820192001111&xkzy=&trjf=
    repeat = 0
    while repeat < repeat_time:
        try:
            response = session.get(url=url, cookies=cookies, headers=headers, allow_redirects=False, timeout=6)
        except requests.exceptions.Timeout:
            repeat = repeat + 1
            if repeat == repeat_time:
                return -1
            continue
        break

    if int(response.status_code) >= 400:
        return -2

    import json
    status = json.loads(response.text)

    if status['success'] is True:
        return 1
    else:
        return status['message']


if __name__ == '__main__':
    print("aaa")

