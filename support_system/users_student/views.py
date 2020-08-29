from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from complaint.models import Complaint
from support_system.views import append_likes
from .models import student
from django.core.files.storage import FileSystemStorage


def username_avaliable(request):
    username = request.GET.get('username', None)
    print(username)
    data = {
        "is_valid": User.objects.filter(email=username).exists()
    }
    return JsonResponse(data)


def username_available_login(request):
    username = request.GET.get('username', None)
    password = request.GET.get('password',None)
    print(password)
    print(username)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        if student.objects.filter(user=user).exists():
            status = True
        else:
            status=False
    else:
        status = False

    data = {
        "is_valid": status
    }
    return JsonResponse(data)

def register_student(request):

    if request.method == 'POST':
        first_name = request.POST.get('txtFirstname_student')
        last_name = request.POST.get('txtLastname_student')
        college_id = request.POST.get('txtCollegeID_student')
        gender = request.POST.get('lstGender_student')
        dob = request.POST.get('txtDob_student')
        branch = request.POST.get('txtBranch_student')
        college_name = request.POST.get('collage_student')
        email = request.POST.get('txtEmail_student')
        phone_no = request.POST.get('txtStudphone_student')
        address = request.POST.get('txtResaddress_student')
        password = request.POST.get('txtPasswd1_student')
        cnf_password = request.POST.get('txtPasswd2_student')

        if not User.objects.filter(username=email).exists():
            user_obj = User.objects.create_user(username=email, password=password, email=email)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.save()

            user = authenticate(request, username=email, password=password)

            student_details = student(user=user, college_id=college_id,dob=dob,gender=gender, college_name=college_name,branch=branch,
                                      phone_no=phone_no,address=address)
            student_details.save()

        return redirect('/login')


def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('txtEmail_student')
        password = request.POST.get('txtPasswd1_student')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')


def student_profile(request):
    requested_data = request.GET.get('requesteddata')
    user_name = request.GET.get('user_name')
    print(requested_data)
    print(user_name)

    if user_name is None:
        user_name = request.user.username
    print(user_name)

    if request.user.is_authenticated and user_name == request.user.username:
        print("---------------------------utkarsh---------------------------------------")
        posts = []
        userdata = student.objects.get(user=request.user)

        if requested_data is None:
            requested_data = "all"

        if requested_data == "all":
            postsobj = Complaint.objects.filter(user=request.user)
            for post in postsobj:
                posts.append(post)
        if requested_data == "pending":
            posts = Complaint.objects.filter(user=request.user).filter(status="pending")
        if requested_data == "ongoing":
            posts = Complaint.objects.filter(user=request.user).filter(status="ongoing")
        if requested_data == "solved":
            posts = Complaint.objects.filter(user=request.user).filter(status="solved")
        if requested_data == "upvoted":
            posts = []
            likedpostids = userdata.liked_complaint
            likedpostids = likedpostids.split(",")
            if "" in likedpostids:
                likedpostids.remove("")
            for likedpostid in likedpostids:
                if Complaint.objects.filter(id=likedpostid).exists():
                    posts.append((Complaint.objects.get(id=likedpostid)))
                else:
                    likedpostids.remove(likedpostid)
        if requested_data == "rejected":
            posts = Complaint.objects.filter(user=request.user).filter(status="rejected")
        print(posts)
        posts = append_likes(request, posts)
        return render(request, 'users_student/student_profile2.html',
                      {"usernmae": request.user.username, "userdata": userdata, "posts": posts,
                       'requested_data': requested_data})
    else:
        if User.objects.filter(username=user_name).exists():
            user = User.objects.get(username=user_name)
            userdata = student.objects.get(user=user)
            posts = Complaint.objects.filter(user=User.objects.get(username=user_name))
            return render(request, 'users_student/student_profile_another.html',
                          {"usernmae": request.user.username, "userdata": userdata, "posts": posts})
        print("user doesn't exists")
        return redirect('/users_student/login/')


def update_profile(request):
    if request.user.is_authenticated:
        email = request.GET.get('email')
        phone_no = request.GET.get('phone_no')
        college_id = request.GET.get('college_id ')
        college_name = request.GET.get('college_name')
        password = request.GET.get('password')
        profile_pic = request.GET.get('profile_pic')

        image = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        print("Profile picture")
        print(profile_pic)
        print("Profile picture")

        user = authenticate(request, username=request.user.email, password=password)
        if user is None:
            data = {
                "is_updated": "false"
            }
            return JsonResponse(data)

        if student.objects.filter(user=request.user).exists():
            userobj = student.objects.get(user=request.user)
            userobj.phone_no = phone_no
            userobj.college_id = college_id
            userobj.college_name = college_name
            userobj.profile_pics = profile_pic
            userobj.url = uploaded_file_url
            user = User.objects.get(email=request.user.email)
            user.email = email
            user.username = email

            if not User.objects.filter(email=request.user.email).exists():
                data = {
                    "is_updated": "false"
                }
                return JsonResponse(data)

            if User.objects.filter(email=email).exists() and request.user.email != email:
                data = {
                    "is_updated": "false"
                }
                return JsonResponse(data)

            if user.username == email and user.email == email and userobj.college_name == college_name and \
                    userobj.college_id == college_id and userobj.phone_no == phone_no and \
                    userobj.url == uploaded_file_url :
                data = {
                    "is_updated": "false"
                }
                return JsonResponse(data)

            user.save()
            userobj.save()
            logout(request)
            user_auth = authenticate(request, username=email, password=password)
            login(request, user_auth)
            data = {
                "is_updated": "true"
            }
            return JsonResponse(data)
    else:
        data = {
            "is_updated": "false"
        }
        return JsonResponse(data)
