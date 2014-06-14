#!/usr/bin/env

from lxml import etree
import datetime
import requests
import csv
import sys


RUNNERS = {
    'male': "8364",
    'female': "8541"
    }

MARATHON_SE_URL = "http://www.racetimer.se/sv/race/resultlist/1997?commit=Visa+resultat&layout=marathon&page={}&per_page=250&race_id=1997&rc_id={}"


def getdoc(url):
    '''Returns the HTML DOM as an etree Elementree'''
    r = requests.get(url)
    parser = etree.HTMLParser()
    return etree.fromstring(r.text, parser)


def stringify(element):
    '''Concatenates all text in the subelements into one string'''
    return u"".join([x.strip() for x in element.itertext()])


def converttime(t):

    if len(t) == 5:
        m, s = t.split(":")
        return datetime.timedelta(minutes=int(m), seconds=int(s))
    else:
        h, m, s = t.split(":")
        return datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))


def readresults(limit=None):

    count = 0
    for page in range(12):
        doc = getdoc(MARATHON_SE_URL.format(page+1, RUNNERS['female']))

        result_table = doc.find(".//table[@class='result-list']")

        for tr in result_table.findall(".//tr")[1:]:
            tds = tr.findall("td")
            r = {
                'name': stringify(tds[1])[1:],
                'tid': stringify(tds[5]),
            }
            if limit is None or count < limit:
                yield r
            else:
                raise StopIteration
            count += 1


def main():

    writer = csv.writer(sys.stdout)

    for runner in readresults():
        writer.writerow([runner['name'].encode("utf-8"), runner['tid'], int(converttime(runner['tid']).total_seconds()), "f"])


if __name__ == '__main__':
    main()
