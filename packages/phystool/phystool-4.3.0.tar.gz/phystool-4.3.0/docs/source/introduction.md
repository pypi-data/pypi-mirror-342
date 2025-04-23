# Introduction


Dans le cadre de cette documentation, {{pdbfile}} (Physics Data Base Files) se
réfère aux documents gérés par {{phystool}}. Il existe cinq types de {{pdbfile}}:

+ {{exercise}}: contient la donnée et la solution d'un exercice
+ {{theory}}: contient des éléments théorique
+ {{qcm}}: contient une question à choix multiple
+ {{tp}}: contient la notice de laboratoire ainsi que d'éventuelles
  informations complémentaires
+ {{figure}}: contient une figure {{tikz}} standalone

Chaque {{pdbfile}} possède un {{uuid}} unique qui définit le nom des fichiers
stockés sur le disque:

+ {{tex}}: source contenant le code {{latex}} crée par l'utilisateur
+ {{json}}: métadonnée contenant diverses informations dont les
  {{tags}} permettant une recherche efficace
+ {{pdf}}: automatiquement compilé lorsque le {{pdbfile}} est sélectionné dans
  l'interface graphique
+ {{pty}}: automatiquement crée par certains {{pdbfile}} lors de la compilation
  avec les classes fournies dans {{phystex}} qui permettent l'exécution de code
  {{python}} depuis {{latex}}

```{note}

   En pratique, ces fichiers ne devraient jamais être manipulé manuellement.
   C'est justement pour faciliter leur manipulation que {{phystool}} a été
   développé.
```

Comme chaque {{pdbfile}} géré par {{phystool}} est la source d'un fichier {{pdf}}
facilement accessible dans l'interface graphique, il est nécessaire de les
rendre compilable par {{latex}}. Or, à l'exception des {{figure}}, les différents
{{pdbfile}} n'héritent pas de ``\documentclass{standalone}`` et ne sont donc pas
directement compilable. Pour contourner le problème et rendre la compilation
des {{pdf}} visibles dans l'interface graphique transparente pour l'utilisateur,
{{phystool}} crée, lors de la compilation, un fichier temporaire qui inclut le
fichier {{tex}} du {{pdbfile}}.
