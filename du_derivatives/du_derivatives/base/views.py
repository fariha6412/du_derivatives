from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from base.forms import MyUserCreationForm

from base.forms import UserForm

from base.models import Project, Collaborator

apps = [
    {
        'id': 1,
        'name': 'renshuu - Japanese learning',
        'rating': 4.4,
    },
    {
        'id': 2,
        'name': 'renshuu - Japanese learning',
        'rating': 4.4,
    },
    {
        'id': 3,
        'name': 'renshuu - Japanese learning',
        'rating': 4.4,
    },
    {
        'id': 4,
        'name': 'renshuu - Japanese learning',
        'rating': 4.4,
    },
    {
        'id': 5,
        'name': 'renshuu - Japanese learning',
        'rating': 4.4,
    },
    {
        'id': 6,
        'name': 'renshuu - Japanese learning',
        'rating': 4.4,
    }
]


def home(request):
    categorical = [
        {'name': 'Educational', 'apps': apps},
        {'name': 'Health'},
        {'name': 'Programming', 'apps': apps},
    ]
    return render(request, 'homepage.html', {'top_chart_apps': apps, 'categorical': categorical})


@login_required(login_url='login')
def profile(request):
    projects = Collaborator.objects.filter(email_address=request.user.email)
    apps = []
    for i, project in enumerate(projects):
        ps = Project.objects.filter(title=project.project_id, type='Application')
        for p in ps:
            apps += [{'i': i+1, 'app': p}]
    return render(request, 'profile.html', {'apps': apps})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    global user
    if request.method == "POST":
        post_data = request.POST or None
        if post_data is not None:
            username = request.POST['username']
            password = request.POST.get('password')

            print(username, password)

            try:
                # user = User.objects.get(username=username)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    print("here")
                    return redirect('home')
            except:
                messages.error(request, 'Username or password doesn\'t exist.')

    return render(request, 'login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('profile')


def signup(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred')
            # print(form.errors.as_data())

    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def addApp(request):
    user = request.user
    context = {}
    return render(request, 'addApp.html', context)


@login_required(login_url='login')
def addWebsite(request):
    user = request.user
    context = {}
    return render(request, 'addWebsite.html', context)
