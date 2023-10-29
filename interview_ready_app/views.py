from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import os
from django.core.mail import send_mail
from dotenv import load_dotenv 
load_dotenv()
import random
import string
import openai 
import json
from django.urls import reverse
import whisper
from datetime import datetime


def index(request):
    data = {
        "error_present" : False
    }
    if "error" in request.GET:
        error = request.GET["error"]
        data["error_present"] = True
        data["error"] = error
    
    if "InterviewReady_privateToken" in request.session:
        private_token = request.session['InterviewReady_privateToken']
        if User.objects.filter(private_key=private_token).exists():
            user = User.objects.get(private_key=private_token)
            return render(request,'index.html',{"data":data,'logged_in':True,'user':user})
        else:
            return render(request,'index.html',{"data":data,'logged_in':False})
    return render(request,'index.html',{"data":data,'logged_in':False})


def interview_info(request):
    if "InterviewReady_privateToken" in request.session:
        private_token = request.session['InterviewReady_privateToken']
        if User.objects.filter(private_key=private_token).exists():
            user = User.objects.get(private_key=private_token)
            return render(request,'interview_info.html',{'logged_in':True,'user':user})
        else:
            url = reverse('login')
            return redirect(url)
    else:
        url = reverse('login')
        return redirect(url)


def chatgpt(api_key,prompt):
    try:
        openai.api_key = api_key
        messages = [
            {
                "role": "system",
                'content' : "Think like an interviewer and evaluate a candidate"

            },
            {"role": "user", "content": prompt
             }]
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content 
        return reply, False
    except Exception as e:
        print(e)
        return e,True

def interview_information(request):
    user=user_logged_in(request)
    if user is None:
        url = reverse('login')
        return redirect(url)
    
    job_desc = request.POST['job_description']
    job_desc_old = job_desc
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
    elif interview_type == "background":
        interview_type = "background"
    elif interview_type == "custom":
        interview_type = "custom"
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
    if interview_type == "background":
        initial_prompt = "Using this candidates resume give exactly 7 question for a "+interview_type+" interview of a "+difficulty+" level.  Give these questions in python list format:['ques','ques2'...]"
        free_prompt = initial_prompt + "\n\n Resume " + job_desc 
    elif interview_type == "custom":
        initial_prompt = "Using this custom data give exactly 7 question an interviewer might ask for a "+interview_type+" interview of a "+difficulty+" level.  Give these questions in python list format:['ques','ques2'...]"
        free_prompt = initial_prompt + "\n\n Custom data: " + job_desc
    else:
        initial_prompt = "Using this job description give exactly 7 question for a "+interview_type+" interview of a "+difficulty+" level.  Give these questions in python list format:['ques','ques2'...]"
        free_prompt = initial_prompt + "\n\n" + job_desc
    current_date_time = datetime.now()
    history = History.objects.create(user=user,job_description=job_desc_old,special_words=special_tags,interview_type=interview_type,interview_difficulty=difficulty,prompt = free_prompt,interview_date=current_date_time)
    history.save()
    try:
        if user.free_trials_left > 0:
            user.free_trials_left-=1
            user.save()
            return redirect('interview_begin_premium')
        else:
            return redirect('interview_mode')
    except:
        url = reverse('login') + '?error=Please Login first'
        return redirect(url)
    

def remove(string,substring):
    result = ""
    for char in string:
        if char != substring:
            result += char
    return result

def interview_begin(request):
    # change as now we need to use prompt to generate questions here and also use regeneration if any error occurs
    user = user_logged_in(request)
    if user is None:
        url = reverse('login')
        return redirect(url)
    # get last history object of the user
    history = History.objects.filter(user=user).last()
    prompt = history.prompt
    api_key = os.environ.get('CHATGPT_KEY')
    questions,error = chatgpt(api_key,prompt)
    if error:
        url = reverse('home') + '?error=ChatGPT Key Expired'
        return redirect(url)
    print(questions)
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
            #if question[0].isdigit():
                #   question = question[2:]
            final_questions.append(question)


    print(final_questions)
    final_final_questions = []
    for x in final_questions:
        if '"' in x:
            x = x.replace('"','')
        if "'" in x:
            x = x.replace("'",'')
        temp_jso = {
            'question' : x,
            'answer' : "",
            'confidence' : {}
        }
        final_final_questions.append(temp_jso)
    
    history.interview_result = final_final_questions
    history.save()
    return redirect('interview_begin_free')
    # return render(request,'interview_begin.html',{'questions':final_final_questions})
    
def interview_begin_free(request):
    user = user_logged_in(request)
    if not user:
        url = reverse('login')
        return redirect(url)
    history = History.objects.filter(user=user_logged_in(request)).last()
    questions = history.interview_result
    final_list = []
    for x in questions:
        final_list.append(x['question'])
    print(user)
    return render(request,'interview_begin.html',{'questions':final_list,'user':user,'logged_in':True})

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

def get_result_for_one_pair(request):
    question = request.POST['question']
    answer = request.POST['answer']
    prompt = 'Interview Question : '+str(question)+'\nCandidate Answer: '+str(answer)+'\n\nIn Json format tell me grammar, clarity, confidence, score that interviewer would give to the answer and some comments on answer to improve chances of getting selected. If not sure about something mark it as 0. All marks should be between 0 to 100. \nExample: {"grammar" : 40,"clarity" : 20,"confidence" : 0,"answer_score_based_on_question_according_to_interviewer" : 0,"advice_to_improve_answer" : "Improve your..."}.'
    api_key = os.environ.get('CHATGPT_KEY')
    result,any_error = chatgpt(api_key,prompt)
    if any_error:
        return JsonResponse({'result': 'Error Occured'})
    return JsonResponse({'result': result})

def save_interview_result(request):
    question_answer_pair = request.POST['question_answer_pair']
    print(question_answer_pair)
    
    try:
        print(question_answer_pair)
        
        # question_answer_pair = question_answer_pair.replace("'",'"')
        question_answer_pair = json.loads(question_answer_pair)
        # question_answer_pair = []
        overall_score = 0
        overall_grammar = 0
        overall_confidence = 0
        overall_clarity = 0
        overall_answer_score_based_on_question_according_to_interviewer = 0
        ques_ans_pair = []
        i=1
        for x in question_answer_pair:
            if type(x["confidence"]) != dict:
                y = json.loads(x["confidence"])
            else:
                y = x["confidence"]
            print(y)
            overall_grammar+= y["grammar"]
            overall_confidence+=y["confidence"]
            overall_clarity+=y["clarity"]
            if "answer_score_based_on_question_according_to_interviewer" in y:
                overall_answer_score_based_on_question_according_to_interviewer+=y["answer_score_based_on_question_according_to_interviewer"]
            if "score" in y:
                overall_answer_score_based_on_question_according_to_interviewer+=y["score"]
            

            #  Creating new array 
            temp_jso = {
                'question_number' : i,
                'question' : x["question"],
                'answer' : x['answer'],
                "grammar_score" : y["grammar"],
                "clarity_score" : y["clarity"],
                "confidence_score" : y["confidence"]
            }
            if "advice_to_improve_answer" in y and y["advice_to_improve_answer"] != "":
                temp_jso["advice"] = y["advice_to_improve_answer"]
            if "answer_score_based_on_question_according_to_interviewer" in y:
                temp_jso["interviewer_score"]=y["answer_score_based_on_question_according_to_interviewer"]
            if "score" in y:
                temp_jso["interviewer_score"]=y["score"]
            
            ques_ans_pair.append(temp_jso)
            i+=1
        overall_grammar=overall_grammar/7
        overall_clarity = overall_clarity/7
        overall_confidence=overall_confidence/7
        overall_answer_score_based_on_question_according_to_interviewer = overall_answer_score_based_on_question_according_to_interviewer/7
        overall_score=(overall_grammar + overall_confidence + overall_clarity + (10*overall_answer_score_based_on_question_according_to_interviewer))/13
        history = History.objects.filter(user=user_logged_in(request)).last()
        history.overall_score = overall_score
        history.overall_grammar = overall_grammar
        history.overall_clarity = overall_clarity
        history.overall_confidence = overall_confidence
        history.overall_answer_score_based_on_question_according_to_interviewer = overall_answer_score_based_on_question_according_to_interviewer
        history.interview_result = ques_ans_pair
        history.interview_completed = True
        history.save()
        return JsonResponse({'question_answer_pair':ques_ans_pair,'overall_score':int(overall_score),'overall_grammar':int(overall_grammar),'overall_clarity':int(overall_clarity),'overall_confidence':int(overall_confidence),'overall_answer_score_based_on_question_according_to_interviewer':int(overall_answer_score_based_on_question_according_to_interviewer)})
    except:
        # Calling chatgpt to fix the json
        
        prompt = "Fix this JSON. Only give correct JSON answer : \n" + question_answer_pair
        api_key = os.environ.get('CHATGPT_KEY')
        result,any_error = chatgpt(api_key,prompt)
        if any_error:
            url = reverse('home') + '?error=ChatGPT Key Expired'
            return redirect(url)
        question_answer_pair =result
        request.session['question_answer_pair'] = question_answer_pair

        # JSON fixed now evaluate
        question_answer_pair = request.session['question_answer_pair']
        print(question_answer_pair)
        
        # question_answer_pair = question_answer_pair.replace("'",'"')
        question_answer_pair = json.loads(question_answer_pair)
        # question_answer_pair = []
        overall_score = 0
        overall_grammar = 0
        overall_confidence = 0
        overall_clarity = 0
        overall_answer_score_based_on_question_according_to_interviewer = 0
        ques_ans_pair = []
        i=1
        for x in question_answer_pair:
            if type(x["confidence"]) != dict:
                y = json.loads(x["confidence"])
            else:
                y = x["confidence"]
            print(y)
            overall_grammar+= y["grammar"]
            overall_confidence+=y["confidence"]
            overall_clarity+=y["clarity"]
            if "answer_score_based_on_question_according_to_interviewer" in y:
                overall_answer_score_based_on_question_according_to_interviewer+=y["answer_score_based_on_question_according_to_interviewer"]
            if "score" in y:
                overall_answer_score_based_on_question_according_to_interviewer+=y["score"]
            

            #  Creating new array 
            temp_jso = {
                'question_number' : i,
                'question' : x["question"],
                'answer' : x['answer'],
                "grammar_score" : y["grammar"],
                "clarity_score" : y["confidence"],
                "confidence_score" : y["clarity"]
            }
            if "advice_to_improve_answer" in y and y["advice_to_improve_answer"] != "":
                temp_jso["advice"] = y["advice_to_improve_answer"]
            if "answer_score_based_on_question_according_to_interviewer" in y:
                temp_jso["interviewer_score"]=y["answer_score_based_on_question_according_to_interviewer"]
            if "score" in y:
                temp_jso["interviewer_score"]=y["score"]
            
            ques_ans_pair.append(temp_jso)
            i+=1
        overall_grammar=overall_grammar/7
        overall_clarity = overall_clarity/7
        overall_confidence=overall_confidence/7
        overall_answer_score_based_on_question_according_to_interviewer = overall_answer_score_based_on_question_according_to_interviewer/7
        overall_score=(overall_grammar + overall_confidence + overall_clarity + (10*overall_answer_score_based_on_question_according_to_interviewer))/13
        history = History.objects.filter(user=user_logged_in(request)).last()
        history.overall_score = overall_score
        history.overall_grammar = overall_grammar
        history.overall_clarity = overall_clarity
        history.overall_confidence = overall_confidence
        history.overall_answer_score_based_on_question_according_to_interviewer = overall_answer_score_based_on_question_according_to_interviewer
        history.interview_result = ques_ans_pair
        history.interview_completed = True
        history.save()
        return JsonResponse({'question_answer_pair':ques_ans_pair,'overall_score':int(overall_score),'overall_grammar':int(overall_grammar),'overall_clarity':int(overall_clarity),'overall_confidence':int(overall_confidence),'overall_answer_score_based_on_question_according_to_interviewer':int(overall_answer_score_based_on_question_according_to_interviewer)})
    

def show_interview_result_free(request):
    user = user_logged_in(request)
    if user is None:
        url = reverse('login')
        return redirect(url)
    
    history = History.objects.filter(user=user).last()
    if history.interview_completed:
        overall_score = history.overall_score
        overall_grammar = history.overall_grammar
        overall_clarity = history.overall_clarity
        overall_confidence = history.overall_confidence
        overall_answer_score_based_on_question_according_to_interviewer = history.overall_answer_score_based_on_question_according_to_interviewer
        ques_ans_pair = history.interview_result

        return render(request,'show_interview_result_free.html',{'user':user,'logged_in':True,'overall_score':int(overall_score),'overall_grammar':int(overall_grammar),'overall_clarity':int(overall_clarity),'overall_confidence':int(overall_confidence),'overall_answer_score_based_on_question_according_to_interviewer':int(overall_answer_score_based_on_question_according_to_interviewer),'ques_ans_pair':ques_ans_pair})
    else:
        url = reverse('home') + '?error=Interview not completed'
        return redirect(url)
def evaluate_result(request):
    try:
        question_answer_pair = request.session['question_answer_pair']
        print(question_answer_pair)
        
        # question_answer_pair = question_answer_pair.replace("'",'"')
        question_answer_pair = json.loads(question_answer_pair)
        # question_answer_pair = []
        overall_score = 0
        overall_grammar = 0
        overall_confidence = 0
        overall_clarity = 0
        overall_answer_score_based_on_question_according_to_interviewer = 0
        ques_ans_pair = []
        i=1
        for x in question_answer_pair:
            if type(x["confidence"]) != dict:
                y = json.loads(x["confidence"])
            else:
                y = x["confidence"]
            print(y)
            overall_grammar+= y["grammar"]
            overall_confidence+=y["confidence"]
            overall_clarity+=y["clarity"]
            if "answer_score_based_on_question_according_to_interviewer" in y:
                overall_answer_score_based_on_question_according_to_interviewer+=y["answer_score_based_on_question_according_to_interviewer"]
            if "score" in y:
                overall_answer_score_based_on_question_according_to_interviewer+=y["score"]
            

            #  Creating new array 
            temp_jso = {
                'question_number' : i,
                'question' : x["question"],
                'answer' : x['answer'],
                "grammar_score" : y["grammar"],
                "clarity_score" : y["confidence"],
                "confidence_score" : y["clarity"]
            }
            if "advice_to_improve_answer" in y and y["advice_to_improve_answer"] != "":
                temp_jso["advice"] = y["advice_to_improve_answer"]
            if "answer_score_based_on_question_according_to_interviewer" in y:
                temp_jso["interviewer_score"]=y["answer_score_based_on_question_according_to_interviewer"]
            if "score" in y:
                temp_jso["interviewer_score"]=y["score"]
            
            ques_ans_pair.append(temp_jso)
            i+=1
        overall_grammar=overall_grammar/7
        overall_clarity = overall_clarity/7
        overall_confidence=overall_confidence/7
        overall_answer_score_based_on_question_according_to_interviewer = overall_answer_score_based_on_question_according_to_interviewer/7
        overall_score=(overall_grammar + overall_confidence + overall_clarity + (10*overall_answer_score_based_on_question_according_to_interviewer))/13
        return JsonResponse({'question_answer_pair':ques_ans_pair,'overall_score':int(overall_score),'overall_grammar':int(overall_grammar),'overall_clarity':int(overall_clarity),'overall_confidence':int(overall_confidence),'overall_answer_score_based_on_question_according_to_interviewer':int(overall_answer_score_based_on_question_according_to_interviewer)})
    except:
        # Calling chatgpt to fix the json
        question_answer_pair = request.session['question_answer_pair']
        prompt = "Fix this JSON. Only give correct JSON answer : \n" + question_answer_pair
        if "chatgpt_key_interview_ready" not in request.session:
            return redirect('home')
        api_key = request.session['chatgpt_key_interview_ready']
        result,any_error = chatgpt(api_key,prompt)
        if any_error:
            url = reverse('home') + '?error=ChatGPT Key Expired'
            return redirect(url)
        question_answer_pair =result
        request.session['question_answer_pair'] = question_answer_pair

        # JSON fixed now evaluate
        question_answer_pair = request.session['question_answer_pair']
        print(question_answer_pair)
        
        # question_answer_pair = question_answer_pair.replace("'",'"')
        question_answer_pair = json.loads(question_answer_pair)
        # question_answer_pair = []
        overall_score = 0
        overall_grammar = 0
        overall_confidence = 0
        overall_clarity = 0
        overall_answer_score_based_on_question_according_to_interviewer = 0
        ques_ans_pair = []
        i=1
        for x in question_answer_pair:
            if type(x["confidence"]) != dict:
                y = json.loads(x["confidence"])
            else:
                y = x["confidence"]
            print(y)
            overall_grammar+= y["grammar"]
            overall_confidence+=y["confidence"]
            overall_clarity+=y["clarity"]
            if "answer_score_based_on_question_according_to_interviewer" in y:
                overall_answer_score_based_on_question_according_to_interviewer+=y["answer_score_based_on_question_according_to_interviewer"]
            if "score" in y:
                overall_answer_score_based_on_question_according_to_interviewer+=y["score"]
            

            #  Creating new array 
            temp_jso = {
                'question_number' : i,
                'question' : x["question"],
                'answer' : x['answer'],
                "grammar_score" : y["grammar"],
                "clarity_score" : y["confidence"],
                "confidence_score" : y["clarity"]
            }
            if "advice_to_improve_answer" in y and y["advice_to_improve_answer"] != "":
                temp_jso["advice"] = y["advice_to_improve_answer"]
            if "answer_score_based_on_question_according_to_interviewer" in y:
                temp_jso["interviewer_score"]=y["answer_score_based_on_question_according_to_interviewer"]
            if "score" in y:
                temp_jso["interviewer_score"]=y["score"]
            
            ques_ans_pair.append(temp_jso)
            i+=1
        overall_grammar=overall_grammar/7
        overall_clarity = overall_clarity/7
        overall_confidence=overall_confidence/7
        overall_answer_score_based_on_question_according_to_interviewer = overall_answer_score_based_on_question_according_to_interviewer/7
        overall_score=(overall_grammar + overall_confidence + overall_clarity + (10*overall_answer_score_based_on_question_according_to_interviewer))/13
        return JsonResponse({'question_answer_pair':ques_ans_pair,'overall_score':int(overall_score),'overall_grammar':int(overall_grammar),'overall_clarity':int(overall_clarity),'overall_confidence':int(overall_confidence),'overall_answer_score_based_on_question_according_to_interviewer':int(overall_answer_score_based_on_question_according_to_interviewer)})
        
def login(request):
    data = {
        "error_present" : False
    }
    if "error" in request.GET:
        error = request.GET["error"]
        data["error_present"] = True
        data["error"] = error
    print(data)
    return render(request,'login.html',{'data':data})

def login_user(request):
    email = request.POST['email']
    password = request.POST['password']
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        if user.password == password:
            if user.otp_verified == False:
                otp = ''.join(random.choices(string.ascii_uppercase +string.digits, k=6))
                user.otp = otp
                user.save()
                data_to_be_sent = "Here is your OTP for InterviewReady.ai. Please do not share it with anyone. OTP : " + otp + " ."
                # sendMail([email],data_to_be_sent)
                from_email = os.getenv('EMAIL_HOST_USER')
                subject = "OTP for InterviewReady.ai"
                send_mail(subject,data_to_be_sent,from_email,[email])
                return render(request,'otp.html',{'email':email})
            
            private_token  = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15))
            request.session['InterviewReady_privateToken'] = private_token
            user.private_key = private_token
            user.save()
            return redirect('home')
        else:
            url = reverse('login') + '?error=Invalid Password'
            return redirect(url)
    else:
        url = reverse('login') + '?error=Invalid Email'
        return redirect(url)
    
def signup(request):
    return render(request,'signup.html')

def signup_user(request):
    first_name = request.POST['f_name']
    last_name = request.POST['l_name']
    email = request.POST['email']
    password = request.POST['password']
    if User.objects.filter(email=email).exists():
        url = reverse('signup') + '?error=User Already Exists'
        return redirect(url)
    else:
        private_token  = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15))
        otp = ''.join(random.choices(string.ascii_uppercase +string.digits, k=6))
        user = User(email=email,password=password,private_key=private_token,otp=otp,first_name=first_name,last_name=last_name)
        user.save()
        data_to_be_sent = "Here is your OTP for InterviewReady.ai. Please do not share it with anyone. OTP : " + otp + " ."
        from_email = os.getenv('EMAIL_HOST_USER')
        subject = "OTP for InterviewReady.ai"
        send_mail(subject,data_to_be_sent,from_email,[email])
        request.session['InterviewReady_privateToken'] = private_token
        return render(request,'otp.html',{'email':email})

def otp_verify(request):
    email = request.POST['email']
    otp = request.POST['otp']
    print(request.POST)
    if User.objects.filter(email=email,otp=otp).exists():
        user = User.objects.get(email=email)
        user.otp_verified = True
        private_key = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15))
        user.private_key = private_key
        request.session['InterviewReady_privateToken'] = private_key
        user.save()
        return redirect('home')
    else:
        url = reverse('login') + '?error=Invalid OTP'
        return redirect(url)
    
def interview_mode(request):
    # user login in required
    user = user_logged_in(request)
    if not user:
        url = reverse('login')
        return redirect(url)
    return render(request,'interview_mode.html',{'user':user,'logged_in':True})
    
def user_logged_in(request):
    if "InterviewReady_privateToken" in request.session:
        private_token = request.session['InterviewReady_privateToken']
        if User.objects.filter(private_key=private_token).exists():
            return User.objects.get(private_key=private_token)
        else:
            return False
    else:
        return False

def interview_begin_premium(request):
    return render(request,'interview_begin_premium.html')

def logout(request):
    try:
        del request.session['InterviewReady_privateToken']
    except:
        pass
    return redirect('home')

def edit_profile(request):
    user = user_logged_in(request)
    if not user:
        url = reverse('login')
        return redirect(url)
    return render(request,'edit_profile.html',{'user':user,'logged_in':True})

def changeName(request):
    user = user_logged_in(request)
    if not user:
        url = reverse('login')
        return redirect(url)
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return JsonResponse({'data':'success'})

def changePassword(request):
    user = user_logged_in(request)
    if not user:
        url = reverse('login')
        return redirect(url)
    new_password = request.POST['new_pwd']
    user.password = new_password
    user.save()
    return JsonResponse({'data':'success'})

def deleteAccount(request):
    user = user_logged_in(request)
    if not user:
        url = reverse('login')
        return redirect(url)
    
    user.delete()
    return redirect('home')

def history(request):
    user = user_logged_in(request)
    if not user:
        url = reverse('login')
        return redirect(url)
    histories = History.objects.filter(user=user)
    for x in histories:
        words_in_job_desc = x.job_description.split(" ")
        if len(words_in_job_desc) > 5:
            x.job_description = ' '.join(words_in_job_desc[:5]) + '...'
    # reverse histories
    histories = histories[::-1]
    
    return render(request,'history.html',{'histories':histories,'user':user,'logged_in':True})



