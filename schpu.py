# TODO: add multyselection support
import sublime, sublime_plugin, re

class schpuCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		logMsg = ""
		found = 0
		new_content = ""

		def transform(s):
			flag = 0
			new_line = ''

			first = re.search("^(\S+)\s", s)
			if first is not None:
				first = first.group(1)
				first = re.search("/([^/]+)/?$", s)
				if first is not None:
					first = first.group(1)
					new_line += "'" + first + "' => '"
					flag = flag + 1

			second = re.search("\s(\S+)$", s)
			if second is not None:
				second = second.group(1)
				second = re.search("/([^/]+)/?$", s)
				if second is not None:
					second = second.group(1)
					new_line += second + "',"
					flag = flag + 1

			if flag  == 2:
				return new_line
			else:
				return False

		if self.view.size():
			if len(self.view.sel()[0]) > 0:
				selection = self.view.substr(self.view.sel()[0]).replace("'", "").replace("\"", "").replace("\t", " ")

				content_list = selection.strip().splitlines()
				if len(content_list) > 0:
					for item in content_list:
						line = item.strip()
						# if line == "" or ((' ' in line) == False and ('\t' in line) == False):
						if line == "" or line.find(' ') <= 0 or line.find('/') <= 0:
							new_content = new_content + line + "\n"
							continue
						try_conv = transform(line)
						if try_conv != False:
							new_content = new_content + try_conv + "\n"
							found = found + 1
						else:
							new_content = new_content + line + "\n"

				self.view.replace(edit, self.view.sel()[0], "\n" + new_content)

			else:
				dregion = sublime.Region(0, self.view.size())
				content = self.view.substr(dregion).replace("'", "").replace("\"", "").replace("\t", " ")

				content_list = content.strip().splitlines()
				if len(content_list) > 0:
					for item in content_list:
						line = item.strip()
						# if line == "" or ((' ' in line) == False and ('\t' in line) == False):
						if line == "" or line.find(' ') <= 0 or line.find('/') <= 0:
							new_content = new_content + line + "\n"
							continue
						try_conv = transform(line)
						if try_conv != False:
							new_content = new_content + try_conv + "\n"
							found = found + 1
						else:
							new_content = new_content + line + "\n"

				self.view.replace(edit, dregion, new_content)
			
			if found > 0:
				logMsg += "Done! Found " + str(found) + " from " + str(len(content_list)) + " lines."
			else:
				logMsg += "Nothing found."
		else:
			logMsg += "Empty document!"

		sublime.status_message(logMsg)
		sublime.message_dialog(logMsg)
