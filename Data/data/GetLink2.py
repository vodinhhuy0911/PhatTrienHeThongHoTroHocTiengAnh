from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os
#day

def checkLink(link,paper):
    if paper == "https://www.nationalgeographic.com" or paper == "https://www.newscientist.com":
        if link.find("article") != -1:
            return True
        else:
            return False
    elif paper == "https://vietnamnews.vn":
        if link.find(".html") != -1:
            return True
        else:
            return False
    elif paper == "https://www.dailymail.co.uk":
        if link.find("article") != -1 and link.find("html") != -1 and link.find("#comment") == -1 and link.find("#video") == -1:
            return True
        else:
            return False
    else:
        return True

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
                            if(checkLink(link,linkR) == True):
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
getLinkDay("2021/08/16","linkReadDay.txt")
getLinkDay("2021/aug/16","linkReadDay1.txt")
getLinkDay("2021-08-16","linkReadDay2.txt")
getLinkDay("20210816","linkReadDay3.txt")
getLinkDay("html","linkReadHtml.txt")

