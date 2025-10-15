from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.metrics import dp
from datetime import datetime

class SavedListScreen(Screen):
    def on_enter(self):
        self.load_saved_characters()

    def load_saved_characters(self):
        app = App.get_running_app()
        saved_chars = app.dm.get_saved_characters()
        layout = self.ids.saved_layout
        layout.clear_widgets()
        
        if not saved_chars:
            no_chars_label = Label(
                text='Нет сохраненных персонажей. Сначала выполните расчет и сохраните персонажа.',
                size_hint_y=None, height=dp(100), text_size=(None, None), halign='center'
            )
            layout.add_widget(no_chars_label)
            return
        
        for char in saved_chars:
            box = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
            
            created_date = datetime.fromisoformat(char['created_at'].replace('Z', '+00:00'))
            date_str = created_date.strftime("%d.%m.%Y %H:%M")
            char_info = f"{char['name']}\n(создан: {date_str})"
            
            char_btn = Button(text=char_info, size_hint_x=0.7, text_size=(None, None), halign='left', valign='middle')
            char_btn.char_data = char
            char_btn.bind(on_release=lambda instance: app.load_saved_character(instance.char_data))
            
            delete_btn = Button(text='Удалить', size_hint_x=0.3, background_color=(1, 0, 0, 1))
            delete_btn.char_id = char['id']
            delete_btn.bind(on_release=lambda instance: app.delete_character(instance.char_id))
            
            box.add_widget(char_btn)
            box.add_widget(delete_btn)
            layout.add_widget(box)