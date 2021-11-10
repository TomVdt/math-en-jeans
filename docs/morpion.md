---
layout: post
title: Morpion
description: L'opportunité de revoir des bases
permalink: morpion
---

# 1. Règles du jeu

Au cas où vous ne connaitriez pas, je vous fait un cours résumé des règles du jeux:
- Le jeu se joue dans une grille 3x3
- Il y a 2 joueurs, chacun avec des pions symbolisés par des X ou O
- Chacun son tour, les joueurs vont placer un pion sur la grille
- Pour gagner, un joueur doit aligner 3 pions à l'horizontale, verticale ou en diagonale

![Morpion](#)


# 2. Notre approche

Le Morpion étant un jeu assez simple à modéliser, nous avons établi un arbre représentant toutes les situations initiales
![Situations initiales](#)

On a rapidement vu que beaucoup des situations initiales étaient symétriques, ce qui nous laissait 3 places où commencer
![Possibilités initiales](#)

À partir de ces différentes configurations, nous avons tracé quelques parties.
![Quelques parties](#)


# 3. De l'arbre à des idées

Lors de la réalisation de ces arbres, nous avons observé un "pattern" (motif): pour placer le prochain pion, on a regardé si il y avait une opportunité de gagner, si on pouvait bloquer l'adversaire ou si on pouvait se placer dans une situation avantageuse (2 pions alignés).

En pseudocode, un algorithme auquel on a pensé serait:
```
pour chaque case libre:
	si elle nous fait gagner:
		jouer ici
	sinon si on bloque l'adversaire:
		jouer ici
	sinon si on a aligne 2 pions et 1 case vide:
		jouer ici
```

Cet algorithme, bien que fonctionnel, ne permet pas d'assurer la victoire.
Une attaque en bifurcation permettrait à un joueur de l'emporter sur la machine.

![Attaque biffurquée](#)

Ce n'est pas ce qu'on veut!

Il ne suffit donc pas de se contenter de regarder l'état actuel des choses, mais regarder aussi les mouvements futurs.
L'ordinateur doit donc simuler le tour du joueur pour mieux choisir!


# 4. Et si on cherchait plus loin?

Au lieu de seulement observer un instant de la grille et choisir en fonction de sa configuration actuelle, pourquoi pas essayer de prédire le futur? Mais comment?

À un instant t<sub>0</sub>, on a cette grille de jeu:

![Grille t0](#)

Si on utilise l'algorithme précédent sur cette grille, on obtient ceci:

![Grille t1](#)

C'est là qu'on s'est arrêté avant. Mais pourquoi pas continuer a partir de cette nouvelle grille? On simulerait alors le tour de l'adversaire, et on suppose donc qu'il jouera le mieux possible. On obtient donc la grille à l'instant t<sub>2</sub>:

![Grille t2](#)

Et si on continuait encore? L'arbre deviendrait très grand, puisqu'on est en réalité en train de vérifier toutes les possibilités.
Une illustration de cette arbre est trop grande pour cette page!

En réalité, on pourrait, avec cet algorithme, aller de l'instant t<sub>0</sub> à t<sub>n</sub> et vérifier toutes les combinaisons possibles pour s'assurer une victoire

Mais comment choisit-on, avec toutes ces donnéss, l'emplacement final du pion? Une idée qu'on a eu était d'attribuer un score à une configuration de la grille.
On aurait par exemple:
- +5 points par alignement de 2 pions et un espace vide
- +5 points pour occuper le centre, +3 pour les coins et +1 pour les côtes
- -5 points par alignement de 2 pions adverses et un espace vide
- Et plus...

À la fin de l'execution de l'algorithme, on voudrait donc qu'il nous renvoie un score, le score associé à la grille.
C'est donc l'emplacement avec le plus grand score où on va placer le pion!


# 5. Récurrence, chère récurrence...

En théorie, on a un algorithme qui fonctionne. Il nous suffit donc de l'implémenter!

Une première aproche pourrait être de juste copier-coller l'algorithme plusieurs fois.

```py
for emplacement in emplacements_libres:
	if nous_fait_gagner(emplacement):
		jouer(emplacement)
		for emplacement in emplacements_libres:
			if nous_fait_gagner(emplacement):
				jouer(emplacement)
				...
			elif bloque_victoire_adversaire(emplacement):
				jouer(emplacement)
				...
			elif alignement(emplacement):
				jouer(emplacement)
				...
	elif bloque_victoire_adversaire(emplacement):
		jouer(emplacement)
		for emplacement in emplacements_libres:
			if nous_fait_gagner(emplacement):
				jouer(emplacement)
				...
			elif bloque_victoire_adversaire(emplacement):
				jouer(emplacement)
				...
			elif alignement(emplacement):
				jouer(emplacement)
				...
	elif alignement(emplacement):
		jouer(emplacement)
		for emplacement in emplacements_libres:
			if nous_fait_gagner(emplacement):
				jouer(emplacement)
				...
			elif bloque_victoire_adversaire(emplacement):
				jouer(emplacement)
				...
			elif alignement(emplacement):
				jouer(emplacement)
				...
```

Hmmm... C'est vraiment pas propre, pas pratique à utiliser et ca prend énormément de place. On a un remède à ça! C'est la *récurrence*!
Comment ça fonctionne?

Commençons par définir une fonction en python équivalent à l'algorithme initial. On donnera la grille de jeu comme argument de la fonction.

```py
def trouver_meilleur(grille):
	for emplacement in emplacements_libres(grille):
		if nous_fait_gagner(emplacement):
			jouer(emplacement)
		elif bloque_victoire_adversaire(emplacement):
			jouer(emplacement)
		elif alignement(emplacement):
			jouer(emplacement)
```

Parfait!

Maintenant: la sauce magique. On va appeller la fonction *depuis la fonction*. C'est la raison pour laquelle il fallait donner la grille comme argument.

```py
def trouver_meilleur(grille):
	for emplacement in emplacements_libres(grille):
		if nous_fait_gagner(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
		elif bloque_victoire_adversaire(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
		elif alignement(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
```

Super! On remarque que, si on étend les fonctions par leurs définitions, on obtient le même algorithme pas beau précédent. Sauf que maintenant il est beau!
Mais la fonctionne ne retourne toujours rien... et ne s'arrête jamais... Il faudrait donc une manière de lui dire qu'il faut arrêter. 
On va devoir retourner aux règles: le jeu s'arrête quand:
1. Un joueur gagne
2. La grille de jeu est remplie

Rajoutons ces conditions au début de la fonction.

```py
def trouver_meilleur(grille):
	if quelqun_a_gagne(grille) or grille_pleine(grille):
		return

	for emplacement in emplacements_libres(grille):
		if nous_fait_gagner(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
		elif bloque_victoire_adversaire(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
		elif alignement(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
```

D'après ce qu'on a dit avant, il faut retourner un score associé à la grille. La fonction finale est donc:

```py
def trouver_meilleur(grille):
	if quelqun_a_gagne(grille) or grille_pleine(grille):
		return score(grille)

	for emplacement in emplacements_libres(grille):
		if nous_fait_gagner(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
		elif bloque_victoire_adversaire(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
		elif alignement(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
```

On a donc un algorithme récursif fonctionnel!


# 6. L'évaluation de la grille de jeu

Bien bien. On doit noter cette grille.

Pour être parfaitement honête, je n'ai pas trop envi de traduire [les exemples de score](#4-et-si-on-cherchait-plus-loin) donnés avant...
Puisqu'on cherche toutes les possibilités jusqu'à la fin du jeu, on peut se contenter de noter en fonction de qui à gagné.

```py
def score(grille):
	if victoire_ordinateur(grille):
		score = 1000
	elif victoire_joueur(grille):
		score = -1000
	else:
		score = 0
	return score
```

Notons que le score est négatif si le joueur gagne, puisqu'on veut éviter cette situation à tout prix. Aussi, si personne n'a gagné, on met le score à 0 par défaut.
Cette méthode fainéante ne fonctionne cependant que pour le morpion, puisque le nombre de combinaisons à vérifier est relativement faible. C'est donc à revoir pour la suite.


# 7. Petite(s) révision(s) nécessaire(s)...

Je dois vous avouer une chose. L'algorithme final du [5.](#5-récurrence-chère-récurrence) n'est pas encore complet.
On ne sait pas qui est censé jouer lorsqu'on appelle la fonction!
Solution simple: on rajoute un argument.

```py
def trouver_meilleur(grille, player):
	if quelqun_a_gagne(grille) or grille_pleine(grille):
		return score(grille)

	for emplacement in emplacements_libres(grille):
		if nous_fait_gagner(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
		elif bloque_victoire_adversaire(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
		elif alignement(emplacement):
			jouer(emplacement)
			trouver_meilleur(grille)
```

Mais pourquoi doit-on savoir cela me direz vous. 
En tant qu'ordinateur, on cherche à maximiser le score qu'on obtient, ce qui équivaut à gagner, alors qu'en tant que joueur, on essaye de minimiser le score, ce qui équivaut à faire perdre la machine.
On doit donc séparer les deux cas.

```py
def trouver_meilleur(grille):
	if quelqun_a_gagne(grille) or grille_pleine(grille):
		return score(grille)

	if joueur == ordinateur:
		for emplacement in emplacements_libres(grille):
			if nous_fait_gagner(emplacement):
				jouer(emplacement)
				trouver_meilleur(grille)
			elif bloque_victoire_adversaire(emplacement):
				jouer(emplacement)
				trouver_meilleur(grille)
			elif alignement(emplacement):
				jouer(emplacement)
				trouver_meilleur(grille)

	elif joueur == humain:
		for emplacement in emplacements_libres(grille):
			if nous_fait_gagner(emplacement):
				jouer(emplacement)
				trouver_meilleur(grille)
			elif bloque_victoire_adversaire(emplacement):
				jouer(emplacement)
				trouver_meilleur(grille)
			elif alignement(emplacement):
				jouer(emplacement)
				trouver_meilleur(grille)
```

Ça avance!
Rajoutons deux variables qui sauvegardent le score maximum et minimum.

```py
def trouver_meilleur(grille):
	if quelqun_a_gagne(grille) or grille_pleine(grille):
		return score(grille)

	if joueur == ordinateur:
		score_max = -infini
		for emplacement in emplacements_libres(grille):
			if nous_fait_gagner(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			elif bloque_victoire_adversaire(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			elif alignement(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			score_max = max(score_max, score)

	elif joueur == humain:
		score_min = infini
		for emplacement in emplacements_libres(grille):
			if nous_fait_gagner(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			elif bloque_victoire_adversaire(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			elif alignement(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			score_min = min(score_min, score)
```

Elles sont initialisées à -∞ et ∞ respectivement, puisque n'importe quel nombre est plus grand que -∞ et n'importe quel nombre est plus petit que ∞.
Bien. On a les scores maximaux et minimaux. On en fait quoi maintenant? On les retourne!

```py
def trouver_meilleur(grille):
	if quelqun_a_gagne(grille) or grille_pleine(grille):
		return score(grille)

	if joueur == ordinateur:
		score_max = -infini
		for emplacement in emplacements_libres(grille):
			if nous_fait_gagner(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			elif bloque_victoire_adversaire(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			elif alignement(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			score_max = max(score_max, score)
		return score_max

	elif joueur == humain:
		score_min = infini
		for emplacement in emplacements_libres(grille):
			if nous_fait_gagner(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			elif bloque_victoire_adversaire(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			elif alignement(emplacement):
				jouer(emplacement)
				score = trouver_meilleur(grille)
			score_min = min(score_min, score)
		return score_min
```

La seule chose qui nous interesse de savoir est quel emplacement nous donne le meilleur (ou pire) score, pas les scores intermédiaires.
L'animation ci-dessous illustre cet aspect.

[Animation fusion des grilles](#)

Une dernière optimisation que l'on peut faire est de revisiter l'algorithme initial.
Ce n'est plus nécessaire de vérifier si un emplacement nous fait perdre, gagner ou nous donne un avantage: la fonction de score nous donne déjà cette information.
De plus, on vérifie toutes les combinaisons possibles dans tous les cas, il n'est donc pas nécessaire de faire ces petites vérifications intermédiaires.
L'algorithme final est donc:

```py
def trouver_meilleur(grille):
	if joueur_a_gagne(grille) or grille_pleine(grille):
		return score(grille)

	if joueur == ordinateur:
		score_max = -infini
		for emplacement in emplacements_libres(grille):
			jouer(emplacement)
			score = trouver_meilleur(grille)
			score_max = max(score_max, score)
		return score_max

	elif joueur == humain:
		score_min = infini
		for emplacement in emplacements_libres(grille):
			jouer(emplacement)
			score = trouver_meilleur(grille)
			score_min = min(score_min, score)
		return score_min
```



# 8. Enfin du code fonctionnel!

On y est presque! L'algorithme est complet, le score est complet, il nous une toute petite étape avant de pouvoir déterminer quel emplacement est le meilleur.
Une petite boucle et quelques variables suffisent!

```py
score_max = -∞
meilleur_emplacement = 0
for emplacement in emplacements_libres(grille):
	jouer(emplacement)
	score = trouver_meilleur(grille, humain)
	if score > score_max:
		score_max = score
		meilleur_emplacement = emplacement

jouer(meilleur_emplacement)
```

Le code est *très* similaire à celui de l'algorithme, puisqu'on réalise la première étape de l'algorithme (trouver le meilleur emplacement pour l'ordinateur) en sauvegardant le meilleur emplacement.

En dessous j'ai mis un programme python fonctionnel, pour jouer au morpion contre l'ordinateur (il est un peu plus complexe mais vous retrouverez bien tous les éléments)

```py
import numpy as np
print("Hello, World!")


# Real player object, handles interaction with the human player
class Player:

	# Initialise player class by giving it it's corresponding piece
	def __init__(self, player):
		self.player = player

	# Handle player input correctly, only send back a valid move
	def get_next_move(self, grid):
		while True:
			move = 0
			try:
				move = int(input(f"Player {1 if self.player == 1 else 2}'s turn: "))
			except ValueError:
				print("Invalid")
			if 1 <= move <= 9:
				if not check_valid_move(grid, move - 1):
					print("Occupied!")
				else:
					break
		return move - 1


# Bot object, handles the minimax algorithm to find the best move
class Bot:

	def __init__(self, player):
		self.player = player

	# Attribute a score to a certain board state
	def get_score(self, grid):
		if check_victory(grid, self.player):
			score = 1000000000
		elif check_victory(grid, -self.player):
			score = -1000000000
		else:
			score = 0
		return score

	# Recursive best-move finder
	def minimax(self, grid, player):
		if game_end(grid):
			return self.get_score(grid)

		valid_moves = get_valid_moves(grid)
		if player == self.player:
			max_score = -np.inf
			for move in valid_moves:
				grid[move // 3, move % 3] = player
				score = self.minimax(grid, -player)
				# Put grid back in initial state (important!)
				grid[move // 3, move % 3] = 0
				max_score = max(max_score, score)
			return max_score

		elif player == -self.player:
			min_score = np.inf
			for move in valid_moves:
				grid[move // 3, move % 3] = player
				score = self.minimax(grid, -player)
				# Put grid back in initial state (important!)
				grid[move // 3, move % 3] = 0
				min_score = min(min_score, score)
		return min_score

	# Get the best move for the bot
	def get_next_move(self, grid):
		valid_moves = get_valid_moves(grid)
		max_score = -np.inf
		best_move = 0
		for move in valid_moves:
			grid[move // 3, move % 3] = self.player
			score = self.minimax(grid, -self.player)
			# Put grid back in initial state (important!)
			grid[move // 3, move % 3] = 0
			if score > max_score:
				max_score = score
				best_move = move

		return best_move


# See if the game has ended (full or player win)
def game_end(grid):
	return len(get_valid_moves(grid)) == 0 or check_victory(grid, 1) or check_victory(grid, -1)


# Give a list with all valid moves
def get_valid_moves(grid):
	moves = []
	for i in range(3):
		for j in range(3):
			if grid[i, j] == 0:
				moves.append(i * 3 + j)
	return moves


# Check if a player has won
def check_victory(grid, player):
	for i in range(3):
		# Check the columns
		if grid[i, 0] == grid[i, 1] == grid[i, 2] == player:
			return True
		# Check the rows
		if grid[0, i] == grid[1, i] == grid[2, i] == player:
			return True

	# Check the top-left down-right diagonal
	if grid[0, 0] == grid[1, 1] == grid[2, 2] == player:
		return True
	# Check the down-left top-right diagonal
	if grid[2, 0] == grid[1, 1] == grid[0, 2] == player:
		return True

	return False


# Check if a move is valid
def check_valid_move(grid, move):
	return grid[move // 3, move % 3] == 0


def main():
	# Initialisation
	grid = np.zeros((3, 3), dtype=int)
	player1 = Player(1)
	player2 = Bot(-1)
	turn = 1
	move = 0
	game = True
	print(grid)

	# Main loop
	while game:
		# Get the move for the correct player
		if turn == 1:
			move = player1.get_next_move(grid)
		elif turn == -1:
			move = player2.get_next_move(grid)
		else:
			raise ValueError('`turn` is not 1 or -1, how did this happen?')

		# Place the player's piece on the selected place
		grid[move // 3, move % 3] = turn

		# Next player's turn
		turn *= -1

		# Show the board to the users
		print(grid)

		# Stop the game if it is done (win or full)
		if game_end(grid):
			game = False

	# Show who has won
	if check_victory(grid, 1):
		print("Player 1 has won the game!")
	elif check_victory(grid, -1):
		print("Player 2 has won the game!")
	else:
		print("No one won :(")


if __name__ == '__main__':
	main()
```

Essayez-le!


# 9. Conclusion

Cette première étape de recherche nous a permis de nous familiariser avec l'algorithmique et la programmation, grâce au niveau relativement facile du la résolution du morpion.
Il faudra surement plus de reflexion pour résoudre le Achi et Picaria, puisque la force brute qu'on a utilisée ici ne fonctionnera pas entièrement pour ces jeux.

Reste à explorer d'une façon similaire au début de cette aventure ces jeux pour trouver des indices de résolution!

Merci!
