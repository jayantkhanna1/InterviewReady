from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index,name='index'),
    path('saveChatGptKey',views.saveChatGptKey,name='saveChatGptKey'),
    path('interview_info',views.interview_info,name='interview_info'),
    path('home',views.index,name='home'),
    path('interview_information',views.interview_information,name='interview_information'),
    path('interview_begin',views.interview_begin,name='interview_begin'),
    path('asr',views.asr,name='asr'),
    path('getResultForOnePair',views.get_result_for_one_pair,name='getResultForOnePair'),
    path('saveInterviewResult',views.save_interview_result,name='saveInterviewResult'),
    path('showInterviewResult',views.show_interview_result,name='showInterviewResult'),
    path('evaluateResult',views.evaluate_result,name='evaluate_result'),
    path('login',views.login,name='login'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)