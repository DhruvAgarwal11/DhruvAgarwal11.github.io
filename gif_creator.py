from PIL import Image
import os
imgs = [Image.open("0/media/part3/" + i) for i in sorted(os.listdir("0/media/part3"))]
imgs[0].save("0/media/part3/output.gif", save_all=True, append_images=imgs[1:], duration=200, loop=0)
