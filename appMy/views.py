from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q
# Create your views here.
def index(request):
    
    product = Product.objects.all()
    category = Category.objects.all()
    
    query = request.GET.get('q')
    if query:
        product = product.filter(
            Q(title__icontains=query) |
            Q(desc__icontains=query) |
            Q(productCategory__title__icontains=query)
        ).distinct
    
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
        com = Comment(productComment=comment, product_id=id, user= request.user )
        com.save()
        
        return redirect('/detail/' + id + '/')
        
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

def addProduct(request,id):
    
    product = Product.objects.get(id=id)
    user = request.user
    cart = Cart.objects.create(user=user,product=product,piece=1, allprice = product.productPrice)
    
    cart.save()
    return redirect('cart')
    
def shopping(request):
    
    category = Category.objects.all()
    cart = Cart.objects.filter(user=request.user)
    total = 0
    
    for item in cart:
        total+=item.product.productPrice * item.piece
    
    context = {
        'cart':cart,
        'total':total,
        'category': category
    }
    return render(request,'shopping.html',context)

def deleteProduct (request,id):
    
    if request.method =='POST':
        cart_item = Cart.objects.get(id=id)
        cart_item.delete()
        
        return redirect('cart')
    
def updateProduct(request,id):
    
    if request.method == 'POST':
        cart_item =Cart.objects.get(id=id)
        quantity = int(request.POST.get('quantity',1))
        cart_item.piece =quantity
        cart_item.allprice = cart_item.product.productPrice * quantity
        cart_item.save()
        
        return redirect('cart')

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