#IMPORTANT ASSUMPTION: WE ASSUME THAT THE PERSON WE SEARCH FOR SHOWS UP FIRST IN IMDB SEARCH RESULT PAGE

# Import the required modules

import cv2, os
import numpy as np
from PIL import Image
import wikipedia
import tkinter as tk
from imdb import IMDb
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
def inputImages(image_path): #Function to Train new Images taking the path of folder containing the user input images, function starts after 16 lines, label: calling face croppping
	def faceCrop(image_path): #Funcrion to crop the input images and crop it to the detected face
		face_cascade = (r'C:\Users\India\Desktop\Project\haarcascade_frontalface_alt.xml') #One of the face detector modules
		cascade = cv2.CascadeClassifier(face_cascade) #initializing the classifier, skips the function from next line and goes to for loop (label: reading images)
		def save_faces(cascade, imgname): #function to save images in thr folder
			img = cv2.imread(os.path.join(image_path, imgname)) #OpenCV function to read images
			for i, face in enumerate(cascade.detectMultiScale(img)): #enum function that returns the counter i and corresponding face from mane faces detected in an image
				x, y, w, h = face #representing image mathematically, x=0,y=0 start from top-left of image so to get full image, w and h are utilised
				sub_face = img[y:y + h, x:x + w] #faces get cropped (x,y are starting coordinates in image and h,w show the distance in bith axis, an image is formed from coordinates y+h and x+w) and are stored in a list sub_faces, may contain multiple faces if an image has them
				path = os.path.join("faces", "{}_{}.jpg".format(imgname, i)) #renaming an image after detecting face in it in path "faces", should be created before
				cv2.imwrite(path, sub_face) #writing an image or saving it in the folder
				print (path) #a confirmation to show where the image is saved, path shown in terminal
#label: reading images
		for f in [f for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))]: #reading each image file 'f' in  folder image_path=images-to-train 
			print (f) #not required
			save_faces(cascade, f) #function to crop images to faces and save them
#label: calling face croppping
	faceCrop(image_path)
	print("Images are being pre-processed")
	#pre-processing: after cropping faces from input images,and renamed to "subject<counter>.train<1-10..>"
	source_path = (r'C:\Users\India\Desktop\Project\faces') #contains faces cropped from faceCrop
	dest_path = (r'C:\Users\India\Desktop\Project\training-faces') #to save images after renaming
	counter = open("count.txt","r+"); #counter file(contains only a number), a global number to uniquely name the files to be saved, everytime next batch when changed counter will have unique number
	count = counter.read()  #reads the number from counter file and initialize to var counter
	print(count) #only for confirmation
	#count=int(count)+1 
	int_of_count=int(count)  #increases the count var as the one read will be for previous batch
	faces = os.listdir(source_path) #reading all files from folder and adding to files list
	i = 0 #for loop iterator
	for face in faces: #'faces[face]' is a single filename from the list of 'faces[]'
		os.rename(os.path.join(source_path, face), os.path.join(dest_path, 'subject'+str(count)+'.train'+str(i))) #reanaming a file subject(count=18..19..20).train(i=1..2..3)
		print("file {} renamed", format(i)) #for confirmation
		i = i+1
	int_of_count=int_of_count+1
	counter.seek(0) #seek function brings cursor to 0, just like accessing arr[0]
	counter.write(str(int_of_count)) #stringifying incremented count and writing it to file[0]
	counter.close() #close file after reading or writing

#IMDB Scraping
def get_image(link):
	#webdriver is a software(light browser limited to web development etc) used by usually web developers for testing sites, etc
	driver = webdriver.PhantomJS() #initialing PhantomJS (a headless browser...i'll explain what it is by call)
	driver.get(link) # load the web page
	innerHTML = driver.execute_script("return document.body.innerHTML") #as it has javascript, this line executes javascript and loads containing html after script execution
	parsed = BeautifulSoup(innerHTML,"html.parser") #parsing the html to scrape tags and other contents
	driver.close() #close driver closes the headless browser, else it unnecessarily takes up RAM
	imageTags = parsed.find_all('img', class_= 'pswp__img') #list of img tags(whose class is like "pswp__img") among all the html tags that are loaded after the script execution
	imgtag = imageTags[3] #imageTags list has all img tags as its elements and the one we require is the 3rd on the list (list starts from [0])
	imgurl = imgtag['src'] #that 3rd element has the required image, so we extract its source as imgurl
	resp = urllib.request.urlopen(imgurl) #urllib module has submodule urllib.request having function urlopen which does as function says
#resp = urllib.urlopen(imgurl)
	image = np.asarray(bytearray(resp.read()), dtype="uint8") #image that are read from url (raw byte-sequence) are converted to bytearray with 'uint8' datatype and then to numpy array
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)# converted np array is a 1D long array, imdecode converts to 2D array assuming RGB components
	cv2.imshow("Image", image) #open the image
	cv2.waitKey(3)
	
# search for a person in imdb
def search_imdb(name):
	person = ia.search_person(name) #imdb package has function to search person, returns a list of search results 
	stringperson = str(person) #converting it to string
	#print (stringperson) #uncomment to see the whole list generated
	id = stringperson[12:19] #IMPORTANT ASSUMPTION: here we assume the one we search for will show up first in search result page
	link = "https://www.imdb.com/name/nm"+id #if the person is robert downey jr, 'link' variable becomes "https://www.imdb.com/name/nm/Robert_Downey_Jr"
	page = requests.get(link) #GET request to the link and saving the webpage
	soup = BeautifulSoup(page.content, 'html.parser')# parsing the webpage using beautifulsoup
	mediastrip = soup.find_all('div', class_ = 'mediastrip')#mediastrip is a class of <div> tag having a thumbnail of 6 images, so find_all()finds all div tags having class="mediastrip"
	for a in mediastrip: #as medaistrip contains 6 image thumbnails each having a link to its own full res image, i.e., 6 anchor (a) tags
		thumbnails = a.find_all('a') #finding each thumbnail
		for a in thumbnails:
			get_image("https://www.imdb.com/"+ a['href'])
def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.test')]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
            cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
            cv2.waitKey(50)
    # return the images list and labels list
    return images, labels

def get_wiki(name):
    summary = wikipedia.summary(name, sentences = 10)
    root = tk.Tk()
    #explanation = summary
    root.geometry("500x500")
    height = 50
    w2 = tk.Label(root,justify=tk.LEFT, padx = 10, text=summary, wraplength=250).pack(side="left")
    #root.resizable(width=100,height=100)	
    root.mainloop()
	
# Path to the Yale Dataset
path = './training-faces'
name_for_faces = []
print(name_for_faces)
#print (len(name_for_faces))
# Call the get_images_and_labels function and get the face images and the 
# corresponding labels
# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.face.LBPHFaceRecognizer_create()
case = input("Do you want to add new training images? y or n: ")
if (case == "Y" or case == "y"):
	name = input("Who is this person?") #name will have the value 'SRK'
	name_for_faces.append(name)
	#print("name_for_faces")
	print("Make sure training images exist in folder images-to-train")
	inputImages("images-to-train")

	
elif (case == "N" or case == "n"):
	print(case)

case = input("Do you want to train the model? y/Y Or n/N: ")
print (case)

if (case == "N" or case == "n"):
	print("Training Skipped, Trained file is loaded and now predicting faces")
	recognizer.read("trained-data.yml")
elif (case == "Y" or case == "y"):
	print ("Trainnig has Started!")
	images, labels = get_images_and_labels(path)
	cv2.destroyAllWindows()
	# Perform the tranining
	recognizer.train(images, np.array(labels))
	recognizer.save("trained-data.yml")
else:
	print("Wrong Input, exiting..")
	exit()
 #testing
# Append the images with the extension .test into image_paths
image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.test')]
print(image_paths)
for image_path in image_paths:
    predict_image_pil = Image.open(image_path).convert('L')
    predict_image = np.array(predict_image_pil, 'uint8')
    faces = faceCascade.detectMultiScale(predict_image)
    for (x, y, w, h) in faces:
        nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
        nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        if nbr_actual == nbr_predicted:
            print ("{} is Correctly Recognized as {} with confidence {}".format(nbr_actual, name_for_faces[nbr_predicted], conf))
        else:
            print ("{} is Incorrect Recognized as {}".format(nbr_actual, nbr_predicted))
        cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
        cv2.waitKey(1000)
        search_imdb(name_for_faces[nbr_predicted])
        get_wiki(name_for_faces[nbr_predicted])
