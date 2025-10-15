from kivy.app import App
from kivy.lang import Builder
from data_manager import DataManager

class MyApp(App):
    def build(self):
        self.dm = DataManager()
        return Builder.load_file('interface.kv')
    
    def select_character(self, character):
        self.selected_character = character
        if hasattr(self, 'calculation_result'):
            delattr(self, 'calculation_result')
        self.root.current = 'calculator'
    
    def save_result(self):
        if hasattr(self, 'calculation_result'):
            save_data = {
                'character_id': self.calculation_result['character']['id'],
                'name': self.calculation_result['character']['name'],
                'data': self.calculation_result
            }
            self.dm.save_character(save_data)
    
    def load_saved_character(self, char_data):
        import json
        self.calculation_result = json.loads(char_data['data'])
        self.root.current = 'result'
    
    def delete_character(self, char_id):
        self.dm.delete_character(char_id)
        saved_screen = self.root.get_screen('saved')
        saved_screen.load_saved_characters()

if __name__ == '__main__':
    MyApp().run()