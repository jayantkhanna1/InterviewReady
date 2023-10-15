from django.shortcuts import render,redirect
from transformers import pipeline
from .models import *
from django.http import JsonResponse
import os
from dotenv import load_dotenv 
load_dotenv()
import random
import string
import openai 
from django.urls import reverse
import whisper

def index(request):
    data = {
        "error_present" : False
    }
    if "error" in request.GET:
        error = request.GET["error"]
        data["error_present"] = True
        data["error"] = error

    return render(request,'index.html',{"data":data})

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

def chatgpt(api_key,prompt):
    try:
        openai.api_key = api_key
        message = prompt
        messages = [{"role": "user", "content": message}]
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        print(chat)
        reply = chat.choices[0].message.content 
        print(f"ChatGPT: {reply}") 
        # message.append({"role": "assistant", "content": reply
        return reply, False
    except Exception as e:
        print(e)
        return e,True

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
        initial_prompt = "Using this job description give exactly 7 question for a "+interview_type+" interview of a "+difficulty+" level.  Give these questions in python list format:['ques','ques2'...]"
        prompt = initial_prompt + "\n\n" + job_desc
    
    if "chatgpt_key_interview_ready" not in request.session:
        return redirect('home')
    api_key = request.session['chatgpt_key_interview_ready']
    result,any_error = chatgpt(api_key,prompt)
    if any_error:
        url = reverse('home') + '?error=Invalid Chatgpt Key'
        return redirect(url)
    request.session['questions_interview_ready'] = result  

    return redirect('interview_begin')

def remove(string,substring):
    result = ""
    for char in string:
        if char != substring:
            result += char
    return result

def interview_begin(request):
    if "questions_interview_ready" in request.session:
        questions = request.session['questions_interview_ready']
        final_questions = []
        if "[" in questions:
            new_question = ""
            for x in questions:
                if x == "[":
                    flag = 1

                elif x == "]":
                    flag = 0

                else:
                    pass

                if flag == 1:
                    new_question +=x
            # remove [ in string if it exists]
            new_question = remove(new_question, "[")
            new_question = new_question.split(',')
            final_questions = new_question

        else:
        # another flow 
            questions = questions.split("\n")
            final_questions = []
            for question in questions:
                # if question has question number delete it 
                if question[0].isdigit():
                    question = question[2:]
                final_questions.append(question)

        print(final_questions)
        return render(request,'interview_begin.html',{'questions':final_questions})
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


