from django.db import models 

class User(models.Model):
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    otp = models.CharField(max_length=200)
    otp_verified = models.BooleanField(default=False)
    private_key = models.CharField(max_length=200)
    free_trials_left = models.IntegerField(default=3)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

class History(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    job_description = models.CharField(max_length=2000000)
    special_words = models.CharField(max_length=20000,default="None")
    interview_type = models.CharField(max_length=20000)
    interview_date = models.DateTimeField(blank=True,null=True)
    interview_result = models.JSONField(null=True,blank=True)
    interview_difficulty = models.CharField(max_length=20000)
    interview_duration = models.CharField(max_length=20000,default="00:00:00")
    interview_completed = models.BooleanField(default=False)
    overall_score = models.IntegerField(default=0)
    prompt = models.CharField(max_length=2000000,null=True,blank=True)
    overall_grammar = models.IntegerField(default=0)
    overall_clarity = models.IntegerField(default=0)
    overall_confidence = models.IntegerField(default=0)
    overall_answer_score_based_on_question_according_to_interviewer = models.IntegerField(default=0)