# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import csv, os
from datetime import date, timedelta
from bs4 import BeautifulSoup

newspaper_base_url = 'http://www.prothom-alo.com/'
newspaper_archive_base_url = 'http://www.prothom-alo.com/archive/'

# set the starting and ending date to crawl
start_date = date(2017, 5, 7)
end_date = date(2017, 5, 9)
delta = end_date - start_date

output_dir = './data-{}-{}'.format(start_date, end_date)

try:
    os.makedirs(output_dir)
except OSError:

    pass

print '\nScrabbing {}'.format(newspaper_base_url)
print '\nSaving (image url, caption) from starting date {} to ending date {} of {}\n'.format(start_date, end_date, delta)

image_index = 0
# get image,caption from starting date to end date
for i in range(delta.days + 1):
    date_str = start_date + timedelta(days=i)
    # check for 15 archive pages, this is not a fixed or predictable number :(
    for index in range(0, 15, 1):
        print '--------------------'
        print 'checking archive page: {id} and date {d}'.format(id=index, d=date_str)
        print '--------------------'

        url = newspaper_archive_base_url + str(date_str) + '?edition=print&page=' + str(index + 1)
        archive_soup = BeautifulSoup(urllib.urlopen(url),"lxml")
        all_links = archive_soup.find_all("a", attrs={"class": "link_overlay"})
        # check if this archive page contains any article
        if len(all_links) != 0:
            for link in all_links:
                article_url = newspaper_base_url + link.get('href')
                article_soup = BeautifulSoup(
                    urllib.urlopen(article_url).read())
                container = article_soup.article.div.p.find_all('img')
                # check if the title length is more then 5
                if len(container) != 0 and len(container[0].get('title')) > 5:
                    # cut the sub-string brefore 'l' character to remove image credic
                    caption = container[0].get('title').rsplit('l', 1)[0]
                    image_url = container[0].get('src')
                    image_name = str(image_index)+'.png'
                    download_by_url = urllib.URLopener()
                    download_by_url.retrieve(url=image_url, filename=output_dir+'/'+image_name)
                    result = [image_name, caption]
                    with open("Output.csv", "ab") as f:
                        writeFile = csv.writer(f)
                        writeFile.writerow(result)
                    image_index += 1
