from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.metrics import dp

class CharacterSelectScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        characters = app.dm.get_characters()
        layout = self.ids.character_layout
        layout.clear_widgets()
        
        for char in characters:
            btn = Button(text=char['name'], size_hint_y=None, height=dp(50))
            btn.char_data = char
            btn.bind(on_release=lambda instance: app.select_character(instance.char_data))
            layout.add_widget(btn)