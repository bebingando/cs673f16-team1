from django import forms
from django.utils import timezone
import datetime
import requirements.models.user_manager
from requirements.models import user_manager
from django.http import HttpResponse, HttpResponseRedirect
from forms import SignUpForm, ChangePwdForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
from requirements.models.ip import IPaddress


def signin(request):
    logout(request)
    username = password = ''
    errormsg = ""
    next = ""

    if request.GET:
        next = request.GET['next']
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        next = request.POST['next']

        # get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip1 = x_forwarded_for.split(',')[-1].strip()
        else:
            ip1 = request.META.get("REMOTE_ADDR")

        # get latest time
        now = timezone.now()
        t = now - datetime.timedelta(seconds=60)
        wrong_times = IPaddress.objects.filter(ip=ip1).count()
        latest_time = IPaddress.objects.filter(last_time__gte=t)

        # if input wrong pwd more than 3 times, the ip will be blocked for 60s
        if wrong_times >= 3 and latest_time:
            print latest_time
            errormsg = 'you have tried many times, please signin after 60s later.'
        else:
            # if input wrong but, this time is 60s after last time, first clear the record of this IP
            if not latest_time:
                IPaddress.objects.filter(ip=ip1).all().delete()
                wrong_times = 0
                print IPaddress.objects.all()
            user = authenticate(username=username, password=password)
            # check whether user name and pwd is correct
            if user is not None:
                if user.is_active:
                    login(request, user)
                    IPaddress.objects.all().filter(ip=ip1).delete()
                    print IPaddress.objects.all()
                    if next == '':
                        return HttpResponseRedirect('/requirements/projects')
                    else:
                        return HttpResponseRedirect(next)
            else:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip1 = x_forwarded_for.split(',')[-1].strip()
                else:
                    ip1 = request.META.get("REMOTE_ADDR")

                # IP address : '+str(ip1)+ "
                if wrong_times == 2:
                    errormsg0 = ''
                    errormsg1 = 'you have tried many times, please signin after 60s later.'
                else:
                    errormsg0 = 'Username or Password is incorrect ! Please try again !'
                    errormsg1 = ' If you fail more than ' + str(
                        2 - wrong_times) + ' times, you need to wait 60s for next try!'
                errormsg = errormsg0 + errormsg1
                ipform = IPaddress(ip=ip1, last_time=now)
                ipform.save(force_insert=True)

    return render_to_response(
        'SignIn.html',
        {
            'errorMsg': errormsg,
            'next': next,
            'isUserSigningInUpOrOut': 'true'
        },
        context_instance=RequestContext(request)
    )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return render(
                request,
                'SignUpFinish.html',
                {
                    'form': form,
                    'isUserSigningInUpOrOut': 'true'
                }
            )
    else:
        form = SignUpForm()
    return render(
        request,
        'SignUp.html',
        {
            'form': form,
            'isUserSigningInUpOrOut': 'true'
        }
    )


@login_required
def signout(request):
    logout(request)
    context = {'isUserSigningInUpOrOut': 'true'}
    return render(request, 'SignOut.html', context)


@login_required(login_url='/signin')
def changepasswd(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePwdForm(request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            logout(request)
            return HttpResponse('')
    else:
        form = ChangePwdForm(user=user)

    context = {
        'form': form,
        'title': 'Change Password',
        'confirm_message': 'After confirming changes. System will automatically logout !',
        'action': '/requirements/changepasswd',
        'button_desc': 'Confirm Change & Logout',
    }
    return render(request, 'ChangePasswd.html', context)


@login_required(login_url='/signin')
def userprofile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse('')
    else:
        form = UserProfileForm(instance=user)

    context = {
        'form': form,
        'title': 'Change User Profile',
        'action': '/requirements/userprofile',
        'button_desc': 'Change Profile'
    }
    return render(request, 'UserProfile.html', context)
