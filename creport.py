import sublime, sublime_plugin, re, urllib
from .libs import *

class creportCommand(sublime_plugin.TextCommand):
		
	def run(self, edit, param):
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
			robots_rules = ''

			# get links disallowed by robots.txt
			if(param == 'robots'):
				rfile = re.search('(https?://[^/]+/)', content)
				robots_rules = xenuTools.getrobots(rfile.group(1)+'robots.txt')

			# shorten large link bloks
			content = re.sub(r":\s+((\thttp\S+\n){10})(\thttp\S+\n){1,}", r":\n\g<1>\tИ другие...\n", content)
			# content = re.sub(r":((\thttp\S+\n){1,10})\t(?s)(.*?)\n\n", r":\g<1>\tи др.\n\n", content)

			broken = re.search('(?s)('+BROKEN+'|'+BROKEN1+')(\n){2,}(.*?)'+TOP, content)
			if broken is not None:
				bcontent = broken.group(3)
				
				bcontent = re.sub(r"(\n){1,}\d+ broken link\(s\) reported\s*", "", bcontent)+"\n\n"
				# bcontent = re.sub(r"^https?:\S+\n.+\w: +((?!(400|401|403|404|410|429))|\d{4,})+(?s)(.*?)\n\n", "", bcontent, flags=re.MULTILINE)
				bcontent = re.sub(r"^https?:\S+\n(\w| )+code: +((?!(400|401|403|404|410|429))|\d{4,}).*:\n(\t\S+\n){1,}", "", bcontent, flags=re.MULTILINE)
				bcontent = bcontent.replace("error code", "код ошибки").replace("linked from page(s)", "найдено на страницах")
				if(param == 'robots' and len(robots_rules) > 26):
					bcontent = re.sub(robots_rules, "", bcontent, flags=re.MULTILINE)
				b = self.view.window().new_file()
				b.set_name('broken.log')
				b.insert(edit, 0, bcontent)
				found+=1

			redirects = re.search('(?s)'+REDIR+'(\n){2,}(.*?)'+TOP, content)
			#redirects = re.search('(?s)List of redirected URLs(\n){2,}(.*?)Return to Top', content)
			if redirects is not None:
				rcontent = redirects.group(2)+"\n\n"
				#rcontent = re.sub(r"^https?:\S+\nredirected.+\n.+code: +((?!(301|302|307|303))|\d{4,})+(?s)(.*?)\n\n", "", rcontent, flags=re.MULTILINE)
				rcontent = re.sub(r"^https?:\S+\nredirected.+\n.+code: +((?!(301|302|307|303))|\d{4,}).*\nlinked.*:\n(\t\S+\n){1,}\n*", "", rcontent, flags=re.MULTILINE)
				rcontent = rcontent.replace("redirected to", "перенаправляет на").replace("status code", "код ответа").replace("linked from page(s)", "найдено на страницах")
				if(param == 'robots' and len(robots_rules) > 26):
					rcontent = re.sub(robots_rules, "", rcontent, flags=re.MULTILINE)
				r = self.view.window().new_file()
				r.set_name('redirects.log')
				r.insert(edit, 0, rcontent)
				found+=1

			#if(param == 'debug'):
			#	ro = self.view.window().new_file()
			#	ro.set_name('robots.txt')
			#	ro.insert(edit, 0, robots_rules+rfile.group(1))

			# content = re.sub(r"(?s)(.*?)\n\n", "", content)
			# content = re.sub(r"Table (of) contents", r"+\1+", content)

			# self.view.replace(edit, dregion, content)

			if found > 0:
				logMsg += "Done!\n Предложения отправляйте на адрес y.vasin@demis.ru"
			else:
				logMsg += "Nothing found."
		else:
			logMsg += "Empty document!"

		sublime.status_message(logMsg)
		sublime.message_dialog(logMsg)
