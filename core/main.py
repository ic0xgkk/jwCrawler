from core import fclient
from core import resolver
from core import database
import json
import requests


def login(session: requests.Session, config):
    open_cookie = fclient.get_open_cookie(session, config['system_url']['login_website_url'], config['host'],
                                          config['timeout_repeat'])
    try:
        if open_cookie == -2:
            raise ConnectionError("Failed to get open cookie,status code with wrong")
        elif open_cookie == -1:
            raise ConnectionError("Connection timeout")
    except TypeError:
        pass

    login_cookie = fclient.post_login(session, open_cookie, config['username'],
                                      config['password'], config['timeout_repeat'],
                                      config['system_url']['login_api'],
                                      config['system_url']['login_website_url'])
    try:
        if login_cookie == -2:
            raise ConnectionError("Failed to post login request, status code with wrong")
        elif login_cookie == -1:
            raise ConnectionError("Connection timeout")
    except TypeError:
        pass

    return login_cookie


def store_all_class(kindName: str, className: str, db: database.Database, course):
    for item in course['aaData']:
        jx0404id = str(item['jx0404id'])
        xf = int(item['xf'])
        dwmc = str(item['dwmc'])
        jx02id = str(item['jx02id'])
        xkrs = int(item['xkrs'])
        zxs = int(item['zxs'])
        sksj = str(item['sksj'])
        xxrs = int(item['xxrs'])
        szkcflmc = str(item['szkcflmc'])
        syrs = int(item['syrs'])
        kcmc = str(item['kcmc'])
        skls = str(item['skls'])
        skdd = str(item['skdd'])
        db.course_to_db(jx0404id, xf, dwmc, jx02id, xkrs, zxs, sksj, xxrs,
                        szkcflmc, syrs, kcmc, skls, skdd, kindName, className)


def base_referer_convert(base_referer: str, url: str):
    base_sign = "xsxkkc/xsxk"

    end_sign = int(url.find(base_sign))
    if end_sign == -1:
        raise Exception("Something went wrong")

    start_sign = end_sign + len(base_sign)
    root = url[start_sign:]

    return base_referer + root


def get_classKind_course(api_url, session, login_cookie, course_class: fclient.CourseList,
                         kindName, className, db: database.Database, repeat_time, host, base_referer: str):
    referer = base_referer_convert(base_referer, api_url)

    class_list = course_class.post_class_list(session, login_cookie, api_url, 0, repeat_time, host, referer)
    try:
        if class_list == -2:
            raise ConnectionError("Failed to get class list, status code with wrong")
        elif class_list == -1:
            raise ConnectionError("Connection timeout")
    except TypeError:
        pass

    course = json.loads(class_list)

    times = int(course['iTotalRecords'] / 15) + 1

    i = 0
    while i < times:
        class_list = course_class.post_class_list(session, login_cookie, api_url,
                                                  i * 15, repeat_time, host, referer)
        course = json.loads(class_list)
        store_all_class(kindName, className, db, course)
        i = i + 1


def get_selectionKind(session, login_cookie, config, db, courseClass):
    portal_website = fclient.get_website(session, login_cookie, config['system_url']['portal_url'],
                                         config['timeout_repeat'],
                                         {
                                             "Accept": "text/html,application/xhtml+xml,application/xml;"
                                                       "q=0.9,*/*;q=0.8",
                                             "Accept-Encoding": "gzip, deflate",
                                             "Accept-Language": "en-US,en;q=0.5",
                                             "Connection": "keep-alive",
                                             "Host": "%s" % config['host'],
                                             "Referer": "%s" % config['system_url']['login_website_url'],
                                             "Upgrade-Insecure-Requests": "1",
                                             "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) "
                                                           "Gecko/20100101 Firefox/64.0"
                                         })
    try:
        if portal_website == -2:
            raise ConnectionError("Failed to get portal website, status code with wrong")
        elif portal_website == -1:
            raise ConnectionError("Connection timeout")
    except TypeError:
        pass
    selection_url = "http://" + config['host'] + resolver.get_class_selection_url(portal_website)
    selection_website = fclient.get_website(session, login_cookie, selection_url, config['timeout_repeat'],
                                            {
                                                "Accept": "text/html,application/xhtml+xml,application/xml;"
                                                          "q=0.9,*/*;q=0.8",
                                                "Accept-Encoding": "gzip, deflate",
                                                "Accept-Language": "en-US,en;q=0.5",
                                                "Connection": "keep-alive",
                                                "Host": "%s" % config['host'],
                                                "Referer": "%s" % config['system_url']['portal_url'],
                                                "Upgrade-Insecure-Requests": "1",
                                                "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) "
                                                              "Gecko/20100101 Firefox/64.0"
                                            })
    try:
        if selection_website == -2:
            raise ConnectionError("Failed to get portal website, status code with wrong")
        elif selection_website == -1:
            raise ConnectionError("Connection timeout")
    except TypeError:
        pass

    for item in config['kinds_attribute']:
        url = "http://" + config['host'] + resolver.get_class_kinds_url(selection_website, item['name'])
        xk_portal_website = fclient.get_website(session, login_cookie, url, config['timeout_repeat'],
                                                {
                                                    "Accept": "text/html,application/xhtml+xml,application/xml;"
                                                              "q=0.9,*/*;q=0.8",
                                                    "Accept-Encoding": "gzip, deflate",
                                                    "Accept-Language": "en-US,en;q=0.5",
                                                    "Connection": "keep-alive",
                                                    "Host": "%s" % config['host'],
                                                    "Referer": "%s" % selection_url,
                                                    "Upgrade-Insecure-Requests": "1",
                                                    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) "
                                                                  "Gecko/20100101 Firefox/64.0"
                                                })
        get_allTag(config['class_post_api'], item, config, login_cookie, courseClass, item['name'], db, session)


def get_allTag(post_api, classAttribute, config, login_cookie, courseClass, kindName, db, session):
    if classAttribute['current_course'] is True:
        get_classKind_course(post_api['current_course'], session, login_cookie, courseClass, kindName,
                             "本学期计划选课", db, config['timeout_repeat'], config['host'],
                             config['system_url']['base_referer'])
    if classAttribute['across_grade'] is True:
        get_classKind_course(post_api['across_grade'], session, login_cookie, courseClass, kindName,
                             "专业内跨年级选课", db, config['timeout_repeat'], config['host'],
                             config['system_url']['base_referer'])
    if classAttribute['cross_functionally'] is True:
        get_classKind_course(post_api['cross_functionally'], session, login_cookie, courseClass, kindName,
                             "跨专业选课", db, config['timeout_repeat'], config['host'],
                             config['system_url']['base_referer'])
    if classAttribute['public_course'] is True:
        get_classKind_course(post_api['public_course'], session, login_cookie, courseClass, kindName,
                             "公选课选课", db, config['timeout_repeat'], config['host'],
                             config['system_url']['base_referer'])


def start():
    with open("./config.json") as fs:
        steam = str(fs.read())
        config = json.loads(steam)
        fs.close()
    session = requests.Session()

    cookie = login(session, config)
    courseClass = fclient.CourseList()
    db = database.Database(config['database']['host'],
                           config['database']['username'],
                           config['database']['password'],
                           config['database']['db_name'],
                           config['database']['port'])

    get_selectionKind(session, cookie, config, db, courseClass)


if __name__ == '__main__':
    start()


