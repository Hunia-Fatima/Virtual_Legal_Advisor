from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from . import views as user_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# ......




app_name = 'virtual_lawyer'

urlpatterns = [
    path('', user_views.index, name='Home'),
    path('about/', user_views.about, name='about'),
    path('chatbot/', user_views.chatbot, name= 'chatbot'),
    path('lawyers/', user_views.getLawyers, name= 'lawyers'),
    
    path('getChat/', views.getChat, name= 'getChat'),

    path('register', views.register, name="register"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('login', auth_views.LoginView.as_view(template_name='virtual_lawyer/login.html'), name="login"),
    path('logout', auth_views.LogoutView.as_view(template_name='virtual_lawyer/index.html'), name="logout"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)