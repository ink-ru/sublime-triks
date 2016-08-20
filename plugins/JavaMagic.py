import sublime, sublime_plugin

class javamagicCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		snippet_code = ''' public void set$TM_SELECTED_PART1($TM_SELECTED_PART1 $TM_SELECTED_PART2) {
	  this.$TM_SELECTED_PART1 = $TM_SELECTED_PART1;
	}'''
		new_content = ''

		for selection in self.view.sel():
			selection_content = self.view.substr(selection)
			if selection_content.find('.') > 0:
				parts = selection_content.split('.')
				new_content = snippet_code.replace('$TM_SELECTED_PART1', parts[0])
				new_content = new_content.replace('$TM_SELECTED_PART2', parts[1])
				self.view.insert(edit, selection.begin(), new_content)
			else:
				sublime.status_message('wrong selection') # statusline message
				# sublime.message_dialog('wrong selection') # popup message

		for selection in self.view.sel():
			self.view.erase(edit, selection)

		print('done') # debug output to console

