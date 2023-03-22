import requests
from bs4 import BeautifulSoup
import urllib.parse


class OGE:
    def backmark(self, r):
        soup = BeautifulSoup(r.text, 'lxml')
        mark = soup.select(".exam-result")

        for i in range(len(mark)):
            mark[i] = mark[i].get_text()
            mark[i] = mark[i].replace("\n", "")
            mark[i] = mark[i].replace("\t", "")

        return mark

    def backobject(self, r):
        soup = BeautifulSoup(r.text, 'lxml')
        object = soup.select(".exam-subject-info")

        for i in range(len(object)):
            object[i].span.decompose()
            object[i] = object[i].get_text()
            object[i] = object[i].replace("\xa0", "")

        return object

    def backsite(self, family, series, number):
        f = {'pLastName': family.encode('windows-1251'), 'Series': str(series), 'Number': str(number),
             'Login': 'Показать результаты'}
        data = urllib.parse.urlencode(f)
        url = 'https://www.ege.spb.ru/result/index.php?mode=gia2022&wave=1'
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://www.ege.spb.ru'}
        return requests.post(url, data=data, headers=headers)

    def composition(self, subject, mark):
        results = []

        for i in range(len(subject)):
            results.append({"subject": subject[i], "mark": mark[i]})
        return results

    def __init__(self, surname, serial, number):

        r = self.backsite(surname, int(serial), int(number))

        object = self.backobject(r)
        mark = self.backmark(r)

        # print(object)
        # print(mark)

        self.value = self.composition(object, mark)
        if not self.value:
            raise ValueError("Неверные данные")