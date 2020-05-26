from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from blog.models import Post
# Create your views here.
def home(request):
    allposts=Post.objects.all()
    context={'allposts':allposts}
    return render(request,'home/home.html',context)

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,'Please fill the form correctly')
        else:
            contact= Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,'Thank You! Your details has been submitted')
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')


def search(request):
    search=request.GET['search']
    if len(search)>80:
        allposts=Post.objects.none()
    else:
        allpostsTitle=Post.objects.filter(title__icontains=search)
        allpostsContent=Post.objects.filter(content__icontains=search)
        allposts=allpostsTitle.union(allpostsContent)
    
    if allposts.count()==0:
        messages.warning(request,"No Search results found.Please refine your query.")
    context={'allposts':allposts,'search':search}
    return render(request,'home/search.html',context)


def handleSignup(request):
    if request.method=="POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #check for errorneous inputs
        #Username must be under 10 characters 
        if len(username) > 10:
            messages.error(request,"Username must be under 10 characters")
            return redirect('home')

        #Username must contain alphanumeric characters
        if not username.isalnum():
            messages.error(request,"Username must contain alphanumeric characters")
            return redirect('home')

        #for checking passwords
        if pass1 != pass2:
            messages.error(request,"Passwords do not match")
            return redirect('home')


        #Create the User
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your vCoder account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse("404-Not Found")
               

def handleLogin(request):
    if request.method=="POST":
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"You are successfully logged in")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials! Please try again")
            return redirect('home')
    
    return HttpResponse("404-Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request,"You are successfully logged out")
    return redirect('home')
