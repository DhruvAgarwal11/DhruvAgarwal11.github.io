To run the code, you should simply install all the modules at the top of main.py and do python3 main.py

Depending on the type of metric we want to use (NCC/Euclidean), the comparison type on line 84 can be modified to "ncc" or "euclidean".

In the same directory as main.py, the folders with the input images (should contain the 3 gray-scale images) and output images (the ones where the image will be outputted to) should also be modified. This is on lines 93, 95, and 112. It will automatically run on all of the input images within the input folder.