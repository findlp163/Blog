from django.contrib import admin

from users.models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'username']


admin.site.register(Users, UsersAdmin)
