from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Cars

UserModel = get_user_model()

class CarTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testemail@example.com',
        )
        self.car = Cars.objects.create(
            manufacturer='Toyota',
            car_model='Corolla',
            year=2020,
            vin='12345678901234567',
            problem_description='Engine issue',
            user=self.user,
        )

    def test_car_created(self):
        self.assertEqual(str(self.car), 'Toyota Corolla made in 2020')

    def test_car_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('registered cars'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/check_registed_cars.html')

    def test_registered_cars_list_view(self):
        self.client.login(username='testuser', password='testpassword')

        car1 = Cars.objects.create(
            manufacturer='Ford',
            car_model='Fiesta',
            year=2018,
            vin='98765432101234568',
            problem_description='Transmission issue',
            user=self.user,
        )
        car2 = Cars.objects.create(
            manufacturer='Honda',
            car_model='Accord',
            year=2019,
            vin='98765432101234569',
            problem_description='Battery issue',
            user=self.user,
        )

        response = self.client.get(reverse('registered cars'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/check_registed_cars.html')

        self.assertContains(response, 'Toyota Corolla')
        self.assertContains(response, 'Ford Fiesta')
        self.assertContains(response, 'Honda Accord')

    def test_add_car_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add car'))
        self.assertEqual(response.status_code, 200)

    def test_claim_car_view(self):
        mechanic_user = UserModel.objects.create_user(
            username='mechanicuser',
            password='mechanicpassword',
            email='mechanic@example.com',
            is_mechanic=True,
        )
        self.client.login(username='mechanicuser', password='mechanicpassword')
        car = Cars.objects.create(
            manufacturer='Ford',
            car_model='Mustang',
            year=2022,
            vin='98765432101234567',
            problem_description='Brake issue',
            user=self.user,
        )
        response = self.client.get(reverse('claim car', args=[car.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cars for service'))


class UserTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
        )

    def test_user_created(self):
        self.assertEqual(str(self.user.username), 'testuser')

    def test_login_view(self):
        response = self.client.post(reverse('login user'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home page'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home page'))

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edit profile'))
        self.assertEqual(response.status_code, 200)

    def test_account_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('delete profile'))
        self.assertEqual(response.status_code, 200)
