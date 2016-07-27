# TODO: add multyselection support
import sublime, sublime_plugin, re

class schpuCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		logMsg = ""
		found = 0
		new_content = ""
		mpt_cnt = 0
		lines_total = 0

		def transform(s):
			flag = 0
			new_line = ''

			first = re.search("^(\S+)\s", s)
			if first is not None:
				first = first.group(1)
				first = re.search("/([^/]+)/?$", first)
				if first is not None:
					first = first.group(1)
					new_line += "'" + first + "' => '"
					flag = flag + 1

			second = re.search("\s(\S+)$", s)
			if second is not None:
				second = second.group(1)
				second = re.search("/([^/]+)/?$", second)
				if second is not None:
					second = second.group(1)
					new_line += second + "',"
					flag = flag + 1

			if flag  == 2:
				return new_line
			else:
				return False

		def highlight(region, mode):
			if(mode == 'selection'):
				# self.view.add_regions('raw', region, "comment")
				# print("skip highlighting")
				self.view.sel().add(region)
			else:
				old_regions = region.find_all("^[^>]+$")
				# self.view.add_regions("mark", dregion, "mark", "dot", sublime.HIDDEN | sublime.PERSISTENT)
				# self.view.add_regions('raw', [sublime.Region(0, self.view.size())], 'comment')
				region.add_regions('raw', old_regions, "mark", "dot")

		if self.view.size():
			if len(self.view.sel()[0]) > 0:
				for sel_region in self.view.sel():
					new_content = ""
					selection = self.view.substr(sel_region).replace("'", "").replace("\"", "").replace("\t", " ")
					content_list = selection.strip().splitlines()

					for item in content_list:
						line = item.strip()
						if line.find(' ') <= 0:
							mpt_cnt = mpt_cnt + 1
					if mpt_cnt >= (len(content_list)/2):
						logMsg += 'Row list detected! '
						content_list = [content_list[i]+' '+content_list[i+1] for i in range(0, len(content_list)-1, 2)]

					if len(content_list) > 0:
						for item in content_list:
							line = item.strip()
							# if line == "" or ((' ' in line) == False and ('\t' in line) == False):
							if line == "" or line.find(' ') <= 0:
								continue
							try_conv = transform(line)
							if try_conv != False:
								new_content = new_content + try_conv + "\n"
								found = found + 1
							else:
								new_content = new_content + line + "\n"
						if len(new_content) > 0:
							# new_content = re.sub('\s+$', '', new_content)
							new_content = new_content[:-1]
					self.view.replace(edit, sel_region, new_content)
					lines_total = lines_total + len(content_list)

				highlight(self.view.sel(), 'selection')

				if len(self.view.sel()) > 0:
					lines_total = lines_total
				else:
					lines_total = len(content_list)

			else:
				dregion = sublime.Region(0, self.view.size())
				content = self.view.substr(dregion).replace("'", "").replace("\"", "").replace("\t", " ")

				content_list = content.strip().splitlines()

				for item in content_list:
					line = item.strip()
					if line.find(' ') <= 0:
						mpt_cnt = mpt_cnt + 1
				if mpt_cnt >= (len(content_list)/2):
					logMsg += 'Row list detected! '
					content_list = [content_list[i]+' '+content_list[i+1] for i in range(0, len(content_list)-1, 2)]

				if len(content_list) > 0:
					for item in content_list:
						line = item.strip()
						# if line == "" or ((' ' in line) == False and ('\t' in line) == False):
						if line == "":
							continue
						try_conv = transform(line)
						if try_conv != False:
							new_content = new_content + try_conv + "\n"
							found = found + 1
						else:
							new_content = new_content + line + "\n"

				self.view.replace(edit, dregion, new_content)
				
				highlight(self.view, 'all')

				lines_total = len(content_list)
			
			if found > 0:
				logMsg += "Done! Found " + str(found) + " from " + str(lines_total) + " lines."
			else:
				logMsg += "Nothing found."
		else:
			logMsg += "Empty document!"

		sublime.status_message(logMsg)
		sublime.message_dialog(logMsg)
