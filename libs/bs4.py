import requests
from bs4 import BeautifulSoup
from static import messages
from static.dicts import sign_choices


class Parser:
    DOLLAR_RUB = 'https://www.google.com/search?q=доллар+к+рублю'
    EURO_RUB = 'https://www.google.com/search?q=евро+к+рублю'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.149 Safari/537.36'}

    def get_currency(self):
        try:
            dollar = requests.get(self.DOLLAR_RUB, headers=self.headers)
            euro = requests.get(self.EURO_RUB, headers=self.headers)
        except:
            return messages.went_wrong
        dollarsoup = BeautifulSoup(dollar.content, 'html.parser')
        eurosoup = BeautifulSoup(euro.content, 'html.parser')
        dollardata = dollarsoup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})[0].text
        eurodata = eurosoup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})[0].text
        ans = messages.wallet % (dollardata, eurodata)
        return ans

    def get_horoscope(self, sign):
        if sign not in sign_choices:
            return messages.not_a_sign
        try:
            horoscope = requests.get(f"https://www.astrostar.ru/horoscopes/main/{sign_choices[sign]}/day.html",
                                     headers=self.headers)
        except:
            return messages.went_wrong
        hsoup = BeautifulSoup(horoscope.content, 'html.parser')
        data = hsoup.find("p")
        return 'Гороскоп на сегодня:☯\n\n' + data.text
