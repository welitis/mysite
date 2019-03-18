# author:Welisit Wang
# email:Welisit123@gmail.com
from django.conf.urls import url
from . import views

app_name = 'login'
urlpatterns = [
    url(r'index/', views.index, name='index'),
    url(r'login/', views.login, name='login'),
    url(r'register/', views.register, name='register'),
    url(r'logout/', views.logout, name='logout'),
    url(r'confirm/', views.user_confirm, name='confirm'),
]



