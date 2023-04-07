from PIL import Image
import os

frames = [Image.open(f"gifframes/{file.name}") for file in os.scandir("gifframes")]

# frames = [frame.convert('PA') for frame in frames]

frames[0].save('sheet.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=100, loop=0, transparency=0)