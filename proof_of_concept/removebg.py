import PIL
import rembg

image = PIL.Image.open('your file here.')

rembg.remove(image).save("output file goes brrr (.png)")
