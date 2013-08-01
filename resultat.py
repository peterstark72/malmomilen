#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv
import datetime
import time

HERRAR_URL = "http://racetimer.se/sv/race/resultlist/1289?commit=Visa+resultat+%3E%3E&amp;layout=marathon&amp;page={}&amp;per_page=250&amp;race_id=1289&amp;rc_id=6134#top"

DAMER_URL = "http://www.racetimer.se/sv/race/resultlist/1289?commit=Visa+resultat+%3E%3E&layout=marathon&page={}&per_page=250&race_id=1289&rc_id=6403#top"


def get_runners(page):

    html = urlopen(HERRAR_URL.format(page)).read()
    soup = BeautifulSoup(html, "lxml")
    resultlist = soup.find("table", "result-list")

    for tr in resultlist.find_all('tr'):
        runner = {}
        data = tr.find_all('td')

        if len(data) > 0:
            runner['pos'] = data[0].string            
            runner['name'] = data[1].find('a').string.encode('utf-8')
            runner['birth'] = data[2].string
            if data[3].string:
                runner['origin'] = data[3].string.encode('utf-8')
            else:
                runner['origin'] = None 
            runner['number'] = data[4].string

            runner['time'] = data[5].string.strip()

            if len(runner['time'].split(":")) < 3:
                time_str = "00:" + runner['time']
            else:
                time_str = runner['time']
            x = time.strptime(time_str, "%H:%M:%S")
            runner['total_seconds'] = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()

            runner['sex'] = "m"

            print runner['pos']

            yield runner


def main():
    runners = []

    for page in range(1,14):
        for runner in get_runners(page):
            runners.append(runner)

    writer = csv.DictWriter(open('mrunners.csv','w'), ('pos','name','birth','origin','number','time', 'total_seconds','sex'))
    writer.writeheader()
    writer.writerows(runners)
    


if __name__ == '__main__':
    main()

