from pyimagesearch.transform import four_point_transform
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image file")
ap.add_argument("-c", "--coords", help="comma separated list of source points")
args = vars(ap.parse_args())

if args["image"] is None or args["coords"] is None:
    print("[ERROR] You must provide both --image and --coords")
    exit(1)

# load the image
image = cv2.imread(args["image"])

# parse the coordinate string into a NumPy array
pts = np.array([float(x) for x in args["coords"].split(",")], dtype="float32").reshape(4, 2)

# apply the four point transform
warped = four_point_transform(image, pts)

# show the images
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)
