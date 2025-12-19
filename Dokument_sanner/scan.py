from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

'''image_path = 'c:\\Users\\yanni\\Desktop\\IMG_20250404_225729.jpg'''

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,default= 'c:\\Users\\yanni\\Desktop\\IMG_20250404_225729.jpg', help="Path to the image to be scanned")
args = vars(ap.parse_args())
# ap.add_argument("-i", "--image", required=True, help="Path to the image to be scanned")


"""Lädt das Bild und skaliert es auf eine einheitliche Höhe."""
image_path = args["image"]
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Image not found at path: {image_path}")

ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

"""Konvertiert das Bild in Graustufen und findet Kanten."""
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert the image to grayscale
#gray = cv2.GaussianBlur(gray, (5, 5), 0) # blur it
edged = cv2.Canny(gray, 75, 200) # and find edges in the image


"""Findet die Kontur des Dokuments im Bild."""
# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse= True)[:5]


# loop over the contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        screenCnt = approx
        break   
if screenCnt is None:
    raise ValueError("Could not find a document contour")

# show the original image and the edge detected image
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)

# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)

# apply the four point transform to obtain a top-down
# view of the original image
#warped = four_point_transform(orig, ratio * screenCnt.reshape(4, 2).astype("float32"))
screenCnt = screenCnt.reshape(4, 2).astype("float32") * ratio
warped = cv2.warpPerspective(
        orig,
        cv2.getPerspectiveTransform(screenCnt, np.array([[0, 0], [500, 0], [500, 700], [0, 700]], dtype="float32")),
        (500, 700)
    )
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)  # convert the image to grayscale
T = threshold_local(warped, 11, offset=10, method="gaussian")  # black and white effect
warped = (warped > T).astype("uint8") * 255  # convert to black and white
      

# show the original and scanned images
print("STEP 3: Apply perspective transform")
cv2.imshow("Scanned", imutils.resize(warped, height = 500))
cv2.waitKey(0)
cv2.destroyAllWindows()



'''import argparse
import cv2
import imutils
from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local

def load_and_preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)
    return image, orig, ratio

def detect_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 75, 200)
    return edged

def find_document_contour(edged):
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            return approx
    raise ValueError("Could not find a document contour")

def apply_perspective_transform(orig, screenCnt, ratio):
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset=10, method="gaussian")
    warped = (warped > T).astype("uint8") * 255
    return warped

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False, default="c:\\Users\\yanni\\Desktop\\IMG_20250404_225729.jpg", help="Path to the image to be scanned")
    ap.add_argument("--output", type=str, default="scanned_output.jpg", help="Path to save the scanned image")
    args = vars(ap.parse_args())

    image, orig, ratio = load_and_preprocess_image(args["image"])
    edged = detect_edges(image)
    screenCnt = find_document_contour(edged)
    warped = apply_perspective_transform(orig, screenCnt, ratio)

    cv2.imshow("Scanned", imutils.resize(warped, height=750))
    cv2.imwrite(args["output"], warped)
    print(f"Scanned image saved to {args['output']}")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()    '''