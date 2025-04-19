# Configuration

Comme présenté [précédemment](quickstart.md#premier-demarrage), le fichier de
configuration `~/.phystool/phystool.conf` contient quatre sections qui seront
présentées une à une ci-dessous.

```{literalinclude} ../../src/phystool/static/phystool.conf
    :linenos:
```

## Phystool

Le paramètre `db` fixe le chemin du répertoire contenant les {{pdbfile}}. Ce
répertoire peut être placé n'importe où sur le disque et son contenu ne devrait
en principe pas être modifié sans passer par les outils {{phystool}}.

## Physnoob

Le paramètre `editor` fixe la commande utilisée par {{physnoob} pour ouvrir les
fichier {{tex}} associés aux {{pdbfile}}.

```{note}
Jusqu'à présent seul `vim` et `kile` on été testé mais n'importe quel éditeur
de text graphique devrait fonctionner sans problème.
```

## LaTeX

Le paramètre `auto` correspond à la classe {{latex}} utilisée par {{phystool}}
pour compiler automatiquement les différents types de {{pdbfile}} à l'exception
de {{figure}} qui utilise lui la classe définie par le paramètre `tikz`.

```{attention}
Le contenu de ces classes {{latex}} est central au bon fonctionnement de
{{phystool}}, il est vivement conseiller de prendre le temps de lire la
[documentation](latex.md#latex) qui s'y rapporte.
```

## Git

Le paramètre `theme` n'a d'effet que sur la coloration syntaxique utilisée par
`delta` au travers de `git diff`. Les différents style sont configurable dans
le menu dédié de {{physnoob}}.
