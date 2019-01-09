# ADD INTO TARGET FILE --> import readline

class Completatore (object):  # Custom completer

	def __init__(self, options):
		self.options = sorted(options)

	def complete(self, text, state):
		if state == 0:  # on first trigger, build possible matches
			if text:  # cache matches (entries that start with entered text)
				self.matches = [s for s in self.options 
									if s and s.startswith(text)]
			else:  # no text entered, all matches possible
				self.matches = self.options[:]

		# return match indexed by state
		try: 
			return self.matches[state]
		except IndexError:
			return None


c_list = [
	"cmd_clear",
	"cmd_lpwd",
	"cmd_lls",
	"cmd_lcd",
	"cmd_help",
	"cmd_exit",
	"cmd_list",
	"cmd_interact ",
	"cmd_stop",
	"cmd_put ",
	"cmd_get ",
	"cmd_download ",
	"cmd_reverse_shell ",
	"cmd_flood_add ",
	"cmd_flood_remove ",
	"cmd_flood_start ",
	"global_flood_add ",
	"global_flood_remove ",
	"global_flood_start ",
	"cmd_screenshot ",
	"cmd_screenshot_save ",
	"cmd_camera ",
	"cmd_camera_save ",
	"cmd_mic ",
	"cmd_ransome ",
	"cmd_unransome ",
	"cmd_msgbox ",
	"cmd_functional "
		]