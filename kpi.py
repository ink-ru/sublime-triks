import sublime, sublime_plugin, re, urllib, random, json, collections, socket

class kpiCommand(sublime_plugin.TextCommand):

	def parse_url(self, url):
		request = urllib.request.Request(url)
		# request.add_header('Referer', 'https://www.google.ru/?q='+self.randomword(5))
		# request.add_header = ('User-agent', 'Googlebot/2.1 (+http://www.google.com/bot.html)')
		# urllib.request.urlcleanup()
		resorce = urllib.request.urlopen(request)
		html = resorce.read().decode("utf-8").strip()
		return html

	def auth(self, url, username, password):		
		data = urllib.parse.urlencode({'ldap-mail': username, 'ldap-pass': password, 'go': ' Войти '})
		data = data.encode('ascii') # data should be bytes
		request = urllib.request.Request(url, data)
		resorce = urllib.request.urlopen(request)
		html = resorce.read().decode("utf-8").strip()
		return html

	def get_data(self, resource):
		# resources = sublime.find_resources('unicode-characters.html')
		resources = sublime.find_resources(resource)
		content = sublime.load_resource(resources[0])
		return content

	def get_content(self, url):
		content = self.parse_url(url)
		# content_list = content.decode("utf-8").strip().splitlines()
		content= content.decode("utf-8").strip()
		return content

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

	def show_opanel(self, content):
		pt = sublime.active_window().get_output_panel("paneltest")
		pt.set_read_only(False)
		pt.insert(edit, pt.size(), str(content))
		sublime.active_window().run_command("show_panel", {"panel": "output.paneltest"})
		# sublime.active_window().active_view().show_popup(html, flags=1, location=1, max_width=860, max_height=640, on_navigate=self.on_choice_html, on_hide=self.on_hide_html)

	def run(self, edit):
		socket.setdefaulttimeout(10)
		dregion = sublime.Region(0, self.view.size())		
		self.view.replace(edit, dregion, '') # clear screen

		logMsg = ''
		total = 0
		authstring = ''
		username = ''
		password = ''
		table = ''

		domain_url = "http://otp.demis.ru"
		api_uri = "/smoke/oto/uto-kpi-api.php"
		kpi_uri = "/smoke/oto/uto-kpi-tmp.php"
		smoke_uri = "/smoke/"
		api_employees_get = "?action=users&da-rest=json"
		api_result_get = "?action=result&da-rest=json"

		self.this_settings = 'kpi.sublime-settings'
		self.settings = sublime.load_settings(self.this_settings)
		authstring = self.settings.get("authstring")

		if authstring is not None:
			authstring = authstring.split(':')
			if len(authstring) >= 2:
				username = authstring[0]
				password = authstring[1]

		try:
			content = self.auth(domain_url+smoke_uri, username, password)
			if content.find("Авторизация LDAP") > 0:
				sublime.message_dialog("Требуется авторизация, \nвведите учетные данные ниже. \nДля отмены нажмите ESC.")
				self.view.window().show_input_panel("login:password", '', self.save_sett, None, None)
			else:
				full_url = domain_url + api_uri + api_result_get
				rjson = self.auth(full_url, username, password)
				cdict = json.loads(rjson)

				full_url = domain_url + api_uri + api_employees_get
				rjson = self.auth(full_url, username, password)
				udict = json.loads(rjson)

				result_rus_dict = {
				'intime': 'задач в срок',
				'overdue_cnt':'просроченно задач',
				'dept_intime':'подразделение - в срок',
				'result':'баллы грязные',
				'dept_labor':'подразделение - баллы чистые',
				'dept_result':'подразделение - баллы грязные',
				'dept_issues_cnt':'подразделение - всего задач',
				'idle_penalty':'штраф за провис',
				'intime_perc':'процент в срок',
				'dept_idle_penalty':'подразделение - штраф за провис',
				'issues_cnt':'всего задач',
				'labor':'баллы чистые',
				'dept_labor_vip':'подразделение - VIP',
				'dept_overdue_cnt':'подразделение - просроченно задач',
				'dept_intime_perc':'подразделение - процент в срок',
				'labor_vip':'VIP',
				# '':'',
				}

				for record in cdict:
					table += str(udict[record]['name'])+"\n"
					# cdict[record]['avg_result'] = cdict[record]['result']/cdict[record]['issues_cnt']
					od = collections.OrderedDict(sorted(cdict[record].items(), reverse=True))
					for r_feild in od:
						if not ( (cdict[record]['dept_issues_cnt'] == 0 and str(r_feild).find('dept_') >= 0) or (str(r_feild).find('_vip') >= 0 and int(cdict[record][r_feild]) == 0) ):
							try:
								param_name = str(result_rus_dict[r_feild])
							except KeyError as e:
								param_name = str(r_feild)
								# raise ValueError('Undefined unit: {}'.format(e.args[0]))

							param_name += ':'
							table += "\t{0:40}{1}".format(param_name, str(cdict[record][r_feild]))+"\n"
							# table += "\t{0:40}{:.2f}".format( param_name, str(cdict[record][r_feild]))+"\n"

					# table += "\t{0:40}{1}".format('Средний балл', str( cdict[record]['result']/cdict[record]['issues_cnt'] ) ) + "\n"

					r = float(cdict[record]['result'])
					c = int(cdict[record]['issues_cnt'])
					c = c if c > 0 else 1
					a = r/c
					table += "\t{0:40}{1}".format('Средний балл', str( a ) ) + "\n"

				if not self.view.is_read_only():
					self.view.replace(edit, dregion, str(table))
					self.view.run_command('fold_all')
					sublime.status_message("Раскройте нужный вам блок")

				else:
					logMsg += "Readonly document!"
		finally:
			logMsg += "Done!"
		# except Exception as e: # urllib.error.URLError: <urlopen error timed out>
		# 	sublime.status_message("Сервер не отвечает! Попробуйте позже."+str(e))
		# 	sublime.message_dialog("Ошибка: "+str(e))

		if len(logMsg) > 6:
			sublime.status_message(logMsg)
			# sublime.message_dialog(logMsg)

	def save_sett(self, authstring):
		if authstring.find(':') > 0:
			self.settings.set("authstring", authstring)
			sublime.save_settings(self.this_settings)
			sublime.status_message("Настройки сохранены")
			self.view.run_command('kpi')
		else:
			sublime.status_message("Вы забыли ввести разделитель!!!")
