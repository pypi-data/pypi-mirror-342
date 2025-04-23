# Quickstart

## Installation

Pour installer {{phystool}} dans un environnement virtuel, il suffit de passer
par `pip`:

    pip install phystool


```{important}

Afin de permettre à {{phystool}} de parser correctement les logs {{latex}}, il
faut légèrement modifier la configuration du compilateur afin que les logs
affichent des lignes plus longues. Pour cela, il suffit de modifier/rajouter la
ligne suivante au fichier `texmf.cnf`:

    max_print_line=1000
```

### Dépendances

+ Python 3.12
+ git
+ [ripgrep](https://github.com/BurntSushi/ripgrep): Utilisé pour chercher des
  chaines de caractères dans les fichiers {{tex}}.
+ [bat](https://github.com/sharkdp/bat): Utilisé pour afficher le contenu des
  fichier {{tex}} dans le terminal et pour afficher les modifications suivies par
  {{git}}.
+ [delta](https://github.com/dandavison/delta): Utilisé pour afficher les
  modifications suivies par {{git}}.


## Premier démarrage

Lors de la première utilisation, il est conseillé d'exécuter {{physnoob}} car
l'interface graphique donne directement accès aux {{pdf}}. Au démarrage, le
fichier de configuration `~/.phystool/phystool.conf` est chargé. Si celui-ci
n'existe pas, il est automatiquement crée et son contenu est par défaut:

```{literalinclude} ../../src/phystool/static/phystool.conf
```

Une explication détaillée de ce fichier de configuration sera abordée [plus
loin](#configuration) mais il est pour l'instant suffisant de comprendre que
durant ce premier démarrage, le répertoire `~/physdb` a été crée et qu'il
contient quelques {{pdbfile}} qui féliciteront la prise en main de
{{phystool}}.
