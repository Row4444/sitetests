from django.contrib import admin
from .models import Test, TestUserList, User, Comment, Question, Answer


# Register your models here.




class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 5





class TestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('IMG', {"fields": ['img'], 'classes': ['collapse']})
    ]
    inlines = [QuestionInLine]


admin.site.register(Test, TestAdmin)
admin.site.register(TestUserList)
admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Answer)
