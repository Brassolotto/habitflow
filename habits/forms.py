from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'color', 'icon']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes do Tailwind a todos os campos
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
        
        # Personalizações específicas para cada campo
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Nome do hábito',
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
        })
        
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Descrição (opcional)',
            'rows': 3,
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
        })
        
        self.fields['color'].widget.attrs.update({
            'type': 'color',
            'class': 'mt-1 h-10 w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
        })
        
        self.fields['icon'].widget.attrs.update({
            'placeholder': 'Nome do ícone (opcional)',
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
        })
