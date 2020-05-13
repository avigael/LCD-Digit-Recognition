# email: code@gaels.us

import cv2, csv
import numpy as np

# load in data we collected from training
samples = np.loadtxt('data/sample.data', np.float32)
responses = np.loadtxt('data/response.data', np.float32)
# create model from collected data
responses = responses.reshape((responses.size, 1))
model = cv2.ml.KNearest_create()
model.train(samples, cv2.ml.ROW_SAMPLE, responses)

# sets row length of csv file
MAX_LENGTH = 50

webcam = cv2.VideoCapture(0)

# tags stored in row and previous tag stored in prevtag
prevtag = ""
row = list()

# creates csv file where numbers will be stored
with open('tags.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)

    while True:
        # capture frame by frame 
        ret, frame = webcam.read()
        im = frame
        # convert image to be more easily processed. treshhold is custom to this application 
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, 0, 1, 31, 2)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # we store tags as pairs with their x-coordinate to sort numbers left to right
        pair = []
        tag = ""

        for contour in contours:
            # for this application we discard areas smaller than 50
            if cv2.contourArea(contour) > 50:
                # collects dimension and coordinates for area
                [x, y, w, h] = cv2.boundingRect(contour)
                # restrict size of digit and placement of digits
                if h > 75 and y > 180 and y < 280:
                    # draws a box around detected area
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # use this region of interest with our model to get a possible number
                    rect = thresh[y:y + h, x:x + w]
                    subrect = cv2.resize(rect, (10, 10))
                    subrect = subrect.reshape((1, 100))
                    subrect = np.float32(subrect)
                    ret, res, nei, dis = model.findNearest(subrect, k=1)
                    # convert the results into an integer
                    token = str(int((res[0][0])))
                    # draw the found number above the detected area
                    cv2.putText(im, token, (x, y), 0, 2, (0, 0, 255), 2)
                    # add token and x-coord to pair for sorting
                    pair.append([x,token])
        # takes unsorted values and sort them according to their x-coordinate
        if len(pair) > 1:
            pair.sort(key = lambda x:x[0])
            for i in range(0,len(pair)):
                rec = pair[i]
                num = rec[1]
                tag += num

        # display image with collected data
        cv2.imshow("Capture", im)

        # current tag is the current detected tag
        print("Current Tag: " + tag)
        # previous tag added to the csv
        print("Previous Tag: " + prevtag)


        # max number of tags per row defined here
        if len(row) == MAX_LENGTH:
            print("Row complete!")
            csv_writer.writerow(row)
            row.clear()

        key = cv2.waitKey(0)
        # if user presses 'esc' or 'q' the program ends
        if key == 27 or key == ord('q'):
            # unadded tags are added to csv
            if len(row) != 0:
                csv_writer.writerow(row)
            break
        # tags are only added if the user presses 'c' to confirm the number is correct
        elif key == ord('c'):
            print("ADDED to CSV: " + tag)
            row.append(tag)
            prevtag = tag

        # if a user accidently adds a tag, the can remove the previous tag with 'r'
        elif key == ord('r'):
            print("REMOVED from CSV: " + prevtag)
            row.remove(prevtag)
            prevtag = ""   

video.release()