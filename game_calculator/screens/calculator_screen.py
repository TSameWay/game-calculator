from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.app import App
from kivy.metrics import dp
from calculator import CalculatorTabbedPanel

class CalculatorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calculator = None
    
    def on_enter(self):
        app = App.get_running_app()
        if hasattr(app, 'selected_character'):
            self.ids.character_name.text = f"Расчет для: {app.selected_character['name']}"
            
            if self.calculator is None:
                self.calculator = CalculatorTabbedPanel()
                self.ids.calculator_container.add_widget(self.calculator)
            
            self.show_current_resources()
    
    def on_leave(self):
        if self.calculator:
            self.calculator.reset_all_values()
    
    def show_current_resources(self):
        app = App.get_running_app()
        resources = app.dm.get_player_resources()
        resources_text = "Ваши текущие ресурсы:\n"
        
        for resource, amount in sorted(resources.items()):
            if amount > 0:
                resources_text += f"{resource}: {amount}\n"
        
        if not hasattr(self, 'resources_label'):
            self.resources_label = Label(text=resources_text, size_hint_y=None, height=dp(100), text_size=(None, None))
            self.ids.calculator_container.add_widget(self.resources_label)
        else:
            self.resources_label.text = resources_text
    
    def calculate_total(self):
        if self.calculator:
            resources = self.calculator.calculate_total()
            app = App.get_running_app()
            player_resources = app.dm.get_player_resources()
            
            resources_diff = {}
            for resource, needed in resources.items():
                current = player_resources.get(resource, 0)
                difference = needed - current
                resources_diff[resource] = {
                    'needed': needed, 'current': current, 'difference': difference
                }
            
            app.calculation_result = {
                'character': app.selected_character, 'resources': resources,
                'resources_diff': resources_diff, 'player_resources': player_resources
            }
            
            self.calculator.reset_all_values()
            app.root.current = 'result'