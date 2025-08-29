from PIL import Image
import os
imgs = [Image.open("0/media/part4/" + i) for i in os.listdir("0/media/part4")]
imgs[0].save("output.gif", save_all=True, append_images=imgs[1:], duration=200, loop=0)
