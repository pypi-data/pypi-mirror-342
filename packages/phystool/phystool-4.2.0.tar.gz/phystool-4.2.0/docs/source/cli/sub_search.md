# Search


Effectue une recherche dans la base de donnée et affiche le résultat dans le
terminal.

```{table} Exemples d'utilisation
    :width: 100%

| Afficher dans le terminal tous les ...               | Commande                                                               |
| ---                                                  | ---                                                                    |
| {{pdbfile}}                                          | {code}`phystool search`                                                |
| {{exercise}} et {{qcm}} contenant "champ magnétique" | {code}`phystool search --type exercise,qcm --query "champ magnétique"` |
| {{pdbfile}} avec les {{tags}}                        | {code}`phystool search --tags Cinématique,Énergie`                     |
| {{tp}} dont l'{{uuid}} contient "a4bd1"              | {code}`phystool search --type tp --uuid a4bd1`                         |
```

```{argparse}
   :filename: ../../src/phystool/cli.py
   :func: get_parser
   :prog: phystool
   :path: search
   :nodefaultconst: 
```
