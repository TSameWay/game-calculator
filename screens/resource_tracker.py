from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.metrics import dp

class ResourceTrackerScreen(Screen):
    def on_enter(self):
        self.load_resources()

    def load_resources(self):
        app = App.get_running_app()
        resources = app.dm.get_player_resources()
        layout = self.ids.resources_container
        layout.clear_widgets()
        
        for resource_name, amount in sorted(resources.items()):
            resource_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
            
            resource_box.add_widget(Label(text=f"{resource_name}:", size_hint_x=0.5))
            
            amount_input = TextInput(text=str(amount), size_hint_x=0.3, multiline=False)
            amount_input.resource_name = resource_name
            resource_box.add_widget(amount_input)
            
            update_btn = Button(text='Обновить', size_hint_x=0.2)
            update_btn.resource_input = amount_input
            update_btn.bind(on_release=self.update_single_resource)
            resource_box.add_widget(update_btn)
            
            layout.add_widget(resource_box)

    def update_single_resource(self, instance):
        try:
            resource_name = instance.resource_input.resource_name
            new_amount = int(instance.resource_input.text)
            app = App.get_running_app()
            app.dm.update_resource(resource_name, new_amount)
        except ValueError:
            pass

    def update_all_resources(self):
        app = App.get_running_app()
        layout = self.ids.resources_container
        
        for child in layout.children:
            for widget in child.children:
                if isinstance(widget, TextInput):
                    try:
                        resource_name = getattr(widget, 'resource_name', None)
                        if resource_name:
                            new_amount = int(widget.text)
                            app.dm.update_resource(resource_name, new_amount)
                    except ValueError:
                        pass