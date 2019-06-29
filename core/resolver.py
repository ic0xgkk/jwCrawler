from bs4 import BeautifulSoup


def get_class_selection_url(web_text: str):
    soup = BeautifulSoup(web_text, 'html.parser')
    find_result = soup.find_all("a")
    for item0 in find_result:
        try:
            for item1 in item0.contents:
                try:
                    for item2 in item1.contents:
                        try:
                            for item3 in item2.contents:
                                try:
                                    if item3 == '选课中心':
                                        return item0.attrs['href']
                                    else:
                                        pass
                                except IndexError:
                                    continue
                        except AttributeError:
                            continue
                except AttributeError:
                    continue
        except AttributeError:
            continue


def get_class_kinds_url(web_text: str, class_name: str):
    soup = BeautifulSoup(web_text, 'html.parser')
    find_result = soup.find_all("tr")
    for item0 in find_result:
        try:
            for item1 in item0.contents:
                try:
                    for item2 in item1.contents:
                        try:
                            if item2 == class_name:
                                for item3 in item1.parent.contents:
                                    try:
                                        for item4 in item3.contents:
                                            try:
                                                if item4.contents[0] == '进入选课':
                                                    return item4.attrs['href']
                                                else:
                                                    pass
                                            except AttributeError:
                                                continue
                                    except AttributeError:
                                        continue
                            else:
                                pass
                        except AttributeError:
                            continue
                except AttributeError:
                    continue
        except AttributeError:
            continue


def get_xk_portal_comeIn_url(website: str, tagName: str):
    soup = BeautifulSoup(website, 'html.parser')
    find_result = soup.find_all("center")

    for item0 in find_result:
        if str(item0.contents[0]).find("未开放选课") != -1:
            return -1  # wei kai fang

    find_result = soup.find_all("a")

    if find_result is None:
        return -3  # kong zhi

    for item0 in find_result:
        if item0.contents[0] == tagName:
            return item0.attrs['href']
        else:
            continue

    return -2  # wei pi pei dao


if __name__ == '__main__':
    ii = get_xk_portal_comeIn_url(test1, "公选课选课")
    print(ii)
