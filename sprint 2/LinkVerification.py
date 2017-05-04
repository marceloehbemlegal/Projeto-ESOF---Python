import requests
import bs4
import os

already_downloaded={}

page_url = 'http://www.cityofpage.org/'
page_request = requests.get(page_url)
page_request.raise_for_status()

number_of_pages=1

os.makedirs('links', exist_ok=True)

soup = bs4.BeautifulSoup(page_request.text, "lxml")

page_links = soup.select('a[href]')
for i in range(len(page_links)):
    link = page_links[i].get('href')
    if not link.startswith('http') and link.startswith('/'):
        link = page_url + link[1:]
    if link.startswith('http'):

        link_request = requests.get(link)
        try:
            link_request.raise_for_status()
        except:
            print("Page %s not found." % link)

        if link not in already_downloaded.keys():
            print("Downloading %s..." % link)
            already_downloaded[link]=1

            link_file = open('./links/link_%03d.html' % number_of_pages, 'wb')
            number_of_pages += 1
            for chunk in link_request.iter_content(100000):
                link_file.write(chunk)

            link_file.close()


print("%d pages downloaded." % (number_of_pages-1))