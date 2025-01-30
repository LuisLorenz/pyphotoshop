from PIL import Image

# Load the JPG image
jpg_image = Image.open('input/Italia2.jpg')

# Save as PNG
jpg_image.save('input/Italia2.png', format='PNG')
