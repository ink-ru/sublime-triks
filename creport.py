import sublime, sublime_plugin, re, urllib

class creportCommand(sublime_plugin.TextCommand):
	
	def download_url_to_string(self, url):
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		html = response.read()
		return html

	def getrobots(self, url):
		#TODO: split single line files
		robots_rules = ''

		robots = self.download_url_to_string(url)
		# remove leading and trailing white space
		robots = robots.strip()
		# put each line into a list
		robots_list = robots.decode("utf-8").strip().splitlines()

		for item in robots_list:
			mach = re.search('^Disallow: +([^\s]+)$', item, flags=re.IGNORECASE)
			if item == "" or mach == None:
				continue

			item = mach.group(1)

			if item.find('#') > 0:
				# comment removing
				item = re.sub(r"([^#]*)#.*", r"\1", item)

			item = re.sub(r"\*$", "", item)
			item = item.replace("*", ".*").replace("?", "\?").replace("$", "\n").strip()
			
			robots_rules = robots_rules + item + '|'
		robots_rules = robots_rules[:-1]

		# TODO: cut images
		robots_rules = r'(?s)^https?:\S+('+robots_rules+')(.*?)\n\n'
		
		return robots_rules
		
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

			# remove links disallowed by robots.txt
			rfile = re.search('(https?://[^/]+/)', content)
			robots_rules = self.getrobots(rfile.group(1)+'robots.txt')
			content = re.sub(robots_rules, "", content, flags=re.MULTILINE)
			# shorten large link bloks
			content = re.sub(r":\s+((\thttp\S+\n){1,10})(\thttp\S+\n){1,}", r":\n\g<1>\tИ другие...\n", content)

			broken = re.search('(?s)('+BROKEN+'|'+BROKEN1+')(\n){2,}(.*?)'+TOP, content)
			if broken is not None:
				bcontent = broken.group(3)
				
				bcontent = re.sub(r"(\n){1,}\d+ broken link\(s\) reported\s*", "", bcontent)
				bcontent = bcontent.replace("error code", "код ошибки").replace("linked from page(s)", "найдено на страницах")
				b = self.view.window().new_file()
				b.set_name('broken.log')
				b.insert(edit, 0, bcontent)
				found+=1

			redirects = re.search('(?s)'+REDIR+'(\n){2,}(.*?)'+TOP, content)
			#redirects = re.search('(?s)List of redirected URLs(\n){2,}(.*?)Return to Top', content)
			if redirects is not None:
				rcontent = redirects.group(2)
				rcontent = rcontent.replace("redirected to", "перенаправляет на").replace("status code", "код ответа").replace("linked from page(s)", "найдено на страницах")
				r = self.view.window().new_file()
				r.set_name('redirects.log')
				r.insert(edit, 0, rcontent)
				found+=1

			# ro = self.view.window().new_file()
			# ro.set_name('robots.txt')
			# ro.insert(edit, 0, robots_rules+rfile.group(1))

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
		sublime.message_dialog(logMsg)
