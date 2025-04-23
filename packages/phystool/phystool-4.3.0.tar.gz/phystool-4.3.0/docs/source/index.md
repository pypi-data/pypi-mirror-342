# Phystool

Ce projet propose deux outils pour gérer une base de donnée de documents
{{latex}}. La motivation initiale vient de la difficulté de gérer de gros
documents {{latex}} en exploitant le fait qu'il est simple de séparer un tel
document en plusieurs fichiers. Cette séparation offre de nombreux avantages au
détriment d'une prolifération de fichiers individuels. L'objectif initial de ce
projet est de remédier à ce problème dans le contexte de la gestion de document
destinés à l'enseignement en physique (exercices, figures, notices de
laboratoire, notions théorique, questions à choix multiple).

{{phystool}} simplifie la gestion d'une base de donnée de fichiers {{latex}} et
permet notamment de:

* tagger les documents afin de les retrouver rapidement
* gérer l'historique des modifications de fichiers au travers de git
* compiler les documents {{latex}} en évitant la multiplication des fichiers
  auxiliaires de compilation
* parser les logs liés à la compilation {{latex}} afin de les rendre plus lisibles
* automatiquement déclencher une seconde compilation {{latex}} en cas de besoin
  (par exemple si certaines références ont changé)

Les deux outils offerts dans ce projet sont:

+ {{phystool}}: une interface en ligne de commande qui permet d'accéder à
  toutes les fonctionnalités.
+ {{physnoob}}: une interface graphique Qt réalisée avec
  [PySide6](https://doc.qt.io/qtforpython-6/index.html) qui simplifie la
  recherche et la manipulation de fichier.


```{toctree}
    :caption: Table des matière
    :hidden:
    :maxdepth: 2

self
introduction
quickstart
configuration
latex
usage
api
changelog
```
