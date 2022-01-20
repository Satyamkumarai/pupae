from globals import *

# based on threshold values return the index and the class of the PUPAE
def classify_range(val,THRESHOLDS =THRESHOLDS,CLASSES=CLASSES):
	print(f"Classifying the pupae for avg : {val}")
	if val==0:
		return 0,CLASSES[0]
	for index, th in enumerate(THRESHOLDS):
		if val<=th:
			return index-1,CLASSES[index-1]

# util function to retrive the  slider values from the filter window
def getTh(window,low = True):
	r,g,b = 'Rl','Gl','Bl'
	if not low:
		r,g,b = 'Rh','Gh','Bh'
	r = cv2.getTrackbarPos(r,window)
	g = cv2.getTrackbarPos(g,window)
	b = cv2.getTrackbarPos(b,window)
	return np.array([r,g,b])
