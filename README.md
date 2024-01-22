# MINLP optimisation pour Interclub Maitre

## Formalisation du problème mathématique et choix d'implémentation

Voir le fichier "formalisation.pdf".
Latex sur overleaf.

## Packages

- Sur mon PC IUT environnement conda : ```interclub```
- Sinon installer les packages suivants :

```
pandas 2.1.4
pyomo 6.7.0
scipy 1.11.4
```

## Structure du code
Deux codes selon que l'on considère la version linéaire (MILP) ou non linéaire (MINLP) du problème.
- MILP : résolue par scipy
- MINLP : résolue par pyomo (non-linéarité uniquement dans la fonction coût)

Dans tout les cas, il suffit de lancer `main.py` pour générer l'équipe optimale.

## Structure des données d'entrée

5 fichiers, au format `.csv` :
- ffnex_table_cotation : table de cotation de la FFN
- nageur_points : point marqué par chaque nageur sur chaque nage
- participation : table binaire, 1 participe, 0 ne participe pas
- relais_coef : Coefficient de rajeunissement à appliquer pour le calcul des points des relais
- relais_temps : Temps réalisé par chaque nageur sur chaque nage du relais

Voir les fichiers sur ce git pour plus d'informations.