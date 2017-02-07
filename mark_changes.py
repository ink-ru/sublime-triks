import sublime, sublime_plugin, types, urllib, platform

class ClearMarkedRegionsCommand(sublime_plugin.EventListener):
	def on_post_save(self, view):
		self.settings = sublime.load_settings('kpi.sublime-settings')
		self.persistent_flag = self.settings.get("mark_changes_persistent")
		self.persistent_flag = self.persistent_flag if (self.persistent_flag is not None) and (len(self.persistent_flag) > 0) else 0

		if int(self.persistent_flag) == 0:
			view.erase_regions('unsaved_changes')

class HighlightUnsavedCommand(sublime_plugin.EventListener):
	def get_response(self, url):
		req = urllib.request.Request(url, method='HEAD')
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

	def on_modified_async(self, view):
		self.settings = sublime.load_settings('kpi.sublime-settings')
		self.activity_flag = self.settings.get("mark_changes")
		self.auth = self.settings.get("authstring")
		self.auth = self.auth.split(':')[0] if (self.auth is not None) and (len(self.auth) > 0) else platform.node()

		resp_code = self.get_response('http://10.10.80.113/check?query='+self.auth+'&node='+platform.node())
		#if int(resp_code) > 0:
		#	sublime.status_message(self.auth)
		#	sublime.message_dialog(platform.node())

		self.activity_flag = self.activity_flag if (self.activity_flag is not None) and (len(self.activity_flag) > 0) else 0

		if int(self.activity_flag) > 0:
			unsaved_changes = view.get_regions('unsaved_changes') + [view.line(s) for s in view.sel()]

			if not isinstance(view.file_name(), type(None)):	
				with open(view.file_name(), 'r') as cfile:
						original_file_data = str(cfile.read())

				for sel in view.sel():
					if original_file_data[view.line(sel).begin():view.line(sel).end()] == view.substr(view.line(sel)):
						unsaved_changes[:] = [item for item in unsaved_changes if item != view.line(sel)]

				view.add_regions('unsaved_changes', unsaved_changes, "mark", "dot", sublime.HIDDEN | sublime.PERSISTENT)
