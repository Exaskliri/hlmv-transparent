try:
    from cv2 import *
except:
    print("Fatal Error: CV2 is not installed. Please refer to README.md for dependencies.")
    print("Press enter to close...")
    a = input()
    sys.exit(0)
try:
    import PIL
except:
    print("Fatal Error: Pillow is not installed. Please refer to README.md for dependencies.")
    print("Press enter to close...")
    a = input()
    sys.exit(0)
try:
    import pyautogui
except:
    print("Fatal Error: PyAutoGUI is not installed. Please refer to README.md for dependencies.")
    print("Press enter to close...")
    a = input()
    sys.exit(0)
try:
    import keyboard
except:
    print("Fatal Error: Keyboard is not installed. Please refer to README.md for dependencies.")
    print("Press enter to close...")
    a = input()
    sys.exit(0)
try:
    import skimage.exposure
except:
    print("Fatal Error: Skimage is not installed. Please refer to README.md for dependencies.")
    print("Press enter to close...")
    a = input()
    sys.exit(0)
import os
import time
import glob
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
config = []
print("Starting...")
print("Version 2.1")
print("- Made by Lexzach -")
print("Loading config.txt...")

try:
    config = open("config.txt","r+")
    config = config.readlines()
    print("Config loaded successfully.")
except:
    print("\nError: Config.txt read unsuccessfully, perhapse the file is not in the same folder as the program?")
    print("Press enter to close...")
    a = input()
    sys.exit(0)
for x in config:
    config[config.index(x)] = x.replace("\n","")
pairs = 0
count2=0
edgeSmoothing = float(str(config[9]).replace("edgeSmoothing=", ""))

if config[2] == "autoScreenshot=true":
    print("")
    print("Now in automatic mode, switch to HLMV and use the following buttons:")
    print("S - Take a screenshot, the mouse will move on its own.")
    print("P - Finish and start rendering.")
    while not keyboard.is_pressed("p"):
        if keyboard.is_pressed("s"):
            pyautogui.click(59,31) #options
            pyautogui.click(67,49) #background
            pyautogui.click(205,211) #white
            pyautogui.click(46,352) #ok
            time.sleep(0.20)
            print("Taking screenshot w"+str(count2)+".png")
            im = pyautogui.screenshot(region=(int(config[5]),int(config[6]), int(config[7]), int(config[8])))
            im.save("./Rendering Folder/w"+str(count2)+".png")
            pyautogui.click(59,31) #options
            pyautogui.click(67,49) #background
            pyautogui.click(24,212) #black
            pyautogui.click(46,352) #ok
            time.sleep(0.20)
            print("Taking screenshot b"+str(count2)+".png")
            im = pyautogui.screenshot(region=(int(config[5]),int(config[6]), int(config[7]), int(config[8])))
            im.save("./Rendering Folder/b"+str(count2)+".png")
            count2+=1
            pairs+=1

else:
    print("")
    print("Enter number of pairs to make transparent... (ex. if you have 1 black images and 1 white image that would be 1 pair)")
    pairs=input()

    try:
        pairs = int(pairs)
    except:
        print("\nError: You entered something other than a number.")
        print("Press enter to close...")
        a = input()
        sys.exit(0)

count2 =0
while count2 != pairs:
    try:
        img1 = cv2.imread("./Rendering Folder/w" + str(count2) +".png")
        print("Reading white image #" + str(count2))
    except:
        print("\nError: File 'w" + str(count2) +".png' does not exist.")
        print("Press enter to close...")
        a = input()
        sys.exit(0)


    try:
        img2 = cv2.imread("./Rendering Folder/b" + str(count2) +".png")
        print("Reading black image #" + str(count2))
    except:
        print("\nError: File 'b" + str(count2) +".png' does not exist.")
        print("Press enter to close...")
        a = input()
        sys.exit(0)

    print("Finding differences...")
    try:
        img3 = cv2.subtract(img1,img2)
        print("Found differences")
    except:
        print("\nError: Differences in b"+str(count2)+".png and w" + str(count2) + ".png were not found.")
        print("Press enter to close...")
        a = input()
        sys.exit(0)
    try:
        print("Writing differences to data"+str(count2)+".png")
        cv2.imwrite('./Rendering Folder/data' + str(count2) +'.png',img3)
    except:
        print("\nError: Images are not being found, perhaps you entered a higher number of pairs then intended?")
        print("Press enter to close...")
        a = input()
        sys.exit(0)

    newData = []
    differ = Image.open('./Rendering Folder/data' + str(count2) +'.png')
    differ = differ.convert("RGBA")
    prevData = (255, 255, 255, 255)
    datas = differ.getdata()
    print("Making transparent data...")
    for item in datas:
        #if float(item[0]) >= pixelLenience and float(item[1]) >= pixelLenience and float(item[2]) >= pixelLenience:
        if float(item[0]) < 255 and float(item[1]) < 255 and float(item[2]) < 255:
            newData.append(item)
            prevData = item
        else:
            newData.append((255, 255, 255, 0))
            prevData = item

    

    differ.putdata(newData)
    #differ.save('./Rendering Folder/transparent' + str(count2) +'.png')
    newData = []

    #differ = Image.open('./Rendering Folder/transparent' + str(count2) +'.png')
    differ = differ.convert("RGBA")
    prevData = (255, 255, 255, 255)
    datas = differ.getdata()
    print("Cleaning up data...")
    for item in datas:
        #if float(item[0]) >= pixelLenience and float(item[1]) >= pixelLenience and float(item[2]) >= pixelLenience:
        if float(item[0]) > 10 and float(item[1]) > 10 and float(item[2]) > 10 and float(item[3]) != 0:
            newData.append((255, 255, 255, 0))
            prevData = item
        else:
            newData.append(item)
            prevData = item
    differ.putdata(newData)
    print("Opening and converting...")
    differ.save('./Rendering Folder/transparent' + str(count2) +'.png')

    layer1 = Image.open("./Rendering Folder/b" + str(count2) +".png")
    layer2 = Image.open("./Rendering Folder/transparent" + str(count2) +".png")
    layer1 = layer1.convert("RGBA")
    layer2 = layer2.convert("RGBA")

    layer1data = layer1.getdata()
    layer2data = layer2.getdata()
    newData = []
    count=-1
    print("Writing data onto transparent image...")
    for item in layer2data:
        if item[3] != 0:
            count+=1
            try:
                newData.append((layer1data[count]))
            except:
                print("...")
        else:
            count+=1
            newData.append(item)
    print("Data written successfully!")

    differ=Image.open("./Rendering Folder/transparent" + str(count2) +".png")
    differ.putdata(newData)
    print("./Rendering Folder/Saving finished"+ str(count2) +".png")
    differ.save("./Rendering Folder/finished" + str(count2) +".png")
    if edgeSmoothing > 0:
        print("Smoothing edges...")
        img = cv2.imread("./Rendering Folder/finished" + str(count2) +".png", cv2.IMREAD_UNCHANGED)
        bgr = img[:, :, 0:3]
        a = img[:, :, 3]
        ab = cv2.GaussianBlur(a, (0,0), sigmaX=edgeSmoothing, sigmaY=edgeSmoothing, borderType = cv2.BORDER_DEFAULT)
        aa = skimage.exposure.rescale_intensity(ab, in_range=(127.5,255), out_range=(0,255))
        out = img.copy()
        out[:, :, 3] = aa
        cv2.imwrite("./Rendering Folder/finished" + str(count2) +".png", out)

    if config[0] == "deleteTempFiles=true":
        print("Deleting temp files...")
        os.remove("./Rendering Folder/transparent" + str(count2) +".png")
        os.remove("./Rendering Folder/data" + str(count2) +".png")
    count2+=1

if config[1] == "autoCrop=true":
    def trim(im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)
            
    for filename in glob.glob('./Rendering Folder/*.png'):
        if str(filename[19]) == "f":
            im = Image.open(filename)
            print("Cropping "+filename)
            im = trim(im)
            im.save(filename[:-4] + "_cropped.png")

print("")
print(" ______   _______  _        _______    ")
print("(  __  \ (  ___  )( (    /|(  ____ \   ")
print("| (  \  )| (   ) ||  \  ( || (    \/   ")
print("| |   ) || |   | ||   \ | || (__       ")
print("| |   | || |   | || (\ \) ||  __)      ")
print("| |   ) || |   | || | \   || (         ")
print("| (__/  )| (___) || )  \  || (____/\ _ ")
print("(______/ (_______)|/    )_)(_______/(_)")
print("\nDo you like this project? Let me know on my talk page:")
print("wiki.teamfortress.com/wiki/User_talk:Lexzach")
a=input("\nPress enter to exit...")
