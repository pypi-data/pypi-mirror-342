# PDBFile

Effectue une action sur un {{pdbfile}}.

```{table} Exemples d'utilisation
    :width: 100%

| Action                                                                        | Commande                                                                                       |
| ---                                                                           | ---                                                                                            |
| Ne fait rien                                                                  | {code}`phystool pdbfile bb6a9049-9289-4d2b-a6af-f76cf42da16a`                                  |
| Affiche le fichier {{tex}} dans le terminal                                   | {code}`phystool pdbfile bb6a9049-9289-4d2b-a6af-f76cf42da16a --cat`                            |
| Parse le fichier {{tex}} afin de mettre à jours les métadonnée du {{pdbfile}} | {code}`phystool pdbfile bb6a9049-9289-4d2b-a6af-f76cf42da16a --parse`                          |
| Liste les {{tags}} du {{pdbfile}}                                             | {code}`phystool pdbfile bb6a9049-9289-4d2b-a6af-f76cf42da16a tags --list`                      |
| Ajoute les {{tags}} au {{pdbfile}}                                            | {code}`phystool pdbfile bb6a9049-9289-4d2b-a6af-f76cf42da16a tags --add "Cinématique,Énergie"` |
```

```{argparse}
   :filename: ../../src/phystool/cli.py
   :func: get_parser
   :prog: phystool
   :path: pdbfile
   :nodefaultconst:
```
