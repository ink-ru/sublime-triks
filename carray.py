import sublime, sublime_plugin, re

class carrayCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		logMsg = ""
		found = 0
		# window = sublime.active_window()



		if self.view.size():
			dregion = sublime.Region(0, self.view.size())
			content = self.view.substr(dregion)

			if len(self.view.sel()[0]) > 0:
				selection = self.view.substr(self.view.sel()[0])
				sm = re.search('(\S+)[ ]+(\S+)(\n|\Z)', selection)

				if sm is not None:
					selection = re.sub(r"(\S+)[ ]+(\S+)(\n|\Z)", r"'\1' => '\2',\3", selection)
					found = 1
					self.view.replace(edit, self.view.sel()[0], selection)

			else:

				m = re.search('(\S+)[ ]+(\S+)(\n|\Z)', content)
				if m is not None:
					content = re.sub(r"(\S+)[ ]+(\S+)(\n|\Z)", r"'\1' => '\2',\3", content)
					found = 1
					self.view.replace(edit, dregion, content)

			if found > 0:
				logMsg += "Done!"
			else:
				logMsg += "Nothing found."
		else:
			logMsg += "Empty document!"

		sublime.status_message(logMsg)
