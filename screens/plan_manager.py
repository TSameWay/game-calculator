from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp
import json

class PlanManagerScreen(Screen):
    def on_enter(self):
        self.load_plans()

    def load_plans(self):
        app = App.get_running_app()
        plans = app.dm.get_character_plans()
        layout = self.ids.plans_container
        layout.clear_widgets()
        
        if not plans:
            no_plans_label = Label(
                text='Планы еще не созданы. Создайте план из сохраненного персонажа.',
                size_hint_y=None, height=dp(100), text_size=(None, None), halign='center'
            )
            layout.add_widget(no_plans_label)
            return
        
        for plan in plans:
            plan_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), spacing=dp(5))
            
            header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
            header.add_widget(Label(text=f"{plan['character_name']} - {plan['plan_name']}", size_hint_x=0.7, text_size=(None, None)))
            
            delete_btn = Button(text='Удалить', size_hint_x=0.3, background_color=(1, 0, 0, 1))
            delete_btn.plan_id = plan['id']
            delete_btn.bind(on_release=self.delete_plan)
            header.add_widget(delete_btn)
            plan_box.add_widget(header)
            
            resources_text = "Ресурсы:\n"
            for resource, amount in plan['resources_needed'].items():
                resources_text += f"{resource}: {amount}\n"
            
            resources_label = Label(text=resources_text, size_hint_y=None, height=dp(80), text_size=(None, None))
            plan_box.add_widget(resources_label)
            layout.add_widget(plan_box)

    def show_plan_creation(self):
        app = App.get_running_app()
        saved_chars = app.dm.get_saved_characters()
        
        if not saved_chars:
            self.show_popup('Нет данных', 'Нет сохраненных персонажей. Сначала сохраните персонажа в разделе "Мои персонажи".')
            return
        
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        char_spinner = Spinner(text='Выберите сохраненного персонажа', values=[char['name'] for char in saved_chars], size_hint_y=None, height=dp(50))
        plan_name_input = TextInput(hint_text='Название плана', size_hint_y=None, height=dp(50))
        
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        create_btn = Button(text='Создать план')
        cancel_btn = Button(text='Отмена')
        
        def create_plan(instance):
            selected_name = char_spinner.text
            plan_name = plan_name_input.text.strip() or f"План {selected_name}"
            selected_char = next((char for char in saved_chars if char['name'] == selected_name), None)
            
            if selected_char:
                char_data = json.loads(selected_char['data'])
                resources = char_data['resources']
                app.dm.save_character_plan(selected_char['character_id'], plan_name, resources)
                self.load_plans()
                popup.dismiss()
                self.show_popup('Успех', 'План успешно создан!')
        
        create_btn.bind(on_release=create_plan)
        cancel_btn.bind(on_release=lambda x: popup.dismiss())
        button_layout.add_widget(create_btn)
        button_layout.add_widget(cancel_btn)
        
        content.add_widget(Label(text='Сохраненный персонаж:'))
        content.add_widget(char_spinner)
        content.add_widget(Label(text='Название плана:'))
        content.add_widget(plan_name_input)
        content.add_widget(button_layout)
        
        popup = Popup(title='Создание плана из сохраненного персонажа', content=content, size_hint=(0.9, 0.7))
        popup.open()

    def delete_plan(self, instance):
        app = App.get_running_app()
        app.dm.delete_plan(instance.plan_id)
        self.load_plans()

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=message))
        ok_btn = Button(text='OK', size_hint_y=None, height=dp(50))
        ok_btn.bind(on_release=lambda x: popup.dismiss())
        content.add_widget(ok_btn)
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        popup.open()