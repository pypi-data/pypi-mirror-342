import sys
import urwid
import re

class SmartEdit(urwid.Edit):
    def keypress(self, size, key):
        if key == 'enter':
            self.insert_smart_indent()
            return
        elif key == 'tab':
            self.insert_tab()
            return
        return super().keypress(size, key)

    def insert_smart_indent(self):
        text = self.edit_text
        pos = self.edit_pos
        lines = text[:pos].splitlines()
        current_line = lines[-1] if lines else ""
        indent = re.match(r'\s*', current_line).group()
        stripped = current_line.strip()

        increase_indent_keywords = ('def', 'class', 'if', 'for', 'while', 'with', 'try')
        dedent_keywords = ('else', 'elif', 'except', 'finally')

        new_indent = indent
        if stripped.endswith(":") or any(stripped.startswith(k) and stripped.endswith(":") for k in increase_indent_keywords):
            new_indent += "    "
        elif any(stripped.startswith(k + ":") for k in dedent_keywords):
            new_indent = indent[:-4] if len(indent) >= 4 else ""

        newline = "\n" + new_indent
        self.edit_text = text[:pos] + newline + text[pos:]
        self.edit_pos = pos + len(newline)

    def insert_tab(self):
        text = self.edit_text
        pos = self.edit_pos
        self.edit_text = text[:pos] + "    " + text[pos:]
        self.edit_pos = pos + 4

class SaveDialog(urwid.WidgetWrap):
    def __init__(self, editor, callback):
        self.editor = editor
        self.callback = callback
        self.filename_edit = urwid.Edit(edit_text=editor.filename or "")
        pile = urwid.Pile([
            urwid.Text("Save changes to file?"),
            urwid.Divider(),
            urwid.Text("File name:"),
            self.filename_edit,
            urwid.Divider(),
            urwid.GridFlow([
                urwid.Button("Save", on_press=self.save),
                urwid.Button("Don't Save", on_press=self.dont_save),
                urwid.Button("Cancel", on_press=self.cancel),
            ], cell_width=14, h_sep=1, v_sep=1, align='center')
        ])
        super().__init__(urwid.LineBox(urwid.Filler(pile, valign='top')))

    def save(self, button=None):
        self.editor.filename = self.filename_edit.edit_text
        self.editor.save_file()
        self.callback("save")

    def dont_save(self, button=None):
        self.callback("dont_save")

    def cancel(self, button=None):
        self.callback("cancel")

class PyCodaEditor:
    def __init__(self, filename=None):
        self.filename = filename
        self.edit_widget = SmartEdit(multiline=True, wrap='clip')
        self.save_dialog = None

        self.header_title = urwid.Text("PyCoda", align='center')
        self.menu_bar = urwid.Text("[Ctrl+X] Save and Exit", align='center')

        self.header = urwid.Pile([
            urwid.AttrWrap(self.header_title, 'header'),
            urwid.AttrWrap(self.menu_bar, 'menu')
        ])

        self.theme = [
            ('header', 'white', 'dark gray'),
            ('menu', 'light magenta', 'dark gray'),
            ('body', 'light magenta', 'black'),
            ('dialog', 'white', 'black'),
            ('button', 'light gray', 'dark magenta'),
            ('focus button', 'black', 'light cyan')
        ]

        self.editor_widget = urwid.Filler(urwid.AttrMap(self.edit_widget, 'body'), valign='top', top=1)

        self.layout = urwid.Frame(
            header=self.header,
            body=self.editor_widget
        )

        self.loop = urwid.MainLoop(
            self.layout,
            palette=self.theme,
            unhandled_input=self.handle_input
        )

    def handle_input(self, key):
        if key == 'ctrl x':
            if self.save_dialog:
                return
            self.exit_editor()
        elif key == 'ctrl o':
            if not self.save_dialog:
                self.show_save_dialog()
        elif key == 'esc' and self.save_dialog:
            self.remove_dialog()

    def exit_editor(self):
        if self.edit_widget.edit_text != self.original_text:
            self.show_save_dialog(exit_after=True)
        else:
            raise urwid.ExitMainLoop()

    def show_save_dialog(self, exit_after=False):
        def callback(result):
            self.remove_dialog()
            if result == "save":
                if exit_after:
                    raise urwid.ExitMainLoop()
            elif result == "dont_save":
                if exit_after:
                    raise urwid.ExitMainLoop()

        self.save_dialog = SaveDialog(self, callback)
        overlay = urwid.Overlay(
            urwid.AttrMap(self.save_dialog, 'dialog'),
            self.editor_widget,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50)
        )
        self.layout.body = overlay

    def remove_dialog(self):
        self.save_dialog = None
        self.layout.body = self.editor_widget

    def prompt_open_file(self):
        try:
            if self.filename:
                with open(self.filename, 'r') as f:
                    self.edit_widget.edit_text = f.read()
            else:
                self.edit_widget.edit_text = ""
        except FileNotFoundError:
            self.edit_widget.edit_text = "# File not found.\n"
        self.original_text = self.edit_widget.edit_text

    def save_file(self):
        if not self.filename:
            return False
        try:
            with open(self.filename, 'w') as f:
                f.write(self.edit_widget.edit_text)
            self.original_text = self.edit_widget.edit_text
            return True
        except Exception as e:
            self.edit_widget.edit_text += f"\n# Error saving file: {e}"
            return False

    def run(self):
        self.prompt_open_file()
        self.loop.run()

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    PyCodaEditor(filename).run()

if __name__ == "__main__":
    main()
