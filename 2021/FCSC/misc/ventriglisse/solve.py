from PIL import Image, ImageDraw
from pprint import pprint

def solve(img):
    data = parse(img.load())
    chemin = trouverChemin(data)
    if chemin[-1] != "N":
        chemin += "N"
    return chemin

def parse(img):
    data = {}
    xDebut, yDebut = 64, 128
    haut, larg = 0, 0
    while img[xDebut+larg*64, yDebut] == (0, 0, 255):
        larg += 1
    xFin = xDebut+larg*64 - 1
    while img[xFin, yDebut+haut*64] == (0, 0, 255):
        haut += 1
    yFin = yDebut+haut*64 - 1

    data["dimension"] = (larg, haut)

    for x in range(larg):
        if img[xDebut+32+x*64, yDebut-10][2] < 10:
            data["sortie"] = (x, 0)

    for x in range(larg):
        if img[xDebut+32+x*64, yFin+30][2] < 10:
            data["entrée"] = (x, haut-1)

    data["walls"] = []

    for y in range(haut):
        for x in range(larg):
            if x > 0 and img[xDebut+x*64, yDebut+32+y*64] == (0, 0, 255):
                data["walls"].append(((x-1, y), (x,y)))
            if y > 0 and img[xDebut+32+x*64, yDebut+y*64] == (0, 0, 255):
                data["walls"].append(((x, y-1), (x,y)))

    return data

def positionFinale(data, pos, direction):
    x, y = pos
    while mouvementPossible(data, (x, y), direction):
        x, y = avancer((x, y), direction)
    return (x,y)
    
def avancer(pos, dir):
    x, y = pos
    if dir == "N": y -= 1
    if dir == "S": y += 1
    if dir == "O": x -= 1
    if dir == "E": x += 1
    return (x,y)

def mouvementPossible(data, pos, direction):
    nextPos = avancer(pos, direction)
    if nextPos[0] < 0 or nextPos[1] < 0:
        return False
    if nextPos[0] >= data["dimension"][0] or nextPos[1] >= data["dimension"][1]:
        return False
    if (pos, nextPos) in data["walls"] or (nextPos, pos) in data["walls"]:
        return False
    return True
    
def trouverChemin(data):
    pos = data["entrée"]
    nextPos = positionFinale(data, pos, "N")

    posEssayes = [pos]
    aEssayer = {'pos': [nextPos], 'path': ["N"]}

    while len(aEssayer) > 0:
        pos, path = aEssayer['pos'].pop(0), aEssayer['path'].pop(0)
        for direction in "NSEO":
            if mouvementPossible(data, pos, direction):
                nextPos = positionFinale(data, pos, direction)
                if nextPos == data["sortie"]:
                    return path+direction
                if nextPos not in posEssayes and nextPos not in aEssayer['pos']:
                    aEssayer['pos'].append(nextPos)
                    aEssayer['path'].append(path+direction)
            posEssayes.append(pos)
    

if __name__ == "__main__" :
    img = Image.open("maze.png")
    pixelMap = img.load()
    data = parse(pixelMap)
    print(solve(img))
