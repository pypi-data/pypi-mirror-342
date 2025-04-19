# LaTeX

{{phystool}} est conçu de façon à laisser à l'utilisateur un maximum de
liberté quant à son utilisation de {{latex}}. Comme {{latex}} est extrêmement
personnalisable et que chaque utilisateur possède des attentes particulières,
{{phystool}} offre la possibilité de définir comment chaque {{pdbfile}} doit
être compilé.

```{code-block} latex
    :linenos:
    :caption: 9d1f2b06-fc3a-4eb4-8f7e-dadc8f0f0888.tex

    \begin{exercise}[title=Eureka]
        Vérifiez que la période d’oscillation d'Archimède est indépendante de
        la température du chat de Schrödinger.
    \end{exercise}
```

```{code-block} latex
    :linenos:
    :caption: /tmp/physauto-9d1f2b06-fc3a-4eb4-8f7e-dadc8f0f0888.tex

    \documentclass{physauto}
    \PdbSetDBPath{~/physdb}
    \begin{document}
        \PdbPrint{9d1f2b06-fc3a-4eb4-8f7e-dadc8f0f0888}
    \end{document}

```

```{code-block} latex
    :linenos:
    :caption: serie-A.tex

    \documentclass[pdb=~/physdb]{physperso}

    \begin{document}
        \PdbExercise{9d1f2b06-fc3a-4eb4-8f7e-dadc8f0f0888}
    \end{document}

```
