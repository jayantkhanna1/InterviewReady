from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from dotenv import load_dotenv 
load_dotenv()
import json
from django.core.mail import send_mail

def index(request):
    return render(request,'index.html')

def saveChatGptKey(request):
    chatgpt_key = request.POST['chatGptKey']
    request.session['chatgpt_key_interview_ready'] = chatgpt_key
    return redirect('interview_info')

def interview_info(request):
    if "chatgpt_key_interview_ready" in request.session:
        chatgpt_key = request.session['chatgpt_key_interview_ready']
        print(chatgpt_key)
        return render(request,'interview_info.html',{'chatgpt_key':chatgpt_key})
    else:
        return redirect('home')