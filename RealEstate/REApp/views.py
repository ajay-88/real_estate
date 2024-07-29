
from django.shortcuts import render, redirect
from REApp.models import RegistrationDB, PropertyDB, Feedback
from django.contrib import messages
import re
from REApp.forms import Feedback_form
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import View,CreateView
from django.urls import reverse_lazy


# Create your views here.
# logined user home page
def home(request):
    if 'userid' in request.session:
        
        profile = RegistrationDB.objects.get(UserId=request.session['userid'])
        
        return render(request,'index.html',{'profile':profile})
    else:
        return render(request, "index.html")


# class Indexview(View):
#     def get(self,request,*args,**kwargs):
#         if 'userid' in request.session:
#             profile = RegistrationDB.objects.get(UserId=request.session['userid'])
#             return render(request, "index.html", {'profile': profile})
#         else:
#             return render(request,"index.html")
    
#     def post(self,request,*args,**kwargs):
#         form=request.POST
#         print(request.POST)

# login page
def login(request):
    return render(request, "login.html")

# Registration page
def registration(request):
    return render(request, "register.html")

#registration code
from django.contrib import messages

def save_registration(request):
    if request.method == "POST":
        n = request.POST.get('name')
        e = request.POST.get('email')
        p = request.POST.get('password')
        r = request.POST.get('role')

        # Check if any of the required fields are empty
        if not (n and e and p and r):
            messages.error(request, "Please fill all the fields.")
            return redirect(registration)

        if RegistrationDB.objects.filter(Email=e).exists():
            messages.error(request, "Email Id already exists..!!")
            return redirect(registration)
        
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$", p):
            messages.error(request, "Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
            return redirect(registration)

        obj = RegistrationDB(Name=n, Email=e, Password=p, Role=r)
        obj.save()
        messages.success(request, "Registration Successfully Completed..!!")
        return redirect(login)


# login code
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        un = request.POST.get('email')
        pwd = request.POST.get('password')
        
        if not un or not pwd:
            # If email or password is missing, display a message
            messages.error(request, "Please enter both email and password")
            return redirect(login)
        
        if RegistrationDB.objects.filter(Email=un, Password=pwd).exists():
            request.session['Email'] = un
            request.session['Password'] = pwd
            user = RegistrationDB.objects.get(Email=un, Password=pwd)
            request.session['userid'] = user.UserId
            messages.success(request, "Logged in Successfully..!!")
            return render(request, "index.html")
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect(login)
    return redirect(login)


# user logout
def user_logout(request):
    del request.session['Email']
    del request.session['Password']
    del request.session['userid']
    return redirect(home)

# property adding
def add_property(request):
    if 'userid' in request.session:
        profile = RegistrationDB.objects.get(UserId=request.session['userid'])
        return render(request, "addProperty.html", {'profile': profile})
    else:
        return redirect(login)

# property saving to the database
def save_property(request):
    if request.method == "POST":
        pu = request.POST.get('purpose')
        ty = request.POST.get('type')
        ti = request.POST.get('title')
        de = request.POST.get('description')
        pr = request.POST.get('price')
        lo = request.POST.get('location')
        ph = request.POST.get('phone')
        uid = RegistrationDB.objects.get(UserId=request.session['userid'])
        img = request.FILES['image']
        pdf = request.FILES.get('pdf')
        obj = PropertyDB(Purpose=pu, Type=ty, Title=ti, Price=pr, Location=lo, Phone=ph, UserId=uid, Description=de, Image=img, PDF=pdf)
        obj.save()
        messages.success(request, "Property Posted Successfully")
        return redirect(home)

# list all properties
def property_list(request):
    pdata = PropertyDB.objects.all()
    if 'userid' in request.session:
        profile = RegistrationDB.objects.get(UserId=request.session['userid'])
       
        return render(request, "propertyList.html", {'profile': profile, 'pdata': pdata })
    else:
        return render(request, "propertyList.html", {'pdata': pdata})

# 

def search(request):
    if request.method=="POST":
            # price=request.POST.get("price")
            p_type=request.POST.get("type")
            location=request.POST.get("location")
            data=PropertyDB.objects.filter(Type=p_type,Location=location)
            print(data)
            print(p_type,location)
            return render(request, "propertyList.html", {'data':data})


def my_post(request):
    pdata = PropertyDB.objects.filter(UserId_id=request.session['userid'])
    if 'userid' in request.session:
        profile = RegistrationDB.objects.get(UserId=request.session['userid'])
        return render(request, "myPost.html", {'profile': profile, 'pdata': pdata})
    else:
        return redirect(home)


def view_post(request, postId):
    post = PropertyDB.objects.get(PropertyId=postId)
    if 'userid' in request.session:
        profile = RegistrationDB.objects.get(UserId=request.session['userid'])
        return render(request, "viewPost.html", {'profile': profile, 'post': post})
    else:
        return render(request, "viewPost.html", {'post': post})


def delete_post(request, postId):
    data = PropertyDB.objects.get(PropertyId=postId)
    data.delete()
    messages.error(request, "Post Removed..!!")
    return redirect(property_list)


def edit_post(request, postId):
    post = PropertyDB.objects.get(PropertyId=postId)
    if 'userid' in request.session:
        profile = RegistrationDB.objects.get(UserId=request.session['userid'])
        return render(request, "editPost.html", {'profile': profile, 'post': post})
    else:
        return render(request, "editPost.html", {'post': post})


def update_post(request, postId):
    if request.method == "POST":
        lo = request.POST.get('location')
        ty = request.POST.get('type')
        pu = request.POST.get('purpose')
        pr = request.POST.get('price')
        ph = request.POST.get('phone')
        ti = request.POST.get('title')
        de = request.POST.get('description')

        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = PropertyDB.objects.get(PropertyId=postId).Image
        PropertyDB.objects.filter(PropertyId=postId).update(Location=lo, Type=ty, Purpose=pu, Price=pr, Phone=ph, Title=ti, Description=de, Image=file)
        messages.success(request, "Post updated successfully..!!")
        return redirect(my_post)
    
class Feed(CreateView):
    template_name="feedback.html"
    model=Feedback
    form_class=Feedback_form
    success_url=reverse_lazy('home')