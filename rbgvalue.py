from PIL import Image
import requests
from datetime import datetime, timedelta


def getURL():
    fmiTime = datetime.now() - timedelta(hours = 2) # Different timezone
    stringDate = str(fmiTime)
    print(stringDate)
    stringDate = stringDate.split(".")[0][:-3].replace("-", "").replace(" ", "").replace(":", "")
    print(stringDate)
    minutes = int(stringDate[-2:])

    if minutes < 19 and minutes >= 4: # New forecast/picture comes 4 minutes late
        stringDate = stringDate[:-2] + "00"
    elif minutes < 34 and minutes >= 19:
        stringDate = stringDate[:-2] + "15"
    elif minutes < 49 and minutes >= 34:
        stringDate = stringDate[:-2] + "30"
    elif minutes >= 49: 
        stringDate = stringDate[:-2] + "45"
    elif minutes <= 3:
        stringDate = stringDate[:-2] + "45"
        stringDate = stringDate[:9] + str(int(stringDate[9])-1) + stringDate[10:]


    URL = "https://cdn.fmi.fi/weather-radar/observations/flash/keski-suomi_500x500/HAV_" + stringDate + "_DBZ.png"
    print(URL)

    print(stringDate)
    return URL


def rgbOfPixel(picuture, x, y):
    pic = Image.open(picuture).convert('RGB')
    r, g, b = pic.getpixel((x, y))
    rgb = (r, g, b)
    return rgb


def getPicture(URL):
    pic = requests.get(URL)
    file = open("sample_image.png", "wb")
    file.write(pic.content)
    file.close()


def analyzeResults(results):
    rainArea = []
    colorsAlppila = {"light rain": (74, 143, 186), "light to moderate rain": (71, 175, 152), "moderate": (156, 190, 57), "no rain": (185, 124, 122)}
    
    for i in results:
        for k, v in colorsAlppila.items():
            if i == v:
                rainArea.append(k)

    mostFreq = (max(set(rainArea), key = rainArea.count))
    rainArea = [i for i in rainArea if i != mostFreq]
    try:
        secondMostFreq = (max(set(rainArea), key = rainArea.count))
    except:
        secondMostFreq = "nothing else"
    if secondMostFreq == "nothing else":
        return mostFreq + " with 100 % certainty"            
    return f"{mostFreq} or {secondMostFreq}"


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
results = analyzeResults(results)
print(results)

colorsBar = [(0, 118, 200), (6, 193, 162), (107, 176, 15), (182, 182, 12), (196, 154, 0), (182, 18, 0), (182, 23, 12)] # Heikosta rankkaan
