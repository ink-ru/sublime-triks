import sublime, sublime_plugin, re

class creportCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		BROKEN  = "Broken links, ordered by link:"
		BROKEN1 = "Broken links, ordered by page:"
		REDIR   = "List of redirected URLs"
		LIST    = "List of valid URLs you can submit to a search engine:"
		MAP     = "Site Map of valid HTML pages with a title:"
		LOCAL   = "Broken page-local links (also named 'anchors', 'fragment identifiers'):"
		ORPHAN  = "Orphan files:"
		STAT    = "Statistics for managers"
		TOP     = "Return to Top"

		logMsg = ""
		found = 0
		window = sublime.active_window()

		if self.view.size():
			dregion = sublime.Region(0, self.view.size())
			content = self.view.substr(dregion)

			broken = re.search('(?s)('+BROKEN+'|'+BROKEN1+')(\n){2,}(.*?)'+TOP, content)
			if broken:
				bcontent = broken.group(3)
				# TODO: cut images
				# bcontent = re.sub(r"^http.*\.(png|css|pdf|jpg|gif|zip|js)(?s)(.*?)\n\n", "", bcontent)
				# bcontent = re.sub(r"^(?s)http\S+\.(png|css|pdf|jpg|gif|zip|js)(.*?)\n\n", "", bcontent)
				# bcontent = re.sub(r"^\S+\.(png|css)(?s)(.*?)\n\n", "", bcontent)
				# bcontent = re.sub(r"^http.*", r"#################", bcontent)
				
				# shorten large link bloks
				bcontent = re.sub(r":\s+((\thttp\S+\n){1,10})(\thttp\S+\n){1,}", r":\n\g<1>\tИ другие...\n", bcontent)
				bcontent = re.sub(r"(\n){1,}\d+ broken link\(s\) reported\s*", "", bcontent)
				bcontent = bcontent.replace("error code", "код ошибки").replace("linked from page(s)", "найдено на страницах")
				b = self.view.window().new_file()
				b.set_name('broken.log')
				b.insert(edit, 0, bcontent)
				found+=1

			redirects = re.search('(?s)'+REDIR+'(\n){2,}(.*?)'+TOP, content)
			#redirects = re.search('(?s)List of redirected URLs(\n){2,}(.*?)Return to Top', content)
			if redirects:
				rcontent = redirects.group(2)
				rcontent = rcontent.replace("redirected to", "перенаправляет на").replace("status code", "код ответа").replace("linked from page(s)", "найдено на страницах")
				r = self.view.window().new_file()
				r.set_name('redirects.log')
				r.insert(edit, 0, rcontent)
				found+=1


			# content = re.sub(r"(?s)(.*?)\n\n", "", content)
			# content = re.sub(r"Table (of) contents", r"+\1+", content)

			# self.view.replace(edit, dregion, content)

			if found > 0:
				logMsg += "Done!"
			else:
				logMsg += "Nothing found."
		else:
			logMsg += "Empty document!"

		sublime.status_message(logMsg)



# r.run_command('My1Append', {'text': newcontent})
# class My1AppendCommand(sublime_plugin.TextCommand):
# 	def run(self, edit, text):
# 		self.view.insert(edit, self.view.size(), text)
# 		self.view.insert(edit, 0, 'New tab \n')
