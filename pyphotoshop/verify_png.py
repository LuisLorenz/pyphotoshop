# from PIL import Image as PILImage
# try:
#     img = PILImage.open('Italia1.png')
#     img.verify()
#     print("Image is valid")
# except Exception as e:
#     print(f"Invalid image file: {e}")


# from PIL import Image

# img = Image.open('/Users/luislorenz/Documents/IT/git/py beginner projects/photo_manipulation_general/input/Italia2.jpg')
# img.show()

from PIL import Image

img = Image.open('/Users/luislorenz/Documents/IT/git/py beginner projects/photo_manipulation_general/input/Italia2.jpg')
print(f"Image format: {img.format}")
print(f"Image size: {img.size}")
print(f"Image mode: {img.mode}")
img.show()
