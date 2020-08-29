from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import CommitteeMember, Otp


def register_admin(request):
    if request.POST:
        first_name = request.POST.get('txtFirstname_admin')
        last_name = request.POST.get('txtLastname_admin')
        gender = request.POST.get('lstGender_admin')
        dob = request.POST.get('txtDob_admin')
        branch = request.POST.get('branch_admin')
        phone_no = request.POST.get('txtStudphone_admin')
        username = request.POST.get('username_admin')
        committee = request.POST.get('level_admin')
        college = request.POST.get('college_admin')
        teacher_id = request.POST.get('txtCollegeID_admin')
        email = request.POST.get('txtEmail_admin')
        password = request.POST.get('txtPasswd1_admin')
        address = request.POST.get('txtResaddress_admin')
        cnf_password = request.POST.get('txtPasswd2_admin')

        if not User.objects.filter(username=username).exists():
            user_obj = User.objects.create_user(username=username, password=password, email=email)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.save()

        user = authenticate(request, username=username, password=password)
        committee_obj = CommitteeMember(user=user, committee=committee, phone_no=phone_no,address=address,
                                        college=college, teacher_id=teacher_id,gender=gender,dob=dob,branch=branch)
        committee_obj.save()

        return redirect("/login")


def send_request(committee_obj):
    print(committee_obj.usern)


def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('txtPasswd1')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("i am in loogin")
            login(request, user)
            return redirect("/users_admin/profile_admin")

def profile_admin(request):
    print("i am here")
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        print(username)

        return render(request, "users_admin/profile_admin.html")


def phone_no_available(request):
    phone_no = request.GET.get('phone_no', None)
    print(phone_no)

    data = {
        "is_valid": CommitteeMember.objects.filter(phone_no=phone_no).exists()
    }

    return JsonResponse(data)


def username_available(request):
    username = request.GET.get('username', None)
    print(username)

    data = {
        "is_valid": User.objects.filter(username=username).exists()
    }

    return JsonResponse(data)


def teacher_id_available(request):
    teacher_id = request.GET.get('teacher_id', None)
    print(teacher_id)

    data = {
        "is_valid": CommitteeMember.objects.filter(teacher_id=teacher_id).exists()
    }

    return JsonResponse(data)


def email_available(request):
    email = request.GET.get('email', None)
    print(email)

    data = {
        "is_valid": User.objects.filter(email=email).exists()
    }

    return JsonResponse(data)


def phone_no_char(request):
    phone_no = request.GET.get('phone_no', None)
    print(phone_no)
    send = "False"

    for no in phone_no:
        if no not in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            send = "True"
            break

    data = {
        "is_valid": send
    }
    return JsonResponse(data)


def generate_otp(request):
    phone_no = request.GET.get('phone_no', None)
    print(phone_no)
    email = request.GET.get('email', None)
    print(email)

    otp_phone_no = "123456"
    otp_email = "123456"

    otp_details = Otp(phone_no = phone_no,otp_phone_no = otp_phone_no,
                      email = email,otp_email = otp_email)
    otp_details.save()

    data = {
        "is_valid": "Sent successfully"
    }

    return JsonResponse(data)


def check_otp(request):
    flag = 0

    phone_no = request.GET.get('phone_no', None)
    print(phone_no)
    email = request.GET.get('email', None)
    print(email)

    otp_phone_no = request.GET.get('otp_phone_no', None)
    print(otp_phone_no)
    otp_email = request.GET.get('otp_email', None)
    print(otp_email)

    # check

    check_otp = Otp.objects.filter(phone_no=phone_no).filter(email=email).first()

    if check_otp:
        if otp_phone_no == check_otp.otp_phone_no and otp_email == check_otp.otp_email:
            flag = 1

    if flag == 1:
        data = {
            "correct_otp": "true"
        }
        return JsonResponse(data)
    else:
        data = {
            "correct_otp": "false"
        }
        return JsonResponse(data)



