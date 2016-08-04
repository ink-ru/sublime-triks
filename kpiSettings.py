import sublime, sublime_plugin, re

class kpisettingsCommand(sublime_plugin.ApplicationCommand):

	def get_data(self, resource): # open external data file
		# resources = sublime.find_resources('unicode-characters.html')
		resources = sublime.find_resources(resource)
		content = sublime.load_resource(resources[0])
		return content

	def show_opanel(self, content): # output panel
		pt = sublime.active_window().get_output_panel("paneltest")
		pt.set_read_only(False)
		pt.insert(edit, pt.size(), str(content))
		sublime.active_window().run_command("show_panel", {"panel": "output.paneltest"})
		# sublime.active_window().active_view().show_popup(html, flags=1, location=1, max_width=860, max_height=640, on_navigate=self.on_choice_html, on_hide=self.on_hide_html)

	def run(self, param):
		# dregion = sublime.Region(0, self.view.size())

		logMsg = ''
		authstring = ''

		self.this_settings = 'kpi.sublime-settings'
		self.settings = sublime.load_settings(self.this_settings)


		args_dict = {
				'authstring': {'name':'authstring', 'hint':'login:password'},
				'vacation' : {'name':'my_id', 'hint':'количество пропущенных дней'}
		}

		try:
			self.param_name = str(args_dict[param]['name'])
			param_hint = str(args_dict[param]['hint'])
		except KeyError as e:
			mess = 'Несуществующий параметр: {}'.format(e.args[0])
			sublime.status_message(mess)
			sublime.message_dialog(mess)
			raise ValueError(mess)


		parametr = self.settings.get(self.param_name)
		parametr = parametr if (parametr is not None) and (len(parametr) > 0) else ""

		sublime.active_window().show_input_panel(param_hint, parametr, self.save_sett, None, None)

		if len(logMsg) > 6:
			sublime.status_message(logMsg)
			# sublime.message_dialog(logMsg)

	def save_sett(self, prmtr_val):
		if len(prmtr_val) > 0:
			self.settings.set(self.param_name, prmtr_val)
			sublime.save_settings(self.this_settings)
			sublime.status_message("Настройки сохранены")
			sublime.message_dialog("Настройки сохранены")
		else:
			sublime.status_message("Неверный формат ввода!!!")
			sublime.message_dialog("Неверный формат ввода!!!")
