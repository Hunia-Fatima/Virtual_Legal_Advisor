
from django.contrib.auth.models import User
from .forms import UserRegisrationForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse,HttpResponse
from .models import Chatbot,Lawyer
from django.views.decorators.csrf import csrf_exempt

from django.contrib.sites.shortcuts import get_current_site  
from .tokens import account_activation_token 
from django.utils.encoding import force_bytes, force_text  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string


# Create your views here.
def index(request):
    return render(request, 'virtual_lawyer/index.html')

def about(request):
    return render(request,'virtual_lawyer/about.html')
@login_required
@csrf_exempt
def chatbot(request):
    return render(request, 'virtual_lawyer/chatbot.html')
@csrf_exempt
def getChat(request):
    # bot = Chatbot()
    myBot, mySettings = Chatbot.get_ChatBot()
    botResponse = ''
    if request.method == "POST":
        User = request.POST["talk"]
        botResponse = myBot.get_response(User,myBot, mySettings)
        print(botResponse)
        print("printing bot response***************************************")
        return HttpResponse(botResponse)
    else:
        return HttpResponse(botResponse)



def register(request): 
    if request.method == 'POST':  
        form = UserRegisrationForm(request.POST)  
        # print(form.errors.as_data())  
        if form.is_valid():  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            current_site = get_current_site(request)  
            mail_subject = 'Activate your account.'  
            msg = {                
                'user': user,  
                'domain': current_site.domain,  
                'uid': urlsafe_base64_encode(force_bytes(user.id)),  
                'token': account_activation_token.make_token(user),
                }
            message = render_to_string('virtual_lawyer/activate.html',{  
                'user': user,  
                'domain': current_site.domain,  
                'uid': urlsafe_base64_encode(force_bytes(user.id)),  
                'token': account_activation_token.make_token(user),  
            })
            to_email = form.cleaned_data.get('email')  
            print(to_email)
            email = EmailMultiAlternatives(  
                mail_subject, message, to=[to_email]  
            )  
            html_body = render_to_string("virtual_lawyer/activate.html", msg)
            email.attach_alternative(html_body, "text/html")
            email.send()  
            return render(request, 'virtual_lawyer/confirmationPage.html')
            # return HttpResponse('Please confirm your email address to complete the registration') 
  
    else:  
        form = UserRegisrationForm()  
    return render(request, 'virtual_lawyer/register.html', {'form': form})


def activate(request, uidb64, token):  
        try:  
            uid = force_text(urlsafe_base64_decode(uidb64))  
            user = User.objects.get(id=uid)  
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is not None and account_activation_token.check_token(user, token):  
            user.is_active = True  
            user.save()  
            return render(request, 'virtual_lawyer/accountActivationConfirmed.html')
            # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
        else:  
            return HttpResponse('Activation link is invalid!')

def getLawyers(request):
    all_lawyers = Lawyer.objects.all()
    return render(request, 'virtual_lawyer/lawyers.html', {'all_lawyers': all_lawyers})




#integration of new model





#end


