from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib import messages,auth
from django.contrib.auth.models import User
from .models import Profile,Post_Upload,Post_Like,FollowersCount
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='signin')
def Home(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post_Upload.objects.all()
    context = {"posts":posts,"profile":profile}
    return render(request,'index.html',context)


def SignUp(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        Password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        if Password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email is already taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.warning(request , "Username is already taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=Password)
                user.save()

                #log user 
                user_log = auth.authenticate(username=username,password=Password)
                auth.login(request, user_log)

                #add to profile db
                user_model = Profile.objects.create(
                    user=request.user,
                    username=username,
                    name=name,
                    email=email,
                    password=Password
                )

                return redirect('home')
        else:
            messages.warning(request , "Password doesn't match")
            return redirect('signup')


        


    context = {}
    return render(request, 'signup.html',context)

def SignIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.warning(request, "Invalid")
    context = {}
    return render(request, 'signin.html',context)


@login_required(login_url='signin')
def Logout(request):
    
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def Profile_view(request,pk):
    user_object = User.objects.get(username=pk)
    
    if request.method == "POST":
        follower_username = request.POST['follower']
        user_username = request.POST['user']
        
        # Get User model instances based on usernames
        follower_user = User.objects.get(username=follower_username)
        user_user = User.objects.get(username=user_username)

        if FollowersCount.objects.filter(follower=follower_user,user=user_user).first():
            delete_follower = FollowersCount.objects.get(follower=follower_user,user=user_user)
            delete_follower.delete()
            
        else:
            add_follower = FollowersCount.objects.create(follower=follower_user,user=user_user)
            add_follower.save()
    return redirect('profile',pk=pk)

    text_button = ""
    followers = request.user.username
    user = pk
    user_user = User.objects.get(username=user)
    followers_followers = User.objects.get(username=followers)
    if FollowersCount.objects.filter(follower=followers_followers,user=user_user).first():
        text_button = "Unfollow"
    else:
        text_button = "Follow"


    following_count = FollowersCount.objects.filter(follower=user_object).count()
    followers_count = FollowersCount.objects.filter(user=user_object).count()


    user_profile = Profile.objects.get(user=user_object)
    user_post = Post_Upload.objects.filter(user=user_object)

    post_count = user_post.count()
    context = {
        "user_profile":user_profile,
        "user_post":user_post,
        "post_count":post_count,
        "following_count":following_count,
        "followers_count":followers_count,
        "text_button":text_button
        }
    return render(request, 'profile.html',context)

@login_required(login_url='signin')
def Setting(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if request.FILES.get('image') == None:
            image = profile.profileImg
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            bio = request.POST['bio']

            profile.name = name
            profile.username = username
            profile.email = email
            profile.profileImg = image
            profile.bio = bio
            profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            bio = request.POST['bio']

            profile.name = name
            profile.username = username
            profile.email = email
            profile.profileImg = image
            profile.bio = bio
            profile.save()

        return redirect('home')



    context = {"profile":profile}
    return render(request, 'setting.html',context)



def Upload(request):
    
    if request.method == "POST":
        user = request.user
        profile_pic = Profile.objects.get(user=user)
        image = request.FILES.get('image')
        caption = request.POST['caption']

        new_Post = Post_Upload.objects.create(user=user, image=image , caption=caption,profile_pic=profile_pic)
        new_Post.save()
        return redirect("home")
    else:
        return redirect('home')


def Post_like(request):
    user = request.user
    post_id = request.GET.get('post_id')
    
    post = Post_Upload.objects.get(id=post_id)

    like_filter = Post_Like.objects.filter(user=user , post_id=post_id).first()

    if like_filter == None:
        new_like = Post_Like.objects.create(user=user , post_id=post_id)
        new_like.save()
        post.no_of_like = post.no_of_like+1
        post.save()
        return redirect('home')
    else:
        like_filter.delete()
        post.no_of_like = post.no_of_like-1
        post.save()
        return redirect('home') 
