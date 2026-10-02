from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.login_view),

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
    path('edit_profile/', views.edit_profile),
    path('edit_profile_post/', views.edit_profile_post),
    path('chatbotmsg/', views.chatbotmsg),
    path('newchat/', views.newchat),
    path('Translator/', views.Transalator),
    path('Transalatorpost/', views.Transalatorpost),
]