from visual import *
from subprocess import call
import time

image_path = "vpython_img/3dstudy_"
screenshot_cmd = ["spectacle", "-a", "--background", "-o"] # image_path will be appended

def screenshot(outfile):
    time.sleep(1)
    call(screenshot_cmd + [outfile])


scene2 = display(background=(0.85,0.85,0.85), width=1000, height=700, autoscale=False, center=(-7, 4, 3))
scene2.select()

xy=[]
xy.append( box(pos=vector(0,0,0), size=(8,4,0),color=color.red, opacity=0.2) )
xy.append( arrow(pos=vector(-3.8,1,0), color=color.red) )


#Basic rotate-x/y/z planes

rotatex=[]
for obj in xy:
    rotatex.append( obj.__copy__() )
for obj in rotatex:
    obj.rotate( angle=radians(90), axis=(1,0,0), origin=(0,0,0) )

rotatey=[]
for obj in xy:
    rotatey.append( obj.__copy__(color=color.blue) )
for obj in rotatey:
    obj.rotate( angle=radians(90), axis=(0,1,0), origin=(0,0,0) )


rotatez=[]
for obj in xy:
    rotatez.append( obj.__copy__(color=(1,0,1)) ) # purple
for obj in rotatez:
    obj.rotate( angle=radians(90), axis=(0,0,1), origin=(0,0,0) )

label=label(pos=(-12,8,0), text="The basic rotate-x/y/z planes\nArrow marks top left corner")

screenshot(image_path + "1.png")


# Add the missing 2 to cover all angles: rotatexz and rotateyz

rotatezx=[] # sibling with rotatey
for obj in xy:
    rotatezx.append( obj.__copy__(color=color.blue) )
for obj in rotatezx:
    obj.rotate( angle=radians(90), axis=(1,0,0), origin=(0,0,0) )
    obj.rotate( angle=radians(90), axis=(0,0,1), origin=(0,0,0) )

rotatezy=[] # sibling with rotatez
for obj in xy:
    rotatezy.append( obj.__copy__(color=(1,0,1)) ) # purple
for obj in rotatezy:
    obj.rotate( angle=radians(90), axis=(0,1,0), origin=(0,0,0) )
    obj.rotate( angle=radians(90), axis=(0,0,1), origin=(0,0,0) )


label.text = "The basic rotate-x/y/z planes\nAdd rotatexz & rotateyz\nOrder matters: z first, x/y last\nBlue/Purple mismatch!"

screenshot(image_path + "2.png")


# Show the above if rotating x/y axis first
for obj in rotatezx:
    obj.opacity = 0
for obj in rotatezy:
    obj.opacity = 0

rotatexz=[] # sibling with rotatey
for obj in xy:
    rotatexz.append( obj.__copy__(color=color.blue) )
for obj in rotatexz:
    obj.rotate( angle=radians(90), axis=(0,0,1), origin=(0,0,0) )
    obj.rotate( angle=radians(90), axis=(1,0,0), origin=(0,0,0) )

rotateyz=[] # sibling with rotatez
for obj in xy:
    rotateyz.append( obj.__copy__(color=(1,0,1)) ) # purple
for obj in rotateyz:
    obj.rotate( angle=radians(90), axis=(0,0,1), origin=(0,0,0) )
    obj.rotate( angle=radians(90), axis=(0,1,0), origin=(0,0,0) )

label.text = "The basic rotate-x/y/z planes\nAdd rotatexz & rotateyz\nNow: x/y first, z last\nThis matches impress.js\n(Note that y-axis in a browser DOM\npoints down.)"

screenshot(image_path + "3.png")

# Take the basic planes, rotate 45 deg around y
for obj in rotatexz:
    obj.opacity = 0
for obj in rotateyz:
    obj.opacity = 0

all= xy + rotatex + rotatey + rotatez + rotatexz + rotateyz + rotatezx + rotatezy
for obj in all:
    obj.rotate( angle=radians(45), axis=(0,1,0), origin=(0,0,0) )

label.text = "Rotate everything 45 deg\nDirection is opposite, due to y-axis\nUnlike impress.js,\nred plane follows others!"

screenshot(image_path + "4.png")

# Also show the rotate x/y+z planes for full picture
rotatexz[0].opacity = 0.2
rotatexz[1].opacity = 1
rotateyz[0].opacity = 0.2
rotateyz[1].opacity = 1

label.text = "Rotate everything 45 deg\nDirection is opposite, due to y-axis\nUnlike impress.js,\nred plane follows others!\nAdd the last two planes\nAgain, blue plane is ok."

screenshot(image_path + "5.png")
