# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from bs4 import BeautifulSoup
import urllib
import csv
from datetime import date, timedelta

newspaper_base_url = 'http://www.prothom-alo.com/'
newspaper_archive_base_url = 'http://www.prothom-alo.com/archive/'

start_date = date(2017, 5, 7)
end_date = date(2017, 5, 9)
delta = end_date - start_date 

for i in range(delta.days + 1):
    date_str = start_date + timedelta(days=i)
    for index in range(0, 15, 1):
        print('--------------------')
        print('checking archive page: {id} and date {d}'.format(id=index, d=date_str))
        print('--------------------')

        url = newspaper_archive_base_url+str(date_str)+'?edition=print&page=' + str(index+1)
        archive_soup = BeautifulSoup(urllib.urlopen(url))
        all_links = archive_soup.find_all("a", attrs={"class" : "link_overlay"})
        # check if this archive page contains any article
        if(len(all_links) != 0):
            for link in all_links:
                article_url = newspaper_base_url + link.get('href')
                article_soup = BeautifulSoup(urllib.urlopen(article_url).read())
                container = article_soup.article.div.p.find_all('img')
                # check if the title length is more then 5
                if len(container) != 0 and len(container[0].get('title')) > 5:
                    # cut the sub-string brefore 'l' character to remove image credic
                    caption = container[0].get('title').rsplit('l', 1)[0]
                    image = container[0].get('src')
                    result = [caption, image]
                    with open("Output.csv", "ab") as f:
                        writeFile = csv.writer(f)
                        writeFile.writerow(result)


