from django.db import models
from django.urls import reverse
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

def validate_even(value):
    if len(value) < 2:
        raise ValidationError(
            _('%(value)s is too short'),
            params={'value': value},
        )

    if value == 'questino':
        raise ValidationError(
            _('Cannot name question question'),
            params={'value': value},
        )


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
    
    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]


class Survey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    survey = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    customer_id = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.survey
    
    class Meta:
        permissions = [
            ('freeze_survey', 'Can freeze a survey')
        ]


class Question(models.Model):

    question = models.CharField(max_length=255, validators=[validate_even])
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True, blank=True)


    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.question


class Option(models.Model):

    option = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.option
