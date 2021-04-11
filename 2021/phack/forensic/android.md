# Android Cloud - 128 pts

> Un service américain propose de se  débarasser définitivement de son smartphone grâce à sa nouvelle  plateforme de AaaS (Android as a Service).
>  
>  Mais méfiant de nature, vous décidez d'aller vérifier par vous même que la sécurité correspond à vos standards. 
>  
>  Lien du challenge : `http://android-cloud.phack.fr` 
>
>  Artiste : `@Pdrooo`

La page web contient un joli smartphone Android où l'on doit dessiner un schéma de déverrouillage. Le chemin dessiné est envoyé à un script PHP qui nous répond si notre schéma est accepté ou non.

En bas de la page on distingue ceci : `Last backup on Sat Mar 10 2020, 17:16:18 (UTC+1)`. Le mot `backup` dirige vers la page `backup.php` qui contient le code suivant :

```php
 <?php

# For debug, must remove later !!!
highlight_file ( __FILE__, false ); die();

$filename = "backup@" . date("m-d-Y") . ".zip";
$archive  = new ZipArchive();

if (!$archive->open("./dev-backups/" . $filename, (ZipArchive::CREATE | ZipArchive::OVERWRITE))) {
    die("Archive init failed");
}

$source = realpath("/mnt/mtp/device/029746912983");

$files = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($source), RecursiveIteratorIterator::SELF_FIRST);

foreach ($files as $file) {

    if (in_array(substr($file, strrpos($file, '/') + 1), array('.', '..'))) {
        continue;
    }               

    $file = realpath($file);

    if (is_dir($file)) {
        $archive->addEmptyDir(str_replace($source . '/', '', $file . '/'));
    } elseif (is_file($file)) {
        $archive->addFromString(str_replace($source . '/', '', $file), file_get_contents($file));
    } else {
        die("Dealing with unknown file type.");
    }
}

$archive->close();

?>
```

Ce site fait des backups d'un téléphone sous forme de zip. Si l'on essaye de trouver celui de la date correspondante (http://android-cloud.phack.fr/dev-backups/backup@03-10-2020.zip) on récupère en effet une archive de 114 Mo. Une rapide recherche sur Internet nous apprend que le pattern de déverrouillage est stocké dans `/data/system/gesture.key` et qu'il est très facile à cracker car c'est un SHA-1 d'une assez petite suite de chiffres. On trouve [un outil](https://github.com/sch3m4/androidpatternlock/) qui va faire le travail :

```
$ python2 aplc.py android/data/system/gesture.key 

################################
# Android Pattern Lock Cracker #
#             v0.2             #
# ---------------------------- #
#  Written by Chema Garcia     #
#     http://safetybits.net    #
#     chema@safetybits.net     #
#          @sch3m4             #
################################

[i] Taken from: http://forensics.spreitzenbarth.de/2012/02/28/cracking-the-pattern-lock-on-android/

[:D] The pattern has been FOUND!!! => 04137658

[+] Gesture:

  -----  -----  -----
  | 1 |  | 3 |  |   |  
  -----  -----  -----
  -----  -----  -----
  | 4 |  | 2 |  | 7 |  
  -----  -----  -----
  -----  -----  -----
  | 6 |  | 5 |  | 8 |  
  -----  -----  -----

It took: 0.5186 seconds
```

On dessine le pattern sur le site et c'est gagné.

```
Congrats !
The flag is : PHACK{T4ke_c4rE_oF_Ur_B4cKupS!}
```

