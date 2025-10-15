from kivy.uix.screenmanager import Screen
from kivy.app import App

class ResultScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        if hasattr(app, 'calculation_result'):
            result = app.calculation_result
            self.ids.result_label.text = f"Результат для {result['character']['name']}:"
            
            resources_text = "Нужно ресурсов:\n"
            for resource, data in result.get('resources_diff', {}).items():
                status = "Есть" if data['difference'] <= 0 else "Нет"
                resources_text += f"{status} {resource}: {data['needed']} (есть: {data['current']})"
                if data['difference'] > 0:
                    resources_text += f" - нужно еще: {data['difference']}"
                resources_text += "\n"
            
            self.ids.resources_label.text = resources_text