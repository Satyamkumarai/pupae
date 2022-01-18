from globals import *

def classify_range(val,THRESHOLDS =THRESHOLDS,CLASSES=CLASSES):
	if val==0:
		return CLASSES[0]
	for index, th in enumerate(THRESHOLDS):
		if val<=th:
			return CLASSES[index-1]
		
def getTh(window,low = True):
	r,g,b = 'Rl','Gl','Bl'
	if not low:
		r,g,b = 'Rh','Gh','Bh'
	r = cv2.getTrackbarPos(r,window)
	g = cv2.getTrackbarPos(g,window)
	b = cv2.getTrackbarPos(b,window)
	return np.array([r,g,b])
