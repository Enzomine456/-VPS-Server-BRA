from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import UserProfile, VPNServer
else:
    from .models import UserProfile, VPNServer


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")
    first_name = forms.CharField(max_length=30, required=True, label="Nome")
    last_name = forms.CharField(max_length=30, required=True, label="Sobrenome")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nome de usuário"
        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirmar senha"
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['preferred_server', 'favorite_games']
        labels = {
            'preferred_server': 'Servidor Preferido',
            'favorite_games': 'Jogos Favoritos',
        }
        widgets = {
            'preferred_server': forms.Select(attrs={'class': 'form-control'}),
            'favorite_games': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preferred_server'].queryset = VPNServer.objects.filter(is_active=True)
        self.fields['preferred_server'].empty_label = "Selecione um servidor"