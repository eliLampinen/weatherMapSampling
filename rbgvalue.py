from difflib import restore
from PIL import Image
import requests

def rgb_of_pixel(picuture, x, y):
    im = Image.open(picuture).convert('RGB')
    r, g, b = im.getpixel((x, y))
    a = (r, g, b)
    return a


def getPicture():
    pic = requests.get("https://cdn.fmi.fi/weather-radar/observations/flash/keski-suomi_500x500/HAV_202202180730_DBZ.png")
    file = open("sample_image.png", "wb")
    file.write(pic.content)
    file.close()
    return "sample_image.png"


def analyzeResults(results):
    sadealue = []
    varitPallossa = {"heikkoa sadetta": (74, 143, 186), "kohtalaista sadetta": (71, 175, 152), "ei sadetta": (185, 124, 122)}
    
    for i in results:
        for k, v in varitPallossa.items():
            if i == v:
                sadealue.append(k)

    mostFreq = (max(set(sadealue), key = sadealue.count))
    return mostFreq


def getRGB():
    AlppilaCoords = [(225, 150), (225, 151), (225, 152), (226, 150), (226, 151), (226, 152), (227, 150), (227, 151), (227, 152)]
    results = []
    for i in AlppilaCoords:
        rgb = rgb_of_pixel(getPicture(), i[0], i[1])
        #print(rgb)
        results.append(rgb)
    return results
results = getRGB()
print(analyzeResults(results))


varitPalkissa = [(0, 118, 200), (6, 193, 162), (107, 176, 15), (182, 182, 12), (196, 154, 0), (182, 18, 0), (182, 23, 12)] # Heikosta rankkaan
