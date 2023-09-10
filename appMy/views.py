from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login,logout,authenticate
# Create your views here.
def index(request):
    
    product = Product.objects.all()
    category = Category.objects.all()
    
    context = {
        'product': product,
        'category': category
    }
    
    return render(request, 'index.html', context)

def detail(request, id):
    
    product = Product.objects.get(id=id)
    category = Category.objects.all()
    comments = Comment.objects.filter(product_id=id)
    
    if request.method == 'POST':
        comment = request.POST["comment"]
        com = Comment(productComment=comment, product_id=id)
        com.save()
        
    context = {
        'product': product,
        'category': category,
        'comments': comments
    }
    
    return render(request, 'detail.html', context)

def category(request, id):
    
    category = Category.objects.all()
    product = Product.objects.filter(productCategory=id)
    
    context = {
        'category': category,
        'product': product
    }
    
    return render(request, 'category.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            
            return redirect('homepage')
        else:
            context = {
                'information':'Girmiş olduğunuz bilgiler hatalıdır. Tekrar deneyiniz.'
            }
        
            return render(request,'part/login.html',context)
    
    return render(request,'part/login.html')
    


def signup(request):
    if request.method == 'POST':
        firstname=request.POST['firstname']
        lastname =request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password==password2:
            if User.objects.filter(username=firstname).exists():
                context = {
                    'information':'Böyle bir kullanıcı mevcut, farklı bir kullanıcı adıyla deneyin'
                }
                return render(request,'part/register.html',context)
            
            if User.objects.filter(email=email).exists():
                context = {
                    'information':'Sisteme kaydetmek istediğiniz e-posta adresi kullanılmaktadır. Farklı bir e-posta adresiyle kayıt olmayı deneyin.'
                }
                
                return render (request,'part/register.html',context)
            
            else: 
                user = User.objects.create_user(username=firstname,last_name=lastname,first_name=firstname,email=email,password=password)
                user.save()
                
                context = {
                    'information':'Kayıt işleminiz gerçekleştirilmiştir.'
                }
                
                return render(request,'part/register.html',context)
        else:
            context = {
                'information':'Parolanız girdiğiniz parolayla uyuşmuyor, kontrol ederek tekrar deneyin.'
            }
            
            return render(request,'part/register.html',context)
    
    return render(request,'part/register.html')

def exit(request):
    
    logout(request)
    
    return redirect('homepage')

def profile(request):
    
    if request.user.is_authenticated:       
        try:
            appMy_profile = Profile.objects.get(user=request.user)
                
        except Profile.DoesNotExist:
            appMy_profile = Profile(user=request.user)
            appMy_profile.save()
                
    if request.method =="POST" and 'profile-img-btn' in request.POST:
        filee = request.FILES.get('profile-img')
        
        if filee:
            appMy_profile.profile_img =filee
            appMy_profile.save()
            
            
    if request.method == "POST" and 'person-btn' in request.POST:
        
        user = request.user
        user.username = request.POST['username']
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.email = request.POST['email']
        
        user.save()                
    context ={
        'appMy_profile': appMy_profile
    }
    return render(request,'profile.html',context)