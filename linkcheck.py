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

	# Check all links in view
	def check_links(self, view):
		# Find all URL's in the view
		url_regions = view.find_all ("https?://[^\"'\s]+")

		i = 0
		for region in url_regions:
			cl = view.substr(region)

			# URL regions in selection
			if len(view.sel()[0]) > 0:
				if view.sel().contains(region):
					code = self.get_response(cl)
					view.add_regions('url'+str(i), [region], "mark", "Packages/SeoTools/icons/"+str(code)+".png", flags=sublime.DRAW_NO_FILL|sublime.DRAW_NO_OUTLINE|sublime.DRAW_SOLID_UNDERLINE)
					i = i + 1
			else:
				if len(url_regions) > 200:
					return False

				code = self.get_response(cl)
				# Region is either in the selection or there is no selection
				view.add_regions('url'+str(i), [region], "mark", "Packages/SeoTools/icons/"+str(code)+".png", flags=sublime.DRAW_NO_FILL|sublime.DRAW_NO_OUTLINE|sublime.DRAW_SOLID_UNDERLINE)
				i = i + 1
		return i

	def run(self, edit):
		logMsg = ''
		total = 0

		if not self.view.is_read_only() or self.view.size() < 1:
			total = self.check_links(self.view)

			if total > 0:
				logMsg += "Done!"
			elif total == False:
				logMsg = 'Слишком много ссылок. Выделите нужный фрагмент.'
			else:
				logMsg += "Nothing found."
		else:
			logMsg += "Empty or readonly document!"

		sublime.status_message(logMsg)
		sublime.message_dialog(logMsg)
