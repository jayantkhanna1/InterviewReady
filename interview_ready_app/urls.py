from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index,name='index'),
    path('saveChatGptKey',views.saveChatGptKey,name='saveChatGptKey'),
    path('interview_info',views.interview_info,name='interview_info'),
    path('home',views.index,name='home'),
    # path("home_chatgpt_error", views.index_with_chatgpt_error, name=""),
    path('interview_information',views.interview_information,name='interview_information'),
    path('interview_begin',views.interview_begin,name='interview_begin'),
    path('asr',views.asr,name='asr'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)