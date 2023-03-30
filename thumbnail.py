from PIL import Image, ImageChops
import math
import os
import sys

image_size = (500, 500)
top_face_size = (int(image_size[0]* 0.71), int(image_size[0]* 0.71))

folder = f"imagefolders/{sys.argv[1]}"


def DarkenImage(image, value):

    assert isinstance(image, Image.Image), "Must be Image"

    return ImageChops.multiply(image, Image.new('RGBA', image.size, (value, value, value)))   



def FormTopFace(image):

    assert isinstance(image, Image.Image), "Must be Image"

    image = image.resize(top_face_size)
    new_image = Image.new(mode='RGBA', size=image_size, color=(0,0,0,0))
    new_image.paste(image, box= [int(image_size[0] * 0.15), int(image_size[0] * 0.15)])
    new_image = new_image.rotate(-45)
    new_image = new_image.resize((image_size[0], int(image_size[1] / 2.208)))
    
    return new_image

def GetSideLength():
    h = image_size[1] / 2.208
    w = image_size[0]

    return int(math.sqrt( (h/2)**2 + (w/2)**2 ))

def FormSideFace(image, dir="left"):

    assert isinstance(image, Image.Image), "Must be Image"

    shear_amount = 0.45

    face_size = (int(image_size[0]/2), GetSideLength())

    image = image.resize(face_size)
    new_image = Image.new(mode='RGBA', size=(int(image_size[0]/2), image_size[0]), color=(0,0,0,0))
    
    if dir == "left":
        new_image.paste(image)
        new_image = new_image.transform(image_size, Image.Transform.AFFINE, (1, 0, 0, -shear_amount, 1, 0), Image.Resampling.BILINEAR)
    elif dir == "right":
        new_image.paste(image, box=(0, int((image_size[1] / 2.2)/ 2)))
        new_image = new_image.transform(image_size, Image.Transform.AFFINE, (1, 0, 0, shear_amount, 1, 0), Image.Resampling.BILINEAR)

    return new_image

def CreateThumbnail(filename):

    base_image = Image.new(mode='RGBA', size=image_size, color=(0,0,0,0))

    basest_image = Image.new(mode='RGBA', size=(int(image_size[0] * 1.1), int(image_size[0] * 1.1)), color=(0,0,0,0))

    sprite_image = Image.open(f"{folder}/{filename}")

    top_face = FormTopFace(sprite_image)
    left_side_face = FormSideFace(sprite_image)
    right_side_face = FormSideFace(sprite_image, "right")

    left_side_face = DarkenImage(left_side_face, 220)
    right_side_face = DarkenImage(right_side_face, 180)

    base_image.paste(top_face, mask=top_face)
    base_image.paste(left_side_face, mask=left_side_face, box=(0, int((image_size[1] / 2.2)/ 2)))
    base_image.paste(right_side_face, mask=right_side_face, box=(int(image_size[0] / 2), int((image_size[1] / 2.2)/ 2)))

    base_image = base_image.resize(size=[int(image_size[0]), int((image_size[1] * 1.1))])
    basest_image.paste(base_image, mask=base_image, box=(int((image_size[0] * 1.1 - image_size[0]) / 2), 0))

    basest_image = basest_image.resize(size=[int(basest_image.size[0] / 5), int(basest_image.size[1] / 5)])
    
    return basest_image

images =[]

for file in os.scandir(folder):
    if file.is_file():
        print("Adding " + file.name)
        images.append(file.name)

spritesheet = Image.new(mode="RGBA", size=[110 * len(images), 110], color=(0,0,0,0))

for i in range(len(images)):
    image = CreateThumbnail(images[i])
    spritesheet.paste(image, mask=image, box=[i * 110, 0])

spritesheet.save(f"{folder}.png")
