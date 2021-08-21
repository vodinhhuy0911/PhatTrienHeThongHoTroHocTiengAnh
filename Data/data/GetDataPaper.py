from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os
#day
from newspaper import Article
import codecs


def getPaper(path):
    fR = open(path,"r")
    while (fR.tell() != os.fstat(fR.fileno()).st_size):
        linkR = fR.readline()
        linkR = linkR.rstrip('\n')
        paperR = linkR.replace("link","data")
        paperR = paperR.rstrip('\n')
        print(linkR + " - " + paperR)
        if linkR.find("..") == -1:
            if linkR != paperR:
                print("a")
                return
            else:
                website = linkR
        else:

            fr = open(paperR,"r")
            count = 1
            while (fr.tell() != os.fstat(fr.fileno()).st_size):
                try:
                    url = fr.readline()
                    url = url.rstrip('\n')
                    print(url)
                    article = Article(url)
                    article.download()
                    article.parse()
                    print(article.text)
                    # url2 = "F:\python\\venv\paper\\" + str("%06d" % count) + ".txt"
                    paperW = paperR.replace("/url/", "/paper/")
                    fw = codecs.open(paperW, "a+", "utf-8")
                    fw.write(article.text)
                    fw.write("\n")
                    fw.write("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    print("%d - complete...." % (count))
                    fw.close()
                    count += 1
                except:
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            fr.close()
    return




getPaper("linkRead.txt")
getPaper("linkReadDay.txt")
getPaper("linkReadDay1.txt")
getPaper("linkReadDay2.txt")
getPaper("linkReadDay3.txt")
getPaper("linkReadHtml.txt")




