import sublime
import sublime_plugin
import re
import json


CONFIG_FILE_PATH = 'Packages/selective-uppercase/keywords.json'
word_match = re.compile(r"(\W|\w+)")


class SelectiveUppercaseCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        window = sublime.active_window()
        view = window.active_view()
        sel = view.sel()
        self.keywords_list = json.loads(
            sublime.load_resource(CONFIG_FILE_PATH))['list']
        for region in sel:
            self.convert_one_by_one(edit, region)

    def convert_one_by_one(self, edit, region):
        begin = region.begin()
        end = region.end()
        lines = self.view.substr(region).split('\n')
        for line_index, line in enumerate(lines):
            words = word_match.findall(line)
            for word_index, word in enumerate(words):
                if self.is_keyword(word):
                    words[word_index] = word.upper()
            lines[line_index] = ''.join(words)
        self.view.replace(edit, region, '\n'.join(lines))

    def is_keyword(self, word):
        return word.upper() in self.keywords_list or word.lower() in self.keywords_list
