import datetime
from datetime import datetime
from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models
from django.core import validators
from django.contrib.auth import models as auth_models, get_user_model

from mechanic_project_v2.web.validators import validate_only_letters_in_name
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]


class ServiceUser(auth_models.AbstractUser):
    FIRST_NAME_MIN_LENGTH = 2
    LAST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MAX_LENGTH = 30

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(FIRST_NAME_MIN_LENGTH, message=f"Name cannot be less than {FIRST_NAME_MIN_LENGTH} symbols!"),
            validators.MaxLengthValidator(FIRST_NAME_MAX_LENGTH, message=f"Name cannot be more than {FIRST_NAME_MAX_LENGTH} symbols!"),
            validate_only_letters_in_name,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(LAST_NAME_MIN_LENGTH, message=f"Name cannot be less than {LAST_NAME_MIN_LENGTH} symbols!"),
            validators.MaxLengthValidator(LAST_NAME_MAX_LENGTH, message=f"Name cannot be more than {LAST_NAME_MAX_LENGTH} symbols!"),
            validate_only_letters_in_name,
        )
    )

    email = models.EmailField(
        unique=True
    )

    gender = models.IntegerField(
        choices=Gender.choices(),
        default=Gender.OTHER.value,
    )

    is_mechanic = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"


class Cars(models.Model):
    UserModel = get_user_model()
    MANUFACTURER_MIN_LENGTH = 1
    CARMODEL_MIN_LENGTH = 1
    MANUFACTURER_MAX_LENGTH = 30
    CARMODEL_MAX_LENGTH = 30

    manufacturer = models.CharField(
        max_length=MANUFACTURER_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(MANUFACTURER_MIN_LENGTH, message=f"Manufacturer name cannot be less than {MANUFACTURER_MIN_LENGTH} symbols!"),
            validators.MaxLengthValidator(MANUFACTURER_MAX_LENGTH,
                                          message=f"Manufacturer name cannot be more than {MANUFACTURER_MAX_LENGTH} symbols!"),
        ]
    )
    car_model = models.CharField(
        max_length=CARMODEL_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(CARMODEL_MIN_LENGTH,
                                          message=f"Manufacturer name cannot be less than {CARMODEL_MIN_LENGTH} symbols!"),
            validators.MaxLengthValidator(CARMODEL_MAX_LENGTH,
                                          message=f"Manufacturer name cannot be more than {CARMODEL_MAX_LENGTH} symbols!"),
        ]
    )
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1886, message="No cars existed before the year 1886!!!"),
            MaxValueValidator(datetime.now().year + 1, message="Car has not been made yet! Enter valid year!"),
        ]
    )
    vin = models.CharField(
        max_length=17,
        unique=True,
        validators=[
            validators.MinLengthValidator(16, message="Invalid VIN! VIN number has 17 symbols!"),
            validators.MaxLengthValidator(17, message="Invalid VIN! VIN number has 17 symbols!"),
        ]
    )
    problem_description = models.TextField()

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, default=0, related_name='cars_owned')
    mechanic = models.ForeignKey(ServiceUser, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='cars_worked_on')

    def __str__(self):
        return f"{self.manufacturer} {self.car_model} made in {self.year}"



