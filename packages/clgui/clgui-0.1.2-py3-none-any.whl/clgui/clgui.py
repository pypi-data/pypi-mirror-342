import colorama, keyboard, threading, time
colorama.init()

class GUI:
	def __init__(self, layout):
		self.layout = layout
		self.thread = None
		self.stop_flag = False
	
	def _keyboardWait(self):
		while not self.stop_flag:
			if (keyboard.is_pressed("control+c")):
				return
			time.sleep(0.01)

	def show(self):
		self.layout._render()
		keyboard.hook(self.layout._handleKeyPress)
		self.thread = threading.Thread(target=self._keyboardWait)
		self.thread.start()

	def destroy(self):
		keyboard.unhook(self.layout._handleKeyPress)
		self.stop_flag = True

class ButtonList:
	def __init__(self):
		self.buttons = []
		self.title = None
		self.selected_index = 0

	def setTitle(self, title):
		self.title = title

	def addButtons(self, buttons):
		for button in buttons:
			self.addButton(button)

	def addButton(self, button):
		self.buttons.append(button)
		
	def _render(self, print_func, state):
		if (self.title):
			print_func(colorama.Fore.YELLOW + self.title + colorama.Style.RESET_ALL)
		for i, button in enumerate(self.buttons):
			button._render(print_func, state, i == self.selected_index)

	def _handleInput(self, key):
		initial_selected_index = self.selected_index
		match (key.name):
			case "up":
				self.selected_index = (self.selected_index - 1) % len(self.buttons)
			case "down":
				self.selected_index = (self.selected_index + 1) % len(self.buttons)
			case _:
				for i, button in enumerate(self.buttons):
					if (i == self.selected_index):
						return button._handleInput(key)
		return initial_selected_index != self.selected_index

class Button:
	def __init__(self, label, callback=None, data=None):
		self.label = label
		self.callback = callback
		self.data = data

	def _render(self, print_func, state, isSelected=True):
		match (state):
			case 1:
				print_func(colorama.Fore.BLUE + self.label + colorama.Style.RESET_ALL)
			case 2:
				print_func(colorama.Fore.LIGHTBLACK_EX + self.label + colorama.Style.RESET_ALL)
			case _:
				style = colorama.Fore.WHITE
				if (isSelected and state == 3):
					style = colorama.Back.WHITE + colorama.Fore.BLACK
				print_func(style + self.label + colorama.Style.RESET_ALL)
				
	def _handleInput(self, key):
		match (key.name):
			case "enter":
				if(self.callback):
					self.callback(self.data)
		return False
	