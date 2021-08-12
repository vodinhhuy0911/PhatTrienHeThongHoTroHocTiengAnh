from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os
#day


def getLinkDay(day,path):
    fR = open(path,"r")
    linkR = ""
    linkW = ""
    website = ""
    while (fR.tell() != os.fstat(fR.fileno()).st_size):
        linkR = fR.readline()
        linkR = linkR.rstrip('\n')
        linkW = linkR.replace("link","data")
        linkW = linkW.rstrip('\n')
        print(linkR + " - " + linkW)
        if linkR.find("..") == -1:
            if linkR != linkW:
                print("a")
                return
            else:
                website = linkR
        else:
            fr = open(linkR,"r")
            fw = open(linkW,"a")
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
                                print("URL: " + website + link)
                                fw.write(website + link + "\n")
                    except:
                        print()
            fr.close()
            fw.close()
    return



getLinkDay("","linkRead.txt")
getLinkDay("2021/08/11","linkReadDay.txt")
getLinkDay("2021/aug/11","linkReadDay1.txt")
getLinkDay("2021-08-11","linkReadDay2.txt")
getLinkDay("20210811","linkReadDay3.txt")
getLinkDay("html","linkReadHtml.txt")

