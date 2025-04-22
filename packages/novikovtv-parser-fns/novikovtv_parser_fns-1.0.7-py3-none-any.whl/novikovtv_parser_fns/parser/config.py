import time


def get_parse_config(*, query: str, page: int = 1, captcha: str = "") -> dict:
    params = {
        "mode": "search-ul",
        "queryAll": "",  # Поиск по названию
        "queryUl": query,  # Поиск по организациям
        "okvedUl": "",  # Категория
        "regionUl": "",
        "statusUl": "",
        "isMspUl": "",
        "mspUl1": "1",
        "mspUl2": "1",
        "mspUl3": "1",
        "queryIp": "",  # Поиск по ИП
        "okvedIp": "",
        "regionIp": "",
        "statusIp": "",
        "isMspIp": "",
        "mspIp1": "1",
        "mspIp2": "1",
        "mspIp3": "1",
        "taxIp": "",
        "queryUpr": "",  # Поиск по "Участие в ЮЛ"
        "uprType1": "1",
        "uprType0": "1",
        "queryRdl": "",  # Поиск по "Дисквалификация"
        "dateRdl": "",
        "queryAddr": "",  # Поиск по адресу
        "regionAddr": "",
        "queryOgr": "",  # Поиск по "Ограничения участия в ЮЛ"
        "ogrFl": "1",
        "ogrUl": "1",
        "ogrnUlDoc": "",
        "ogrnIpDoc": "",
        "npTypeDoc": "1",
        "nameUlDoc": "",
        "nameIpDoc": "",
        "formUlDoc": "",
        "formIpDoc": "",
        "ifnsDoc": "",
        "dateFromDoc": "",
        "dateToDoc": "",
        "page": page,
        "pageSize": "100",
        "pbCaptchaToken": captcha,
        "token": ""
    }
    return params


def get_parse_ext_config(*, query: str = "", page: int = 1, captcha: str = "") -> dict:
    params = {
        "mode": "search-ul-ext",
        "page": 1,
        "pageSize": 10,
        "pbCaptchaToken": "",
        "queryUlExt": query,
        "okvedUlExt": "11.02,11.07,13.93,14,15,17.24,23,25,26,27.51,29.3,30.91,30.92.1,31,32,33,41.2,45,47,49.42,51.10,52,53.20.31,55,56,64,65.1,68,74.1,75.00.2,77.1,77.2,77.3,79,81.2,81.3,85.4,90,95,96.01,96.02",
        "okvedexUlExt": "",
        "regionUlExt": "77,78,23,47,50",
        "opfUlExt": "10000,50100",
        "statusUlExt": "10",
        "arrearUlExt": "0;10000001",
        "sschrUlExt": "0;10001",
        "taxpayUlExt": "0;10000001",
        "expenseUlExt": "0;10000001",
        "revenueUlExt": "0;10000001",
        "taxmodeUlExt": "",
        "ausnUlExt": "1",
        "eshnUlExt": "1",
        "sprUlExt": "1",
        "usnUlExt": "1",
        "offenseUlExt": "",
        "invalidUlExt": "",
        "rsmpUlExt": "",
        "page": page,
        "pageSize": "100",
        "pbCaptchaToken": captcha,
    }
    return params


def get_excel_config(*, captcha: str = "", ext_params=None) -> dict:
    if ext_params is None:
        ext_params = {}

    params = {
        "method": "get-search-excel-request",
        "t": str(int(round(time.time() * 1000))),
        **ext_params,
        "pbCaptchaToken": captcha,
    }

    if params["queryUlExt"] == "":
        del params["queryUlExt"]

    return params
