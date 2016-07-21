# TODO: add multyselection support
import sublime, sublime_plugin, re

class uri2arrayCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		logMsg = ""
		found = 0

		def transform(s):
			s = re.sub(r"https?://[^/]+", "", s)
			s = re.sub(r"(\S+)([ ]+[^\n]+)", r"'\1' => \2", s)
			s = re.sub(r"(\S+ =>).* (\S+)(\n|\Z)", r"\1 '\2',\3", s)
			return s

		if self.view.size():
			if len(self.view.sel()[0]) > 0:
				selection = self.view.substr(self.view.sel()[0]).replace("'", "").replace("\"", "").replace("\t", " ")
				sm = re.search('(\S+)[ ]+[^\s]*[ ]*(\S+)(\n|\Z)', selection)

				if sm is not None:
					found = 1
					selection = transform(selection)
					self.view.replace(edit, self.view.sel()[0], selection)

			else:
				dregion = sublime.Region(0, self.view.size())
				content = self.view.substr(dregion).replace("'", "").replace("\"", "").replace("\t", " ")

				m = re.search('(\S+)[ ]+[^\s]*[ ]*(\S+)(\n|\Z)', content)
				if m is not None:
					found = 1
					content = transform(content)
					self.view.replace(edit, dregion, content)

			if found > 0:
				logMsg += "Done!"
			else:
				logMsg += "Nothing found."
		else:
			logMsg += "Empty document!"

		sublime.status_message(logMsg)
