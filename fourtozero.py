class FourToZero:

	def __init__(self, i):
		self.position = i

	def initial_position(self):
		return self.position

	def primitive(self, pos):
		return pos == 0

	def gen_moves(self):
		if self.position == 0:
			return []
		elif self.position == 1:
			return [0]
		else:
			return [self.position - 1, self.position - 2]

	def do_moves(self, move):
		if self.primitive(self.position):
			print("No more tokens remaining, the game is over.")
		elif move == 1 or move == 2:
			self.position -= move
			print(self.position)
		else:
			print("Invalid move. Remove 1 or 2 tokens per turn.")


state_map = dict()
state_map[0] = 0 #0 stands for losing position, 1 for winning

def main():
	for i in range(50):
		game = FourToZero(i)
		solve(game)
	print(state_map)


def solve(game):
	children = [state_type(pos) for pos in game.gen_moves()]
	if 0 in children:
		state_map[game.initial_position()] = 1
	else:
		state_map[game.initial_position()] = 0
	return state_map[game.initial_position()]

def state_type(pos):
	if pos in state_map.keys():
		return state_map[pos]
	children = [state_type(pos) for pos in game.gen_moves]
	if 0 in children:
		return 1
	else:
		return 0



if __name__ == "__main__":
    main()
