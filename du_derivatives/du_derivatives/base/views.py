from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models import Max, Min
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, AppForm
from .models import Project, User, Photo, Review, Reply, ProjectType


def home(request):
    if request.GET.get('Website') == 'Websites':
        type = 'Website'
    else:
        type = 'Application'
    projectType = ProjectType.objects.get(name=type)
    top_apps = {}
    if request.method == "POST":
        min_batch = request.POST['min-batch']
        max_batch = request.POST['max-batch']
        projects = Project.objects.none()
        try:
            users = User.objects.filter(csedu_batch__gte=min_batch, csedu_batch__lte=max_batch)
        except:
            try:
                users = User.objects.filter(csedu_batch__gte=min_batch)
            except:
                users = User.objects.filter(csedu_batch__lte=max_batch)

        for user in users:
            projects = Project.objects.filter(type=projectType) & Project.objects.filter(developer=user)
        i = 0
        top_apps = []
        for pr in projects.order_by('rate'):
            top_apps += [{'id': i + 1, 'app': pr}]
            i += 1
            if i == 10:
                break
    else:
        projects = Project.objects.filter(type=projectType)
        i = 0
        top_apps = []
        for pr in projects.order_by('rate'):
            top_apps += [{'id': i + 1, 'app': pr}]
            i += 1
            if i == 10:
                break
    project_count = projects.count()
    return render(request, 'homepage.html',
                  {'top_chart_apps': top_apps, 'general_apps': projects,
                   'selected_text': type, 'project_count' : project_count})


@login_required(login_url='login')
def profile(request):
    if request.GET.get('Website') == 'Websites':
        type = 'Website'
    else:
        type = 'Application'

    projectType = ProjectType.objects.get(name=type)
    projects = Project.objects.filter(developer=request.user) & Project.objects.filter(type=projectType)
    project_count = projects.count()
    apps = []
    for i, project in enumerate(projects):
        apps += [{'i': i + 1, 'app': project}]
    return render(request, 'profile.html', {'apps': apps, 'selected_text': type, 'project_count' : project_count})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    global user
    if request.method == "POST":
        post_data = request.POST or None
        if post_data is not None:
            username = request.POST['username']
            password = request.POST.get('password')

            try:
                # user = User.objects.get(email=username)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            except:
                messages.error(request, 'Username or password doesn\'t exist.')
                return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('profile')


def signup(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Re-check everything')
            # print(form.errors.as_data())
            return redirect('signup')

    form = MyUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def addProject(request):
    developer = request.user
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.developer = developer
            project.save()
            return redirect('projectPage', pk=project.id)
        else:
            messages.error(request, 'An error has occurred')
            print(form.errors.as_data())
    form = AppForm()
    return render(request, 'addProject.html', {'form': form})


@login_required(login_url='login')
def projectPage(request, pk):
    project = Project.objects.get(pk=pk)
    photos = Photo.objects.filter(project=project)
    collaborators = project.collaborators.all()
    tag_str = Project.objects.get(pk=pk).tags
    if tag_str is None or tag_str == '':
        tags = []
        tag_str = ''
    else:
        tags = tag_str.split(',')
        if '' in tags:
            tags.remove('')

    reviews_qs = Review.objects.filter(project=project)
    reviews = []
    for rqs in reviews_qs:
        reply = Reply.objects.get(review=rqs)
        reviews += [{
            'reviewer_profile_picture': rqs.reviewer.profile_picture,
            'reviewer': rqs.reviewer,
            'date': rqs.date_added,
            'comment': rqs.comment,
            'reply_date': reply.date_added,
            'reply_body': reply.details
        }]
    review_count = reviews_qs.count()
    if request.method == 'POST':

        # for adding collaborator
        if request.POST.get('email', False):
            try:
                new_collaborator = User.objects.get(email=request.POST['email'])
                if new_collaborator not in collaborators:
                    project.collaborators.add(new_collaborator)
                    project.save()
                    return redirect('projectPage', pk)
            except:
                messages.error(request, 'No user found')
                # print("no user found")

        # for adding tag
        if request.POST.get('tag', False):
            tag_str += (',' + request.POST['tag'])
            project.tags = tag_str
            project.save()
            return redirect('projectPage', pk)

        # for uploading images
        if request.FILES:
            files = request.FILES.getlist('files')
            file_list = []

            for file in files:
                new_photo_file = Photo.objects.create(
                    project=project,
                    photo=file
                )
                new_photo_file.save()
            return redirect('projectPage', pk)

        # for adding review

    return render(request, 'projectPage.html',
                  {'project': project, 'photos': photos, 'tags': tags, 'collaborators': collaborators,
                   'reviews': reviews, 'review_count': review_count})


def appDetails(request):
    return render(request, 'appDetails.html')
