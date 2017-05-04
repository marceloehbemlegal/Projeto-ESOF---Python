#! python3
# LinkVerification.py - Searches a page for all the links in it and downloads all the available pages found


import requests
import bs4
import os

already_downloaded={}

page_url = 'http://www.cityofpage.org/'
page_request = requests.get(page_url) # downloads the page where the links are
page_request.raise_for_status()

number_of_pages=0

os.makedirs('links', exist_ok=True)

soup = bs4.BeautifulSoup(page_request.text, "lxml")

page_links = soup.select('a[href]') # links are normally the value for the attribute 'href' inside the <a> elements
for i in range(len(page_links)):
    link = page_links[i].get('href')
    if not link.startswith('http') and link.startswith('/'): # in this page, if the link is a subpage, it starts with '/'
        link = page_url + link[1:]                           # if it starts with '/', the url will be the original url plus the link
    if link.startswith('http'): # at this point, all page links found should start with 'http'
        link_request = requests.get(link)
        try:
            link_request.raise_for_status()
        except:
            print("Page %s not found." % link)

        if link not in already_downloaded.keys(): # avoids repeated links
            print("Downloading %s..." % link)
            already_downloaded[link]=1
            
            number_of_pages += 1
            link_file = open('./links/link_%03d.html' % (number_of_pages), 'wb')

            for chunk in link_request.iter_content(100000):
                link_file.write(chunk)

            link_file.close()


print("%d pages downloaded." % number_of_pages)
