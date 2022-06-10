from PIL import Image, ImageFont, ImageDraw
from os.path import exists
import textwrap

def decode_image(file_location="images/SUS_encode.png"):

    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    tmp = 0

    decoded_image = Image.new("RGB", encoded_image.size)
    px = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            if bin(red_channel.getpixel((i, j)))[-1] == '0':
                px[i, j] = (255, 255, 255)
            else:
                px[i, j] = (0, 0, 0)

    file_exists = exists("images/SUS_decode.png")
    while file_exists is True:
        tmp += 1
        file_exists = exists("images/SUS_decode" + str(tmp) + ".png")
        if file_exists is False:
            decoded_image.save("images/SUS_decode" + str(tmp) + ".png")
    
    decoded_image.save("images/SUS_decode.png")

def write_text(text_to_write, image_size):

    img_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(img_text)

    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return img_text

def encode_image(text_to_encode, tempPNG="Stegano/images/SUS.png"):

    tempPNG = Image.open(tempPNG)
    redtmp = tempPNG.split()[0]
    greentmp = tempPNG.split()[1]
    bluetmp = tempPNG.split()[2]

    x_size = tempPNG.size[0]
    y_size = tempPNG.size[1]

    img_text = write_text(text_to_encode, tempPNG.size)
    drawtext = img_text.convert('1')
    encoded_image = Image.new("RGB", (x_size, y_size))
    px = encoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            redpx = bin(redtmp.getpixel((i, j)))
            encodepx = bin(drawtext.getpixel((i, j)))

            if encodepx[-1] != '1':
                redpx = redpx[:-1] + '0'
            else:
                redpx = redpx[:-1] + '1'
            px[i, j] = (int(redpx, 2), greentmp.getpixel((i, j)), bluetmp.getpixel((i, j)))
    encoded_image.save("images/SUS_encode.png")


#decode_image()
encode_image("Encoding the image...!")