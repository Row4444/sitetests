

from django.urls import path, include

from .views import TestView, TestList, TestRun, CreateTest, TestListYet

urlpatterns = [
    path('<int:id>', TestView.as_view(), name='test_detail'),
    path('', TestList.as_view(), name='tests'),
    path('run/<int:id>', TestRun.as_view(), name='run_test'),
    path('create/test', CreateTest.as_view(), name='create_test'),
    path('me/', TestListYet.as_view(), name='mytests')
    ]