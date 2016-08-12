import sublime, sublime_plugin
import re, urllib, random, json, collections, operator, math

if sublime.platform() == 'windows':
	import socket
	socket.setdefaulttimeout(10)
else:
	import signal

from .pcal import *
from .kpi_dicts import *

class kpiCommand(sublime_plugin.TextCommand):

	def get_auth_url(self, url, username, password):		
		data = urllib.parse.urlencode({'ldap-mail': username, 'ldap-pass': password, 'go': ' Войти '})
		data = data.encode('ascii') # data should be bytes
		request = urllib.request.Request(url, data)
		resorce = urllib.request.urlopen(request)
		html = resorce.read().decode("utf-8").strip()
		return html

	def lines_highlight(self,vspace):
		regions = vspace.find_all("(баллы\s+чистые|план\s+на\s+сегодня)[^:]*:")
		vspace.add_regions('important', regions, "mark")
		regions = vspace.find_all("премия[^:]+:")
		vspace.add_regions('inform', regions, "comment")
		return True

	def run(self, edit):
		if sublime.platform() == 'windows':
			socket.setdefaulttimeout(10)
		else:
			signal.signal(signal.SIGALRM, self.signal_handler) # execution time watcher

		logMsg = ''
		total = 0
		authstring = ''
		username = ''
		password = ''
		table = 'Demis KPI\n'

		# Reading settings
		self.this_settings = 'kpi.sublime-settings'
		self.settings = sublime.load_settings(self.this_settings)
		authstring = self.settings.get("authstring")
		my_id = self.settings.get("my_id")

		if authstring is not None:
			authstring = authstring.split(':')
			if len(authstring) >= 2:
				username = authstring[0]
				password = authstring[1]

		# Setting MAX execution time
		if sublime.platform() == 'linux':
			signal.alarm(10)

		try:
			content = self.get_auth_url(domain_url+smoke_uri, username, password)
			if content.find("Авторизация LDAP") > 0:
				sublime.message_dialog("Требуется авторизация, \nвведите учетные данные ниже. \nДля отмены нажмите ESC.")
				self.view.window().show_input_panel("login:password", '', self.save_sett, None, None)
			else:
				full_url = domain_url + api_uri + api_result_get
				rjson = self.get_auth_url(full_url, username, password)
				cdict = json.loads(rjson)

				full_url = domain_url + api_uri + api_employees_get
				rjson = self.get_auth_url(full_url, username, password)
				udict = json.loads(rjson)

				# sorting by groups
				users_ungrouped = {k : udict[k]['department_sys_name'] for k in cdict}
				users_grouped = collections.OrderedDict(sorted(users_ungrouped.items(), key=operator.itemgetter(1)))

				for record in users_grouped:
					# === RECORD grade_name ===
					grade = str(udict[record]['grade_name'])
					
					# разделитель строк
					if(grade.find('уководитель') > 0):
						table += ("{0}"*80).format( "━" ) + "\n"

					# === RECORD department_sys_name ===
					table += "{0:34}{1:30}{2}".format( str(udict[record]['name']), grade, str(udict[record]['department_sys_name']) ) + "\n"

					# keys modification
					cdict[record]['1_labor'] = cdict[record].pop("labor")
					lbr = float(cdict[record]['1_labor'])

					rslt = cdict[record]['2_result'] = cdict[record].pop("result")
						
					isues_amount = int(cdict[record]['issues_cnt'])
					vip_isues_amount = int(cdict[record]['labor_vip'])
					if vip_isues_amount > 0:
						isues_amount = isues_amount + vip_isues_amount

					avg_issue_index = float(rslt)/(isues_amount if isues_amount > 0 else 1)

					try:
						plan_rate = str(plan_rate_dict[udict[record]['grade_name']])
					except KeyError as e:
						plan_rate = 0
						# print ("Error: %s.\n" % str(e))

					if float(plan_rate) > 0:
						plan_per_day = float(plan_rate)/20
						real_plan = plan_per_day*int(pCal.working_days())
					else:
						plan_per_day = real_plan = 0

					daily_index = float(lbr)/pCal.working_days_passed()

					if lbr<150:
						fot = math.floor(lbr/25)*400
					elif lbr<350:
						fot = math.floor((lbr-150)/50)*2300+2100
					elif lbr>450:
						fot = 12000+(lbr-350)*25
					else:
						fot = 12000+math.sin((lbr-350)*0.0157)*2500
					
					cdict[record]['средний балл за задачу'] = avg_issue_index
					cdict[record]['план'] = float(real_plan)
					cdict[record]['порог амнистии'] = float( plan_per_day*int(pCal.working_days())*1.3 )
					cdict[record]['план на сегодня'] = float( plan_per_day*int(pCal.working_days_passed()) )
					cdict[record]['план амнистии на сегодня'] = float( plan_per_day*int(pCal.working_days_passed()*1.3) )
					cdict[record]['баллов в день'] = float(daily_index)
					cdict[record]['прогноз'] = float(daily_index*float(pCal.working_days()))
					cdict[record]['премия программиста (руб.)'] = round(fot)

					if (lbr == rslt) and (cdict[record]['idle_penalty'] > 0) and (float(rslt) < cdict[record]['порог амнистии']):
						cdict[record]['1_labor'] = lbr - cdict[record]['idle_penalty']

					od = collections.OrderedDict(sorted(cdict[record].items(), reverse=False))
					for r_feild in od:
						if not ( (cdict[record]['dept_issues_cnt'] == 0 and str(r_feild).find('dept_') >= 0) or (str(r_feild).find('_vip') >= 0 and int(cdict[record][r_feild]) == 0) ):
							try:
								param_name = str(result_rus_dict[r_feild])
							except KeyError as e:
								param_name = str(r_feild)
								# print ("Error: %s.\n" % str(e))
								# raise ValueError('Undefined unit: {}'.format(e.args[0]))

							param_name += ':'
							table += "\t{0:40}{1:.2f}".format(param_name, float(cdict[record][r_feild]))+"\n"

				if self.view.name() == 'Demis KPI' and (not self.view.is_read_only()):
					self.view.erase(edit, sublime.Region(0, self.view.size()))
					self.view.replace(edit, sublime.Region(0, self.view.size()), str(table))
					self.view.run_command('fold_all')
					self.view.sel().clear()
					self.lines_highlight(self.view)
				else:
					target_view = self.view.window().new_file()
					target_view.set_name('Demis KPI')
					target_view.insert(edit, 0, table)
					target_view.run_command('fold_all')
					target_view.sel().clear()
					self.lines_highlight(target_view)

				sublime.status_message("Раскройте нужный вам блок")

		except Exception as e: # urllib.error.URLError: <urlopen error timed out>
			sublime.status_message("Сервер не отвечает! Попробуйте позже."+str(e))
			sublime.message_dialog("Ошибка: "+str(e))
			print ("Error: %s.\n" % str(e))
		finally:
			# Reset MAX execution time
			if sublime.platform() == 'linux':
				signal.alarm(0)

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

	def signal_handler(signum, frame, e):
		raise Exception("Timed out!")
