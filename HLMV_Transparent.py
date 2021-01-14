try:
    import cv2
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
    import glob
except:
    print("Fatal Error: Glob is not installed. Please refer to README.md for dependencies.")
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
import os
import time
import sys
from PIL import Image, ImageDraw, ImageFont, ImageChops
config = []
print("Starting...")
print("- Made by Lexzach -")
print("Loading config.txt...")

try:
    config = open("config.txt","r+")
    config = config.readlines()
    print("Config loaded successfully")
except:
    print("")
    print("Error: Config.txt read unsuccessfully.")
    print("Press enter to close...")
    a = input()
    sys.exit(0)
config[5] = config[5].replace("\\","")
config[5] = config[5].replace("n","")

config[6] = config[6].replace("\\","")
config[6] = config[6].replace("n","")

config[7] = config[7].replace("\\","")
config[7] = config[7].replace("n","")

config[8] = config[8].replace("\\","")
config[8] = config[8].replace("n","")
pairs = 0
count2=0
if config[2] == "autoScreenshot=true\n":
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
            im.save("w"+str(count2)+".png")
            pyautogui.click(59,31) #options
            pyautogui.click(67,49) #background
            pyautogui.click(24,212) #black
            pyautogui.click(46,352) #ok
            time.sleep(0.20)
            print("Taking screenshot b"+str(count2)+".png")
            im = pyautogui.screenshot(region=(int(config[5]),int(config[6]), int(config[7]), int(config[8])))
            im.save("b"+str(count2)+".png")
            count2+=1
            pairs+=1

else:
    print("")
    print("Enter number of pairs to make transparent... (ex. if you have 1 black images and 1 white image that would be 1 pair)")
    pairs=input()

    try:
        pairs = int(pairs)
    except:
        print("")
        print("Error: You entered something other than a number.")
        print("Press enter to close...")
        a = input()
        sys.exit(0)

count2 =0
while count2 != pairs:
    try:
        img1 = cv2.imread("w" + str(count2) +".png")
        print("Reading white image #" + str(count2))
    except:
        print("")
        print("Error: File 'w" + str(count2) +".png' does not exist.")
        print("Press enter to close...")
        a = input()
        sys.exit(0)


    try:
        img2 = cv2.imread("b" + str(count2) +".png")
        print("Reading black image #" + str(count2))
    except:
        print("")
        print("Error: File 'b" + str(count2) +".png' does not exist.")
        print("Press enter to close...")
        a = input()
        sys.exit(0)

    print("Finding differences...")
    try:
        img3 = cv2.subtract(img1,img2)
        print("Found differences")
    except:
        print("")
        print("Error: Differences in b"+str(count2)+".png and w" + str(count2) + ".png were not found.")
        print("Press enter to close...")
        a = input()
        sys.exit(0)
    try:
        print("Writing differences to data"+str(count2)+".png")
        cv2.imwrite('data' + str(count2) +'.png',img3)
    except:
        print("")
        print("Error: Images are not being found, perhaps you entered a higher number of pairs then intended?")
        print("Press enter to close...")
        a = input()
        sys.exit(0)

    newData = []
    differ = Image.open('data' + str(count2) +'.png')
    differ = differ.convert("RGBA")

    datas = differ.getdata()
    print("Appending similarities to list...")
    for item in datas:
        if item[0] != 0 and item[1] != 0 and item[2] != 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)



    differ.putdata(newData)
    print("Opening and converting...")
    differ.save('transparent' + str(count2) +'.png')
    layer1 = Image.open("b" + str(count2) +".png")
    layer2 = Image.open("transparent" + str(count2) +".png")
    layer1 = layer1.convert("RGBA")
    layer2 = layer2.convert("RGBA")

    layer1data = layer1.getdata()
    layer2data = layer2.getdata()
    newData = []
    count=0
    print("Writing data onto transparent image...")
    for item in layer2data:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            count+=1
            try:
                newData.append((layer1data[count]))
            except:
                print("...")
        else:
            count+=1
            newData.append(item)
    print("Data written successfully!")

    differ=Image.open("transparent" + str(count2) +".png")
    differ.putdata(newData)
    print("Saving finished"+ str(count2) +".png")
    differ.save("finished" + str(count2) +".png")

    if config[0] == "deleteTempFiles=true\n":
        print("Deleting temp files...")
        os.remove("transparent" + str(count2) +".png")
        os.remove("data" + str(count2) +".png")
    count2+=1

if config[1] == "autoCrop=true\n":
    def trim(im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)
            
    for filename in glob.glob('*.png'):
        if str(filename[0]) == "f":
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
print("")
print("Do you like this project? Let me know on my talk page:")
print("wiki.teamfortress.com/wiki/User_talk:Lexzach")
print("")
print("Press enter to exit...")
a=input()