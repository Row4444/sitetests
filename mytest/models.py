from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from myaccount.models import User
from django.db import models



class Test(models.Model):
    """Тесты"""
    title = models.CharField(max_length=250, unique=True)
    img = models.ImageField(upload_to='uploads', height_field=None, width_field=None, max_length=100,
                            null=True, blank=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    """Вопросы к тестам"""
    question = models.TextField(null=True, blank=True)
    test_q = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Answer(models.Model):
    """Ответы к вопросам"""
    answer = models.CharField(max_length=100, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    is_correctly = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class TestUserManager(BaseUserManager):
    def get(self, user=None, test=None):
        return super(TestUserManager, self).get(test=test, user=user).first()


class TestUserList(models.Model):
    """База связывающая Юзеров и Тесты, котрые они прошли"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    completed_on = models.IntegerField()


    objects = models.Manager()
    be = TestUserManager()

    def __str__(self):
        return '{} completed by {}%'.format(self.date.strftime("%H:%M %d/%m/%Y"), self.completed_on)


class Comment(models.Model):
    """Комментарии к тестам"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return '{}: {}'.format(self.author, self.body)
