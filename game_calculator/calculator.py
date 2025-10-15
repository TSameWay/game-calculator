from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.metrics import dp
from collections import defaultdict
import re

class CalculatorTabbedPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        
        self.agent_tab = AgentLevelTab()
        self.core_tab = CoreSkillsTab()
        self.talent_tab = TalentTab()
        
        self.add_widget(TabbedPanelItem(text='Уровень агента', content=self.agent_tab))
        self.add_widget(TabbedPanelItem(text='Основные навыки', content=self.core_tab))
        self.add_widget(TabbedPanelItem(text='Таланты', content=self.talent_tab))

    def calculate_total(self):
        total_resources = defaultdict(int)
        
        agent_resources = self.agent_tab.get_current_resources()
        for resource, amount in agent_resources.items():
            total_resources[resource] += amount
        
        core_resources = self.core_tab.get_current_resources()
        for resource, amount in core_resources.items():
            total_resources[resource] += amount
        
        talent_resources = self.talent_tab.get_all_talents_resources()
        for resource, amount in talent_resources.items():
            total_resources[resource] += amount
        
        return dict(total_resources)

    def reset_all_values(self):
        self.agent_tab.reset_values()
        self.core_tab.reset_values()
        self.talent_tab.reset_values()

class AgentLevelTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        self.current_resources = {}
        
        self.add_widget(Label(text='Калькулятор уровня агента', size_hint_y=None, height=dp(40), font_size='20sp'))
        
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        input_layout.add_widget(Label(text='Текущий уровень:'))
        
        self.current_spinner = Spinner(text='1', values=('1', '10', '20', '30', '40', '50'))
        input_layout.add_widget(self.current_spinner)
        
        input_layout.add_widget(Label(text='Целевой уровень:'))
        self.target_spinner = Spinner(text='10', values=('10', '20', '30', '40', '50', '60'))
        input_layout.add_widget(self.target_spinner)
        
        calculate_btn = Button(text='Рассчитать', size_hint_x=None, width=dp(100))
        calculate_btn.bind(on_press=self.calculate)
        input_layout.add_widget(calculate_btn)
        self.add_widget(input_layout)
        
        self.results_label = Label(text='Выберите уровни и нажмите Рассчитать', size_hint_y=None, height=dp(200))
        self.add_widget(self.results_label)
    
    def calculate(self, instance):
        current = int(self.current_spinner.text)
        target = int(self.target_spinner.text)
        
        level_data = {
            (1, 10): "Senior Investigator Log: 2; Basic Support Certification Seal: 4; Dennies: 24000",
            (1, 20): "Senior Investigator Log: 10; Basic Support Certification Seal: 4; Advanced Support Certification Seal: 12; Dennies: 80000",
            (1, 30): "Senior Investigator Log: 30; Basic Support Certification Seal: 4; Advanced Support Certification Seal: 32; Dennies: 200000",
            (1, 40): "Senior Investigator Log: 75; Basic Support Certification Seal: 4; Advanced Support Certification Seal: 32; Ruler Certification Seal: 10; Dennies: 400000",
            (1, 50): "Senior Investigator Log: 150; Basic Support Certification Seal: 4; Advanced Support Certification Seal: 32; Ruler Certification Seal: 30; Dennies: 800000",
            (1, 60): "Senior Investigator Log: 300; Basic Support Certification Seal: 4; Advanced Support Certification Seal: 32; Ruler Certification Seal: 30; Dennies: 800000"
        }
        
        result_str = level_data.get((current, target), "Комбинация не найдена")
        self.results_label.text = f"Ресурсы для перехода с уровня {current} на {target}:\n\n{result_str}"
        self.current_resources = self.parse_resources(result_str)
    
    def parse_resources(self, resource_string):
        pattern = r'([A-Za-z\s]+):\s*(\d+)'
        return {name.strip(): int(amount) for name, amount in re.findall(pattern, resource_string)}
    
    def get_current_resources(self):
        return self.current_resources
    
    def reset_values(self):
        self.current_spinner.text = '1'
        self.target_spinner.text = '10'
        self.results_label.text = 'Выберите уровни и нажмите Рассчитать'
        self.current_resources = {}

class CoreSkillsTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        self.current_resources = {}
        
        self.add_widget(Label(text='Калькулятор основных навыков', size_hint_y=None, height=dp(40), font_size='20sp'))
        
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        input_layout.add_widget(Label(text='Целевой уровень:'))
        
        self.target_spinner = Spinner(text='A', values=('A', 'B', 'C', 'D', 'E', 'F'))
        input_layout.add_widget(self.target_spinner)
        
        calculate_btn = Button(text='Рассчитать', size_hint_x=None, width=dp(100))
        calculate_btn.bind(on_press=self.calculate)
        input_layout.add_widget(calculate_btn)
        self.add_widget(input_layout)
        
        self.results_label = Label(text='Выберите целевой уровень и нажмите Рассчитать', size_hint_y=None, height=dp(150))
        self.add_widget(self.results_label)
    
    def calculate(self, instance):
        target = self.target_spinner.text
        skills_data = {
            'A': "Dennies: 5000", 'B': "Purple boss material: 2; Dennies: 17000",
            'C': "Purple boss material: 6; Dennies: 45000", 'D': "Gold boss material: 2; Purple boss material: 15; Dennies: 105000",
            'E': "Gold boss material: 5; Purple boss material: 30; Dennies: 205000", 'F': "Gold boss material: 9; Purple boss material: 60; Dennies: 405000"
        }
        
        result_str = skills_data.get(target, "Уровень не найден")
        self.results_label.text = f"Ресурсы для уровня {target}:\n\n{result_str}"
        self.current_resources = self.parse_resources(result_str)
    
    def parse_resources(self, resource_string):
        pattern = r'([A-Za-z\s]+):\s*(\d+)'
        return {name.strip(): int(amount) for name, amount in re.findall(pattern, resource_string)}
    
    def get_current_resources(self):
        return self.current_resources
    
    def reset_values(self):
        self.target_spinner.text = 'A'
        self.results_label.text = 'Выберите целевой уровень и нажмите Рассчитать'
        self.current_resources = {}

class TalentTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        self.added_talents = {}
        self.current_talent_resources = {}
        
        self.add_widget(Label(text='Калькулятор талантов', size_hint_y=None, height=dp(40), font_size='20sp'))
        
        talent_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        talent_layout.add_widget(Label(text='Талант:'))
        self.talent_spinner = Spinner(text='Базовая атака', values=('Базовая атака', 'Уклонение', 'Помощь', 'Особая атака', 'Цепная атака + Ультимейт'))
        talent_layout.add_widget(self.talent_spinner)
        self.add_widget(talent_layout)
        
        level_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        level_layout.add_widget(Label(text='Текущий уровень:'))
        self.current_spinner = Spinner(text='1', values=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'))
        level_layout.add_widget(self.current_spinner)
        
        level_layout.add_widget(Label(text='Целевой уровень:'))
        self.target_spinner = Spinner(text='2', values=('2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
        level_layout.add_widget(self.target_spinner)
        
        calculate_btn = Button(text='Рассчитать', size_hint_x=None, width=dp(100))
        calculate_btn.bind(on_press=self.calculate)
        level_layout.add_widget(calculate_btn)
        self.add_widget(level_layout)
        
        add_button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        add_button_layout.add_widget(Label(text='Добавить этот талант к итогу:'))
        self.add_to_total_btn = Button(text='Добавить к итогу', size_hint_x=None, width=dp(120))
        self.add_to_total_btn.bind(on_press=self.add_to_total)
        add_button_layout.add_widget(self.add_to_total_btn)
        self.add_widget(add_button_layout)
        
        clear_btn = Button(text='Очистить все таланты', size_hint_y=None, height=dp(40))
        clear_btn.bind(on_press=self.clear_all_talents)
        self.add_widget(clear_btn)
        
        self.results_label = Label(text='Выберите талант и уровни, затем нажмите Рассчитать. Затем нажмите "Добавить к итогу" для включения в сумму', size_hint_y=None, height=dp(150))
        self.add_widget(self.results_label)
        
        self.talents_summary_label = Label(text='Таланты еще не добавлены', size_hint_y=None, height=dp(100))
        self.add_widget(self.talents_summary_label)
    
    def calculate(self, instance):
        talent = self.talent_spinner.text
        current = int(self.current_spinner.text)
        target = int(self.target_spinner.text)
        
        talent_data = {
            (1, 2): "Basic Chip: 2; Dennies: 2000", (1, 3): "Basic Chip: 5; Dennies: 5000",
            (1, 4): "Basic Chip: 5; Advanced Chip: 2; Dennies: 11000", (1, 5): "Basic Chip: 5; Advanced Chip: 5; Dennies: 20000",
            (1, 6): "Basic Chip: 5; Advanced Chip: 9; Dennies: 32000", (1, 7): "Basic Chip: 5; Advanced Chip: 15; Dennies: 50000",
            (1, 8): "Basic Chip: 5; Advanced Chip: 15; Specialized Chip: 5; Dennies: 95000",
            (1, 9): "Basic Chip: 5; Advanced Chip: 15; Specialized Chip: 13; Dennies: 162500",
            (1, 10): "Basic Chip: 5; Advanced Chip: 15; Specialized Chip: 23; Dennies: 252500",
            (1, 11): "Basic Chip: 5; Advanced Chip: 15; Specialized Chip: 35; Dennies: 365000",
            (1, 12): "Basic Chip: 5; Advanced Chip: 15; Specialized Chip: 50; Hamster Cage Pass: 1; Dennies: 500000"
        }
        
        result_str = talent_data.get((1, target), "Комбинация уровней не найдена")
        self.results_label.text = f"Ресурсы для {talent} с уровня {current} на {target}:\n\n{result_str}"
        self.current_talent_resources = self.parse_resources(result_str)
        self.current_talent_key = f"{talent}_{current}_{target}"
    
    def add_to_total(self, instance):
        if not self.current_talent_resources:
            self.results_label.text = "Сначала рассчитайте талант!"
            return
        
        if self.current_talent_key in self.added_talents:
            self.results_label.text = f"Талант {self.talent_spinner.text} уже добавлен!"
            return
        
        self.added_talents[self.current_talent_key] = {
            'name': self.talent_spinner.text,
            'current_level': self.current_spinner.text,
            'target_level': self.target_spinner.text,
            'resources': self.current_talent_resources.copy()
        }
        
        self.update_talents_summary()
        self.results_label.text += f"\n\nДобавлен {self.talent_spinner.text} к итогу!"
    
    def clear_all_talents(self, instance):
        self.added_talents.clear()
        self.update_talents_summary()
        self.results_label.text = "Все таланты очищены!"
    
    def update_talents_summary(self):
        if not self.added_talents:
            self.talents_summary_label.text = "Таланты еще не добавлены"
            return
        
        summary_text = "Текущие таланты в итоге:\n"
        for talent_data in self.added_talents.values():
            summary_text += f"- {talent_data['name']} (Ур. {talent_data['current_level']}->{talent_data['target_level']})\n"
        
        self.talents_summary_label.text = summary_text
    
    def parse_resources(self, resource_string):
        pattern = r'([A-Za-z\s]+):\s*(\d+)'
        return {name.strip(): int(amount) for name, amount in re.findall(pattern, resource_string)}
    
    def get_all_talents_resources(self):
        total_resources = defaultdict(int)
        for talent_data in self.added_talents.values():
            for resource, amount in talent_data['resources'].items():
                total_resources[resource] += amount
        return dict(total_resources)
    
    def reset_values(self):
        self.talent_spinner.text = 'Базовая атака'
        self.current_spinner.text = '1'
        self.target_spinner.text = '2'
        self.added_talents.clear()
        self.current_talent_resources = {}
        self.results_label.text = 'Выберите талант и уровни, затем нажмите Рассчитать. Затем нажмите "Добавить к итогу" для включения в сумму'
        self.talents_summary_label.text = 'Таланты еще не добавлены'