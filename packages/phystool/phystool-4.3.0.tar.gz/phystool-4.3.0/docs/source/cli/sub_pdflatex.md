# PdfLaTex

Compile des {{pdbfile}} ou des fichiers {{latex}}.

```{table} Exemples d'utilisation
    :width: 100%

| Action                                                 | Commande                                                                           |
| ---                                                    | ---                                                                                |
| Compilation d'un {{pdbfile}}                           | {code}`phystool pdflatex bb6a9049-9289-4d2b-a6af-f76cf42da16a`                     |
| Compilation d'un fichier {{tex}}                       | {code}`phystool pdflatex mon_fichier.tex --output mon_fichier.pdf`                 |
| Compilation simple ou double d'un fichier {{tex}}      | {code}`phystool pdflatex mon_fichier.tex --output mon_fichier.pdf --can-recompile` |
| Affichage des logs de compilation d'un fichier {{tex}} | {code}`phystool pdflatex mon_fichier.tex --logtex`                                 |
```

```{argparse}
   :filename: ../../src/phystool/cli.py
   :func: get_parser
   :prog: phystool
   :path: pdflatex
   :nodefaultconst: 
```
