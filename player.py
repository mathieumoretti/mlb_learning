import gamelog

class Player:
	def __init__(self, *args, **kwargs):
		self.name = ""
		self.game_logs = []
		return super().__init__(*args, **kwargs)


