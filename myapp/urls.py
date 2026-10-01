"""
URL configuration for CoursePrediction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('login/', views.login_view),
    path('home/', views.home),
    path('course_prediction/', views.course_prediction),
    path('course_prediction_post/', views.course_prediction_post),
    path('markprediction/', views.markprediction),
    path('markpredictionpost/', views.markpredictionpost),  
    path('chatbot/', views.chatbot),
    path('signup/', views.signup_view),
    path('logout/', views.logout_view),
    path('login_post/', views.login_post),
    path('signup_post/', views.signup_view_post),
    path('profile/', views.view_profile),
    path('edit_profile/',views.edit_profile),
    path('edit_profile_post/',views.edit_profile_post),
    path('chatbotmsg/',views.chatbotmsg),
    path('chatbot/',views.chatbot),
    path('newchat/',views.newchat),
    # path('leukemia/',views.leukemia),
    # path('leukemiapost/',views.leukemiapost),
    path('Translator/',views.Transalator),
    path('Transalatorpost/',views.Transalatorpost)
    
]
