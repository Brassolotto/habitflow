from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'color', 'icon']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes do Tailwind a todos os campos
        self.fields['name'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full rounded-md',
            'placeholder': 'ex: Meditação Matinal'
        })
        
        self.fields['description'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full rounded-md',
            'rows': 3,
            'placeholder': 'Breve descrição do seu hábito'
        })
        
        self.fields['color'].widget.attrs.update({
            'class': 'sr-only'
        })
        
        self.fields['icon'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full rounded-md'
        })

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("O nome do hábito deve ter pelo menos 2 caracteres.")
        return name
