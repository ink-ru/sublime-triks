# coding: utf-8

'''Библиотеки SEO модуля'''

import sublime, sublime_plugin, re, urllib

class xenuTools:

	def download_url_to_string(url):
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		html = response.read()
		return html

	def getrobots(url):
		#TODO: split single line files
		robots_rules = ''

		robots = xenuTools.download_url_to_string(url)
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
