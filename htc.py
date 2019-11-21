import sys
import cv2 as cv
import numpy as np
def main(argv):
    
    default_file = 'smarties.png'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_COLOR)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1
    
    
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    
    
    gray = cv.medianBlur(gray, 5)
    
    
    rows = gray.shape[0]
    param0 = int(20 if rows / 8 < 20 else 50 if rows / 12 > 50 else rows / 12)
    param1 = int(100 if rows * 1.5 < 100 else 500 if rows * 1.5 > 500  else rows * 1.5)
    param2 = int(20 if rows / 12 < 20 else 45 if rows / 12 > 45 else rows / 12)
    
    print(rows, param0, param1, param2)
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, param0,
                               param1=param1, param2=param2,
                               minRadius=0, maxRadius=int(rows / 4.5))
    
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(src, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(src, center, radius, (255, 0, 255), 3)
    
    
    cv.imshow("detected circles", src)
    cv.waitKey(0)
    
    return 0
if __name__ == "__main__":
    main(sys.argv[1:])