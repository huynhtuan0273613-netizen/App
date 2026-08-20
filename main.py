# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.utils import platform
import os

KV = '''
<SBRTop>:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: 0.05, 0.05, 0.05, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(56)
        canvas.before:
            Color:
                rgba: 0.07, 0.58, 0.52, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [12]
        Label:
            text: 'SBR AUTO TYPER'
            bold: True
            color: 1,1,1,1
            font_size: '18sp'

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        spacing: dp(5)
        Button:
            text: 'Choose .txt file'
            on_release: app.open_file_chooser()
            background_color: 0.07, 0.58, 0.52, 1
        Label:
            text: root.loaded_file or 'No file selected'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            color: 1,1,1,1

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        Label:
            text: 'Rows per send:'
            size_hint_x: 0.5
            color: 1,1,1,1
        Spinner:
            id: rows
            text: str(root.rows_per_send)
            values: ['1','2','3','4','5']
            size_hint_x: 0.5
            on_text: root.rows_per_send = int(self.text)
            background_color: 0.07, 0.58, 0.52, 1

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        Label:
            text: 'Delay (ms):'
            size_hint_x: 0.6
            color: 1,1,1,1
        TextInput:
            id: delay
            text: str(root.delay_ms)
            input_filter: 'int'
            multiline: False
            size_hint_x: 0.4
            on_text: root.delay_ms = int(self.text) if self.text.isdigit() else root.delay_ms
            background_color: 0.2, 0.2, 0.2, 1
            foreground_color: 1,1,1,1

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        CheckBox:
            id: delay_chk
            active: root.delay_enabled
            on_active: root.delay_enabled = self.active
            color: 0.07, 0.58, 0.52, 1
        Label:
            text: 'Enable delay between sends'
            size_hint_x: 0.9
            color: 1,1,1,1

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        CheckBox:
            id: watermark_chk
            active: root.watermark_enabled
            on_active: root.watermark_enabled = self.active
            color: 0.07, 0.58, 0.52, 1
        TextInput:
            text: root.watermark_text
            on_text: root.watermark_text = self.text
            hint_text: 'Watermark text'
            background_color: 0.2, 0.2, 0.2, 1
            foreground_color: 1,1,1,1

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        spacing: dp(5)
        Button:
            text: 'Choose Wallpaper'
            on_release: app.open_image_picker()
            background_color: 0.07, 0.58, 0.52, 1
        Button:
            text: 'Use Gradient'
            on_release: app.toggle_gradient()
            background_color: 0.58, 0, 0.83, 1

    BoxLayout:
        size_hint_y: None
        height: dp(50)
        spacing: dp(5)
        Button:
            text: 'Start AutoType'
            on_release: app.start_autotype()
            background_color: 0, 0.8, 0, 1
            bold: True
        Button:
            text: 'Stop'
            on_release: app.stop_autotype()
            background_color: 0.8, 0, 0, 1
            bold: True

    Label:
        text: 'Preview (first 10 lines):'
        size_hint_y: None
        height: dp(26)
        color: 1,1,1,1
        halign: 'left'
        text_size: self.size
        padding: dp(5), 0
    
    ScrollView:
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        GridLayout:
            id: preview
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            row_default_height: dp(26)
            row_force_default: True
            padding: dp(5)
            spacing: dp(2)
'''

class SBRTop(BoxLayout):
    loaded_file = StringProperty('')
    rows_per_send = NumericProperty(1)
    delay_ms = NumericProperty(1000)
    delay_enabled = BooleanProperty(False)
    watermark_text = StringProperty('SBR RULEX')
    watermark_enabled = BooleanProperty(True)
    lines = ListProperty([])

class SBRApp(App):
    def build(self):
        Builder.load_string(KV)
        self.top = SBRTop()
        Clock.schedule_once(lambda dt: self.show_disclaimer(), 0.5)
        if platform == 'android':
            from android import activity
            activity.bind(on_activity_result=self.on_activity_result)
        return self.top
    
    def on_activity_result(self, request_code, result_code, intent):
        if request_code == 1234:
            if result_code == -1 and intent is not None:
                try:
                    from jnius import autoclass
                    Uri = autoclass('android.net.Uri')
                    ContentResolver = autoclass('android.content.ContentResolver')
                    BufferedReader = autoclass('java.io.BufferedReader')
                    InputStreamReader = autoclass('java.io.InputStreamReader')
                    
                    uri = intent.getData()
                    if uri:
                        PythonActivity = autoclass('org.kivy.android.PythonActivity')
                        activity = PythonActivity.mActivity
                        resolver = activity.getContentResolver()
                        input_stream = resolver.openInputStream(uri)
                        reader = BufferedReader(InputStreamReader(input_stream))
                        
                        lines = []
                        line = reader.readLine()
                        while line is not None:
                            if line.strip():
                                lines.append(line)
                            line = reader.readLine()
                        reader.close()
                        
                        self.top.lines = lines
                        self.top.loaded_file = "Selected file"
                        self.refresh_preview()
                except Exception as e:
                    self.show_error(f"Error reading file: {e}")

    def show_disclaimer(self):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(
            text="This keyboard is made only for fun purpose.\nJai Shree Ram Jai Bhavani🧡", 
            halign='center'
        ))
        btn = Button(text='I Agree', size_hint_y=None, height=40)
        box.add_widget(btn)
        popup = Popup(
            title='Disclaimer', 
            content=box, 
            size_hint=(0.9, 0.5), 
            auto_dismiss=False
        )
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def open_file_chooser(self):
        if platform != 'android':
            from kivy.uix.filechooser import FileChooserListView
            from kivy.uix.popup import Popup
            fc = FileChooserListView(path='.', filters=['*.txt'])
            popup = Popup(title='Choose .txt', content=fc, size_hint=(0.9, 0.9))
            def on_select(instance):
                if fc.selection:
                    popup.dismiss()
                    self.load_file(fc.selection[0])
            fc.bind(on_submit=lambda *_: on_select(None))
            popup.open()
            return

        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            activity = PythonActivity.mActivity
            intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.setType('text/plain')
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            activity.startActivityForResult(Intent.createChooser(intent, "Select Text File"), 1234)
        except Exception as e:
            self.show_error(f"Error opening file picker: {e}")

    def open_image_picker(self):
        if platform != 'android':
            from kivy.uix.filechooser import FileChooserListView
            from kivy.uix.popup import Popup
            fc = FileChooserListView(path='.', filters=['*.jpg', '*.png', '*.jpeg'])
            popup = Popup(title='Choose Wallpaper', content=fc, size_hint=(0.9, 0.9))
            popup.open()
            return

        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            activity = PythonActivity.mActivity
            intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.setType('image/*')
            activity.startActivityForResult(Intent.createChooser(intent, "Select Wallpaper"), 5678)
        except Exception as e:
            self.show_error(f"Error opening image picker: {e}")

    def toggle_gradient(self):
        from kivy.graphics import Color, Rectangle
        self.top.canvas.before.clear()
        with self.top.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=self.top.pos, size=self.top.size)
            Color(0.58, 0, 0.83, 0.3)
            Rectangle(pos=self.top.pos, size=self.top.size)

    def load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            lines = [ln for ln in text.splitlines() if ln.strip()]
            self.top.lines = lines
            self.top.loaded_file = os.path.basename(path)
            self.refresh_preview()
        except Exception as e:
            self.show_error(f'Error loading file: {e}')

    def refresh_preview(self):
        from kivy.uix.label import Label
        preview = self.top.ids.preview
        preview.clear_widgets()
        for i, ln in enumerate(self.top.lines[:10]):
            preview.add_widget(Label(
                text=f"{i+1}. {ln[:120]}", 
                size_hint_y=None, 
                height=26,
                color=(1, 1, 1, 1),
                halign='left',
                text_size=(None, None)
            ))

    def start_autotype(self):
        if not self.top.lines:
            self.show_error('Please load a .txt file first')
            return
        
        chunks = []
        r = int(self.top.rows_per_send)
        for i in range(0, len(self.top.lines), r):
            group = self.top.lines[i:i+r]
            text = "\n".join(group)
            if self.top.watermark_enabled and self.top.watermark_text.strip():
                text = text + " " + self.top.watermark_text
            chunks.append(text)
        payload = '\u241E'.join(chunks)

        if platform == 'android':
            try:
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                intent = Intent('com.sbr.autotyper.ACTION_START')
                intent.putExtra('payload', payload)
                intent.putExtra('rows', int(self.top.rows_per_send))
                intent.putExtra('delay_ms', int(self.top.delay_ms) if self.top.delay_enabled else 0)
                intent.putExtra('delay_enabled', bool(self.top.delay_enabled))
                activity.sendBroadcast(intent)
                self.show_info('AutoType started! Switch to target app.')
            except Exception as e:
                self.show_error(f'Error starting autotype: {e}')
        else:
            print('Start requested (non-android): would start typing')
            self.show_info('AutoType simulation (desktop mode)')

    def stop_autotype(self):
        if platform == 'android':
            try:
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                intent = Intent('com.sbr.autotyper.ACTION_STOP')
                activity.sendBroadcast(intent)
                self.show_info('AutoType stopped.')
            except Exception as e:
                self.show_error(f'Error stopping autotype: {e}')
        else:
            print('Stop requested')

    def show_error(self, message):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        popup = Popup(
            title='Error',
            content=Label(text=str(message)),
            size_hint=(0.8, 0.3)
        )
        popup.open()

    def show_info(self, message):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        popup = Popup(
            title='Info',
            content=Label(text=str(message)),
            size_hint=(0.8, 0.3)
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

if __name__ == '__main__':
    SBRApp().run()
