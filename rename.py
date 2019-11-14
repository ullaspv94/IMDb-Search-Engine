import os
def inputImages()
	source_path = (r'C:\Users\ullaspv94\Desktop\face_recognizer\face_recognizer\images-to-train')
	dest_path = (r'C:\Users\ullaspv94\Desktop\face_recognizer\face_recognizer\training-faces') 
	files = os.listdir(source_path)
	counter = open("count.txt","r+");
	count = counter.read()
	print(count)
	count=int(count)+1
	counter.seek(0)
	counter.write(str(count))
	# close file after reading or writing
	counter.close()
	i = 1
	for file in files:
		os.rename(os.path.join(source_path, file), os.path.join(dest_path, 'subject'+str(count)+'.train'+str(i)))
		print("file {} renamed"), format(i)
		i = i+1
