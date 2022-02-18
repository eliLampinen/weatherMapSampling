import string
from PIL import Image
import requests
from datetime import datetime, timedelta


def getURL():
    lastHourDateTime = datetime.now() - timedelta(hours = 2)
    stringDate = str(lastHourDateTime)
    print(stringDate)
    stringDate = stringDate.split(".")[0][:-3].replace("-", "").replace(" ", "").replace(":", "")
    print(stringDate)
    print(stringDate[-2:])

    if int(stringDate[-2:]) < 19 and int(stringDate[-2:]) > 4: # New forecast/picture comes 4 minutes late
        stringDate = stringDate[:-2] + "00"
    elif int(stringDate[-2:]) < 34 and int(stringDate[-2:]) >= 19:
        stringDate = stringDate[:-2] + "15"
    elif int(stringDate[-2:]) < 49 and int(stringDate[-2:]) >= 34:
        stringDate = stringDate[:-2] + "30"
    elif int(stringDate[-2:]) >= 49:
        stringDate = stringDate[:-2] + "45"

    URL = "https://cdn.fmi.fi/weather-radar/observations/flash/keski-suomi_500x500/HAV_" + stringDate + "_DBZ.png"
    print(URL)

    print(stringDate)
    return URL


def rgbOfPixel(picuture, x, y):
    pic = Image.open(picuture).convert('RGB')
    r, g, b = pic.getpixel((x, y))
    a = (r, g, b)
    return a


def getPicture(URL):
    pic = requests.get(URL)
    file = open("sample_image.png", "wb")
    file.write(pic.content)
    file.close()


def analyzeResults(results):
    rainArea = []
    colorsAlppila = {"heikkoa sadetta": (74, 143, 186), "kohtalaista sadetta": (71, 175, 152), "ei sadetta": (185, 124, 122)}
    
    for i in results:
        for k, v in colorsAlppila.items():
            if i == v:
                rainArea.append(k)

    mostFreq = (max(set(rainArea), key = rainArea.count))
    return mostFreq


def getRGB():
    alppilaCoords = [(225, 150), (225, 151), (225, 152), (226, 150), (226, 151), (226, 152), (227, 150), (227, 151), (227, 152)]
    results = []
    for i in alppilaCoords:
        rgb = rgbOfPixel("sample_image.png", i[0], i[1])
        print(rgb)
        results.append(rgb)
    return results

getPicture(getURL())
results = getRGB()
print(analyzeResults(results))


colorsBar = [(0, 118, 200), (6, 193, 162), (107, 176, 15), (182, 182, 12), (196, 154, 0), (182, 18, 0), (182, 23, 12)] # Heikosta rankkaan
