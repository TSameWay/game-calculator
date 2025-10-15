from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp
import json

class CharacterCompareScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_chars = {1: None, 2: None}

    def on_enter(self):
        self.selected_chars = {1: None, 2: None}
        self.ids.select_char1_btn.text = 'Выбрать 1-го персонажа'
        self.ids.select_char2_btn.text = 'Выбрать 2-го персонажа'
        self.ids.comparison_container.clear_widgets()

    def show_character_selection(self, slot):
        app = App.get_running_app()
        saved_chars = app.dm.get_saved_characters()
        
        if not saved_chars:
            self.show_popup('Нет данных', 'Нет сохраненных персонажей. Сначала сохраните персонажей в разделе "Мои персонажи".')
            return
        
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        spinner = Spinner(text='Выберите сохраненного персонажа', values=[char['name'] for char in saved_chars], size_hint_y=None, height=dp(50))
        
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        confirm_btn = Button(text='Выбрать')
        cancel_btn = Button(text='Отмена')
        
        def confirm_selection(instance):
            selected_name = spinner.text
            selected_char = next((char for char in saved_chars if char['name'] == selected_name), None)
            if selected_char:
                self.selected_chars[slot] = selected_char
                self.ids[f'select_char{slot}_btn'].text = selected_char['name']
            popup.dismiss()
        
        confirm_btn.bind(on_release=confirm_selection)
        cancel_btn.bind(on_release=lambda x: popup.dismiss())
        button_layout.add_widget(confirm_btn)
        button_layout.add_widget(cancel_btn)
        
        content.add_widget(spinner)
        content.add_widget(button_layout)
        
        popup = Popup(title=f'Выбор персонажа {slot}', content=content, size_hint=(0.8, 0.6))
        popup.open()

    def compare_characters(self):
        if not all(self.selected_chars.values()):
            self.show_popup('Ошибка', 'Выберите обоих персонажей для сравнения!')
            return
        
        layout = self.ids.comparison_container
        layout.clear_widgets()
        
        char1, char2 = self.selected_chars[1], self.selected_chars[2]
        
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        header.add_widget(Label(text=char1['name'], size_hint_x=0.5, font_size=dp(16)))
        header.add_widget(Label(text='Ресурсы', size_hint_x=0.2, font_size=dp(16)))
        header.add_widget(Label(text=char2['name'], size_hint_x=0.5, font_size=dp(16)))
        layout.add_widget(header)
        
        separator = Label(text='.' * 50, size_hint_y=None, height=dp(20), color=(0.5, 0.5, 0.5, 1))
        layout.add_widget(separator)
        
        char1_data = json.loads(char1['data'])
        char2_data = json.loads(char2['data'])
        
        total1 = sum(char1_data['resources'].values())
        total2 = sum(char2_data['resources'].values())
        
        total_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        color1 = (0, 1, 0, 1) if total1 < total2 else (1, 1, 1, 1)
        color2 = (0, 1, 0, 1) if total2 < total1 else (1, 1, 1, 1)
        
        total1_label = Label(text=str(total1), size_hint_x=0.5, color=color1)
        total_param_label = Label(text='Всего ресурсов', size_hint_x=0.2)
        total2_label = Label(text=str(total2), size_hint_x=0.5, color=color2)
        
        total_box.add_widget(total1_label)
        total_box.add_widget(total_param_label)
        total_box.add_widget(total2_label)
        layout.add_widget(total_box)
        
        all_resources = set(char1_data['resources'].keys()) | set(char2_data['resources'].keys())
        
        for resource in sorted(all_resources):
            amount1 = char1_data['resources'].get(resource, 0)
            amount2 = char2_data['resources'].get(resource, 0)
            
            if amount1 > 0 or amount2 > 0:
                resource_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(35))
                color1 = (0, 1, 0, 1) if amount1 < amount2 else (1, 1, 1, 1)
                color2 = (0, 1, 0, 1) if amount2 < amount1 else (1, 1, 1, 1)
                
                label1 = Label(text=str(amount1), size_hint_x=0.5, color=color1)
                label_param = Label(text=resource, size_hint_x=0.2)
                label2 = Label(text=str(amount2), size_hint_x=0.5, color=color2)
                
                resource_box.add_widget(label1)
                resource_box.add_widget(label_param)
                resource_box.add_widget(label2)
                layout.add_widget(resource_box)

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=message, text_size=(None, None), halign='center'))
        ok_btn = Button(text='OK', size_hint_y=None, height=dp(50))
        ok_btn.bind(on_release=lambda x: popup.dismiss())
        content.add_widget(ok_btn)
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.4))
        popup.open()