import cv2
import imutils

# Bild laden
image = cv2.imread('c:\\Users\\yanni\\Desktop\\IMG_20250404_224613.jpg')  # oder vollständiger Pfad
image = imutils.resize(image, height = 500)

if image is None:
    print("Fehler: Bild nicht gefunden!")
else:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert the image to grayscale
    gray = cv2.GaussianBlur(gray, (5, 5), 0) # blur it
    edged = cv2.Canny(gray, 75, 200) # and find edges in the image

    # Bilder anzeigen
    cv2.imshow('Original', image)
    cv2.imshow('Kanten', edged)
    
    # Warten auf Tastendruck & Fenster schließen
    cv2.waitKey(0)
    cv2.destroyAllWindows()