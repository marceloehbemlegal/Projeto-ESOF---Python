#! python3
# ImageDownloader.py - Downloads results for search input

import requests
import os
import bs4


# search_input = sys.argv[1]
search_input = input()
os.makedirs(search_input, exist_ok=True)
search_results = 'http://imgur.com/search?q='+search_input

image_request = requests.get(search_results)
image_request.raise_for_status()

soup = bs4.BeautifulSoup(image_request.text, "lxml")

image_element = soup.select('img[alt=""]')
print (len(image_element))
for i in range(len(image_element)):
    imageUrl = 'http://i.imgur.com/' + image_element[i].get('src')[14:21] + '.gif'
    print('Downloading ' + image_element[i].get('src')[14:21] + '...')
    image_request = requests.get(imageUrl)
    image_request.raise_for_status()
    imageFile = open(os.path.join(search_input, os.path.basename(imageUrl)), 'wb')

    for chunk in image_request.iter_content(100000):
        imageFile.write(chunk)

    imageFile.close()

print("Downloads successful.")