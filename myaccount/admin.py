from django.contrib import admin
from myaccount.models import User
from mytest.models import TestUserList


class UserAnswersInLine(admin.TabularInline):
    model = TestUserList
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = [UserAnswersInLine]


admin.site.register(User, UserAdmin)
