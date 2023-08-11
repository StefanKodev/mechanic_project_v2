from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import views as auth_views, get_user_model, login, logout
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.views import View
from .models import Cars, ServiceUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from asgiref.sync import async_to_sync

from .forms import RegisterUserForm, CarForm, ConfirmFixCarForm, EditProfileForm, AccountDeleteConfirmForm


class RegisterUserView(views.CreateView):
    template_name = 'web/create-profile.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home page')

    def form_valid(self, form):
        if form.cleaned_data['password1'] != form.cleaned_data['password2']:
            messages.error(self.request, 'Passwords do not match. Please try again.')
            return self.form_invalid(form)

        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['next'] = self.request.GET.get('next', '/')

        return context

    def get_success_url(self):
        return self.request.POST.get('next', self.success_url)


class LoginUserView(auth_views.LoginView):
    template_name = 'web/log-in.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class LogoutUserView(auth_views.LogoutView):
    pass


class AddCarView(LoginRequiredMixin, CreateView):
    login_url = 'login user'
    model = Cars
    form_class = CarForm
    template_name = 'web/add_car.html'
    success_url = reverse_lazy('home page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.mechanic = None
        return super().form_valid(form)


class RegisteredCarsListView(LoginRequiredMixin, ListView):
    login_url = 'login user'
    model = Cars
    template_name = 'web/check_registed_cars.html'
    context_object_name = 'cars'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_name'] = user.username
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'paginator': paginator,
            'page_number': page_number,
            'page_obj': page_obj,
        })

        return context



class AboutListView(ListView):
    model = ServiceUser
    template_name = 'web/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mechanicsQueryset = ServiceUser.objects.filter(is_mechanic=True)
        paginator = Paginator(mechanicsQueryset, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'mechanics': mechanicsQueryset,
            'paginator': paginator,
            'page_number': page_number,
            'page_obj': page_obj,
        })

        return context




def index(request):
    user = request.user

    context = {
        'user': user
    }
    return render(request, 'web/index.html', context)

"""
UNUSED
def aboutView(request):
    return render(request, 'web/about.html')
"""

def checkPriceView(request):
    return render(request, 'web/checkpricing.html')



class DeleteCarView(LoginRequiredMixin, DeleteView):
    login_url = 'web/log-in.html'
    model = Cars
    success_url = reverse_lazy('registered cars')
    template_name = 'web/car_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        car = self.get_object()
        if car.user != self.request.user:
            raise Http404("You don't have permission to delete this car.")
        return super().dispatch(request, *args, **kwargs)


class EditCarView(UpdateView):
    model = Cars
    success_url = reverse_lazy('registered cars')
    fields = ['manufacturer', 'car_model', 'year', 'vin', 'problem_description']
    template_name = 'web/car_edit.html'



class CheckCarsForServiceListView(UserPassesTestMixin, ListView):
    model = Cars
    template_name = 'web/check_cars_for_service.html'
    context_object_name = 'unassigned_cars'
    paginate_by = 3

    def test_func(self):
        return self.request.user.is_mechanic

    def get_queryset(self):
        return super().get_queryset().filter(mechanic=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'paginator': paginator,
            'page_number': page_number,
            'page_obj': page_obj,
        })

        return context


@login_required(login_url='login user')
def claim_car(request, car_id):
    car = get_object_or_404(Cars, pk=car_id, mechanic=None)
    if request.user.is_mechanic:
        car.mechanic = request.user
        car.save()
    return redirect('cars for service')


def details_for_car(request, car_id):
    car = get_object_or_404(Cars, id=car_id)
    context = {'car': car}
    return render(request, 'web/details_for_car.html', context)


class CheckAcceptedCarsView(LoginRequiredMixin, ListView):
    login_url = 'login user'
    model = Cars
    template_name = 'web/check_accepted_cars.html'
    context_object_name = 'accepted_cars'
    paginate_by = 3

    def get_queryset(self):
        current_mechanic = self.request.user
        return super().get_queryset().filter(mechanic=current_mechanic)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'paginator': paginator,
            'page_number': page_number,
            'page_obj': page_obj,
        })

        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_mechanic:
            raise PermissionDenied("You don't have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)


def confirm_fix_car(request, car_id):
    car = get_object_or_404(Cars, id=car_id)

    if request.method == 'POST':
        form = ConfirmFixCarForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            car.delete()
            return redirect('check accepted cars')
    else:
        form = ConfirmFixCarForm()

    context = {
        'car': car,
        'form': form,
    }

    return render(request, 'web/confirm_fix_car.html', context)


@login_required(login_url='login user')
def account_details(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'web/account_details.html', context)


@login_required(login_url='login user')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account details page')
    else:
        form = EditProfileForm(instance=user)

    context = {
        'user': user,
        'form': form,
    }

    return render(request, 'web/edit_profile.html', context)

@login_required(login_url='login user')
def delete_account(request):
    if request.method == 'POST':
        confirm_form = AccountDeleteConfirmForm(request.POST)
        if confirm_form.is_valid() and confirm_form.cleaned_data['confirm_delete']:
            try:
                user = request.user
                user.delete()
                return HttpResponseRedirect(reverse('home page'))
            except User.DoesNotExist as ex:
                raise User.DoesNotExist("You are not logged in yet." "Create a account or log in first.") from ex
    else:
        confirm_form = AccountDeleteConfirmForm()

    return render(request, 'web/confirm_delete_profile.html', {'confirm_form': confirm_form})


class RejectCarView(View):
    def get(self, request, *args, **kwargs):
        car_id = self.request.GET.get('car_id')
        try:
            car = Cars.objects.get(id=car_id, mechanic=request.user)
            car.mechanic = None
            car.save()
            return redirect('check accepted cars')
        except Cars.DoesNotExist:
            return HttpResponseBadRequest("Car not found or not assigned to you.")

"""

@login_required(login_url='login user')
def confirm_delete_profile(request):
    return render(request, 'web/confirm_delete_profile.html')


@login_required(login_url='login user')
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return redirect('home page')
    return redirect('account details')
    
"""