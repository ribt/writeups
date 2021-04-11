# A-Maze-Ing - 256 pts

>Un étrange serveur souhaite vous mettre à l'épreuve. 
> Soyez à la hauteur.
> 
> === Connexion ===
> **Serveur** : `a-maze-ing.phack.fr`
> **Port** : `4242` 
>
> Artiste : `@Pdrooo`

On essaie de se connecter à l'adresse donnée avec netcat... et on nous renvoie du HTML. ALors on y va avec le navigateur :

> ```
> routes
> 
> | Route  | Method |
> |--------|--------|
> | /      | GET    |
> | /chall | GET    |
> | /chall | POST   |
> | /flag  | GET    |
> 
> rules
> 
> Hello x,
> 
> Your goal today is to rob the bank.
> But the police is fast, you have 5 sec to reach the vault and grab the cash.
> 
> Good luck !
> ```

Le `/flag` ne donne bien évidemment pas le flag mais voici ce que renvoie `/chall` :

```json
{"token": "79cdcf1fd2e842d6a639c6866f9e7eab", "solveMe": "######################x# #         #     ## # # # # ##### # # ## # # # # #     # # ## # # # ### ##### # ## #   #   # #   # # ## ####### # ### # #### #       # #   #   ## # ####### # # ### ## #   #   # # # #   ## # # # # # # # # #### # #   # #   # #   ## ####### # ##### # ##       # # #   # # ######## # # # # ### ## #     #   # #     ## # ######### ##### ## # #       #     # ## # ### ### ##### # ##       #         #$######################"}
```

Bon, vu le nom du challenge on a clairement un labyrinthe à résoudre. La chaîne de caractère `solveMe` fait 441 caractères. Après avoir essayer de l'afficher dans tous les sens, on se rend compte que 441 c'est 21x21 et en effet, vu comme ça, ça ressemble à quelque chose :

```
#####################
#x# #         #     #
# # # # # ##### # # #
# # # # # #     # # #
# # # # ### ##### # #
# #   #   # #   # # #
# ####### # ### # ###
# #       # #   #   #
# # ####### # # ### #
# #   #   # # # #   #
# # # # # # # # # ###
# # #   # #   # #   #
# ####### # ##### # #
#       # # #   # # #
####### # # # # ### #
# #     #   # #     #
# # ######### ##### #
# # #       #     # #
# # ### ### ##### # #
#       #         #$#
#####################
```

On essaie de faire une requête POST et on voit que le serveur veut du JSON avec notre token et le chemin sous forme de chaîne avec les flèches `↑↓←→`.

Voici mon code :

```python
import requests

chall = requests.get("http://a-maze-ing.phack.fr:4242/chall").json()
directions = "↑↓←→"

for i in range(21):
    print(chall["solveMe"][i*21:i*21+21])

def nextPos(pos, dir):
    x, y = pos
    if dir=="↑": y -= 1
    if dir=="↓": y += 1
    if dir=="←": x -= 1
    if dir=="→": x += 1
    return(x,y)

def getMapBloc(pos):
    x, y = pos
    return chall["solveMe"][y*21+x]
    
def isMovePossible(pos, dir):
    x, y = nextPos(pos, dir)
    if not 0 <= x < 21 and 0 <= y < 21:
        return None
    if getMapBloc((x,y)) == "#":
        return None
    return (x,y)

def opposedDirection(dir):
    if dir=="↑": return "↓"
    if dir=="↓": return "↑"
    if dir=="←": return "→"
    if dir=="→": return "←"

toTry = []
startingPoisition = (1,1)
solve = None

for dir in directions:
    if isMovePossible(startingPoisition, dir):
        toTry.append([nextPos(startingPoisition, dir), dir])

while not solve and len(toTry) > 0:
    pos, path = toTry.pop(0)
    for dir in directions:
        if dir == opposedDirection(path[-1]):
            continue
        next = isMovePossible(pos, dir)
        if next:
            if getMapBloc(next) == "$":
                solve = path+dir
            toTry.append([next, path+dir])

print(solve)

print(requests.post("http://a-maze-ing.phack.fr:4242/chall", json={"token":chall["token"], "solution":solve}).content)
```

```
Congrats ! The flag is PHACK{M4zEs_4Re_7rUly_4m@zIng}
```

