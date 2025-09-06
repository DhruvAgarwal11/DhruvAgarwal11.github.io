# CS194-26 (CS294-26): Project 1 starter Python code

# these are just some suggested libraries
# instead of scikit-image you could use matplotlib and opencv to read, write, and display images

import numpy as np
import skimage as sk
import skimage.io as skio

# name of the input file
imname = 'monastery.jpg'

# read in the image
im = skio.imread(imname)

# convert to double (might want to do this later on to save memory)    
im = sk.img_as_float(im)
    
# compute the height of each part (just 1/3 of total)
height = np.floor(im.shape[0] / 3.0).astype(np.int64)
width = np.floor(im.shape[1]).astype(np.int64)
# separate color channels
b = im[:height]
g = im[height: 2*height]
r = im[2*height: 3*height]

# align the images
# functions that might be useful for aligning the images include:
# np.roll, np.sum, sk.transform.rescale (for multiscale)

def getValueImgEuclidean(oldEuclidean, oldCombinedImg, img1Temp, img2Temp, i, j, origImg1):
    curEuclidean = np.sqrt(np.sum(np.sum(np.square(img1Temp-img2Temp))))
    if curEuclidean < oldEuclidean:
        return curEuclidean, np.roll(np.roll(origImg1, i, axis=0), j, axis = 1)
    return oldEuclidean, oldCombinedImg

def getValueImgNCC(oldNCCValue, oldCombinedImg, img1Temp, img2Temp, i, j, origImg1):
    normPt1 = img1Temp.flatten() / np.linalg.norm(img1Temp, 2)
    normPt2 = img2Temp.flatten() / np.linalg.norm(img2Temp, 2)
    curNCC = np.dot(normPt1, normPt2)
    if curNCC > oldNCCValue:
        return curNCC, np.roll(np.roll(origImg1, i, axis=0), j, axis = 1)
    return oldNCCValue, oldCombinedImg

def align(img1, img2, comparisonType="euclidean"):
    if comparisonType == "euclidean":
        bestValue = float('inf')
    else:
        bestValue = -1
    combinedImg = None
    heightCropping = np.floor(0.05*height).astype(np.int64)
    widthCropping = np.floor(0.05*width).astype(np.int64)
    startImg1 = img1[heightCropping:-heightCropping, widthCropping:-widthCropping]
    startImg2 = img2[heightCropping:-heightCropping, widthCropping:-widthCropping]
    for i in range(-15, 15):
        for j in range(-15, 15):
            if i < 0:
                tempImg1 = startImg1[-i:]
                tempImg2 = startImg2[:len(img2) + i]
            else:
                tempImg1 = startImg1[:len(img1) - i]
                tempImg2 = startImg2[i:]
            if j < 0:
                tempImg1 = tempImg1[:, -j:]
                tempImg2 = tempImg2[:, :len(img2[0]) + j]
            else:
                tempImg1 = tempImg1[:, :len(img1[0]) - j]
                tempImg2 = tempImg2[:, j:]
            minX = min(len(tempImg1), len(tempImg2))
            minY = min(len(tempImg1[0]), len(tempImg2[0]))
            tempImg1 = tempImg1[:minX, :minY]
            tempImg2 = tempImg2[:minX, :minY]
            if comparisonType == "euclidean":
                bestValue, combinedImg = getValueImgEuclidean(bestValue, combinedImg, tempImg1, tempImg2, i, j, img1)
            else:
                bestValue, combinedImg = getValueImgNCC(bestValue, combinedImg, tempImg1, tempImg2, i, j, img1)
    return combinedImg

ag = align(g, b)
ar = align(r, b)
# create a color image
im_out = (np.dstack([ar, ag, b]) * 255).astype(np.uint8)
print(np.shape(im_out))

# save the image
fname = 'output/out_fname2.jpg'
skio.imsave(fname, im_out)

# display the image
skio.imshow(im_out)
skio.show()
