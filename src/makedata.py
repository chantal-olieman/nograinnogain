#!/usr/bin/env python
import numpy as np
from PIL import Image
from sklearn import svm
import matplotlib.pyplot as plt

def makearray(imname, x, y):
	filename = "../img/%s.jpeg" % imname
	imgs = Image.open(filename)
	im = imgs.resize((x, y), Image.ANTIALIAS)
	arr = np.array(im)
	#instead of a matrix make a vector
	arr2d = arr.reshape(-1,arr.shape[2])
	return arr2d

def maketxtfile(imname, x, y):
	filename = "../img/%s.jpeg" % imname
	imgs = Image.open(filename)
	im = imgs.resize((x, y), Image.ANTIALIAS)
	arr = np.array(im)
	#instead of a matrix make a vector
	arr2d = arr.reshape(-1,arr.shape[2])
	#Already halve x and y
	return arr2d

	y = y/2
	x = x/2 
	#fill the rest of the array
	while x > 0 and y > 0:
		im = imgs.resize((x, y), Image.ANTIALIAS)
		arr = np.array(im)
		arr2dres = arr.reshape(-1,arr.shape[2])
		y = y/2 
		x = x/2 
		arr2d = np.concatenate((arr2d, arr2dres))

	#save the file 
	filename = "../data/%s.txt" % imname
	np.savetxt(filename, arr2d,fmt='% 4d' ,delimiter=' ')
	return arr2d

def createXY(types):
	X = maketxtfile(types[0], (x/2) ,(y/2))
	m, n = X.shape
	Y = 0 * np.ones((m,1),int)
	for i in range(1, len(types)):
		#read in i case 
		Xres = maketxtfile(types[i], x ,y)
		m, n = Xres.shape
		Yres = i * np.ones((m,1),int)
		#merge red with X and Y 
		X = np.concatenate((X, Xres))
		Y = np.concatenate((Y, Yres))
	return (X, Y)

def classify(clf, Z, n):
	result = 0 * np.ones((n,1))
	for i in range(len(Z)):
    		label = clf.predict(Z[i].reshape(1,-1))
		label = int(round(label))
		result[label] = result[label] + 1 
	return result/len(Z)

def plot(results, labels):
	sizes = results*100
	colors = ['red', 'gold', 'lightskyblue', 'yellowgreen', 'purple', 'blue']
	explode = (0, 0, 0, 0, 0, 0)  # explode a slice if required

	plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        	autopct='%1.1f%%', shadow=True)
        
	#draw a circle at the center of pie to make it look like a donut
	centre_circle = plt.Circle((0,0),0.40,color='black', fc='white',linewidth=0.75)
	fig = plt.gcf()
	fig.gca().add_artist(centre_circle)
	outside = plt.Circle((0,0),1.0,color='black', linewidth=0.75, fill=False)
	fig.gca().add_artist(outside)

	# Set aspect ratio to be equal so that pie is drawn as a circle.
	plt.axis('equal')
	plt.show()


types = ["stro", "red", "green", "graan", "stone", "black"] 
x = 16
y = 32


#read in data 
(X, Y) = createXY(types)
#preprocess Y
Y = Y.ravel()

# Fit estimators
from sklearn.neighbors import KNeighborsClassifier



#read in test file
x = 320
y = 160
Z = makearray("conta", x, y)
labels = 'Straw', 'Red kidney beans', 'Pumpkin seeds', 'Grain', 'Stones', 'Black lentils'


#train model
clf = KNeighborsClassifier( n_neighbors=5, weights='distance')
clf.fit(X, Y)

#classify test data
results = classify(clf, Z, len(types))
plot(results, labels)

