from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os

day = "2021/08/11"
#https://www.usatoday.com
fr = ""
fw = ""
i = 1
while i < 9:
    if(i == 1):
        fr = open("../data/link/usatoday/link/news.txt", "r")
        fw = open("../data/link/usatoday/data/news.txt", "a")
    elif i == 2:
        fr = open("../data/link/usatoday/link/entertainment.txt", "r")
        fw = open("../data/link/usatoday/data/entertainment.txt", "a")
    elif i == 3:
        fr = open("../data/link/usatoday/link/life.txt", "r")
        fw = open("../data/link/usatoday/data/life.txt", "a")
    elif i == 4:
        fr = open("../data/link/usatoday/link/money.txt", "r")
        fw = open("../data/link/usatoday/data/money.txt", "a")
    elif i == 5:
        fr = open("../data/link/usatoday/link/opinion.txt", "r")
        fw = open("../data/link/usatoday/data/opinion.txt", "a")
    elif i == 6:
        fr = open("../data/link/usatoday/link/travel.txt", "r")
        fw = open("../data/link/usatoday/data/travel.txt", "a")
    elif i == 7:
        fr = open("../data/link/usatoday/link/sports.txt", "r")
        fw = open("../data/link/usatoday/data/sports.txt", "a")
    elif i == 8:
        fr = open("../data/link/usatoday/link/tech.txt", "r")
        fw = open("../data/link/usatoday/data/tech.txt", "a")

    while (fr.tell() != os.fstat(fr.fileno()).st_size):
        url = fr.readline()
        url = url.rstrip('\n')
        req = Request(url)
        html_page = urlopen(req)

        soup = BeautifulSoup(html_page, "lxml")

        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))
        for link in links:
            try:
                if (len(link) > 50 and link.find(day) != -1):
                    if (link.find("http") != -1):
                        print("URL: " + link)
                        fw.write(link + "\n")
                    else:
                        print("URL: https://www.usatoday.com" + link)
                        fw.write("https://www.usatoday.com" + link + "\n")
            except:
                print()
    fr.close()
    fw.close()
    i += 1

