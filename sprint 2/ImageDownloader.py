#! python3
# ImageDownloader.py - Downloads results for search input

import requests
import os
import bs4


# search_input = sys.argv[1]
search_input = input()
os.makedirs(search_input, exist_ok=True)
search_results = 'http://imgur.com/search?q='+search_input # how the imgur search url is defined

image_request = requests.get(search_results) # downloads the page with the search results
image_request.raise_for_status()

soup = bs4.BeautifulSoup(image_request.text, "lxml")

image_elements = soup.select('img[alt=""]') # selects all the <img> elements that have the attribute 'alt' equals to nothing

for i in range(len(image_elements)):
    imageUrl = 'http://i.imgur.com/' + image_elements[i].get('src')[14:21] + '.gif' # the last part of the link to the image can be found 
                                                                                    # as the value for the 'src' attribute in the specified
                                                                                    # positions ([14:21])
    print('Downloading ' + image_elements[i].get('src')[14:21] + '...')
    image_request = requests.get(imageUrl) # downloads the image
    image_request.raise_for_status()
    imageFile = open(os.path.join(search_input, os.path.basename(imageUrl)), 'wb')

    for chunk in image_request.iter_content(100000): # saves image to computer
        imageFile.write(chunk)

    imageFile.close()

print("Downloads successful.")
