from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Survey, Question, Option, User, Customer
# Register your models here.


admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Option)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )


admin.site.register(Customer)