from PIL import Image,ImageFont,ImageDraw

def writeClyde(text):
    img = Image.open("clyde-message.jpeg")
    font = ImageFont.truetype("arial.ttf", 14)


    draw = ImageDraw.Draw(img)

    draw.text((70,30), text, (255,255,255),font=font)
    img.save("msg.png")
