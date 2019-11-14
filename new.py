
import os
import sys
from imdb import IMDb
import numpy as np
import requests
import webbrowser
from contextlib import closing
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import numpy as np
import urllib.request
import cv2
ia = IMDb()
def get_image(link):
	driver = webdriver.PhantomJS()
	driver.get(link) # load the web page
	innerHTML = driver.execute_script("return document.body.innerHTML")
	parsed = BeautifulSoup(innerHTML,"html.parser")
	driver.close()
	mediastrip = parsed.find_all('img', class_= 'pswp__img')
	imgtags = mediastrip[3]
	imgurl = imgtags['src']
	resp = urllib.request.urlopen(imgurl)
#resp = urllib.urlopen(imgurl)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
# search for a person
person = ia.search_person('Shah Rukh Khan')
stringperson = str(person)
#print (stringperson)
id = stringperson[12:19]
link = "https://www.imdb.com/name/nm"+id
page = requests.get(link)
soup = BeautifulSoup(page.content, 'html.parser')
mediastrip = soup.find_all('div', class_ = 'mediastrip')
for a in mediastrip:
	thumbnails = a.find_all('a')
	for a in thumbnails:
		get_image("https://www.imdb.com/"+ a['href'])