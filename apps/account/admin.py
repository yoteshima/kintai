from django.contrib import admin
from apps.account.models import User, UserRole

admin.site.register(User)
admin.site.register(UserRole)
