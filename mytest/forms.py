from django import forms
from django.forms import RadioSelect

from .models import Test, Question, Answer, Comment, TestUserList




class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'img', 'description')


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question',)



class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer', 'is_correctly')



class CommentForm(forms.ModelForm):
    body = forms.CharField(max_length=250, label='Comment')

    class Meta:
        model = Comment
        fields = ('body',)


class TestUserListForm(forms.ModelForm):
    class Meta:
        model = TestUserList
        fields = ('completed_on',)
