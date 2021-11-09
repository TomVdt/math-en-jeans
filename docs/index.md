---
layout: page
title: Projet MATh.en.JEANS
permalink: /
---

# MATh.en.JEANS

Bonjour !

Vous pourrez lire ici nos traces de recherche pour l'atelier [MATh.en.JEANS](https://mathenjeans.fr)


# Notre mission

Nous avons choisi de chercher des solutions pour les jeux du Morpion, Atchi et Picaria.

Pour commencer, nous allons explorer le Morpion


# Le Morpion

Au cas où vous ne connaitriez pas, je vous fait un cours résumé des règles du jeux:
- Le jeu se joue dans une grille 3x3
- Il y a 2 joueurs, chacun avec des pions symbolisés par des X ou O
- Chacun son tour, les joueurs vont placer un pion sur la grille
- Pour gagner, un joueur doit aligner 3 pions à l'horizontale, verticale ou en diagonale
![Morpion](#)


## Notre approche

Le Morpion étant un jeu assez simple à modéliser, nous avons établi un arbre représentant toutes les situations initiales
![Situations initiales](#)

On a rapidement vu que beaucoup des situations initiales étaient symétriques, ce qui nous laissait 3 places où commencer
![Possibilités initiales](#)

À partir de ces différentes configurations, nous avons tracé quelques parties.
![Quelques parties](#)


## De l'arbre à des idées

Lors de la réalisation de ces arbres, nous avons observé un "pattern" (motif): pour placer le prochain pion, on a regardé si il y avait une opportunité de gagner, si on pouvait bloquer l'adversaire ou si on pouvait se placer dans une situation avantageuse (2 pions alignés).

En pseudocode, un algorithme auquel on a pensé serait
```
pour chaque case libre:
	si elle nous fait gagner:
		jouer ici
	sinon si on bloque l'adversaire:
		jouer ici
	sinon si on a aligne 2 pions et 1 case vide:
		jouer ici
```


