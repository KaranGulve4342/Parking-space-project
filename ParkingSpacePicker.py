
import cv2
import pickle

width, height = 107, 48
posList = []

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

serialNumber = 1  # Initial serial number

def mouseClick(events, x, y, flags, params):
    global serialNumber

    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y, serialNumber))  # Append serial number to the position tuple
        serialNumber += 1  # Increment serial number

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1, _ = pos  # Extract only the (x, y) coordinates from the position tuple
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread('carParkImg.png')

    for pos in posList:
        x, y, serial = pos  # Extract the (x, y) coordinates and serial number from the position tuple
        cv2.rectangle(img, (x, y), (x + width, y + height), (255, 0, 255), 2)
        cv2.putText(img, str(serial), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
