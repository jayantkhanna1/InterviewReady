from django.shortcuts import render,redirect
from transformers import pipeline
from .models import *
from django.http import JsonResponse
import os
from dotenv import load_dotenv 
load_dotenv()
import random
import string
import whisper

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

def chatgpt(prompt):
    return prompt

def interview_information(request):
    job_desc = request.POST['job_description']
    interview_type = request.POST['interview_type']
    difficulty = request.POST['difficulty']
    special_tags = None
    if "special_tags" in request.POST:
        special_tags = request.POST['special_tags']

    # Updating job description
    if special_tags is not None:
        job_desc = job_desc + " \nKey Requirements : " + special_tags
    
    # creating interview type
    if interview_type == "basic":
        interview_type = "telephonic"
    elif interview_type == "technical":
        interview_type = "technical"
    else:
        interview_type = "hr and behavioral"
    
    # creating difficulty
    if difficulty == "easy":
        difficulty = "fresher"
    elif difficulty == "medium":
        difficulty = "intermediate"
    else:
        difficulty = "expert"

    # creating initial prompt
    if interview_type == "technical":
        # get 3 questions from the database and tell user to solve them. Integrate IDE later
        pass
    else:
        initial_prompt = "Using this job description give exactly 4 question for a "+interview_type+" interview of a "+difficulty+" level.  Give these questions in python list format:['ques','ques2'...]"
        prompt = initial_prompt + "\n\n" + job_desc
    
    result = chatgpt(prompt)
    request.session['questions_interview_ready'] = result  

    return redirect('interview_begin')

def interview_begin(request):
    if "questions_interview_ready" in request.session:
        questions = request.session['questions_interview_ready']
        print(questions)
        temp_questions = [
            "ques 1",
            "ques 2",
            "ques 3",
            "ques 4",
            "ques 5",
            "ques 6",
            "ques 7"
        ]
        return render(request,'interview_begin.html',{'questions':temp_questions})
    else:
        return redirect('home')
    
def asr(request):
    audio_file = request.FILES['audio']

        # Define the directory where you want to save the audio files
    save_directory = 'temp_files'
    random_file_name = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15))
    random_file_name = random_file_name+ ".wav"
    # You can generate a unique filename for the audio file, or use the original filename
    filename = os.path.join(save_directory, random_file_name)

    with open(filename, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
    
    model = whisper.load_model("base.en")
    result = model.transcribe(filename)
    print(result["text"])
    os.remove(filename)
   
    # You can now process the audio file or respond with a success message
    return JsonResponse({'result': result['text']})





# To be used during evaluation
# prompt = 'Question : How are you?\nAnswer: I dont want to talk with you\n\nIn Json format tell me grammar, clarity, confidence. If not sure aout something mark it as 0. All answers should be between 0 to 100. \nExample: {"grammar" : 40,"clarity" : 20,"confidence" : 0}'


