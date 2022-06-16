import requests
from bs4 import BeautifulSoup
import urllib.parse


def backmark(r):
    soup = BeautifulSoup(r.text, 'lxml')
    mark = soup.select(".exam-result")

    for i in range(len(mark)):
        mark[i] = mark[i].get_text()
        mark[i] = mark[i].replace("\n", "")
        mark[i] = mark[i].replace("\t", "")

    return mark


def backobject(r):
    soup = BeautifulSoup(r.text, 'lxml')
    object = soup.select(".exam-subject-info")

    for i in range(len(object)):
        object[i].span.decompose()
        object[i] = object[i].get_text()
        object[i] = object[i].replace("\xa0", "")

    return object


def backsite(family, series, number):
    f = {'pLastName': family.encode('windows-1251'), 'Series': str(series), 'Number': str(number),
         'Login': 'Показать результаты'}
    data = urllib.parse.urlencode(f)
    url = 'https://www.ege.spb.ru/result/index.php?mode=gia2022&wave=1'
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://www.ege.spb.ru'}
    return requests.post(url, data=data, headers=headers)


def main():
    r = backsite(input("Введите фамилию: "), input("Введите серию паспорта: "), input("Введите номер паспорта: "))

    object = backobject(r)
    mark = backmark(r)


    print(object)
    print(mark)


if __name__ == '__main__':
    main()
