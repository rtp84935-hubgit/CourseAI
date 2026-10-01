from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from myapp.models import *

import google.generativeai as ai
from deep_translator import GoogleTranslator

import google.generativeai as ai
from deep_translator import GoogleTranslator

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set")

ai.configure(api_key=api_key)

modelai = ai.GenerativeModel("gemini-3.5-flash-lite")
# Create your views here.

def login_view(request):
    return render(request, 'loginpage.html')



def login_post(request):
    if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']

         user=authenticate(request,username=username,password=password)
         if user is not None:
             login(request,user)
             print("Login successful")
             return redirect('/myapp/home/')
         else:
            print("Login failed")
            return render(request, 'loginpage.html', {'error_message': 'Invalid username or password'})
    return render(request, 'loginpage.html')

def signup_view(request):
    return render(request, 'signup.html')

def signup_view_post(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        place = request.POST.get('place')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return redirect('/myapp/signup/')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Username already taken')
            return redirect('/myapp/signup/')

        user = User.objects.create_user(username=email,password=password)
        ob=UserProfile()
        ob.LOGIN = user
        ob.full_name = full_name
        ob.email = email
        ob.age=age
        ob.gender=gender
        ob.place=place
        ob.phone=phone
        ob.save()



        messages.success(request, 'Account created — please log in')
        return redirect('/myapp/login/')

    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('/myapp/login/')
@login_required
def home(request):
    return render (request, 'home.html')
@login_required
def course_prediction(request):
    return render(request, 'course_prediction.html')

def course_prediction_post(request):
    skills=request.POST.getlist('skills')
    if skills:
        df=pd.read_csv(r'C:\Users\rahul\OneDrive\Desktop\Regional\ML+JANGO\CoursePrediction\CoursePrediction\myapp\DataSets\Courseprediction.csv')

        x=df.drop(columns='Recommended_Course')
        y=df['Recommended_Course']

        model=RandomForestClassifier()

        model.fit(x,y)

        input_data = [1 if i in skills
                    else 0 
                    for i in x.columns]

        result=model.predict([input_data])[0]

        text2=('breif about ',result,' cource and its future scope and carrier path within maximum 5 sentence')
        result2=modelai.generate_content(text2)
        
        return render(request, 'course_prediction.html',{'result':result,'result2':result2.text})
    else:
        messages.warning(request,'select any options')
        return render(request,'course_prediction.html')
@login_required
def markprediction(request):
    return render(request,'markprediction.html')

def markpredictionpost(request):
    if request.method == 'POST':
        study_hours = request.POST.get('study_hours')
        attendance = request.POST.get('attendance')
        previous_score = request.POST.get('previous_score')
        assignments = request.POST.get('assignments')
        sleep_hours = request.POST.get('sleep_hours')

        
        if not study_hours or not attendance or not previous_score or not assignments or not sleep_hours:
            messages.warning(request, "Please fill all fields")
            return redirect('/myapp/markprediction/')

        
        study_hours = float(study_hours)
        attendance = float(attendance)
        previous_score = float(previous_score)
        assignments = float(assignments)
        sleep_hours = float(sleep_hours)

        df = pd.read_csv(
            r'C:\Users\rahul\OneDrive\Desktop\Regional\ML+JANGO\CoursePrediction\CoursePrediction\myapp\DataSets\markprediction.csv'
        )

        x = df.drop(columns='future_score')
        y = df['future_score']

        model = RandomForestRegressor(n_estimators=42)
        model.fit(x, y)

        data = [[
            study_hours,
            attendance,
            previous_score,
            assignments,
            sleep_hours
        ]]

        result = model.predict(data)[0]
        print(result)

        grade = ''

        if result >= 90:
            grade = 'A+'
        elif result >= 80:
            grade = 'A'
        elif result >= 70:
            grade = 'B+'
        elif result >= 60:
            grade = 'B'
        elif result > 55:
            grade = 'C'
        else:
            grade = 'FAIL'

        text=('i have got a grade of ',grade,'so give me motivation for that , the grade Range is A+,A,B+,B,C and FAILso consider that')
        result2=modelai.generate_content(text)
        return render(request, 'markprediction.html', {'grade': grade,'result2':result2.text})

    else:
        return render(request, 'markprediction.html')
@login_required
def chatbot(request):
    return render(request,'chatbot.html')
@login_required
def view_profile(request):
    user_profile = UserProfile.objects.get(LOGIN=request.user)                           
    return render(request, 'view_profile.html', {'profile': user_profile})

def edit_profile(request):
    ob=UserProfile.objects.get(LOGIN=request.user)
    return render(request,'edit_profile.html',{'profile':ob})

def edit_profile_post(request):
    full_name = request.POST.get('full_name')
    email = request.POST.get('email')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    place = request.POST.get('place')
    phone = request.POST.get('phone')

    user=request.user

    ob=UserProfile.objects.get(LOGIN=request.user)

    ob.full_name=full_name
    ob.email=email
    ob.age=age
    ob.gender=gender
    ob.place=place
    ob.phone=phone
    ob.LOGIN=user
    ob.save()

    user.username=email
    user.save()
    return redirect('/myapp/profile/')


def chatbot(request):
    ob=ChatBot.objects.filter(USER__LOGIN=request.user)
    return render(request,'chatbot.html',{'data':ob})




def chatbotmsg(request):
    text=request.POST['text']
    result=modelai.generate_content(text)

    ChatBot.objects.create(
        question=text,
        answer=result.text,
        datetime=datetime.now(),
        USER=UserProfile.objects.get(LOGIN=request.user)
    ).save()

    ob=ChatBot.objects.filter(USER__LOGIN=request.user)

    return render(request,'chatbot.html',{'result':result.text,'data':ob})

def newchat(request):
    ChatBot.objects.filter(USER__LOGIN=request.user).delete()
    return redirect('/myapp/chatbot/')

def Transalator(request):
    return render(request,'Translator.html')

def Transalatorpost(request):
    text=request.POST['text']
    source=request.POST['source_language']
    target=request.POST['target_language']

    result=GoogleTranslator(source=source,target=target).translate(text)
    print(result)
    return render(request,'Translator.html',{'result':result})