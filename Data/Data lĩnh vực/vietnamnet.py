from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os

day = "2021/08/11"
#https://www.usatoday.com
fr = ""
fw = ""
i = 1
while i < 7:
    if(i == 1):
        fr = open("../data/link/vietnamnews/link/economy.txt", "r")
        fw = open("../data/link/vietnamnews/data/economy.txt" , "a")
    elif i == 2:
        fr = open("../data/link/vietnamnews/link/environment.txt", "r")
        fw = open("../data/link/vietnamnews/data/environment.txt", "a")
    elif i == 3:
        fr = open("../data/link/vietnamnews/link/life-style.txt", "r")
        fw = open("../data/link/vietnamnews/data/life-style.txt", "a")
    elif i == 4:
        fr = open("../data/link/vietnamnews/link/politics-laws.txt", "r")
        fw = open("../data/link/vietnamnews/data/politics-laws.txt", "a")
    elif i == 5:
        fr = open("../data/link/vietnamnews/link/society.txt", "r")
        fw = open("../data/link/vietnamnews/data/society.txt", "a")
    elif i == 6:
        fr = open("../data/link/vietnamnews/link/sports.txt", "r")
        fw = open("../data/link/vietnamnews/data/sports.txt", "a")

    while(fr.tell() != os.fstat(fr.fileno()).st_size):
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
                if (len(link) > 50 and link.find("html")):
                    if (link.find("http") != -1):
                        print("URL: " + link)
                        fw.write(link + "\n")
                    else:
                        print("URL: https://vietnamnews.vn"  + link)
                        fw.write("https://vietnamnews.vn" + link + "\n")
            except:
                print()
    fr.close()
    fw.close()
    i += 1