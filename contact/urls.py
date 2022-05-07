'''urls.py'''
from django.urls import path
from . import views

#now import the views.py file into this code

APP_NAME = 'contact'

urlpatterns=[
  # /contact/
  path('',views.index, name="index"),
  # /contact/login/
  path('login/',views.login,name="login"),
  # /contact/saved/
  path('saved/', views.saved, name="saved"),
  path('info', views.info, name="info"), 
]
