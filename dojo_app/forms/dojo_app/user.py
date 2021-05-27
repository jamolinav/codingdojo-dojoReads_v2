from django.forms import ModelForm, PasswordInput, TextInput
from django import forms
from ...models import User

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirmar Contraseña')
    class Meta:
        model = User
        fields = '__all__'
        #fields = ['name']
        widgets = {
            'password' : PasswordInput,
            'first_name' : TextInput(attrs={'placeholder': '<nombres>'}),
            'last_name' : TextInput(attrs={'placeholder': '<apellidos>'}),
            'birth_date' : TextInput(attrs={'placeholder': '<fecha de nacimiento>', 'type': 'date'}),
        }
        labels = {
            'first_name'  : 'Nombres',
            'last_name'  : 'Apellidos',
            'birth_date'  : 'Fecha de Nacimiento',
            'password'  : 'Contraseña',
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if (password != confirm_password):
            raise forms.ValidationError(
                "Las contraseñas no coinciden"
        )
        
class UserLoginForm(forms.Form):
    email       = forms.EmailField(max_length=100, required=True)
    password    = forms.CharField(max_length=20, widget=forms.PasswordInput, required=True)

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user        = User.authenticate(email, password)
        return user

    def clean(self):
        email       = self.cleaned_data.get('email')
        password    = self.cleaned_data.get('password')
        user        = User.authenticate(email, password)
        if not user:
            raise forms.ValidationError("Lo sentimos, login fallido, vuelva a intentar")

        return self.cleaned_data