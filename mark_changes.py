import sublime, sublime_plugin, types


this_settings = 'kpi.sublime-settings'
settings = sublime.load_settings(this_settings)

activity_flag = settings.get("mark_changes")
activity_flag = activity_flag if (activity_flag is not None) and (len(activity_flag) > 0) else 0

if activity_flag:

	class ClearMarkedRegionsCommand(sublime_plugin.EventListener):
		def on_post_save(self, view):
			view.erase_regions('unsaved_changes')

	class HighlightUnsavedCommand(sublime_plugin.EventListener):
		def on_modified(self, view):
			
			unsaved_changes = view.get_regions('unsaved_changes') + [view.line(s) for s in view.sel()]

			if not isinstance(view.file_name(), type(None)):	
				with open(view.file_name(), 'r') as cfile:
						original_file_data = str(cfile.read())

				for sel in view.sel():
					if original_file_data[view.line(sel).begin():view.line(sel).end()] == view.substr(view.line(sel)):
						unsaved_changes[:] = [item for item in unsaved_changes if item != view.line(sel)]

				view.add_regions('unsaved_changes', unsaved_changes, "mark", "dot", sublime.HIDDEN | sublime.PERSISTENT)
