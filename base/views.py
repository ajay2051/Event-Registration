from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        user = authenticate(email=request.POST['email'],
         password=request.POST['password'])
        
        if user is not None:
            login(request, user)
            return redirect('home')

    context = {
    'page': page,
    }
    return render(request, 'base/login_register.html', context)


def register_page(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request,user)
            return redirect('home')
            # return redirect('login')
    page = 'register'
    context = {
    'page': page,
    'form': form,
    }
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')



def homepage(requset):
    users = User.objects.filter(hackathon_participant=True)
    events = Event.objects.all()
    context = {
        'users': users,
        'events': events,
    }
    return render(requset, 'base/home.html', context)



def eventpage(request, pk):
    event = Event.objects.get(id=pk)
    participants = event.participants.all()
    
    registered = False
    submitted = False

    if request.user.is_authenticated:
        registered = request.user.events.filter(id=event.id).exists()
        submitted = Submission.objects.filter(participant=request.user, event=event).exists()
    context = {
    'event': event,
    'participants': participants,
    'registered': registered,
    'submitted': submitted,
    }
    return render(request, 'base/event.html', context)



@login_required()
def registration_confirmation(request, pk):
    event = Event.objects.get(id=pk)
    if request.method=='POST':
        event.participants.add(request.user)
        return redirect('event', pk=event.id)
    context = {
    'event': event,
    }
    return render(request, 'base/event_confirmation.html', context)
    


@login_required()
def profile(request, pk):
    user = User.objects.get(id=pk)
    context = {
    'user': user,
    }
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def account(request):
    user = request.user
    context={
    'user': user
    }
    return render(request, 'base/account.html', context)


@login_required()
def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    form = SubmissionForm()

    if request.method == 'POST':
        form = SubmissionForm(request.POST,)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()
            return redirect('account')

    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'base/project_submit_form.html', context)



@login_required()
def update_submission(request, pk):
    submission = Submission.objects.get(id=pk)
    
    if request.user != submission.participant:
        return HttpResponse('You Cannot Be Here')


    event = submission.event
    form = SubmissionForm(instance=submission)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
    'form': form,
    'event': event,
    }
    return render(request, 'base/project_submit_form.html', context)






