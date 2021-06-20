from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from django.http import HttpResponseRedirect
from .models import *

# Create your views here.


def index(request):
    return render(request, 'login.html')
    
def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'groups': Group.objects.all(),
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'success.html', context)

def register(request):
    #create a user
    if request.method=='POST':
        errors=User.objects.validator(request.POST)
        if errors:#if a user doesnt pass validation it will throw an error at the top of the screen
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        ## encrypt pw
        #store pw
        user_pw = request.POST['pw']
        #hash the pw
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        
        
        new_user=User.objects.create(#if it passes validation, new user will be created here
            first_name=request.POST['f_n'],
            last_name=request.POST['l_n'],
            email=request.POST['email'],
            password=hash_pw,
            )
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/success')
    return redirect('/')
    
    
    
def login(request):
    if request.method=='POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/success')#if it is a post it checks email if email is in database it assigns it a logged user and checks to see if logged user's passwords match
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def new(request):
    return render(request, 'new.html')

def create(request):
    errors = Group.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    Group.objects.create(
        group_name = request.POST['group_name'],
        description = request.POST['description'],
        prayer_list = request.POST['prayer_list'], 
    )
    return redirect('/success')

def group(request, group_id):
    a_group = Group.objects.get(id=group_id)
    group_messages = Wall_Message.objects.filter(group_id = group_id)
    context = {
        'group' : a_group,
        'group_messages': group_messages
    }
    return render(request, 'group.html', context)

#def addUserToGroup(request, group_id):
 #   userId = request.session['user_id']
  #  a_group = Group.objects.get(id=group_id) #dont actually need group object
   # #First Create a mappging from User to Group (table)
    #here you will write to that table both the foregn keys user id and group id 
    #return redirect('/success')


def joinGroup(request, group_id):
    user = User.objects.get(id=request.session["user_id"])
    group = Group.objects.get(id=group_id)
    user.users_groups.add(group)
    return redirect('/success')

def post_mess(request, group_id):
    Wall_Message.objects.create(
        message=request.POST['mess'],
        poster=User.objects.get(id=request.session['user_id']),
        group=Group.objects.get(id=group_id)
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def user_profile(request, user_id):
    # user_testi=User.objects.create(
    #     user_testimony=request.POST['testi']
    #     )
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'groups': Group.objects.all(),
        'user': User.objects.get(id=request.session['user_id']),
        'isSignedInUser': user.id == user_id,
    }
    return render(request, 'user.html', context)

def create_testimony(request, user_id):
    signed_in_user = User.objects.get(id=request.session['user_id'])
    signed_in_user.user_testimony=request.POST.get('testi')
    signed_in_user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
