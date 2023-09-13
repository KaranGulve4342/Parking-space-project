import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48


def checkParkingSpace(imgPro):
    spaceCounter = 0
    vacantSpaces = []  # List to store the serial numbers and addresses of vacant spaces
    serialNumber = 1  # Serial number counter

    for pos in posList:
        if len(pos) >= 2:
            x, y = pos[:2]  # Extract the first two values (x, y) from the position tuple
        else:
            continue

        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 1000:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1

            # Add the serial number and address of the vacant space to the list
            vacantSpaces.append((serialNumber, pos))
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, (x, y), (x + width, y + height), color, thickness)
        # Display the serial number on the rectangle
        cv2.putText(img, f'{serialNumber}', (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        serialNumber += 1  # Increment the serial number counter

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20,
                       colorR=(157, 50, 168))

    # Create a new panel named "Vacant Spaces" and display the number and address of each vacant space
    panelHeight = 200 + len(vacantSpaces) * 100
    panel = np.ones((panelHeight, 500, 3), np.uint8) * 255  # Create a blank white panel

    for i, (number, address) in enumerate(vacantSpaces):

        if number <= 12:
            n = number
            A = f'C-1  R-{n}'
        elif (number > 12) and (number <= 24):
            n = number - 12
            A = f'C-2  R-{n}'
        elif (number > 24) and (number <= 35):
            n = number - 24
            A = f'C-3  R-{n}'
        elif (number > 35) and (number <= 46):
            n = number - 35
            A = f'C-4  R-{n}'
        elif (number > 46) and (number <= 58):
            n = number - 46
            A = f'C-5  R-{n}'
        else:
            n = number - 58
            A = f'C-6  R-{n}'

        cvzone.putTextRect(img, f'Vacant: {number}', (x + 10, y - 70), scale=1, thickness=1, offset=10,
                           colorR=(157, 50, 168))
        cvzone.putTextRect(img, f'Vacant: {number}', (x + 10, y + 20), scale=1, thickness=1, offset=10,
                            colorR=(157, 50, 168))

        cvzone.putTextRect(panel, f'Number: {number}', (50, 200 + i * 100), scale=2, thickness=3, offset=10,
                           colorR=(0, 0, 0))
        cvzone.putTextRect(panel, f'Address: {A}', (50, 240 + i * 100), scale=1.5, thickness=2, offset=10,
                           colorR=(0, 0, 0))

    # Resize the panel to fit the screen
    panel = cv2.resize(panel, (int(panel.shape[1] * 0.5), int(panel.shape[0] * 0.5)))

    cv2.imshow("Image", img)
    cv2.imshow("Vacant Spaces", panel)


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    key = cv2.waitKey(25) & 0xFF
    if key == 27:
        break
