from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index,name='index'),
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
    path('signup',views.signup,name='signup'),
    path('signup_user',views.signup_user,name='signup_user'),
    path("otp_verify", views.otp_verify, name="otp_verify"),
    path('login_user',views.login_user,name='login_user'),
    path('interview_mode',views.interview_mode,name='interview_mode'),
    path('interview_begin_premium',views.interview_begin_premium,name='interview_begin_premium'),
    path('logout',views.logout,name='logout'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('changeName',views.changeName,name="changeName"),
    path('changePassword',views.changePassword,name = "changePassword"),
    path('deleteAccount',views.deleteAccount,name="deleteAccount")


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)