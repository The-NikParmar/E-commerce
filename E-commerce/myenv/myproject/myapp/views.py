from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
import random

# Create your views here.
def index(request):
    return render(request,'index.html')

def home_2(request):
    return render(request,'home_2.html')

def home_3(request):
    return render(request,'home_3.html')

def shop(request):
    return render(request,'shop.html')

def shoping_cart(request):
    return render(request,'shoping_cart.html')

def blog(request):
    return render(request,'blog.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def signup(request):
    if request.POST:
        print(">>>>>>>>>>>page lode")
        try:
            print(">>>>>>>>>>>Email alredy exits page run")
            user = User.objects.get(uemail = request.POST["uemail"])
            print(">>>>>>>>>>>>> User object : ", user)
            msg1="Email Already Exist !!!"
            messages.error(request, msg1)
            return redirect('signup') 
        except:
            if request.POST['upassword'] == request.POST['ucpassword']:
                user = User.objects.create(
                    uname = request.POST['uname'],
                    uemail = request.POST['uemail'],
                    ucontact = request.POST['ucontact'],
                    upassword = request.POST['upassword'],
                )
                print(user.uname)
                msg = "Your Registration Done ...."
                print("============",msg)
                messages.success(request, msg)
                return render(request,'login.html')
            else:
                pmsg="Password and Confim Password Does Not Matched !!!"
                messages.error(request, pmsg)
                return render(request,'signup.html')
    else:
        return render(request,'signup.html')
    
def login(request):
     if request.POST:
        try:
            print("check password and email")
            user = User.objects.get(uemail = request.POST['uemail'],upassword = request.POST['upassword'])
            request.session['uemail'] = user.uemail
            request.session['uname'] = user.uname
            request.session['upassword'] = user.upassword
            print(">>>>>>>>>session start : ",request.session['uemail'])
            print(">>>>>>>>>>>> login successfully >>>>>>>>>>>>>>>>>...")
            msg = "Login successfully"
            messages.success(request,msg)
            return redirect('index')  
        except: 
            msg="Your email or password is not match !!!!"
            messages.error(request,msg)
            print(msg)
            return redirect('login')
     else:
       return render(request,'login.html')
     
def logout(request):
    del request.session['uemail']
    del request.session['uname']
    del request.session['upassword']
    print(">>>>>>>>>>>>>>>>>>>>>>>>LOGOUT")
    msg="Logout successfully"
    messages.success(request,msg)
    return redirect('login')


def change_password(request):
    if request.POST:
       print("page lode")
       user=User.objects.get(uemail=request.session['uemail'])

       if user.upassword == request.POST['old_password']:
           print("======Current password is match")

           if request.POST['new_password1'] == request.POST['new_password2']:
               print("========Page Loade new password and conifrm password match =========")
               user.upassword = request.POST['new_password2']
               user.save()
               return redirect('index')
           else:
               msg = "New Password conifrm  password Does not match..."
               messages.error(request,msg)
               return redirect('change_password')
           
       else:
           msg1="Current Password Does not match !!!"
           messages.error(request,msg1)
           return redirect('index')
    else:
        return render(request,"change_password.html")
    
def mymail(subject, template, to, context, otp):
    subject = subject
    template_str = 'myapp/' + template+'.html'
    context['otp'] = otp
    html_message = render_to_string(template_str, context)
    plain_message = strip_tags(html_message)
    from_email = 'nikhilparmar1015@gmail.com'
    send_mail(
        subject,
        plain_message,
        from_email,
        [to],
        html_message=html_message,
        fail_silently=False,
    )
    
def fpassword(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(uemail=request.POST['uemail'])
            otp = random.randint(1000, 9999)
            print(otp)
            subject = "OTP for Password Reset"
            template = "etemplate"
            to = user.uemail
            context = {'user': user.uname}
            mymail(subject, template, to, context, otp)
            print("otp sent successfully")
            request.session['otp']=otp
            return render(request, "otp.html", {'uemail':user.uemail,'otp':str(otp)})
        except User.DoesNotExist:
            pass
    return render(request, "fpassword.html")


def otp(request):
    if request.method == 'POST':
        try:
            otp=request.session['otp']
            uotp = int(request.POST['uotp'])

            if otp == uotp:
                # OTP is correct, redirect to reset password page
                return redirect('reset_password')
            else:
                msg1 = "OTP Doesn't Matched !!!"
                return render(request, 'otp.html', {'msg1': msg1, 'uotp': uotp})
        except ValueError:
            # Handle the case when 'otp' or 'otp_sent' is not an integer
            msg1 = "Invalid OTP Format. Please enter a valid numeric OTP."
            return render(request, 'otp.html', {'msg1': msg1})
    else:
        return render(request, 'otp.html')
    

def reset_password(request):
    user = User.objects.get(uemail=request.POST['uemail'])
    if request.POST:
        if request.POST['npassword']==request.POST['cnpassword']:
            user.upassword = request.POST['npassword']
            user.save()
            return render(request,'login.html')
        else:
            print("new password and conifrm password dose not match ")
    else:
        return render(request,"reset_password.html")


    



