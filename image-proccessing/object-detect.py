import cv2
import sys
import os
import serial


refPt = []
mouse_click = False
start_detect = False

ser = serial.Serial(
    port='/dev/ttyMCC',
    baudrate=115200,
    parity=serial.PARITY_ODD, 
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS 
)

# Check if Serial is Open, close it then re-open (to avoid exception)
if ser.isOpen():
    ser.close()
ser.open()


def click_and_crop(event, x, y, flags, param):
	global refPt, cropping, mouse_click, start_detect
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		mouse_click = False

	elif event == cv2.EVENT_LBUTTONUP:
		refPt.append((x, y))
		mouse_click = True
		start_detect = False

video_capture = cv2.VideoCapture(1)
video_capture.set(3, 320)
video_capture.set(4, 240)
screen_width = video_capture.get(3)
screen_height = video_capture.get(4)

x_coord = int(screen_width/2)
y_coord = int(screen_height/2)

print x_coord, y_coord
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
while True:
    ret, frame = video_capture.read()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
   
    if mouse_click == True and start_detect == False:
	if refPt[1][0] - refPt[0][0] > 20:
	    cv2.rectangle(img_gray, refPt[0], refPt[1], (0, 255, 0), 2)
	elif os.path.exists("roi.jpg"):
	    start_detect = True

    if start_detect == True:
	template = cv2.imread('roi.jpg',0)
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	cv2.rectangle(img_gray, max_loc, (max_loc[0] + w, max_loc[1] +h), (0,255,125), 1)
	cv2.rectangle(img_gray, (x_coord - 40, y_coord - 40), (x_coord + 40, y_coord + 40), (0,255,125), 1)

	cv2.imshow("res", res)
	x_object = max_loc[0] + w/2
	y_object = max_loc[1] + h/2
	#1 trai, 2 phai
	if x_object > (x_coord + 40):   
	    ser.write('1')
	elif x_object < (x_coord - 40):
	    ser.write('2')
	else:
	    ser.write('')
	#3 xuong, 4 len
	if y_object > (y_coord + 40):
	    ser.write('3')
	elif y_object < (y_coord - 40):
	    ser.write('4')
	else:
	    ser.write('')

    #wait event from keyboard
    key = cv2.waitKey(1) & 0xFF
    if key == ord("r"):
	mouse_click = False
	start_detect = False
	ser.write('0')
    elif key == ord("q"):
	break
    elif key == ord("c"):
	clone = frame
	roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
	cv2.imwrite("roi.jpg", roi)
	cv2.imshow("roi", roi)
	start_detect = True

    cv2.imshow("image", img_gray)
    
video_capture.release()
cv2.destroyAllWindows()
