from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
from products.models import Product
import re

# Create your views here.


def signin(request):
    if request.method == 'POST' and 'btnlogin' in request.POST:
        # messages.info(request,'this is post')        
        # messages.info(request,'this is btnlogin')
        if 'user' in request.POST:
            username = request.POST['user']

        if 'pass' in request.POST:
            password = request.POST['pass']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
            # messages.success(request,'You are now logged in')
            return render(request , 'pages/index.html')
        else:
            messages.error(request,'Username or Password incorrect')

        return render(request,'accounts/signin.html', {'user':username})
    else:
        return render(request , 'accounts/signin.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('signin')


def signup(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:
        # variables for fields
        fname = None
        lname = None
        address = None
        address2 = None
        city = None
        state = None 
        zip = None
        email = None
        username = None
        password = None
        terms = None
        is_added = None

        #gat values from form
        if 'fname' in request.POST:
            fname = request.POST['fname']
        else:
            messages.error(request, 'Error in Firstname')

        if 'lname' in request.POST:
            lname = request.POST['lname']
        else:
            messages.error(request, 'Error in Lastname')

        if 'address' in request.POST:
            address = request.POST['address']
        else:
            messages.error(request, 'Error in Address')

        if 'address2' in request.POST:
            address2 = request.POST['address2']
        else:
            messages.error(request, 'Error in Address2')

        if 'city' in request.POST:
            city = request.POST['city']
        else:
            messages.error(request, 'Error in City')

        if 'state' in request.POST:
            state = request.POST['state']
        else:
            messages.error(request, 'Error in State')

        if 'zip' in request.POST:
            zip = request.POST['zip']
        else:
            messages.error(request, 'Error in zip')

        if 'email' in request.POST:
            email = request.POST['email']
        else:
            messages.error(request, 'Error in Email')

        if 'user' in request.POST:
            username = request.POST['user']
        else:
            messages.error(request, 'Error in Username')

        if 'pass' in request.POST:
            password = request.POST['pass']
        else:
            messages.error(request, 'Error in Password')

        if 'terms' in request.POST:
            terms = request.POST['terms']
        
        # check value of fields
        if fname and lname and address and address2 and city and state and zip and username and password and email:
            if terms == 'on':
                # check if username already exist
                if User.objects.filter(username=username).exists():
                   messages.error(request, 'username already exists') 
                else:
                    # check if email exists
                    if User.objects.filter(email=email).exists():
                      messages.error(request, 'This Email already exists')   
                    else:
                        pattern = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(pattern,email):
                            # add user
                            user = User.objects.create_user(first_name=fname,last_name=lname,
                            email=email,
                            username=username,
                            password=password)
                            user.save()
                            # add user profile
                            userprofile = UserProfile(user=user,address=address,address2=address2,city=city,state=state,zip=zip)
                            userprofile.save()

                            #clear fields
                            fname = ''
                            lname = ''
                            address =''
                            address2 =''
                            city = ''
                            state = ''
                            zip = ''
                            email = ''
                            username = ''
                            password = ''
                            terms = None

                            # success message
                            messages.success(request, 'your account has been created successfully') 
                            is_added = True
                        else:
                            messages.error(request, 'invalid email') 
            else:
                messages.error(request, 'you have to agree terms')
        else:
            messages.error(request, 'check empty fields')
        
        #messages.info(request,'this is post and signup')
        return render(request , 'accounts/signup.html',{
            'fname':fname,
            'lname':lname,
            'address':address,
            'address2':address2,
            'city':city,
            'state':state,
            'zip':zip,
            'email':email,
            'user':username,
            'pass':password,
            'is_added':is_added
        })
    else:
        return render(request , 'accounts/signup.html')


def profile(request):
    
    if request.method == 'POST' and 'btnsave' in request.POST:

        if request.user is not None and request.user.id != None:

            userprofile = UserProfile.objects.get(user=request.user)

            if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['address2'] and request.POST['city'] and request.POST['state'] and request.POST['zip'] and request.POST['email'] and request.POST['user'] and request.POST['pass']:
                
                request.user.first_name = request.POST['fname']
                request.user.last_name = request.POST['lname']
                userprofile.address = request.POST['address']
                userprofile.address2 = request.POST['address2']
                userprofile.city = request.POST['city']
                userprofile.state = request.POST['state']
                userprofile.zip = request.POST['zip']
                # request.user.email = request.POST['email']
                # request.user.username = request.POST['user']
                
                if not request.POST['pass'].startswith('pbkdf2_sha256$'):  # encode password
                    request.user.set_password(request.POST['pass'])
                
                else:  
                    request.user.password = request.POST['pass']

                request.user.save()
                userprofile.save()
                auth.login(request,request.user)

                messages.success(request, 'your data has been saved')

                # to keep values in fields after save
                userprofile = UserProfile.objects.get(user=request.user)

                context = {
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'address':userprofile.address,
                    'address2':userprofile.address2,
                    'city':userprofile.city,
                    'state':userprofile.state,
                    'zip':userprofile.zip,
                    'email':request.user.email,
                    'user':request.user.username,   
                    'pass':request.user.password
                }
                return render(request , 'accounts/profile.html',context)
                
            else:
               messages.error(request, 'check your values')  

        #messages.info(request,'this is post and save')
        return redirect('profile')
    else:
       
        if request.user is not None:

            context = None

            if not request.user.is_anonymous:

                userprofile = UserProfile.objects.get(user=request.user)

                context = {
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'address':userprofile.address,
                    'address2':userprofile.address2,
                    'city':userprofile.city,
                    'state':userprofile.state,
                    'zip':userprofile.zip,
                    'email':request.user.email,
                    'user':request.user.username,   
                    'pass':request.user.password
                }
            return render(request , 'accounts/profile.html', context)
        else:
            return redirect('index')

        
def product_favourite(request , pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)

        #check if favourit product has been added before or not
        if UserProfile.objects.filter(user=request.user,product_favourites=pro_fav).exists():
            messages.info(request, 'this product alread exists in favourites')
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_favourites.add(pro_fav)
            messages.success(request,'this product has been added to favourites')

        
    else:
         messages.error(request,'You have to login first')
    return redirect('/products/' + str(pro_id))


def show_product_favourite(request):
    context = None

    if request.user.is_authenticated and not request.user.is_anonymous:
        userprofile = UserProfile.objects.get(user=request.user)
        pro_fav = userprofile.product_favourites.all()
        context = {
            'products':pro_fav
        }

    return render(request , 'products/products.html' , context)