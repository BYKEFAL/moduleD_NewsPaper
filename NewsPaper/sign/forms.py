from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='Confirm Password')

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # 'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'password1': forms.PasswordInput(attrs={'class': 'form-control'}), # Для паролей виджет не работает. Чтобы задать атрибуты, например, название класса, следует использовать поле модели, как показано выше.
            # 'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Пользователь с таким именем уже существует")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Пользователь с таким email уже существует")
        return super().clean()


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common = Group.objects.get_or_create(name='common_group')[0]
        common.user_set.add(user)
        return user
