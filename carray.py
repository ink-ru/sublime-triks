# TODO: make single function "transform"
# TODO: add multyselection support
import sublime, sublime_plugin, re

class carrayCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		logMsg = ""
		found = 0
		items = ["текст в массив", "вырезать URI из URL", 'только символьные коды', 'симкоды из чередующегося списка']
		self.choice = -1

		def transform(s):
			s = re.sub(r"(\S+)([ ]+[^\n]+)", r"'\1' => \2", s)
			s = re.sub(r"(\S+ =>).* (\S+)(\n|\Z)", r"\1 '\2',\3", s)
			return s

		def transform1(s):
			s = re.sub(r"https?://[^/]+", "", s)
			s = re.sub(r"(\S+)([ ]+[^\n]+)", r"'\1' => \2", s)
			s = re.sub(r"(\S+ =>).* (\S+)(\n|\Z)", r"\1 '\2',\3", s)
			return s

		def transform2(s):
			s = re.sub(r"\S+/([^/]+)/?([ ]+[^\n]+)", r"'\1' => \2", s)
			s = re.sub(r"(\S+ =>).* \S+/([^/]+)/?(\n|\Z)", r"\1 '\2',\3", s)
			return s

		def transform3(s):
			s = re.sub(r"\n{2,}", "\n", s)
			s = re.sub(r"(\S+)\n(\S+)(\n|\Z)", r"\1 \2\n", s)
			s = re.sub(r"\s+\Z", "", s)
			s = re.sub(r"\S+/([^/]+)/?([ ]+[^\n]+)", r"'\1' => \2", s)
			s = re.sub(r"(\S+ =>).* \S+/([^/]+)/?(\n|\Z)", r"\1 '\2',\3", s)
			return s

		def on_done(e):
			self.choice = e
			# return choice

		vw = sublime.active_window().active_view()
		vw.show_popup_menu(items, on_done)

		if self.view.size():
			if len(self.view.sel()[0]) > 0:
				selection = self.view.substr(self.view.sel()[0]).replace("'", "").replace("\"", "").replace("\t", " ")
				sm = re.search('(\S+)[ ]+[^\s]*[ ]*(\S+)(\n|\Z)', selection)

				if sm is not None:
					found = 1
					if self.choice == 1:
						selection = transform1(selection)
					elif self.choice == 2:
						selection = transform2(selection)
					else:
						selection = transform(selection)
					self.view.replace(edit, self.view.sel()[0], selection)
				elif self.choice == 3:
					found = 1
					selection = transform3(selection)
					self.view.replace(edit, self.view.sel()[0], selection)

			else:
				dregion = sublime.Region(0, self.view.size())
				content = self.view.substr(dregion).replace("'", "").replace("\"", "").replace("\t", " ")

				m = re.search('(\S+)[ ]+[^\s]*[ ]*(\S+)(\n|\Z)', content)
				if m is not None:
					found = 1
					if self.choice == 1:
						content = transform1(content)
					elif self.choice == 2:
						content = transform2(content)
					else:
						content = transform(content)
					self.view.replace(edit, dregion, content)
				elif self.choice == 3:
					found = 1
					content = transform3(content)
					self.view.replace(edit, dregion, content)

			if found > 0:
				logMsg += "Done!"
			else:
				logMsg += "Nothing found."
		else:
			logMsg += "Empty document!"

		sublime.status_message(logMsg)
