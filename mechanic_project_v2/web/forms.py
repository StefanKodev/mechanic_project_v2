from django.contrib.auth import forms as auth_forms, get_user_model
from .models import Cars
from .validators import validate_only_letters_in_name
from django import forms


UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')


class CarForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['manufacturer', 'car_model', 'year', 'vin', 'problem_description']


class ConfirmFixCarForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="I confirm that the car has been fixed",
    )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'gender']


class AccountDeleteConfirmForm(forms.Form):
    confirm_delete = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'is_mechanic')

    def clean_first_name(self):
        validate_only_letters_in_name(self.cleaned_data["first_name"])

        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        validate_only_letters_in_name(self.cleaned_data["last_name"])

        return self.cleaned_data["last_name"]


class CarsAdminForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = '__all__'
