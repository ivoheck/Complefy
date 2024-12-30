import cv2
import numpy as np

image_path = 'stundenplan.png'  # Pfad zu deinem PNG-Bild
image = cv2.imread(image_path)

coords =  {'Montag': [np.float64(151.5), np.float64(25.5)], 
           'Dienstag': [np.float64(333.5), np.float64(25.0)], 
           'Mittwoch': [np.float64(518.0), np.float64(25.0)], 
           'Donnerstag': [np.float64(700.5), np.float64(25.5)], 
           'Freitag': [np.float64(885.0), np.float64(26.0)], 
           '8.00': [np.int32(27), np.int32(47)], 
           '9.00': [np.int32(29), np.int32(111)], 
           '10.00': [np.int32(21), np.int32(173)], 
           '11.00': [np.int32(21), np.int32(235)], 
           '12.00': [np.int32(21), np.int32(297)], 
           '13.00': [np.int32(21), np.int32(359)], 
           '14.00': [np.int32(21), np.int32(421)], 
           '15.00': [np.int32(21), np.int32(483)], 
           '16.00': [np.int32(21), np.int32(545)], 
           '17.00': [np.int32(21), np.int32(607)], 
           '18.00': [np.int32(21), np.int32(669)], 
           '19.00': [np.int32(21), np.int32(731)]}

# Zeichne die Punkte und Beschriftungen
for key, (x, y) in coords.items():
    x, y = int(x), int(y)  # Konvertiere in Ganzzahlen
    cv2.circle(image, (x, y), radius=5, color=(0, 255, 0), thickness=-1)  # Punkt
    cv2.putText(image, key, (x + 10, y + 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=0.5, color=(255, 255, 255), thickness=1)  # Text

# Bild anzeigen
cv2.imshow("Koordinaten auf Bild", image)
cv2.waitKey(0)
cv2.destroyAllWindows()