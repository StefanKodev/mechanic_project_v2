from django.contrib import admin
from django.urls import path, include
from mechanic_project_v2.web.views import RegisterUserView, LoginUserView,\
    LogoutUserView, index, AboutListView, checkPriceView, AddCarView, RegisteredCarsListView,\
    DeleteCarView, EditCarView, CheckCarsForServiceListView, claim_car, details_for_car, \
    CheckAcceptedCarsView, confirm_fix_car, account_details, edit_profile,\
    delete_account, RejectCarView



urlpatterns = [
    path('', index, name='home page'),
    path('register/', RegisterUserView.as_view(), name='register user'),
    path('login/', LoginUserView.as_view(), name='login user'),
    path('logout/', LogoutUserView.as_view(), name='logout user'),
    path('about/', AboutListView.as_view(), name='about page'),
    path('checkprice/', checkPriceView, name='price page'),
    path('add_car/', AddCarView.as_view(), name='add car'),
    path('check_registed_cars/', RegisteredCarsListView.as_view(), name='registered cars'),
    path('delete_car/<int:pk>/', DeleteCarView.as_view(), name='delete car'),
    path('edit_car/<int:pk>/', EditCarView.as_view(), name='edit car'),
    path('check_cars_for_service', CheckCarsForServiceListView.as_view(), name='cars for service'),
    path('claim_car/<int:car_id>', claim_car, name='claim car'),
    path('car/<int:car_id>/', details_for_car, name='details for car'),
    path('check_accepted_cars/', CheckAcceptedCarsView.as_view(), name='check accepted cars'),
    path('confirm_fix_car/<int:car_id>/', confirm_fix_car, name='confirm fix car'),
    path('account_details/', account_details, name='account details page'),
    path('edit_profile/', edit_profile, name='edit profile'),
    path('delete_profile/', delete_account, name='delete profile'),
    path('reject_car/<int:car_id>/', RejectCarView.as_view(), name='reject car')
]
