from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Cars
from .forms import UserAdminForm, CarsAdminForm

UserModel = get_user_model()


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
        list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'is_mechanic')
        search_fields = ('username', 'email', 'first_name', 'last_name', 'gender',)
        ordering = ('-is_mechanic',)
        form = UserAdminForm


@admin.register(Cars)
class CarsModelAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'car_model', 'year', 'vin', 'problem_description', 'user', 'mechanic')
    list_filter = ('manufacturer', 'car_model', 'year')
    search_fields = ('manufacturer', 'car_model', 'year')
    ordering = ('manufacturer',)
    form = CarsAdminForm
