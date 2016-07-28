import sublime, sublime_plugin, re, urllib, random

class linkcheckCommand(sublime_plugin.TextCommand):

	def parse_url(self, url):
		request = urllib.request.Request(url)
		# request.add_header('Referer', 'https://www.google.ru/?q='+self.randomword(5))
		# request.add_header = ('User-agent', 'Googlebot/2.1 (+http://www.google.com/bot.html)')
		# urllib.request.urlcleanup()
		resorce = urllib.request.urlopen(request)
		html = resorce.read()
		return html

	def get_content(self, url):
		content = self.parse_url(url)[0]
		content_list = content.decode("utf-8").strip().splitlines()
		return content_list

	def get_response(self, url):
		req = urllib.request.Request(url)
		try:
			response = urllib.request.urlopen(req)
		except urllib.error.URLError as e:
			# print(e.reason)
			if hasattr(e, 'code'):
				return e.code
			else:
				return 0
		else:
			return 200

	def randomword(self, length):
		string = 'abcdefghijklmnopqrstuvwxyz'
		return ''.join(random.choice(string) for i in range(length))

	def chk_links(self,vspace):
		url_regions = vspace.find_all("https?://[^\"'\s]+")

		i=0
		for region in url_regions:
			cl = vspace.substr(region)
			code = self.get_response(cl)
			vspace.add_regions('url'+str(i), [region], "mark", "Packages/SeoTools/icons/"+str(code)+".png")
			i = i+1
		return i

	def run(self, edit):
		logMsg = ''
		total = 0

		if not self.view.is_read_only():
			if self.view.size():
				if len(self.view.sel()[0]) > 0:
					# DUMMY: not working yet
					# for sel_region in self.view.sel():
					# 	total = total + self.chk_links(sel_region)

					total = self.chk_links(self.view)
					
				else:
					total = self.chk_links(self.view)

					if total > 0:
						logMsg += "Done!"
					else:
						logMsg += "Nothing found."
			else:
				logMsg += "Empty document!"
		else:
			logMsg += "Read only document!"

		sublime.status_message(logMsg)
		sublime.message_dialog(logMsg)

