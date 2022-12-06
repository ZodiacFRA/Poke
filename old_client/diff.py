# import required module
import os
import cv2
# assign directory
directory = './img'

# iterate over files in
# that directory
with open("image_paths.js", "w+") as out:
   out.write("const images = [\n")
   for filename in os.listdir(directory):
      f = os.path.join(directory, filename)
      # checking if it is a file
      if os.path.isfile(f):
         out.write("\t\"" + f + "\",\n")
   out.write("];\n")
