# TODO: make single function "transform"
# TODO: add multyselection support
import sublime, sublime_plugin, re

class schpuCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		logMsg = ""

		def transform(s,mode):
			s = re.sub(r"\n{2,}", "\n", s)
			s = re.sub(r"\s+\Z", "", s)
			# if(mode is 'list'):
			# 	s = re.sub(r"^(\S+)\n(\S+)(\n|\Z)", r"\1 \2\n", s)
			s = re.sub(r"(\S+)\n(\S+)(\n|\Z)", r"\1 \2\n", s)
			s = re.sub(r"\S+/([^/]+)/?([ ]+[^\n]+)", r"'\1' => \2", s)
			s = re.sub(r"(\S+ =>).* \S+/([^/]+)/?(\n|\Z)", r"\1 '\2',\3", s)
			return s

		if self.view.size():
			if len(self.view.sel()[0]) > 0:
				selection = self.view.substr(self.view.sel()[0]).replace("'", "").replace("\"", "").replace("\t", " ")
				sm = re.search('(\S+)[ ]+[^\s]*[ ]*(\S+)(\n|\Z)', selection)

				if sm is not None:
					selection = transform(selection,'normal')
				else:
					selection = transform(selection,'list')
				self.view.replace(edit, self.view.sel()[0], selection)

			else:
				dregion = sublime.Region(0, self.view.size())
				content = self.view.substr(dregion).replace("'", "").replace("\"", "").replace("\t", " ")

				m = re.search('(\S+)[ ]+[^\s]*[ ]*(\S+)(\n|\Z)', content)
				if m is not None:
					content = transform(content,'normal')
				else:
					content = transform(content,'list')
				self.view.replace(edit, dregion, content)
			
			logMsg += "Done!"
		else:
			logMsg += "Empty document!"

		sublime.status_message(sublime.platform()+' '+logMsg)
