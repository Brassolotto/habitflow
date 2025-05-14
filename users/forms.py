from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes do Tailwind a todos os campos
        self.fields['username'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full pl-10 pr-3 py-2 rounded-md',
            'placeholder': 'Nome completo'
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full pl-10 pr-3 py-2 rounded-md',
            'placeholder': 'seu-email@exemplo.com'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full pl-10 pr-3 py-2 rounded-md',
            'placeholder': '••••••••'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full pl-10 pr-3 py-2 rounded-md',
            'placeholder': '••••••••'
        })

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full rounded-md'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full rounded-md'
        })

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full pl-10 pr-3 py-2 rounded-md',
            'placeholder': 'seu-email@exemplo.com'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'bg-gray-700 text-white focus:ring-purple-500 focus:border-purple-500 block w-full pl-10 pr-3 py-2 rounded-md',
            'placeholder': '••••••••'
        })
