import cv2
import numpy as np
import imutils
from skimage.filters import threshold_local
from transform import order_points

def load_and_preprocess_image(image_path):
    """Lädt das Bild und skaliert es auf eine einheitliche Höhe."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Bild nicht gefunden: {image_path}")
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)
    return image, orig, ratio

def detect_edges(image):
    """Konvertiert das Bild in Graustufen und findet Kanten."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 75, 200)
    return edged

def find_document_contour(edged):
    """Findet die Kontur des Dokuments im Bild."""
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            return approx
    raise ValueError("Keine Dokumentenkontur gefunden.")

def order_points(pts):
    """Ordnet die Punkte im Uhrzeigersinn: top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")

    # Summe und Differenz der Koordinaten berechnen
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    # Punkte zuordnen
    rect[0] = pts[np.argmin(s)]  # Top-left hat die kleinste Summe
    rect[2] = pts[np.argmax(s)]  # Bottom-right hat die größte Summe
    rect[1] = pts[np.argmin(diff)]  # Top-right hat den kleinsten Unterschied
    rect[3] = pts[np.argmax(diff)]  # Bottom-left hat den größten Unterschied

    return rect

def apply_perspective_transform(orig, screenCnt, ratio, width=500, height=700):
    """Wendet eine Perspektivtransformation an, um das Dokument zu begradigen."""
    screenCnt = order_points(screenCnt)
    # Scale the points back to the original image size
    warped = cv2.warpPerspective(
        orig,
        cv2.getPerspectiveTransform(screenCnt, np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")),
        (500, 700)
    )
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset=10, method="gaussian")
    warped = (warped > T).astype("uint8") * 255
    return warped


def main(image_path, output_path):
    """Hauptfunktion zum Scannen eines Dokuments."""
    image, orig, ratio = load_and_preprocess_image(image_path)
    edged = detect_edges(image)
    screenCnt = find_document_contour(edged)
    screenCnt = screenCnt.reshape(4, 2).astype("float32") * ratio
    print(f"screenCnt shape: {screenCnt.shape}, dtype: {screenCnt.dtype}")
    scanned = apply_perspective_transform(orig, screenCnt, ratio)

    # Ergebnisse anzeigen und speichern
    cv2.imshow("Original", imutils.resize(orig, height=500))
    cv2.imshow("Scanned", imutils.resize(scanned, height=500))
    cv2.imwrite(output_path, scanned)
    print(f"Gescanntes Dokument gespeichert unter: {output_path}")
    cv2.waitKey(1)
    cv2.destroyAllWindows()

def convert_image_path_to_output_path(image_path):
    """Konvertiert den Bildpfad in den Ausgabeordner."""
    base_name = image_path.split("\\")[-1]
    output_path = f'c:\\Users\\yanni\\Desktop\\python Scanner\\scanned.{base_name}'
    return output_path

if __name__ == "__main__":
   
    image_path = "c:\\Users\\yanni\\Desktop\\IMG_20250404_225729.jpg"
    output_path = convert_image_path_to_output_path(image_path)
    
    main(image_path, output_path)