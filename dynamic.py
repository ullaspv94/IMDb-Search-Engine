# The standard library modules
import os
import sys
import requests
from PIL import Image
from io import StringIO

# The wget module
import wget
import numpy as np
import urllib.request
import cv2
# The BeautifulSoup module
from bs4 import BeautifulSoup
import re

# The selenium module
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
driver = webdriver.PhantomJS()
#options = Options()
#options.set_headless(headless=True)
#driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'C:\Users\ullaspv94\AppData\Local\Programs\Python\Python36-32')
#driver = webdriver.Firefox() # if you want to use chrome, replace Firefox() with Chrome()
driver.get("https://www.imdb.com/name/nm0000375/mediaviewer/rm514148352") # load the web page
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

# for websites that need you to login to access the information
#elem = driver.find_element_by_id("email") # Find the email input field of the login form
#elem.send_keys("user@example.com") # Send the users email
#elem = driver.find_element_by_id("pwd") # Find the password field of the login form
#elem.send_keys("userpwd") # send the users password
#elem.send_keys(Keys.RETURN) # press the enter key

#driver.get("http://www.example.com/path/of/video/page.html") # load the page that has the video
'''print ("waiting")
WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "pswp__img"))) # waits till the element with the specific id appears
print("waiting done")
src = driver.page_source # gets the html source of the page

parser = BeautifulSoup(src,"html.parser") # initialize the parser and parse the source "src"
list_of_attributes = {"class" : "pswp__img"} # A list of attributes that you want to check in a tag
tag = parser.findAll('image',attrs=list_of_attributes) # Get the video tag from the source
print(tag)
n = 0 # Specify the index of video element in the web page
url = tag[n]['src'] # get the src attribute of the video
print(url)
#wget.download(url,out="path/to/output/file") # download the video

driver.close() # closes the driver'''

'''Code 1
from selenium import webdriver
import numpy as np
browser = webdriver.PhantomJS()
 
browser.get("https://www.imdb.com/name/nm0005683/mediaviewer/rm2073384192")
 
divi=browser.find_element_by_id("photo-container")
print(divi)
 
browser.close()
'''
'''code 2
import bs4 as bs
import sys
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def main():
    page = Page('https://www.imdb.com/name/nm0005683/mediaviewer/rm2073384192')
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    imagetag = soup.find('div', id='photo-container')
    print (imagetag)

if __name__ == '__main__': main()'''
'''
code 3 
import dryscrape

sess = dryscrape.Session()
sess.visit('https://www.imdb.com/name/nm0005683/mediaviewer/rm2073384192')
source = sess.body()

soup = bs.BeautifulSoup(source,'html.parser')
js_test = soup.find('div', id='photo-container')
print(js_test)'''