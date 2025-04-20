import os

class VStack:
	def __init__(self):
		self.children = []
		self.selected_index = 0
		self.previewing = False
		
	def add(self, child):
		self.children.append(child)
	
	def _render(self):
		os.system("cls")
		for child in self.children:
			if (self.previewing):
				state = 1 if self.children[self.selected_index] == child else 0
			else:
				state = 3 if self.children[self.selected_index] == child else 2
			
			child._render(print, state)

	def _handleKeyPress(self, key):
		should_render = True
		if (key.event_type != "down"):
			return
		if (self.previewing):
			match (key.name):
				case "up":
					self.selected_index = (self.selected_index - 1) % len(self.children)
				case "down":
					self.selected_index = (self.selected_index + 1) % len(self.children)
				case "enter":
					self.previewing = False
				case _:
					should_render = self.children[self.selected_index]._handleInput(key)
		else:
			if (key.name == "esc" and len(self.children) > 1):
				self.previewing = True
			else:
				should_render = self.children[self.selected_index]._handleInput(key)
		if not should_render:
			return
		self._render()
