from PIL import Image


def change_size(path):
    fixed_height = 350
    img = Image.open(path)
    height_percent = (fixed_height / float(img.size[1]))
    width_size = int((float(img.size[0]) * float(height_percent)))
    new_image = img.resize((width_size, fixed_height))
    rgb_im = new_image.convert('RGB')
    rgb_im.save(path)