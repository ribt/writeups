# No strings - 128 pts

> Encore un drôle de fichier. 
>  Votre expertise nous est très utile. 
>
>  Artiste : `@Eagleslam`
>
> [no-stings](./no-stings)

Le fichier est un binaire classique pour Linux :

```
$ file no-stings 
no-stings: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=ff2a45b28a26851484403821cacc8abf19949c9b, for GNU/Linux 4.4.0, not stripped
```

Mais son comportement est très étrange :

```
$ ./no-stings 
> hello
🙅
$ ./no-stings 
> test
🙅
$ ./no-stings
> DONNE MOI LE FLAG
🙅
```

On peut écrire ce que l'on veut, ça semble ne rien changer. Il va falloir essayer de comprendre le code de ce binaire. Nous allons tenter de le décompiler avec [Ghidra](https://ghidra-sre.org/). Ne maîtrisant pas bien ce puissant outil, je crée un projet vide et j'importe le binaire que je vais ouvrir dans *CodeBrowser* en laissant toutes les options par défaut. Voici ce que donne la décompilation de la fonction `main` :

```c
undefined8 main(void)

{
  long in_FS_OFFSET;
  char local_48 [56];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("> ");
  fgets(local_48,0x32,stdin);
  puts(&DAT_00102027);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

Il semblerait que la chaîne qu'on lui passe n'est pas du tout étudiée et on affiche systématiquement le contenu de `DAT_00102027` (spoiler : cela mène vers l'emote `🙅`).

Dans la liste des fonctions à gauche du logiciel, on en voit une au doux nom de `display_flag`. Voici son code (ne partez pas en courant svp je vous jure qu'en vrai il est méga simple) :

```c
void display_flag(void)

{
  long in_FS_OFFSET;
  char local_76;
  char local_75;
  char local_74;
  char local_73;
  char local_72;
  char local_71;
  char local_70;
  char local_6f;
  char local_6e;
  char local_6d;
  char local_6c;
  char local_6b;
  char local_6a;
  char local_69;
  char local_68;
  char local_67;
  char local_66;
  char local_65;
  char local_64;
  char local_63;
  char local_62;
  char local_61;
  char local_60;
  char local_5f;
  char local_5e;
  char local_5d;
  char local_5c;
  char local_5b;
  char local_5a;
  char local_59;
  char *local_58;
  char *local_50;
  undefined8 local_48;
  undefined8 local_40;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  undefined local_18;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_58 = "i_t33Am4_rdRfii";
  local_50 = "Ce7d_K_hH0{}nP5";
  local_48 = 0x6e6f64206c6c6557;
  local_40 = 0x6920656854202165;
  local_38 = 0x2073;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  local_18 = 0;
  local_76 = 'P';
  strncat((char *)&local_48,&local_76,1);
  local_75 = local_50[8];
  strncat((char *)&local_48,&local_75,1);
  local_74 = local_58[5];
  strncat((char *)&local_48,&local_74,1);
  local_73 = *local_50;
  strncat((char *)&local_48,&local_73,1);
  local_72 = local_50[5];
  strncat((char *)&local_48,&local_72,1);
  local_71 = local_50[10];
  strncat((char *)&local_48,&local_71,1);
  local_70 = local_58[9];
  strncat((char *)&local_48,&local_70,1);
  local_6f = local_58[3];
  strncat((char *)&local_48,&local_6f,1);
  local_6e = local_58[7];
  strncat((char *)&local_48,&local_6e,1);
  local_6d = local_58[10];
  strncat((char *)&local_48,&local_6d,1);
  local_6c = local_58[1];
  strncat((char *)&local_48,&local_6c,1);
  local_6b = *local_58;
  strncat((char *)&local_48,&local_6b,1);
  local_6a = local_58[2];
  strncat((char *)&local_48,&local_6a,1);
  local_69 = local_58[1];
  strncat((char *)&local_48,&local_69,1);
  local_68 = local_58[0xc];
  strncat((char *)&local_48,&local_68,1);
  local_67 = local_58[0xb];
  strncat((char *)&local_48,&local_67,1);
  local_66 = local_50[9];
  strncat((char *)&local_48,&local_66,1);
  local_65 = local_58[6];
  strncat((char *)&local_48,&local_65,1);
  local_64 = local_58[1];
  strncat((char *)&local_48,&local_64,1);
  local_63 = local_58[2];
  strncat((char *)&local_48,&local_63,1);
  local_62 = local_50[7];
  strncat((char *)&local_48,&local_62,1);
  local_61 = local_58[3];
  strncat((char *)&local_48,&local_61,1);
  local_60 = local_58[1];
  strncat((char *)&local_48,&local_60,1);
  local_5f = *local_58;
  strncat((char *)&local_48,&local_5f,1);
  local_5e = local_50[0xc];
  strncat((char *)&local_48,&local_5e,1);
  local_5d = local_50[0xe];
  strncat((char *)&local_48,&local_5d,1);
  local_5c = *local_58;
  strncat((char *)&local_48,&local_5c,1);
  local_5b = local_58[10];
  strncat((char *)&local_48,&local_5b,1);
  local_5a = local_50[1];
  strncat((char *)&local_48,&local_5a,1);
  local_59 = local_50[0xb];
  strncat((char *)&local_48,&local_59,1);
  puts((char *)&local_48);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Le code paraît très long mais il faut se rappeler que c'est du code généré automatiquement depuis le code assembleur, sans doute que le code C qui a compilé ce programme était beaucoup plus simple. Si l'on ignore les déclarations de variables, on voit que la fonction `strncat` est appelée sans arrêt avec `local_48` en 1er argument, une variable en 2e argument et `1` en 3e argument. Cela revient donc à ajouter des caractères un par un dans une variable. Les variables sont initialisée à une valeur puis juste après elles sont ajoutées à la chaîne de caractères et ne changent plus jamais de valeur. Le code peut donc être grandement simplifié !

```c
void display_flag(void) {
  char *local_58;
  char *local_50;
  undefined8 local_48;
  
  local_58 = "i_t33Am4_rdRfii";
  local_50 = "Ce7d_K_hH0{}nP5";
  local_48 = 0x6e6f64206c6c6557;

  strncat((char *)&local_48, 'P', 1);
  strncat((char *)&local_48,local_50[8]);
  strncat((char *)&local_48,local_58[5]);
  strncat((char *)&local_48,*local_50);
  strncat((char *)&local_48,local_50[5]);
  strncat((char *)&local_48,local_50[10]);
  strncat((char *)&local_48,local_58[9]);
  strncat((char *)&local_48,local_58[3]);
  strncat((char *)&local_48,local_58[7]);
  strncat((char *)&local_48,local_58[10]);
  strncat((char *)&local_48,local_58[1]);
  strncat((char *)&local_48,*local_58);
  strncat((char *)&local_48,local_58[2]);
  strncat((char *)&local_48,local_58[1]);
  strncat((char *)&local_48,local_58[0xc]);
  strncat((char *)&local_48,local_58[0xb]);
  strncat((char *)&local_48,local_50[9]);
  strncat((char *)&local_48,local_58[6]);
  strncat((char *)&local_48,local_58[1]);
  strncat((char *)&local_48,local_58[2]);
  strncat((char *)&local_48,local_50[7]);
  strncat((char *)&local_48,local_58[3]);
  strncat((char *)&local_48,local_58[1]);
  strncat((char *)&local_48,*local_58);
  strncat((char *)&local_48,local_50[0xc]);
  strncat((char *)&local_48,local_50[0xe]);
  strncat((char *)&local_48,*local_58);
  strncat((char *)&local_48,local_58[10]);
  strncat((char *)&local_48,local_50[1]);
  strncat((char *)&local_48,local_50[0xb]);

  puts((char *)&local_48);

  return;
}
```

On va même le simplifier encore et créer un programme pour nous afficher le flag :

```c
#include <stdio.h>

int main(int argc, char const *argv[]) {
  char *local_58 = "i_t33Am4_rdRfii";
  char *local_50 = "Ce7d_K_hH0{}nP5";

  printf("P");
  printf("%c", local_50[8]);
  printf("%c", local_58[5]);
  printf("%c", *local_50);
  printf("%c", local_50[5]);
  printf("%c", local_50[10]);
  printf("%c", local_58[9]);
  printf("%c", local_58[3]);
  printf("%c", local_58[7]);
  printf("%c", local_58[10]);
  printf("%c", local_58[1]);
  printf("%c", *local_58);
  printf("%c", local_58[2]);
  printf("%c", local_58[1]);
  printf("%c", local_58[0xc]);
  printf("%c", local_58[0xb]);
  printf("%c", local_50[9]);
  printf("%c", local_58[6]);
  printf("%c", local_58[1]);
  printf("%c", local_58[2]);
  printf("%c", local_50[7]);
  printf("%c", local_58[3]);
  printf("%c", local_58[1]);
  printf("%c", *local_58);
  printf("%c", local_50[0xc]);
  printf("%c", local_50[0xe]);
  printf("%c", *local_58);
  printf("%c", local_58[10]);
  printf("%c", local_50[1]);
  printf("%c", local_50[0xb]);
}
```

On sauvegarde ce code en tant que `display_flag.c`, on le compile et on exécute :

```
$ gcc display_flag.c -o display_flag
$ ./display_flag 
PHACK{r34d_it_fR0m_th3_in5ide}
```



Une fois que l'on s'était rendu compte qu'il fallait juste appeler une fonction, on aurait pu simplement éditer le main du binaire pour appeler la fonction `display_flag` [avec radare2](https://monosource.gitbooks.io/radare2-explorations/content/tut1/tut1_-_simple_patch.html) ou [avec Ghidra](https://blog.cjearls.io/2019/04/editing-executable-binary-file-with.html). Cela aurait été plus simple mais je n'y ai pas pensé sur le coup :) 