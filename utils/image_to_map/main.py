import cv2
import numpy as np
import json

# Opening JSON file
img = cv2.imread('/home/zodiac/code/perso/Poke/utils/bourg_pal.png')
f = open('map_out.json')
data = json.load(f)

for k,v in data["ref"].items():
    if v[0] < 6399 or v[1] < 6399:
        print(v[0],':',v[0]+16," ",v[1],':',v[1]+16)
        # print(v[0],':',v[1])
        cropped_image = img[v[1]:v[1]+16, v[0]:v[0]+16]
        cv2.imwrite("data/"+k+".jpg", cropped_image)

exit(0)

print(img.shape) # Print image shape
cv2.imshow("original", img)

# Cropping an image

# Display cropped image
cv2.imshow("cropped", cropped_image)

# Save the cropped image

cv2.waitKey(0)
cv2.destroyAllWindows()
